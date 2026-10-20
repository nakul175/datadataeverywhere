#!/usr/bin/env python3
"""Durable advisory clarification loop. Queue bookkeeping never grants a pass.

The checker supplies exact current results. Missing/outdated review work belongs
to reviewers; factual gaps belong to author repair or an explicitly named owner.
Creating a batch is not evidence that a person has seen or answered it.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

CONTEXT_LIMIT = 8
ITERATION_LIMIT = 32
CLOSED_QUESTION_LIMIT = 64
ANSWER_LIMIT = 128
EVENT_LIMIT = 64
SUCCESS = {"stage_checks_satisfied", "advisory_checks_satisfied", "synthetic_checks_satisfied", "top_notch"}
FIELD_PATTERN = re.compile(r"\b(?:common|vision|strategy|roadmap|release_goal|epic|user_story|acceptance_criterion|technical_task)\.[A-Za-z0-9_]+\b")


def _canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _digest(value):
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _read(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def _write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    os.replace(temporary, path)


def _meaningful(value):
    return isinstance(value, str) and bool(value.strip()) and not re.fullmatch(r"\s*(?:pending|unknown|tbd|todo|none|n/a|not set)\s*", value, re.I)


def _api(api, name, default):
    if isinstance(api, dict):
        return api.get(name, default)
    return getattr(api, name, default) if api is not None else default


def _functions(api):
    return (_api(api, "digest", _digest), _api(api, "NOW", lambda: datetime.now(timezone.utc).isoformat()),
            _api(api, "read_json", _read), _api(api, "write_json", _write), _api(api, "resolved", _meaningful))


def _object(value, label):
    if not isinstance(value, dict):
        raise ValueError(label + " must be an object.")
    return value


def _list(value, label):
    if not isinstance(value, list):
        raise ValueError(label + " must be a list.")
    return value


def _state(state):
    if state is None:
        state = {}
    _object(state, "Loop state")
    # Old v3 packets are deliberately reconsidered: presentedCount was set on
    # generation, and cannot establish that a person actually acknowledged them.
    upgrading = state.get("loopSchemaVersion") != "2.0"
    for key in ("questions", "groups"):
        _object(state.setdefault(key, {}), "Loop state " + key)
    for key in ("iterations", "answers", "revisions", "batchEvents", "_archivePending"):
        _list(state.setdefault(key, []), "Loop state " + key)
        for entry in state[key]:
            _object(entry, "Loop state " + key + " entry")
    for group_id, group in state["groups"].items():
        if not isinstance(group_id, str):
            raise ValueError("Loop group IDs must be strings.")
        _object(group, "Loop group " + group_id)
        for key in ("occurrence", "followup"):
            value = group.get(key, 0)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise ValueError("Loop group " + key + " must be a nonnegative integer.")
        if group.get("latestId") is not None and not isinstance(group["latestId"], str):
            raise ValueError("Loop group latestId must be a question ID string.")
    for question_id, question in state["questions"].items():
        if not isinstance(question_id, str):
            raise ValueError("Stored question IDs must be strings.")
        _object(question, "Stored question " + str(question_id))
        if question.get("id") != question_id or not isinstance(question.get("groupId"), str):
            raise ValueError("Stored question must retain its string id and groupId.")
        if question.get("status") not in {"unanswered", "answered", "answered_insufficient", "awaiting_review", "dismissed", "resolved", "superseded"}:
            raise ValueError("Unsupported stored question status.")
        _list(question.setdefault("checksToResolve", []), "Stored question checksToResolve")
        for check in question["checksToResolve"]:
            _object(check, "Stored question check reference")
            if not isinstance(check.get("id"), str):
                raise ValueError("Stored question check references require string IDs.")
        if upgrading:
            if question.get("status") == "unanswered":
                question["acknowledgedAt"] = None
                question["generationWasNotAcknowledgement"] = True
            # Do not carry old megabyte context snapshots into this edition.
            old_history = question.pop("contextHistory", [])
            if isinstance(old_history, list):
                for entry in old_history:
                    if isinstance(entry, dict):
                        state["_archivePending"].append({"kind": "legacy_context_digest", "questionId": question_id,
                            "at": entry.get("at"), "contentDigest": _digest(entry)})
            question["contextHistory"] = []
            question["checksToResolve"] = _check_refs(question.get("checksToResolve", []), _digest)
        _list(question.setdefault("contextHistory", []), "Question contextHistory")
        for entry in question["contextHistory"]:
            _object(entry, "Question contextHistory entry")
        _list(question.setdefault("answerIds", []), "Question answerIds")
        if any(not isinstance(item, str) for item in question["answerIds"]):
            raise ValueError("Question answer IDs must be strings.")
    if upgrading:
        # Legacy iterations copied full lists of check IDs. Keep exact list
        # digests and counts, without retaining those lists on every run.
        state["iterations"] = [{"at": entry.get("at"), "reportFingerprint": entry.get("reportFingerprint", entry.get("subjectFingerprint")),
            "unresolvedCount": entry.get("unresolvedCount", len(entry.get("unresolvedIds", []))),
            "unresolvedDigest": entry.get("unresolvedDigest", _digest(entry.get("unresolvedIds", []))),
            "qualityStatus": entry.get("qualityStatus"), "answerCount": entry.get("answerCount", 0),
            "newAnswers": entry.get("newAnswers", 0), "substantiveProgress": entry.get("substantiveProgress", False)} for entry in state["iterations"]]
    state["loopSchemaVersion"] = "2.0"
    state.setdefault("answerCount", len(state["answers"]))
    state.setdefault("batchCounter", 0)
    if not isinstance(state["answerCount"], int) or isinstance(state["answerCount"], bool) or state["answerCount"] < 0:
        raise ValueError("Loop state answerCount must be a nonnegative integer.")
    if not isinstance(state["batchCounter"], int) or isinstance(state["batchCounter"], bool) or state["batchCounter"] < 0:
        raise ValueError("Loop state batchCounter must be a nonnegative integer.")
    if state.get("currentBatch") is not None:
        _object(state["currentBatch"], "Current batch")
        _list(state["currentBatch"].get("questionIds"), "Current batch questionIds")
        if not isinstance(state["currentBatch"].get("id"), str) or any(not isinstance(item, str) for item in state["currentBatch"]["questionIds"]):
            raise ValueError("Current batch and question IDs must be strings.")
        if any(item not in state["questions"] for item in state["currentBatch"]["questionIds"]):
            raise ValueError("Current batch references an unknown question.")
    if state.get("archiveHead") is not None:
        _object(state["archiveHead"], "Archive head")
    return state


def _check_refs(checks, digest):
    refs = []
    for check in checks:
        if not isinstance(check, dict):
            raise ValueError("Question check references must be objects.")
        refs.append({"id": check.get("id"), "checkId": check.get("checkId"), "dimension": check.get("dimension"),
            "status": check.get("status"), "reasonDigest": check.get("reasonDigest") or digest(check.get("reason")),
            "criterionDigest": check.get("criterionDigest") or digest(check.get("passCriterion")),
            "evidenceRequirementDigest": check.get("evidenceRequirementDigest") or digest(check.get("evidenceRequirement")),
            "subjectFingerprint": check.get("subjectFingerprint")})
    return refs


def _excerpt(value, digest, limit=240):
    text = value if isinstance(value, str) else _canonical(value)
    return {"excerpt": text[:limit], "truncated": len(text) > limit, "contentDigest": digest(value)}


def _field_ids(checks):
    values = []
    for check in checks:
        if str(check.get("checkId", "")).startswith("profile_decision_"):
            values.append("productProfile." + check["checkId"].removeprefix("profile_decision_"))
        if check.get("fieldId"):
            values.append(check["fieldId"])
        for key in ("requiredFieldIds", "missingFieldIds"):
            if isinstance(check.get(key), list):
                values.extend(item for item in check[key] if isinstance(item, str))
        values.extend(FIELD_PATTERN.findall(str(check.get("reason", ""))))
    return list(dict.fromkeys(values))


def _owner(check, element, fields, document, meaningful):
    records = [check] + [fields.get(field_id, {}) for field_id in _field_ids([check])]
    profile = document.get("productProfile", {})
    if isinstance(profile, dict):
        records += [profile.get(field_id.removeprefix("productProfile."), {}) for field_id in _field_ids([check]) if field_id.startswith("productProfile.")]
    for record in records + [element, document]:
        if isinstance(record, dict) and isinstance(record.get("decisionOwnerId"), str) and meaningful(record["decisionOwnerId"]):
            return record["decisionOwnerId"]
    return None


def _review_work(check):
    if check.get("resolutionKind") == "independent_review_task":
        return True
    if check.get("resolutionKind") in {"author_repair_or_owner_decision", "author_repair", "owner_decision"}:
        return False
    if check.get("mode") != "review" or check.get("status") not in {"missing", "stale", "unreviewed"}:
        return False
    # A review gate can itself expose absent content. That is not an absent
    # verdict; do not send the same unavailable fact to a reviewer to invent.
    reason = str(check.get("reason", "")).lower()
    content_missing = bool(_field_ids([check])) and any(term in reason for term in ("details unresolved", "empty or unresolved", "missing field", "field is missing"))
    return not content_missing


def _group(check):
    return check.get("questionGroup") or ("field:" + str(check.get("elementId")) + ":" + str(check["fieldId"]) if check.get("fieldId") else "check:" + str(check["id"]))


def _queue(check, lane, digest, element, document, meaningful):
    fields = element.get("fields", {})
    return {"id": check["id"], "checkId": check.get("checkId"), "elementId": check.get("elementId"),
            "fieldId": check.get("fieldId"), "requiredFieldIds": _field_ids([check]), "status": check["status"],
            "lane": lane, "reason": _excerpt(check.get("reason", ""), digest, 500),
            "decisionOwnerId": _owner(check, element, fields, document, meaningful),
            "subjectFingerprint": check.get("subjectFingerprint"), "criterionDigest": digest(check.get("passCriterion")),
            "reportCheckReference": check["id"], "effect": "Work request only; no verdict, approval or completion inferred."}


def _archive_overflow(state):
    for question in state["questions"].values():
        history = question["contextHistory"]
        while len(history) > CONTEXT_LIMIT:
            state["_archivePending"].append({"kind": "question_context", "questionId": question["id"], **history.pop(0)})
        ids = question.get("answerIds", [])
        if len(ids) > 16:
            state["_archivePending"].append({"kind": "older_answer_references", "questionId": question["id"], "answerIds": ids[:-16]})
            question["answerIds"] = ids[-16:]
    for name, limit, kind in (("iterations", ITERATION_LIMIT, "iteration"), ("answers", ANSWER_LIMIT, "answer"), ("batchEvents", EVENT_LIMIT, "batch_event")):
        while len(state[name]) > limit:
            state["_archivePending"].append({"kind": kind, "record": state[name].pop(0)})
    closed = [question_id for question_id, question in state["questions"].items() if question.get("status") in {"resolved", "superseded", "answered_insufficient"}]
    while len(closed) > CLOSED_QUESTION_LIMIT:
        question_id = closed.pop(0)
        state["_archivePending"].append({"kind": "closed_question", "questionId": question_id, "record": state["questions"].pop(question_id)})


def write_state(state_dir, state, api=None):
    """Flush compact overflow to a content-addressed chain, then atomically save.

    Each archive includes the preceding archive reference. A changed archive
    fails its filename/content hash, so the bounded state retains an auditable
    chain without copying every historical report or question into itself.
    """
    digest, now, _, write_json, _ = _functions(api)
    state = _state(state)
    verify_state(state_dir, state, api)
    _archive_overflow(state)
    pending = state.get("_archivePending", [])
    if pending:
        previous = state.get("archiveHead")
        content = {"schemaVersion": "1.0", "createdAt": now(), "previous": previous, "records": pending}
        content_hash = digest(content)
        relative = "loop-archive/" + content_hash + ".json"
        write_json(Path(state_dir) / relative, content)
        state["archiveHead"] = {"path": relative, "contentHash": content_hash,
            "totalRecordCount": len(pending) + (previous.get("totalRecordCount", 0) if previous else 0)}
        state["_archivePending"] = []
    write_json(Path(state_dir) / "loop-state.json", state)
    return state


def verify_state(state_dir, state=None, api=None):
    """Verify every retained archive hash/link/count before a state mutation.

    This verifies local audit integrity, not respondent identity, semantic truth,
    authority, approval or execution permission.
    """
    digest, _, read_json, _, _ = _functions(api)
    if state is None:
        state = read_json(Path(state_dir) / "loop-state.json")
    _object(state, "Loop state")
    root = Path(state_dir).resolve()
    head = state.get("archiveHead")
    verified, visited, record_count = 0, set(), 0
    while head is not None:
        _object(head, "Archive reference")
        content_hash = head.get("contentHash")
        relative = head.get("path")
        total = head.get("totalRecordCount")
        if not isinstance(content_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", content_hash):
            raise ValueError("Archive reference requires a canonical SHA256 contentHash.")
        if relative != "loop-archive/" + content_hash + ".json":
            raise ValueError("Archive path must match its confined content-addressed filename.")
        if not isinstance(total, int) or isinstance(total, bool) or total < 0:
            raise ValueError("Archive cumulative record count must be nonnegative integer.")
        if content_hash in visited:
            raise ValueError("Archive chain contains a repeated/cyclic reference.")
        visited.add(content_hash)
        path = (root / relative).resolve()
        try:
            path.relative_to(root)
        except ValueError as error:
            raise ValueError("Archive reference escapes its state directory.") from error
        retained = _object(read_json(path), "Retained archive")
        if digest(retained) != content_hash:
            raise ValueError("Retained archive hash mismatch; preserve and investigate the altered audit evidence.")
        records = _list(retained.get("records"), "Archive records")
        for record in records:
            _object(record, "Archive record")
        previous = retained.get("previous")
        if previous is not None:
            _object(previous, "Previous archive reference")
            previous_count = previous.get("totalRecordCount")
            if not isinstance(previous_count, int) or isinstance(previous_count, bool) or previous_count < 0:
                raise ValueError("Previous archive cumulative count is invalid.")
        else:
            previous_count = 0
        if total != len(records) + previous_count:
            raise ValueError("Archive cumulative record count does not match retained records/link.")
        verified += 1
        record_count += len(records)
        head = previous
    return {"archiveIntegrity": "verified_local_hash_chain", "verifiedArchiveCount": verified, "verifiedArchivedRecordCount": record_count,
        "effect": "Local audit integrity only; no review independence, identity, approval or quality certification granted."}


def question_packet(report, document, state=None, batch_size=3, api=None):
    """Return (packet, durable_state); generation does not acknowledge a batch."""
    digest, now, _, _, meaningful = _functions(api)
    _object(report, "Report")
    _object(document, "Document")
    _object(report.get("qualityState"), "Report qualityState")
    _object(report.get("assessmentCoverage", {}), "Report assessmentCoverage")
    if not isinstance(report["qualityState"].get("status"), str):
        raise ValueError("Report qualityState.status must be a string.")
    if not isinstance(batch_size, int) or isinstance(batch_size, bool) or batch_size < 1:
        raise ValueError("batch_size must be a positive integer.")
    checks = _list(report.get("checks"), "Report checks")
    elements = {}
    for element in _list(document.get("elements", []), "Document elements"):
        _object(element, "Document element")
        _object(element.get("fields", {}), "Element fields")
        if not isinstance(element.get("id"), str):
            raise ValueError("Document element IDs must be strings.")
        elements[element.get("id")] = element
    if "scope" in document:
        _object(document["scope"], "Document scope")
    checked_ids = {}
    unresolved = []
    for check in checks:
        _object(check, "Report check")
        if not isinstance(check.get("id"), str) or not isinstance(check.get("status"), str):
            raise ValueError("Every report check needs string id and status.")
        for key in ("elementId", "fieldId", "questionGroup", "resolutionKind"):
            if check.get(key) is not None and not isinstance(check[key], str):
                raise ValueError("Report check " + key + " must be a string or null.")
        if check["id"] in checked_ids:
            raise ValueError("Report check IDs must be unique.")
        checked_ids[check["id"]] = check
        if check.get("blocking", True) and check["status"] not in {"passed", "not_applicable"}:
            unresolved.append(check)
    state = _state(state)
    known = state["questions"]
    groups, reviewer_queue, repair_queue = {}, [], []
    for check in unresolved:
        element = elements.get(check.get("elementId"), {})
        if _review_work(check):
            reviewer_queue.append(_queue(check, "independent_review", digest, element, document, meaningful))
        elif check.get("resolutionKind") == "author_repair":
            repair_queue.append(_queue(check, "author_repair", digest, element, document, meaningful))
        else:
            groups.setdefault(_group(check), []).append(check)
    # A solved factual gap awaiting its independent review is not yet resolved.
    # Only observed passed/exempt current results establish resolution.
    for question in list(known.values()):
        if question.get("status") in {"resolved", "superseded"}:
            continue
        refs = [checked_ids.get(item.get("id")) for item in question.get("checksToResolve", [])]
        present = [item for item in refs if item is not None]
        if present and len(present) == len(refs) and all(item["status"] in {"passed", "not_applicable"} for item in present):
            question.update(status="resolved", resolvedAt=now(), resolvedBy="observed_current_check_results")
            state["groups"].setdefault(question.get("groupId"), {})["lastResolvedQuestionId"] = question["id"]
        elif refs and not present and question.get("groupId") not in groups:
            question.update(status="superseded", supersededAt=now(), supersessionReason="These checks are not selected in the current assessment; no pass inferred.")
        elif present and question.get("groupId") not in groups and any(_review_work(item) for item in present if item["status"] not in {"passed", "not_applicable"}):
            question.setdefault("beforeReviewStatus", question.get("status"))
            question["status"] = "awaiting_review"

    fresh, outstanding = [], []
    for group_id, group_checks in groups.items():
        check = group_checks[0]
        element = elements.get(check.get("elementId"), {})
        fields = element.get("fields", {})
        field_ids = _field_ids(group_checks)
        refs = _check_refs(group_checks, digest)
        profile = document.get("productProfile", {})
        if not isinstance(profile, dict):
            raise ValueError("Document productProfile must be an object.")
        target = {"elementId": check.get("elementId"), "fields": [{"fieldId": field_id,
            **_excerpt(profile.get(field_id.removeprefix("productProfile.")) if field_id.startswith("productProfile.") else fields.get(field_id), digest)} for field_id in field_ids]}
        if not field_ids and check.get("elementId") is None:
            target["workspaceDecisionDigest"] = digest(document.get("productProfile", {}))
        context = digest({"checks": refs, "target": target})
        group_state = state["groups"].setdefault(group_id, {"occurrence": 0, "followup": 0})
        previous = known.get(group_state.get("latestId"))
        if previous is None:
            existing = [item for item in known.values() if item.get("groupId") == group_id]
            previous = existing[-1] if existing else None
        legacy_versions = document.get("questionDecisionVersions", {})
        if not isinstance(legacy_versions, dict):
            raise ValueError("questionDecisionVersions, if retained for compatibility, must be an object.")
        decision_version = legacy_versions.get(group_id)
        manual_supersession = previous and decision_version is not None and previous.get("decisionRevision") != decision_version
        regressed = previous and previous.get("status") in {"resolved", "superseded"}
        followup = previous and (previous.get("assessment") == "needs_clarification" and previous.get("status") in {"answered", "awaiting_review"} or
                   previous.get("status") == "answered" and any(item["status"] == "failed" for item in group_checks) and previous.get("answeredContextFingerprint") != context)
        if previous is None or regressed or manual_supersession:
            group_state["occurrence"] = group_state.get("occurrence", 0) + 1
            group_state["followup"] = 0
        elif followup:
            group_state["followup"] = group_state.get("followup", 0) + 1
        question_id = "Q-" + digest([group_id, group_state["occurrence"], group_state["followup"]])[:20]
        if previous and not regressed and not manual_supersession and not followup:
            question_id = previous["id"]
        owner = _owner(check, element, fields, document, meaningful)
        names = ", ".join(field_ids) if field_ids else str(check.get("checkId") or check["id"])
        reason = _excerpt(check.get("reason", "Unresolved current check."), digest, 650)
        question_text = "For " + str(check.get("elementId") or "workspace") + ", resolve " + names + ": " + reason["excerpt"]
        question_text += " What verified fact, explicit decision or evidence resolves this current gap?"
        if owner is None:
            question_text += " The decision owner is unresolved; identify the actual accountable decision owner if this requires a decision."
        else:
            question_text += " Declared decision owner: " + owner + " (identity/authority require external verification)."
        if followup:
            question_text = "Follow-up for " + previous["id"] + ": " + str(previous.get("followUpReason") or "Current re-review still fails the named criterion.") + " " + question_text
        packet = {"id": question_id, "groupId": group_id, "occurrence": group_state["occurrence"], "followup": group_state["followup"],
            "checkResultId": check["id"], "elementId": check.get("elementId"), "fieldId": check.get("fieldId"), "requiredFieldIds": field_ids,
            "checkId": check.get("checkId"), "dimension": check.get("dimension"), "resolutionKind": check.get("resolutionKind", "author_repair_or_owner_decision"),
            "severity": check.get("severity"), "reason": reason["excerpt"], "reasonDigest": reason["contentDigest"],
            "requiredPassCriterion": _excerpt(check.get("passCriterion", ""), digest, 1200),
            "requiredEvidence": _excerpt(check.get("evidenceRequirement", ""), digest, 600), "question": question_text,
            "safeRepair": check.get("repairPrompt"), "subjectFingerprint": check.get("subjectFingerprint") or context,
            "contextFingerprint": context, "targetContext": target, "checksToResolve": refs,
            "decisionRevision": decision_version, "decisionOwnerId": owner, "decisionOwnerStatus": "declared_unverified" if owner else "unresolved",
            "reportCheckReference": check["id"]}
        if question_id not in known:
            if previous and (followup or manual_supersession):
                previous["status"] = "answered_insufficient" if followup else "superseded"
                previous["followUpId" if followup else "supersededBy"] = question_id
            if previous:
                packet["followUpTo" if followup else "regressionOf" if regressed else "supersedes"] = previous["id"]
            known[question_id] = packet | {"firstSeen": now(), "status": "unanswered", "presentedCount": 0, "acknowledgedAt": None, "contextHistory": []}
            fresh.append(question_id)
        else:
            old = known[question_id]
            if old.get("contextFingerprint") != context:
                old["contextHistory"].append({"at": now(), "contextFingerprint": old.get("contextFingerprint"),
                    "checkReferencesDigest": digest(old.get("checksToResolve", [])), "targetDigest": digest(old.get("targetContext")),
                    "reportFingerprint": old.get("latestReportFingerprint")})
            old.update({key: value for key, value in packet.items() if key not in {"id", "subjectFingerprint"}})
            if old.get("status") == "awaiting_review":
                old["status"] = old.pop("beforeReviewStatus", "unanswered")
        known[question_id]["latestReportFingerprint"] = report.get("subjectFingerprint")
        group_state["latestId"] = question_id
        outstanding.append(question_id)

    pending = [known[question_id] for question_id in outstanding if known[question_id]["status"] == "unanswered"]
    answered = [known[question_id] for question_id in outstanding if known[question_id]["status"] == "answered"]
    dismissed = [known[question_id] for question_id in outstanding if known[question_id]["status"] == "dismissed"]
    for question in dismissed:
        repair_queue.append({"id": question["checkResultId"], "checkId": question.get("checkId"), "elementId": question.get("elementId"),
            "lane": "dismissed_but_unresolved", "questionId": question["id"], "reason": question.get("dismissalReason"),
            "effect": "Dismissal does not resolve checks; verified repair or renewed owner clarification remains required."})
    current = state.get("currentBatch")
    pending_ids = {question["id"] for question in pending}
    if current:
        current["questionIds"] = [question_id for question_id in current["questionIds"] if question_id in pending_ids]
        if not current["questionIds"]:
            state["batchEvents"].append({"at": now(), "batchId": current["id"], "kind": "answered_resolved_or_superseded", "effect": "No quality pass inferred."})
            state["currentBatch"] = current = None
    if current is None:
        waiting = [question for question in pending if not question.get("acknowledgedAt")]
        if waiting:
            state["batchCounter"] += 1
            question_ids = [question["id"] for question in waiting[:batch_size]]
            current = {"id": "B-" + digest([document.get("documentId"), state["batchCounter"], question_ids])[:20],
                "questionIds": question_ids, "createdAt": now(), "acknowledged": False}
            state["currentBatch"] = current
    batch = [copy.deepcopy(known[question_id]) for question_id in current["questionIds"]] if current else []
    quality_status = report["qualityState"]["status"]
    auth = report.get("reviewerAuthentication", {})
    _object(auth, "Report reviewerAuthentication")
    if quality_status in SUCCESS:
        loop_status = "synthetic_complete" if quality_status in {"synthetic_checks_satisfied", "top_notch"} or auth.get("status") == "synthetic_test_only" else "advisory_complete"
    elif quality_status == "blocked":
        loop_status = "blocked"
    elif pending:
        loop_status = "needs_input"
    elif reviewer_queue:
        loop_status = "needs_review"
    else:
        loop_status = "needs_revision"
    last = state["iterations"][-1] if state["iterations"] else None
    unresolved_ids = sorted(check["id"] for check in unresolved)
    iteration = {"at": now(), "reportFingerprint": report.get("subjectFingerprint"), "unresolvedCount": len(unresolved_ids),
        "unresolvedDigest": digest(unresolved_ids), "qualityStatus": quality_status, "answerCount": state["answerCount"],
        "currentBatchId": current["id"] if current else None}
    iteration["substantiveProgress"] = bool(last and iteration["unresolvedCount"] < last["unresolvedCount"])
    iteration["newAnswers"] = state["answerCount"] - (last.get("answerCount", 0) if last else 0)
    if last and answered and not pending and not reviewer_queue and not iteration["substantiveProgress"] and not fresh and not iteration["newAnswers"] and last.get("unresolvedDigest") == iteration["unresolvedDigest"]:
        loop_status = "blocked_no_progress"
    state["iterations"].append(iteration)
    _archive_overflow(state)
    result = {"loopStatus": loop_status, "qualityStatus": quality_status, "subjectFingerprint": report.get("subjectFingerprint"),
        "newQuestionCount": len(fresh), "pendingQuestionCount": len(pending), "answeredButUnresolvedCount": len(answered),
        "nextBatch": batch, "currentBatchId": current["id"] if current else None,
        "batchRequiresAcknowledgement": bool(current), "allUnresolvedQuestionIds": outstanding,
        "awaitingAnswerIds": [question["id"] for question in pending if question.get("acknowledgedAt")],
        "awaitingAnswers": [{"id": question["id"], "question": question["question"], "decisionOwnerId": question.get("decisionOwnerId")} for question in pending if question.get("acknowledgedAt")],
        "dismissedQuestionIds": [question["id"] for question in dismissed], "reviewerQueue": reviewer_queue, "repairQueue": repair_queue,
        "reviewerQueueCount": len(reviewer_queue), "repairQueueCount": len(repair_queue),
        "assessedStage": report.get("assessmentCoverage", {}).get("stage"),
        "instruction": "Creating a batch is not acknowledgement. Keep the current unanswered batch until actual answers, explicit acknowledge-batch, current-check resolution or supersession. Acknowledgement/dismissal never passes a check; acknowledged unanswered questions remain awaiting answers. Missing/stale reviews belong to the reviewer queue. Answers require verified revision and independent recheck. Offline stage satisfaction is advisory; synthetic results are test-only. No iteration or time limit grants approval."}
    if loop_status == "blocked_no_progress":
        result["blocker"] = "Answers were retained but no current required check was resolved. Apply a verified revision or clarify the exact unresolved gap; no quality pass granted."
    return result, state


def record_answer(state_dir, question_id, answer, answered_by, assessment="ready_for_revision", follow_up_reason=None, api=None):
    digest, now, read_json, _, meaningful = _functions(api)
    state = _state(read_json(Path(state_dir) / "loop-state.json"))
    question = state["questions"].get(question_id)
    if not question:
        raise ValueError("Unknown question ID; generate a current question packet first.")
    if question.get("status") in {"resolved", "superseded", "answered_insufficient"}:
        raise ValueError("This question is closed; answer its current follow-up or regressed occurrence instead.")
    if not meaningful(answer) or not meaningful(answered_by):
        raise ValueError("Answer and identifiable respondent must be meaningful, not placeholders.")
    if assessment not in {"ready_for_revision", "needs_clarification"} or assessment == "needs_clarification" and not meaningful(follow_up_reason):
        raise ValueError("Ambiguous answers need an explicit unresolved reason for follow-up.")
    state["answerCount"] += 1
    entry = {"id": "A-" + digest([question_id, answer, answered_by, state["answerCount"]])[:20], "questionId": question_id,
        "answer": answer, "answeredBy": answered_by, "at": now(), "subjectFingerprint": question.get("subjectFingerprint"),
        "contextFingerprint": question.get("contextFingerprint"), "effect": "Information only; not approval, verified revision or quality pass."}
    state["answers"].append(entry)
    question.update(status="answered", assessment=assessment, followUpReason=follow_up_reason,
        answeredContextFingerprint=question.get("contextFingerprint"), lastAnsweredAt=entry["at"])
    question.setdefault("answerIds", []).append(entry["id"])
    write_state(state_dir, state, api)
    return entry


def acknowledge_batch(state_dir, batch_id, acknowledged_by, api=None):
    _, now, read_json, _, meaningful = _functions(api)
    state = _state(read_json(Path(state_dir) / "loop-state.json"))
    current = state.get("currentBatch")
    if not current or current.get("id") != batch_id:
        raise ValueError("Unknown/currently superseded batch ID; acknowledge the current batch only.")
    if not meaningful(acknowledged_by):
        raise ValueError("Batch acknowledgement needs an identifiable acknowledging person.")
    at = now()
    ids = []
    for question_id in current["questionIds"]:
        question = state["questions"].get(question_id)
        if question and question.get("status") == "unanswered":
            question.update(acknowledgedAt=at, acknowledgedBy=acknowledged_by,
                presentedCount=question.get("presentedCount", 0) + 1, lastPresented=at)
            ids.append(question_id)
    entry = {"at": at, "batchId": batch_id, "kind": "explicit_acknowledgement", "acknowledgedBy": acknowledged_by,
        "questionIds": ids, "effect": "Seen only; questions remain unanswered and all checks remain unresolved."}
    state["batchEvents"].append(entry)
    state["currentBatch"] = None
    write_state(state_dir, state, api)
    return entry


def dismiss_question(state_dir, question_id, reason, dismissed_by, api=None):
    _, now, read_json, _, meaningful = _functions(api)
    state = _state(read_json(Path(state_dir) / "loop-state.json"))
    question = state["questions"].get(question_id)
    if not question or question.get("status") in {"resolved", "superseded", "answered_insufficient"}:
        raise ValueError("Dismissal requires a current unresolved question.")
    if not meaningful(reason) or not meaningful(dismissed_by):
        raise ValueError("Dismissal needs a precise reason and identifiable actor.")
    question.update(status="dismissed", dismissedAt=now(), dismissedBy=dismissed_by, dismissalReason=reason)
    write_state(state_dir, state, api)
    return {"questionId": question_id, "status": "dismissed_but_unresolved", "reason": reason,
        "effect": "Queue disposition only; the failed check is retained for repair and no quality pass is granted."}
