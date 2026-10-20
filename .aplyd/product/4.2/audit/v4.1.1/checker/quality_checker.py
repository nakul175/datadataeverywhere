#!/usr/bin/env python3
"""Offline, evidence-bound product-documentation checks. No network or auto-approval."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from datetime import datetime, timezone

VERSION = "1.0"
REVIEW_STAGES = ("discovery", "planning", "ready", "delivery", "learning")
SUCCESS_STATES = {"synthetic_checks_satisfied", "stage_checks_satisfied", "advisory_checks_satisfied"}
ELEMENT_TYPES = ("vision", "strategy", "roadmap", "release_goal", "epic", "user_story", "acceptance_criterion", "technical_task")
PARENT_TYPES = {"vision": set(), "strategy": {"vision"}, "roadmap": {"strategy"}, "release_goal": {"roadmap"}, "epic": {"release_goal"}, "user_story": {"epic"}, "acceptance_criterion": {"user_story"}, "technical_task": {"user_story", "technical_task"}}
PLACEHOLDER = re.compile(r"^\s*(?:\[.*(?:pending|todo|tbd|unknown|fill|placeholder).*\]|(?:pending|unknown|tbd|todo|not set|not provided|not applicable|n/a|lorem ipsum)\b.*|(?:owner|approver|reviewer|decision owner)\s*:\s*(?:pending|unknown|tbd|todo)\b.*|none)\s*$", re.I | re.S)
NOW = lambda: datetime.now(timezone.utc).isoformat()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def read_json(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    os.replace(temporary, path)


def normalized(value):
    if isinstance(value, str):
        return " ".join(value.split())
    if isinstance(value, dict):
        return {key: normalized(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalized(item) for item in value]
    return value


def empty(value):
    return value is None or value is False or (isinstance(value, (str, list, dict)) and not value)


def resolved(value):
    if isinstance(value, str):
        return bool(value.strip()) and not PLACEHOLDER.match(value)
    if isinstance(value, list):
        return bool(value) and all(resolved(item) for item in value)
    if isinstance(value, dict):
        return bool(value) and all(resolved(item) for item in value.values())
    return value is not None


def field_value(field):
    return field.get("value") if isinstance(field, dict) else field


def source_hash(source):
    content = {key: source.get(key) for key in ("id", "text", "version", "originality", "approvalStatus", "protected")}
    if "requiredBranches" in source:
        content["requiredBranches"] = source["requiredBranches"]
    return digest(content)


def confined_path(root, relative):
    path = (Path(root) / relative).resolve()
    path.relative_to(Path(root).resolve())
    return path


def evidence_bytes(item, root):
    """References alone are not proof. File reads are confined to the input directory."""
    if "content" in item:
        return canonical(item["content"]).encode("utf-8")
    if item.get("assetPath"):
        return confined_path(root, item["assetPath"]).read_bytes()
    raise ValueError("Evidence needs a retained content snapshot or a confined local asset.")


def evidence_hash(item, root):
    return hashlib.sha256(evidence_bytes(item, root)).hexdigest()


def subject_fingerprint(document, catalogue, root="."):
    """Global audit identity; it is never accepted as a scoped review binding."""
    validate_document_shape(document)
    content = {key: value for key, value in document.items() if key not in {"reviews", "history", "qualityState", "report", "evidence"}}
    assets = []
    for item in document.get("evidence", []):
        try:
            actual = evidence_hash(item, root)
        except (ValueError, OSError):
            actual = "unavailable"
        assets.append({key: item.get(key) for key in ("id", "kind", "description", "syntheticFixture", "origin")} | {"actualHash": actual})
    return digest({"catalogueHash": digest(catalogue), "document": content, "evidence": assets})


def validate_document_shape(document):
    """Reject malformed containers before any .get, set or graph operations."""
    if not isinstance(document, dict):
        raise ValueError("Document must be a JSON object.")
    for name in ("scope", "sourcePins", "assessment", "productProfile", "questionDecisionVersions"):
        if name in document and not isinstance(document[name], dict):
            raise ValueError(name + " must be a JSON object.")
    for name in ("elements", "sources", "evidence", "authorities", "reviews", "approvalRecords", "history"):
        values = document.get(name, [])
        if not isinstance(values, list) or any(not isinstance(value, dict) for value in values):
            raise ValueError(name + " must be a list of objects.")
        if name != "history" and any(value.get("id") is not None and not isinstance(value.get("id"), str) for value in values):
            raise ValueError(name + " IDs must be strings.")
    scope = document.get("scope", {})
    for name in ("includedElementTypes", "contextElementIds"):
        if not isinstance(scope.get(name, []), list) or any(not isinstance(value, str) for value in scope.get(name, [])):
            raise ValueError("scope." + name + " must be a list of strings.")
    for element in document.get("elements", []):
        if not isinstance(element.get("fields", {}), dict):
            raise ValueError("Element fields must be an object.")
        if element.get("parentId") is not None and not isinstance(element.get("parentId"), str):
            raise ValueError("Element parentId must be a string or null.")
        for name in ("sourceIds", "dependencyIds", "designDependencyIds"):
            if not isinstance(element.get(name, []), list) or any(not isinstance(value, str) for value in element.get(name, [])):
                raise ValueError("Element " + name + " must be a list of strings.")
    for authority in document.get("authorities", []):
        for name in ("permissions", "elementIds"):
            if not isinstance(authority.get(name, []), list) or any(not isinstance(value, str) for value in authority.get(name, [])):
                raise ValueError("Authority " + name + " must be a list of strings.")
    for review in document.get("reviews", []):
        if not isinstance(review.get("evidenceIds", []), list) or any(not isinstance(value, str) for value in review.get("evidenceIds", [])):
            raise ValueError("Review evidenceIds must be a list of strings.")
    for item in document.get("evidence", []):
        if "bindings" in item and (not isinstance(item["bindings"], list) or any(not isinstance(value, dict) for value in item["bindings"])):
            raise ValueError("Evidence bindings must be a list of scoped objects.")


def _target_matches(review, element_id, field_id, check_id):
    return all(review.get(key) == value for key, value in (("elementId", element_id), ("fieldId", field_id), ("checkId", check_id)))


def check_subject_payload(document, catalogue, element_id=None, field_id=None, check_id=None, root=".", catalogue_hash=None, check_index=None):
    """Exact dependency closure for one review; queue and audit metadata are excluded.

    Every local gate depends on its own item, ancestors and explicit prerequisite
    closure. Alignment gates additionally depend on direct children. Hierarchy
    gates depend on every assessed item/context. Unrelated sibling edits preserve
    local reviews. Shared sources/evidence genuinely affect every referencing gate.
    """
    validate_document_shape(document)
    elements = {item.get("id"): item for item in document.get("elements", [])}
    checks = check_index or {check.get("id"): check for _, check in catalogue_checks(catalogue)}
    check = checks.get(check_id, {})
    alignment = check.get("dimension") in {"traceability", "consistency", "nonredundancy", "completeness"} or str(check_id).endswith(".01")
    selected, links = set(), []
    def include(node, relation="target", originating=None):
        if node not in elements or node in selected:
            return
        selected.add(node)
        links.append({"elementId": node, "relation": relation, "fromElementId": originating})
        item = elements[node]
        include(item.get("parentId"), "ancestor", node)
        for dependency in item.get("dependencyIds", []):
            include(dependency, "blocking_prerequisite", node)
        for dependency in item.get("designDependencyIds", []):
            include(dependency, "design_reference", node)
    if element_id is None:
        for node in sorted(elements):
            include(node, "hierarchy_member")
    else:
        include(element_id)
        if alignment:
            for node, item in sorted(elements.items()):
                if item.get("parentId") == element_id:
                    include(node, "direct_child_alignment", element_id)
    source_ids = {source_id for node in selected for source_id in elements[node].get("sourceIds", [])}
    for decision in document.get("productProfile", {}).values():
        if isinstance(decision, dict):
            source_ids.update(decision.get("sourceIds", []))
    reviews = [review for review in document.get("reviews", []) if _target_matches(review, element_id, field_id, check_id)]
    evidence_ids = {evidence_id for review in reviews for evidence_id in review.get("evidenceIds", [])}
    evidence = []
    for item in document.get("evidence", []):
        if item.get("id") not in evidence_ids:
            continue
        try:
            actual_hash = evidence_hash(item, root)
        except (ValueError, OSError):
            actual_hash = "unavailable"
        evidence.append({key: item.get(key) for key in ("id", "kind", "description", "syntheticFixture", "origin")} | {"actualHash": actual_hash})
    reviewer_ids = {review.get("reviewerId") for review in reviews}
    approval_records = [record for record in document.get("approvalRecords", []) if not record.get("elementIds") or set(record.get("elementIds", [])) & selected]
    payload = {"bindingVersion": "scoped-v1", "catalogueHash": catalogue_hash or digest(catalogue), "documentId": document.get("documentId"),
               "mode": document.get("mode"), "authorId": document.get("authorId"), "assessment": document.get("assessment", {}),
               "productProfile": document.get("productProfile", {}), "scope": document.get("scope", {}),
               "target": {"elementId": element_id, "fieldId": field_id, "checkId": check_id},
               "elements": [elements[node] for node in sorted(selected)], "dependencyLinks": links,
               "sources": [item for item in document.get("sources", []) if item.get("id") in source_ids],
               "sourcePins": {key: value for key, value in document.get("sourcePins", {}).items() if key in source_ids},
               "approvalRecords": approval_records, "evidence": sorted(evidence, key=lambda item: item["id"]),
               "authorities": [item for item in document.get("authorities", []) if item.get("id") in reviewer_ids]}
    return payload


def check_subject_fingerprint(document, catalogue, element_id=None, field_id=None, check_id=None, root="."):
    validate_review_target(document, catalogue, element_id, field_id, check_id)
    return digest(check_subject_payload(document, catalogue, element_id, field_id, check_id, root))


def validate_review_target(document, catalogue, element_id, field_id, check_id):
    """Public fingerprint/binding helpers may only target an actual catalogue check."""
    validate_document_shape(document)
    element = next((item for item in document.get("elements", []) if item.get("id") == element_id), None)
    if element_id is not None and not element:
        raise ValueError("Unknown review target elementId: " + str(element_id))
    if field_id is not None:
        field = next((item for item in catalogue.get("fields", []) if item.get("id") == field_id), None)
        if not element or not field or field.get("element") not in {"common", element.get("elementType")} or not any(item.get("id") == check_id for item in field.get("checks", [])):
            raise ValueError("Unknown or wrong-level field/check review target.")
    elif element:
        valid = any(item.get("id") == check_id and item.get("element", item.get("scopeElement", "all")) in {"all", "common", element.get("elementType")} for item in catalogue.get("elementChecks", [])) or any(item.get("id") == check_id and element.get("elementType") in item.get("applicable_types", []) for item in catalogue.get("profileChecks", []))
        if not valid:
            raise ValueError("Unknown or wrong-level element/profile review target.")
    elif not any(item.get("id") == check_id for item in catalogue.get("hierarchyChecks", [])):
        raise ValueError("A workspace review must target an explicit hierarchy catalogue check.")


def review_set_fingerprint(document, catalogue, root=".", scoped_payload=None):
    """Receipt identity for exact verdicts and their current semantic subjects.

    Audit revision numbers/question bookkeeping cannot retire this receipt;
    changed verdicts, linked evidence, sources, policies or authority can.
    """
    validate_document_shape(document)
    catalogue_hash = digest(catalogue)
    check_index = {check.get("id"): check for _, check in catalogue_checks(catalogue)}
    entries = []
    for review in document.get("reviews", []):
        target = (review.get("elementId"), review.get("fieldId"), review.get("checkId"))
        payload = scoped_payload(target) if scoped_payload else check_subject_payload(document, catalogue, *target, root=root, catalogue_hash=catalogue_hash, check_index=check_index)
        entries.append({"id": review.get("id"), "reviewHash": digest(review), "currentSubjectFingerprint": digest(payload)})
    return digest({"bindingVersion": "scoped-v1", "catalogueHash": catalogue_hash, "documentId": document.get("documentId"), "entries": sorted(entries, key=lambda item: str(item["id"]))})


def catalogue_checks(catalogue):
    checks = []
    for field in catalogue.get("fields", []):
        for check in field.get("checks", []):
            checks.append((field, check))
    for check in catalogue.get("elementChecks", []):
        checks.append((None, check))
    for check in catalogue.get("hierarchyChecks", []):
        checks.append((None, check))
    for check in catalogue.get("profileChecks", []):
        checks.append((None, check))
    return checks


def assessment_selection(catalogue, document):
    """A missing assessment selects the small default; an unknown profile never falls back."""
    supplied = document.get("assessment", {})
    if not isinstance(supplied, dict):
        raise ValueError("assessment must be an explicit object.")
    mode = supplied.get("mode", "profile")
    if mode not in {"profile", "exhaustive"}:
        raise ValueError("Unknown assessment mode; use profile or explicit exhaustive.")
    if mode == "exhaustive":
        stage = supplied.get("stage", "planning")
        if stage not in REVIEW_STAGES:
            raise ValueError("Exhaustive review still needs a valid applicability stage.")
        return {"mode": mode, "stage": stage, "legacyDefault": not bool(supplied), "checks": {}, "sampleLimit": 0}
    profiles = catalogue.get("review_profiles", {})
    stage = supplied.get("stage", profiles.get("default_stage", "planning"))
    if stage not in REVIEW_STAGES or stage not in profiles.get("stages", {}):
        raise ValueError("Unknown or unavailable review stage; no exhaustive fallback or silent pass.")
    checks = profiles["stages"][stage].get("types", {})
    indexed = {check.get("id"): check for check in catalogue.get("profileChecks", [])}
    selected = {}
    for kind in ELEMENT_TYPES:
        ids = checks.get(kind, [])
        if not isinstance(ids, list) or len(ids) != 7 or len(set(ids)) != 7:
            raise ValueError("Every stage and hierarchy level needs exactly seven mandatory aggregate gates: " + kind)
        selected[kind] = []
        for check_id in ids:
            check = indexed.get(check_id)
            if not check or check.get("profile_stage") != stage or kind not in check.get("applicable_types", []):
                raise ValueError("Profile gate has wrong stage/type or is missing: " + str(check_id))
            selected[kind].append(check)
    limit = profiles.get("sample_limit", 2)
    if not isinstance(limit, int) or isinstance(limit, bool) or not 0 <= limit <= 2:
        raise ValueError("Advisory sample_limit must be an integer between zero and two.")
    return {"mode": mode, "stage": stage, "legacyDefault": not bool(supplied), "checks": selected, "sampleLimit": limit}


def catalogue_errors(catalogue):
    errors = []
    if not isinstance(catalogue, dict):
        return ["Catalogue must be a JSON object."]
    if catalogue.get("schemaVersion") != VERSION:
        errors.append("Unsupported or missing catalogue schemaVersion.")
    fields = catalogue.get("fields", [])
    if not isinstance(fields, list) or not fields:
        return errors + ["Catalogue fields are missing."]
    seen_fields, seen_checks = set(), set()
    for field in fields:
        if not field.get("id") or field["id"] in seen_fields:
            errors.append("Missing or duplicate catalogue field ID.")
        seen_fields.add(field.get("id"))
        if field.get("element") not in (*ELEMENT_TYPES, "common"):
            errors.append("Unknown catalogue element type: " + str(field.get("element")))
        if field.get("requiredness", {}).get("policy") not in {"always", "conditional"}:
            errors.append("Each field needs an explicit always/conditional applicability policy.")
        if not field.get("checks"):
            errors.append("Field has no quality checks: " + str(field.get("id")))
    for _, check in catalogue_checks(catalogue):
        if not check.get("id") or check["id"] in seen_checks:
            errors.append("Missing or duplicate catalogue check ID: " + str(check.get("id")))
        seen_checks.add(check.get("id"))
        if check.get("mode") not in {"structural", "review"}:
            errors.append("Unsupported check mode: " + str(check.get("id")))
        if not check.get("passCriterion") or not check.get("evidenceRequirement"):
            errors.append("Missing observable criterion/evidence requirement: " + str(check.get("id")))
        rule = check.get("structuralRule", "nonempty")
        rule_type = rule.get("type") if isinstance(rule, dict) else rule
        if check.get("mode") == "structural" and rule_type not in {"nonempty", "no_placeholder", "text", "list", "object", "unique_id"}:
            errors.append("Unsupported structural rule (never silently passed): " + str(rule_type))
    aliases = catalogue.get("fieldAliases", {})
    if not isinstance(aliases, dict):
        errors.append("fieldAliases must map legacy IDs to canonical field IDs.")
    else:
        for old, current in aliases.items():
            if old == current or old in seen_fields or current not in seen_fields or current in aliases:
                errors.append("Invalid, cyclic or ambiguous field alias: " + str(old))
    if catalogue.get("review_profiles"):
        for stage in REVIEW_STAGES:
            try:
                selection = assessment_selection(catalogue, {"assessment": {"mode": "profile", "stage": stage}})
                indexed_fields = {field["id"]: field for field in fields}
                for kind, gates in selection["checks"].items():
                    for gate in gates:
                        for field_id in gate.get("requiredFieldIds", []):
                            if field_id not in indexed_fields or indexed_fields[field_id].get("element") not in {"common", kind}:
                                errors.append("Wrong-level or unknown profile requiredFieldId: " + str(field_id))
                        conditional = gate.get("conditionalFieldIds", {})
                        if not isinstance(conditional, dict) or not set(conditional).issubset({"ai", "personalData"}):
                            errors.append("Unknown mandatory conditional branch in profile gate: " + str(gate.get("id")))
                            continue
                        for branch, ids in conditional.items():
                            if not isinstance(ids, list) or any(field_id not in indexed_fields or indexed_fields[field_id].get("element") not in {"common", kind} for field_id in ids):
                                errors.append("Wrong-level or unknown conditional profile field: " + str(gate.get("id")))
            except (ValueError, KeyError, TypeError) as error:
                errors.append(str(error))
    return errors


class Checker:
    def __init__(self, catalogue, document, root=".", trust_store=None):
        validate_document_shape(document)
        if trust_store is not None and not isinstance(trust_store, dict):
            raise ValueError("Trust store must be an object.")
        if trust_store is not None:
            for key in ("authorities", "reviewVerifications"):
                if not isinstance(trust_store.get(key, []), list) or any(not isinstance(value, dict) for value in trust_store.get(key, [])):
                    raise ValueError("Trust store " + key + " must be a list of objects.")
        self.catalogue, self.document, self.root = catalogue, document, root
        self.catalogue_hash = digest(catalogue)
        self.check_index = {check.get("id"): check for _, check in catalogue_checks(catalogue)}
        self._scoped_payloads = {}
        self.trust = trust_store or {}
        self.fingerprint = subject_fingerprint(document, catalogue, root)
        self.results = []
        self.elements = {item.get("id"): item for item in document.get("elements", [])}
        self.evidence = {item.get("id"): item for item in document.get("evidence", [])}
        self.authorities = {item.get("id"): item for item in document.get("authorities", [])}
        self.reviews = document.get("reviews", [])
        self.synthetic = document.get("mode") == "synthetic_fixture"
        try:
            self.selection = assessment_selection(catalogue, document)
            self.selection_error = None
        except (ValueError, KeyError, TypeError) as error:
            self.selection = {"mode": "invalid", "stage": None, "checks": {}, "sampleLimit": 0, "legacyDefault": False}
            self.selection_error = str(error)
        self.samples = []
        self.compatibility_used = []
        self._effective_fields_cache = {}

    def add(self, check_id, status, reason, element=None, field=None, check=None, evidence_ids=None):
        item = {"id": (str(element.get("id")) + ":" if element else "workspace:") + (str(field.get("id")) + ":" if field else "") + check_id,
                "checkId": check_id, "elementId": element.get("id") if element else None,
                "elementType": element.get("elementType") if element else None,
                "fieldId": field.get("id") if field else None,
                "dimension": (check or {}).get("dimension", "integrity"),
                "severity": (check or {}).get("severity", "blocking"), "status": status,
                "reason": reason, "passCriterion": (check or {}).get("passCriterion", reason),
                "evidenceRequirement": (check or {}).get("evidenceRequirement", "Verified current input structure."),
                "evidenceIds": evidence_ids or [], "questionPrompt": (check or {}).get("questionPrompt"),
                "repairPrompt": (check or {}).get("repairPrompt"), "questionGroup": (check or {}).get("questionGroup", (check or {}).get("decisionId")), "mode": (check or {}).get("mode", "structural")}
        item["blocking"] = item["severity"] not in {"advisory", "informational"}
        item["resolutionKind"] = (check or {}).get("resolutionKind", "author_repair_or_owner_decision")
        if item["mode"] == "review" and status == "failed":
            item["resolutionKind"] = "author_repair_or_owner_decision"
        item["requiredFieldIds"] = list((check or {}).get("requiredFieldIds", []))
        item["missingFieldIds"] = list((check or {}).get("missingFieldIds", []))
        if item["mode"] == "review" and status in {"missing", "stale"} and reason.startswith(("Exactly one current review", "Review has no current scoped-v1")):
            item["resolutionKind"] = "independent_review_task"
        target = (item["elementId"], item["fieldId"], check_id)
        payload = self.scoped_payload(target)
        item["subjectFingerprint"] = digest(payload)
        item["fingerprintScope"] = {"bindingVersion": "scoped-v1", "elementIds": [value.get("id") for value in payload["elements"]], "dependencyLinks": payload["dependencyLinks"]}
        self.results.append(item)
        return item

    def scoped_payload(self, target):
        if target not in self._scoped_payloads:
            self._scoped_payloads[target] = check_subject_payload(self.document, self.catalogue, *target, root=self.root, catalogue_hash=self.catalogue_hash, check_index=self.check_index)
        return self._scoped_payloads[target]

    def effective_fields(self, element):
        if element.get("id") in self._effective_fields_cache:
            return self._effective_fields_cache[element.get("id")]
        values = dict(element.get("fields", {}))
        for old, current in self.catalogue.get("fieldAliases", {}).items():
            if old not in values:
                continue
            if current in values and digest(values[old]) != digest(values[current]):
                self.add("alias_conflict_" + old, "invalid", "Legacy and canonical field values conflict; an authority must resolve them without dropping protected content.", element)
            else:
                values.setdefault(current, values[old])
            values.pop(old)
            self.compatibility_used.append({"elementId": element.get("id"), "legacyFieldId": old, "canonicalFieldId": current})
        self._effective_fields_cache[element.get("id")] = values
        return values

    def profile_decisions(self):
        """Applicability is an unsampled decision, never inferred from a missing module."""
        if self.selection["mode"] not in {"profile", "exhaustive"}:
            return
        profile = self.document.get("productProfile", {})
        if not isinstance(profile, dict):
            self.add("product_profile", "invalid", "productProfile must be an explicit object.")
            return
        source_ids = set(self.document.get("sourcePins", {}))
        for branch in ("ai", "personalData"):
            decision = profile.get(branch, {})
            if not isinstance(decision, dict):
                self.add("profile_decision_" + branch, "invalid", "Applicability decision must be an object.")
                continue
            choice = decision.get("applicability", "unknown")
            if choice not in {"yes", "no", "unknown"}:
                self.add("profile_decision_" + branch, "invalid", "Use an explicit yes/no/unknown applicability decision; unknown cannot mean exempt.")
                continue
            if choice == "unknown":
                if self.selection["stage"] != "discovery":
                    self.add("profile_decision_" + branch, "missing", "Resolve " + branch + " applicability from authoritative scope before this decision-dependent stage; all branch obligations remain unsampled.", check={"mode": "review", "questionGroup": "profile:" + branch})
                elif not resolved(decision.get("resolutionPlan")) or not resolved(decision.get("rationale")) or not isinstance(decision.get("sourceIds"), list) or not decision["sourceIds"] or not set(decision["sourceIds"]).issubset(source_ids):
                    self.add("profile_decision_" + branch, "missing", "Discovery may retain unknown applicability only with a named, sourced resolution plan and no consequential runtime evaluation.", check={"mode": "review", "questionGroup": "profile:" + branch})
                continue
            sources = decision.get("sourceIds", [])
            good = isinstance(sources, list) and bool(sources) and set(sources).issubset(source_ids) and resolved(decision.get("rationale"))
            if choice == "no" and any(source.get("requiredBranches", {}).get(branch) is True for source in self.document.get("sources", []) if isinstance(source.get("requiredBranches", {}), dict)):
                self.add("profile_required_branch_" + branch, "invalid", "A pinned source explicitly requires this branch. A no/N/A scope claim cannot remove that requirement.", check={"mode": "review", "questionGroup": "profile:" + branch})
                continue
            self.add("profile_decision_" + branch, "passed" if good else "missing", "An explicit " + branch + " scope decision needs a retained source reference and a specific rationale; the aggregate gate must verify that it matches the protected source requirements.", check={"mode": "structural", "questionGroup": "profile:" + branch})

    def branch_is_active(self, branch):
        profile = self.document.get("productProfile", {})
        decision = profile.get(branch, {}) if isinstance(profile, dict) else {}
        return isinstance(decision, dict) and decision.get("applicability") == "yes"

    def profile_checks(self):
        fields_by_id = {field["id"]: field for field in self.catalogue.get("fields", [])}
        assessed = [element for element in self.document.get("elements", []) if element.get("id") not in self.document.get("scope", {}).get("contextElementIds", [])]
        for element in assessed:
            present = self.effective_fields(element)
            for original in self.selection["checks"].get(element.get("elementType"), []):
                check = copy.deepcopy(original)
                check["questionGroup"] = "profile:" + str(element.get("id")) + ":" + check["id"]
                required = list(check.get("requiredFieldIds", []))
                active_fields = set()
                for branch, ids in check.get("conditionalFieldIds", {}).items():
                    if self.branch_is_active(branch):
                        required.extend(ids)
                        active_fields.update(ids)
                missing = []
                for field_id in dict.fromkeys(required):
                    field = fields_by_id.get(field_id)
                    value = present.get(field_id, {})
                    if not field:
                        missing.append(field_id + " (unknown catalogue field)")
                        continue
                    if isinstance(value, dict) and value.get("applicability") == "not_applicable":
                        if field_id in active_fields or field.get("requiredness", {}).get("policy") != "conditional" or field.get("protected") or value.get("protected") or not resolved(value.get("scopeJustification")):
                            missing.append(field_id + " (unsupported exemption)")
                        continue
                    if not resolved(field_value(value)):
                        missing.append(field_id)
                if missing:
                    check["resolutionKind"] = "author_repair_or_owner_decision"
                    check["missingFieldIds"] = [value.split(" (", 1)[0] for value in missing]
                    self.add(check["id"], "missing", "Required stage details unresolved: " + ", ".join(missing) + ". Deferred reference details from other stages are not demanded.", element, None, check)
                else:
                    check["resolutionKind"] = "independent_review_task"
                    status, reason, proofs = self.review(element, None, check)
                    self.add(check["id"], status, reason, element, None, check, proofs)
        # At most two deterministic reference targets per hierarchy level, never
        # per field/item. Absence is visible and neither pass nor owner question.
        for kind in ELEMENT_TYPES:
            candidates = []
            for element in assessed:
                if element.get("elementType") != kind:
                    continue
                for field in self.catalogue.get("fields", []):
                    if field.get("element") not in {"common", kind} or field.get("protected"):
                        continue
                    for check in field.get("checks", []):
                        if check.get("mode") != "review" or check.get("severity") in {"critical", "blocking"}:
                            continue
                        seed = [self.document.get("documentId"), self.selection["stage"], self.catalogue_hash, element.get("id"), check["id"]]
                        candidates.append((digest(seed), element, field, check))
            for _, element, field, original in sorted(candidates, key=lambda item: item[0])[:self.selection["sampleLimit"]]:
                status, reason, proofs = self.review(element, field, original)
                target = {"elementId": element.get("id"), "fieldId": field["id"], "checkId": original["id"]}
                matches = [review for review in self.reviews if all(review.get(key) == value for key, value in target.items())]
                disposition = matches[0] if matches else {}
                escalation = disposition.get("status") == "failed" and (status != "failed" or disposition.get("mandatoryDefect") is not False or not resolved(disposition.get("scopeJustification")))
                sample = {**target, "status": "unreviewed" if status == "missing" else status, "reason": reason, "passCriterion": original["passCriterion"], "evidenceIds": proofs, "blocking": escalation, "requiresOwnerQuestion": False, "scope": "advisory_reference_sample"}
                self.samples.append(sample)
                if escalation:
                    self.add("sample_escalation_" + original["id"], "failed", "A sampled failed criterion needs documented triage. Resolve and re-review the responsible mandatory/safety/source-integrity gate, or retain an independently justified out-of-gate advisory disposition; the finding cannot be silently ignored. " + reason, element, None, {"mode": "review", "severity": "critical", "questionGroup": "sample_escalation:" + str(element.get("id"))})

    def proof(self, ids, target, expected_fingerprint):
        if not isinstance(ids, list) or not ids:
            return "No retained evidence supplied."
        if len(ids) != len(set(ids)):
            return "Duplicate evidence references."
        for evidence_id in ids:
            item = self.evidence.get(evidence_id)
            if not item:
                return "Unknown evidence ID: " + str(evidence_id)
            if not resolved(item.get("description")) or not resolved(item.get("origin")):
                return "Evidence description and origin are required."
            bindings = [binding for binding in item.get("bindings", []) if _target_matches(binding, *target)]
            if len(bindings) != 1 or bindings[0].get("bindingVersion") != "scoped-v1" or bindings[0].get("subjectFingerprint") != expected_fingerprint:
                return "Evidence needs exactly one current scoped-v1 binding for this check; legacy global-only bindings are audit metadata, never review proof."
            if bool(item.get("syntheticFixture")) != self.synthetic:
                return "Synthetic evidence cannot certify a real product record."
            try:
                actual = evidence_hash(item, self.root)
            except (ValueError, OSError) as error:
                return str(error)
            if item.get("contentHash") != actual:
                return "Evidence snapshot hash mismatch."
        return None

    def independent(self, reviewer_id, element, subject_ids=None):
        authority = self.authorities.get(reviewer_id)
        context = set(self.document.get("scope", {}).get("contextElementIds", []))
        assessed = [item for item in self.elements.values() if item.get("id") not in context]
        subjects = [self.elements[node] for node in subject_ids if node in self.elements] if subject_ids is not None else ([element] if element else assessed)
        authors = {self.document.get("authorId")} | {item.get("authorId") for item in subjects}
        if not authority or reviewer_id in authors or not reviewer_id:
            return "Reviewer must be registered and distinct from the document and element authors."
        if "quality_review" not in authority.get("permissions", []):
            return "Registered reviewer lacks quality_review authority."
        if not resolved(authority.get("authoritySource")):
            return "Reviewer authority source is missing."
        scope = authority.get("elementIds", [])
        if "*" not in scope and any(item.get("id") not in scope for item in subjects):
            return "Reviewer authority must cover every assessed element in this review's scope; one-item rights cannot approve a whole hierarchy."
        if not self.synthetic:
            trusted = {item.get("id"): item for item in self.trust.get("authorities", [])}
            external = trusted.get(reviewer_id)
            if not external or digest(external) != digest(authority):
                return "Reviewer registry has no matching externally verified independent review profile (AI or human)."
        return None

    def review(self, element, field, check, requested_status="passed"):
        target = {"elementId": element.get("id") if element else None, "fieldId": field.get("id") if field else None, "checkId": check["id"]}
        matches = [review for review in self.reviews if all(review.get(key) == value for key, value in target.items())]
        if len(matches) != 1:
            return "missing" if not matches else "invalid", "Exactly one current review for this field/check is required.", []
        review = matches[0]
        payload = self.scoped_payload((target["elementId"], target["fieldId"], target["checkId"]))
        expected_fingerprint = digest(payload)
        if review.get("bindingVersion") != "scoped-v1" or review.get("subjectFingerprint") != expected_fingerprint:
            return "stale", "Review has no current scoped-v1 binding. Re-review this target and its declared semantic dependency closure; a legacy global hash cannot pass.", []
        if review.get("independent") is not True:
            return "invalid", "An explicit independent review declaration is required.", []
        reason = self.independent(review.get("reviewerId"), element, [item.get("id") for item in payload["elements"]])
        if reason:
            return "invalid", reason, []
        if not resolved(review.get("rationale")):
            return "invalid", "Review rationale is missing or a placeholder.", []
        reason = self.proof(review.get("evidenceIds"), (target["elementId"], target["fieldId"], target["checkId"]), expected_fingerprint)
        if reason:
            return "invalid", reason, []
        if review.get("status") != requested_status:
            return "failed", "Current independent review did not establish " + requested_status + ": " + str(review.get("status")) + ". Reviewer finding: " + review.get("rationale"), review.get("evidenceIds", [])
        if requested_status == "not_applicable" and not resolved(review.get("scopeJustification")):
            return "invalid", "N/A requires an exact, evidence-backed scope justification.", []
        return requested_status, "Current independent review and retained evidence supplied; truth requires human verification.", review.get("evidenceIds", [])

    def integrity(self):
        doc = self.document
        for error in catalogue_errors(self.catalogue):
            self.add("catalogue_invalid_" + digest(error)[:8], "invalid", error)
        if self.selection_error:
            self.add("assessment_profile", "invalid", self.selection_error)
        if doc.get("schemaVersion") != VERSION:
            self.add("model_schema", "invalid", "Unsupported model schemaVersion.")
        if doc.get("catalogueHash") != digest(self.catalogue):
            self.add("catalogue_pin", "stale", "The input must pin the exact full catalogue; deleted/changed checks invalidate it.")
        else:
            self.add("catalogue_pin", "passed", "Exact catalogue hash pinned.")
        for key in ("documentId", "authorId"):
            self.add("identity_" + key, "passed" if resolved(doc.get(key)) else "missing", "Stable " + key + " is required.")
        if not isinstance(doc.get("revision"), int) or isinstance(doc.get("revision"), bool) or doc["revision"] < 1:
            self.add("revision", "invalid", "A positive integer revision is required.")
        if doc.get("mode") not in {"real", "synthetic_fixture"}:
            self.add("mode", "invalid", "Input must explicitly identify real or synthetic_fixture mode.")
        scope = doc.get("scope", {})
        declared = scope.get("includedElementTypes", [])
        actual = {item.get("elementType") for item in doc.get("elements", []) if item.get("id") not in scope.get("contextElementIds", [])}
        if scope.get("mode") not in {"full_hierarchy", "partial"} or set(declared) != actual or not actual or not actual.issubset(set(ELEMENT_TYPES)):
            self.add("declared_scope", "invalid", "Declare exact assessed hierarchy types; missing levels cannot silently count as fully checked.")
        elif scope.get("mode") == "full_hierarchy" and actual != set(ELEMENT_TYPES):
            self.add("full_hierarchy_coverage", "missing", "Full-hierarchy assessment requires every one of the eight element types.")
        elif scope.get("mode") == "partial" and not resolved(scope.get("justification")):
            self.add("partial_scope_justification", "missing", "Partial assessment needs a precise scope justification; it cannot certify omitted levels.")
        else:
            self.add("declared_scope", "passed", "Exact assessment scope declared; contextual ancestors are not certified by this report.")
        for name in ("elements", "sources", "evidence", "authorities", "reviews"):
            values = doc.get(name, [])
            ids = [value.get("id") for value in values]
            status = "passed" if all(ids) and len(set(ids)) == len(ids) and (bool(ids) or name not in {"elements", "sources"}) else "invalid"
            self.add("unique_" + name, status, "Non-empty unique IDs are required; elements and authoritative source snapshots cannot be empty.")
        source_ids = {source.get("id") for source in doc.get("sources", [])}
        for source in doc.get("sources", []):
            good = resolved(source.get("text")) and resolved(source.get("version")) and doc.get("sourcePins", {}).get(source.get("id")) == source_hash(source)
            self.add("source_pin_" + str(source.get("id")), "passed" if good else "stale", "Retain and pin exact source text, source version and approval/originality state.")
            if "requiredBranches" in source:
                branches = source["requiredBranches"]
                valid = isinstance(branches, dict) and set(branches).issubset({"ai", "personalData"}) and all(value is True for value in branches.values())
                self.add("source_required_branches_" + str(source.get("id")), "passed" if valid else "invalid", "Optional source.requiredBranches may only assert ai/personalData true requirements. Missing metadata does not mean no obligation; false cannot remove one.")
        if set(doc.get("sourcePins", {})) != source_ids:
            self.add("source_pin_set", "invalid", "Source pin IDs must exactly match all retained sources.")
        expected_review_targets = set()
        for element in self.document.get("elements", []):
            if element.get("id") in scope.get("contextElementIds", []):
                continue
            for field in self.catalogue.get("fields", []):
                if field.get("element") in {"common", element.get("elementType")}:
                    for check in field.get("checks", []):
                        expected_review_targets.add((element.get("id"), field["id"], check["id"]))
            for check in self.catalogue.get("elementChecks", []):
                if check.get("element", check.get("scopeElement", "all")) in {"all", "common", element.get("elementType")}:
                    expected_review_targets.add((element.get("id"), None, check["id"]))
            for check in self.catalogue.get("profileChecks", []):
                if element.get("elementType") in check.get("applicable_types", []):
                    expected_review_targets.add((element.get("id"), None, check["id"]))
        expected_review_targets.update((None, None, check["id"]) for check in self.catalogue.get("hierarchyChecks", []))
        for review in self.reviews:
            target = (review.get("elementId"), review.get("fieldId"), review.get("checkId"))
            valid = target in expected_review_targets and review.get("status") in {"passed", "failed", "not_applicable"}
            if not valid:
                self.add("review_target_" + str(review.get("id")), "invalid", "Unknown, wrong-level or incompatible review target/status is never silently accepted.")
        for element in doc.get("elements", []):
            kind = element.get("elementType")
            if kind not in ELEMENT_TYPES:
                self.add("element_type", "invalid", "Unknown hierarchy element type.", element)
                continue
            parent_id = element.get("parentId")
            parent = self.elements.get(parent_id)
            valid = (kind == "vision" and parent_id is None) or (parent and parent.get("elementType") in PARENT_TYPES[kind])
            self.add("parent", "passed" if valid else "invalid", "Parent must exist and belong to an allowed hierarchy level.", element)
            if not element.get("sourceIds") or any(item not in source_ids for item in element.get("sourceIds", [])):
                self.add("source_links", "missing", "Every element needs existing authoritative source references.", element)
            for relation in ("dependencyIds", "designDependencyIds"):
                for dependency in element.get(relation, []):
                    if dependency not in self.elements or dependency == element.get("id"):
                        self.add(relation + "_" + str(dependency), "invalid", "Dependencies must reference a different existing element. dependencyIds are completion prerequisites; designDependencyIds are reference relationships and do not authorize completion.", element)
            state = element.get("approvalStatus", "draft")
            if state not in {"draft", "proposed", "approved", "frozen"}:
                self.add("approval_state", "invalid", "Approval state must be separate and explicit.", element)
            if state in {"approved", "frozen"} and (not isinstance(element.get("approvalReference"), (str, dict)) or not resolved(element.get("approvalReference"))):
                self.add("approval_reference", "missing", "Approved/frozen status requires an original authority decision reference; checker results do not grant approval.", element)
        for relation in ("parentId", "dependencyIds"):
            active, visited, stack, cycle_path = set(), set(), [], []
            def visit(node):
                if node in active:
                    cycle_path.extend(stack[stack.index(node):] + [node])
                    return True
                if node in visited or node not in self.elements:
                    return False
                active.add(node)
                stack.append(node)
                value = self.elements[node].get(relation)
                edges = value if isinstance(value, list) else ([value] if value else [])
                cyclic = any(visit(edge) for edge in edges)
                active.remove(node)
                stack.pop()
                visited.add(node)
                return cyclic
            cyclic = any(visit(node) for node in self.elements)
            self.add("acyclic_" + relation, "invalid" if cyclic else "passed", "Cycle in " + relation + ": " + " -> ".join(cycle_path) if cyclic else relation + " is acyclic. Design-reference cycles are permitted; only parent and completion-prerequisite cycles block structural integrity.")
        if not self.synthetic:
            self.real_signoff()

    def real_signoff(self):
        if self.trust.get("catalogueHash") != digest(self.catalogue):
            self.add("external_trust_catalogue", "missing", "Real mode requires separately supplied independent review profiles and a verification receipt pinned to this catalogue.")
            return
        cited_ids = {source_id for element in self.elements.values() for source_id in element.get("sourceIds", [])}
        cited_ids.update(source_id for decision in self.document.get("productProfile", {}).values() if isinstance(decision, dict) for source_id in decision.get("sourceIds", []))
        baseline = self.trust.get("sourcePins", {})
        if not isinstance(baseline, dict) or any(baseline.get(source_id) != self.document.get("sourcePins", {}).get(source_id) for source_id in cited_ids):
            self.add("external_source_baseline", "stale", "Real assessment needs separately verified source pins; local re-pinning cannot prove original text was preserved.")
        receipt_fingerprint = review_set_fingerprint(self.document, self.catalogue, self.root, self.scoped_payload)
        signoffs = [item for item in self.trust.get("reviewVerifications", []) if item.get("bindingVersion") == "scoped-v1" and item.get("subjectFingerprint") == receipt_fingerprint]
        if len(signoffs) != 1:
            self.add("external_review_verification", "missing", "Exactly one current scoped-v1 external verification receipt pinned to the exact scoped review set is required; model-local review names cannot authenticate approval.", check={"mode": "review", "resolutionKind": "independent_review_task"})
            return
        item = signoffs[0]
        hashes = sorted(digest(review) for review in self.reviews)
        authors = {self.document.get("authorId")} | {element.get("authorId") for element in self.elements.values()}
        valid = (item.get("verificationMethod") in {"human_witness", "independent_agent_review"} and item.get("independent") is True and
                 item.get("verifierId") not in authors | {None} and
                 self.independent(item.get("verifierId"), None) is None and item.get("reviewHashes") == hashes and
                 resolved(item.get("verificationRecord")))
        self.add("external_review_verification", "passed" if valid else "invalid", "Supplied external review receipt structurally matches exact review hashes and registered profiles. This editable offline file does not authenticate identities, registry provenance or independence; all real-mode conclusions remain advisory and require verification outside the authoring agent.", check={"mode": "review", "resolutionKind": "independent_review_task"})

    def structural(self, element, field, check):
        value = field_value(self.effective_fields(element).get(field["id"]))
        rule = check.get("structuralRule", "nonempty")
        rule = rule.get("type") if isinstance(rule, dict) else rule
        good = resolved(value)
        if rule == "text":
            good = good and isinstance(value, str)
        elif rule == "list":
            good = good and isinstance(value, list)
        elif rule == "object":
            good = good and isinstance(value, dict)
        elif rule == "unique_id":
            good = good and isinstance(value, str) and value == element.get("id")
        self.add(check["id"], "passed" if good else "missing", "Structural value present and resolved." if good else "Missing, whitespace-only, unresolved placeholder or incorrect value type.", element, field, check)

    def check_fields(self):
        known = {field["id"] for field in self.catalogue.get("fields", [])}
        active_branch_fields = set()
        for gate in self.catalogue.get("profileChecks", []):
            for branch, ids in gate.get("conditionalFieldIds", {}).items():
                if self.branch_is_active(branch):
                    active_branch_fields.update(ids)
        for element in self.document.get("elements", []):
            if element.get("id") in self.document.get("scope", {}).get("contextElementIds", []):
                continue
            present = self.effective_fields(element)
            for unknown in set(present) - known:
                self.add("unknown_field_" + unknown, "invalid", "Unknown field cannot replace a required catalogue field.", element)
            valid_ids = {field["id"] for field in self.catalogue.get("fields", []) if field.get("element") in {"common", element.get("elementType")}}
            for wrong_level in set(present) & known - valid_ids:
                self.add("wrong_level_field_" + wrong_level, "invalid", "A field belonging to another hierarchy level cannot substitute for this level's fields.", element)
            fields = [field for field in self.catalogue.get("fields", []) if field.get("element") in {"common", element.get("elementType")}]
            for field in fields:
                value = present.get(field["id"], {})
                applicability = value.get("applicability", "applicable") if isinstance(value, dict) else "applicable"
                if applicability not in {"applicable", "not_applicable"}:
                    self.add("applicability", "invalid", "Unknown applicability never means exempt.", element, field)
                    applicability = "applicable"
                declared_type = field.get("valueType", "text")
                actual_value = field_value(value)
                allowed_type = {"text": str, "list": list, "object": dict, "number": (int, float), "boolean": bool}.get(declared_type)
                if applicability == "applicable" and (allowed_type is None or resolved(actual_value) and not isinstance(actual_value, allowed_type)):
                    self.add("value_type", "invalid", "Field value must match its declared catalogue valueType; a boolean/object cannot fake a text field.", element, field)
                if self.selection["mode"] != "exhaustive":
                    if applicability == "not_applicable" and (field.get("requiredness", {}).get("policy") != "conditional" or field.get("protected") or value.get("protected")):
                        self.add("applicability", "invalid", "Always-required or protected requirements cannot be exempted even when reference checks are deferred.", element, field)
                    if resolved(actual_value):
                        for check in field.get("checks", []):
                            rule = check.get("structuralRule", "nonempty")
                            rule = rule.get("type") if isinstance(rule, dict) else rule
                            if check.get("mode") == "structural" and rule == "unique_id":
                                self.structural(element, field, check)
                    continue
                if applicability == "not_applicable":
                    conditional = field.get("requiredness", {}).get("policy") == "conditional" and not field.get("protected") and not value.get("protected") and field["id"] not in active_branch_fields
                    for check in field.get("checks", []):
                        if not conditional:
                            self.add(check["id"], "invalid", "Always-required or protected requirements cannot be exempted with N/A.", element, field, check)
                        else:
                            status, reason, proofs = self.review(element, field, check, "not_applicable")
                            self.add(check["id"], status, reason, element, field, check, proofs)
                    continue
                for check in field.get("checks", []):
                    if check.get("mode") == "structural":
                        self.structural(element, field, check)
                    elif check.get("mode") == "review":
                        if not resolved(field_value(value)):
                            self.add(check["id"], "missing", "A semantic review cannot pass an empty or unresolved field.", element, field, check)
                        else:
                            status, reason, proofs = self.review(element, field, check)
                            self.add(check["id"], status, reason, element, field, check, proofs)
                    else:
                        self.add(check["id"], "invalid", "Unsupported quality check mode.", element, field, check)

    def additional_checks(self):
        for check in self.catalogue.get("elementChecks", []):
            applicable = check.get("element", check.get("scopeElement", "all"))
            for element in self.document.get("elements", []):
                if element.get("id") in self.document.get("scope", {}).get("contextElementIds", []):
                    continue
                if applicable not in {"all", "common", element.get("elementType")}:
                    continue
                status, reason, proofs = self.review(element, None, check)
                self.add(check["id"], status, reason, element, None, check, proofs)
        for check in self.catalogue.get("hierarchyChecks", []):
            status, reason, proofs = self.review(None, None, check)
            self.add(check["id"], status, reason, None, None, check, proofs)

    def run(self):
        self.integrity()
        self.profile_decisions()
        self.check_fields()
        if self.selection["mode"] == "exhaustive":
            self.additional_checks()
        elif self.selection["mode"] == "profile":
            self.profile_checks()
        unresolved = [item for item in self.results if item["blocking"] and item["status"] not in {"passed", "not_applicable"}]
        if any(item["status"] == "invalid" for item in unresolved):
            status = "blocked"
        elif unresolved:
            status = "needs_input" if any(item["mode"] == "review" or item["status"] == "missing" for item in unresolved) else "needs_revision"
        else:
            status = "synthetic_checks_satisfied" if self.synthetic else ("stage_checks_satisfied" if self.selection["mode"] == "profile" else "advisory_checks_satisfied")
        counts = {name: sum(item["status"] == name for item in self.results) for name in ("passed", "not_applicable", "missing", "failed", "stale", "invalid")}
        assessed = [element for element in self.document.get("elements", []) if element.get("id") not in self.document.get("scope", {}).get("contextElementIds", [])]
        mandatory_review_count = sum(item["mode"] == "review" and item["blocking"] for item in self.results)
        reference_count = sum(sum(len(field.get("checks", [])) for field in self.catalogue.get("fields", []) if field.get("element") in {"common", element.get("elementType")}) + sum(check.get("element", check.get("scopeElement", "all")) in {"all", "common", element.get("elementType")} for check in self.catalogue.get("elementChecks", [])) for element in assessed) + len(self.catalogue.get("hierarchyChecks", []))
        coverage = {"assessmentMode": self.selection["mode"], "stage": self.selection["stage"], "selectedMandatoryReviewCount": mandatory_review_count,
                    "integrityChecksAlwaysRun": True, "referenceCheckInstances": reference_count, "referenceChecksFullyAssessed": self.selection["mode"] == "exhaustive",
                    "referenceInstancesDeferred": reference_count if self.selection["mode"] == "profile" else 0,
                    "advisorySampleCount": len(self.samples), "advisoryUnreviewedCount": sum(item["status"] == "unreviewed" for item in self.samples),
                    "legacyDefaultWarning": "No assessment supplied: default planning profile selected; this is not a full-reference review." if self.selection["legacyDefault"] else None,
                    "conclusion": "Only the selected stage's seven mandatory gates per assessed item were checked. Advisory samples and deferred reference details do not count as passed." if self.selection["mode"] == "profile" else "Explicit exhaustive reference assessment; offline conclusions remain advisory for real inputs."}
        return {"schemaVersion": VERSION, "bindingVersion": "scoped-v1", "generatedAt": NOW(), "documentId": self.document.get("documentId"), "revision": self.document.get("revision"),
                "catalogueHash": digest(self.catalogue), "subjectFingerprint": self.fingerprint,
                "qualityState": {"status": status, "passed": counts["passed"], "applicable": len(self.results) - counts["not_applicable"], "exemptions": counts["not_applicable"], "counts": counts, "score": None,
                                 "exitRule": "Every selected mandatory stage gate and integrity check must pass with current evidence and supplied review. Deferred/reference-sampled checks cannot certify the full catalogue. No averaging, timeout or iteration limit grants a pass.", "certificationGranted": False},
                "assessmentCoverage": coverage, "advisorySamples": self.samples, "fieldCompatibility": self.compatibility_used,
                "reviewerAuthentication": {"status": "synthetic_test_only" if self.synthetic else "not_authenticated_offline", "advisoryOnly": True, "registryCanBeAuthorCreated": True, "externalApprovalRequired": True},
                "scope": copy.deepcopy(self.document.get("scope", {})),
                "readinessState": {"status": "supplied_unverified", "suppliedClaim": copy.deepcopy(self.document.get("readinessState", {"status": "not_assessed"})), "assessedByChecker": False, "authorizationGranted": False},
                "deliveryState": {"status": "supplied_unverified", "suppliedClaim": copy.deepcopy(self.document.get("deliveryState", {"status": "not_assessed"})), "assessedByChecker": False, "deliveryObservedByChecker": False},
                "assurance": "SYNTHETIC FIXTURE ONLY — not product approval or real delivery." if self.synthetic else "ADVISORY ONLY. Documentation checks relative to the selected stage/catalogue and supplied review files. An author can create a reviewer registry or trust store; the offline checker does not authenticate people, prove independence or semantic truth, or grant execution, business, legal, safety, contractual or release approval. Authority must be verified outside the authoring agent.",
                "checks": self.results, "unresolvedCheckIds": [item["id"] for item in unresolved]}


def scaffold(catalogue, document_id="new-product-plan", author_id="Pending", mode="real", assessment_mode="profile", stage="planning"):
    elements = []
    previous = None
    story = None
    for index, kind in enumerate(ELEMENT_TYPES, 1):
        element_id = kind + "-001"
        parent = story if kind in {"acceptance_criterion", "technical_task"} else previous
        fields = {}
        for field in catalogue.get("fields", []):
            if field.get("element") in {"common", kind}:
                fields[field["id"]] = {"value": "Pending: " + field.get("label", field["id"]), "applicability": "applicable"}
        elements.append({"id": element_id, "elementType": kind, "parentId": parent, "authorId": author_id, "approvalStatus": "draft", "originality": "proposed", "sourceIds": ["source-001"], "dependencyIds": [], "fields": fields})
        previous = element_id
        if kind == "user_story":
            story = element_id
    source = {"id": "source-001", "text": "Pending: retain authoritative source text without editing it.", "version": "Pending", "originality": "proposed_placeholder", "approvalStatus": "draft", "protected": False}
    return {"schemaVersion": VERSION, "documentId": document_id, "revision": 1, "authorId": author_id, "mode": mode,
            "catalogueHash": digest(catalogue), "assessment": {"mode": assessment_mode, **({"stage": stage} if assessment_mode == "profile" else {})},
            "productProfile": {"ai": {"applicability": "unknown", "sourceIds": [], "rationale": ""}, "personalData": {"applicability": "unknown", "sourceIds": [], "rationale": ""}},
            "scope": {"mode": "full_hierarchy", "includedElementTypes": list(ELEMENT_TYPES), "contextElementIds": []}, "elements": elements, "sources": [source], "sourcePins": {source["id"]: source_hash(source)},
            "authorities": [], "evidence": [], "reviews": [], "approvalRecords": [], "history": [],
            "readinessState": {"status": "not_assessed", "reason": "Documentation quality does not authorize implementation or launch."},
            "deliveryState": {"status": "not_assessed", "reason": "No implementation, launch, operational availability or acceptance inferred."}}


def question_packet(report, document, state=None, batch_size=3):
    from quality_loop import question_packet as build_packet
    return build_packet(report, document, state, batch_size, api=globals())


def protect_revision(previous, candidate):
    validate_document_shape(previous)
    validate_document_shape(candidate)
    if candidate.get("documentId") != previous.get("documentId"):
        raise ValueError("A revision must retain its documentId.")
    if candidate.get("revision") != previous.get("revision", 0) + 1:
        raise ValueError("A revision must increment the version exactly once.")
    if not resolved(candidate.get("changeReason")):
        raise ValueError("A revision needs a meaningful changeReason; do not fabricate a reason.")
    old_sources = {item["id"]: item for item in previous.get("sources", [])}
    new_sources = {item["id"]: item for item in candidate.get("sources", [])}
    for source_id, source in old_sources.items():
        if source.get("protected", True) and (source_id not in new_sources or source_hash(source) != source_hash(new_sources[source_id])):
            raise ValueError("Protected original source cannot be changed, unprotected or deleted: " + source_id)
    new_elements = {item["id"]: item for item in candidate.get("elements", [])}
    for old in previous.get("elements", []):
        if old.get("protected") or old.get("approvalStatus") in {"approved", "frozen"}:
            new = new_elements.get(old["id"])
            if new is None or digest(new) != digest(old):
                raise ValueError("Approved/frozen/protected element cannot be overwritten; append a separate proposed amendment: " + old["id"])
        else:
            for field_id, field in old.get("fields", {}).items():
                if isinstance(field, dict) and field.get("protected"):
                    new = new_elements.get(old["id"], {}).get("fields", {}).get(field_id)
                    if digest(new) != digest(field):
                        raise ValueError("Protected field cannot be overwritten: " + field_id)


def apply_revision(document_path, candidate_path, state_dir):
    previous, candidate = read_json(document_path), read_json(candidate_path)
    protect_revision(previous, candidate)
    state_dir = Path(state_dir)
    state_dir.mkdir(parents=True, exist_ok=True)
    snapshot = state_dir / ("revision-" + str(previous["revision"]) + "-" + digest(previous)[:12] + ".json")
    if not snapshot.exists():
        write_json(snapshot, previous)
    candidate.setdefault("history", [])
    candidate["history"] = copy.deepcopy(previous.get("history", [])) + [{"at": NOW(), "previousRevision": previous["revision"], "previousHash": digest(previous), "snapshot": snapshot.name, "changeReason": candidate.get("changeReason", "Pending") }]
    write_json(document_path, candidate)
    return {"revision": candidate["revision"], "preservedSnapshot": str(snapshot), "nextAction": "Rerun integrity and scoped checks. Only changed targets and their actual declared dependency closures lose review/evidence validity; unchanged scoped-v1 reviews remain eligible."}


def migrate_document(catalogue, document_path, output_path, state_dir, stage="planning", reason=None):
    """Explicit representation migration. Originals/protected content remain retained."""
    if Path(document_path).resolve() == Path(output_path).resolve():
        raise ValueError("Migration must write a separate output; the original document is retained.")
    if stage not in REVIEW_STAGES or not resolved(reason):
        raise ValueError("Migration needs a declared stage and a meaningful change reason.")
    original = read_json(document_path)
    candidate = copy.deepcopy(original)
    aliases = catalogue.get("fieldAliases", {})
    renamed, retained = [], []
    for element in candidate.get("elements", []):
        fields = element.get("fields", {})
        for old, current in aliases.items():
            if old not in fields:
                continue
            if current in fields and digest(fields[old]) != digest(fields[current]):
                raise ValueError("Conflicting legacy/canonical values need an explicit authority decision: " + old)
            value = fields[old]
            protected = element.get("protected") or element.get("approvalStatus") in {"approved", "frozen"} or isinstance(value, dict) and value.get("protected")
            if protected:
                retained.append({"elementId": element.get("id"), "legacyFieldId": old, "canonicalFieldId": current})
                continue
            fields.setdefault(current, value)
            fields.pop(old)
            renamed.append({"elementId": element.get("id"), "legacyFieldId": old, "canonicalFieldId": current})
    candidate["revision"] = original.get("revision", 0) + 1
    candidate["changeReason"] = reason
    candidate["assessment"] = {"mode": "profile", "stage": stage}
    candidate["catalogueHash"] = digest(catalogue)
    candidate.setdefault("productProfile", {"ai": {"applicability": "unknown", "sourceIds": [], "rationale": ""}, "personalData": {"applicability": "unknown", "sourceIds": [], "rationale": ""}})
    candidate["reviews"] = []
    for evidence in candidate.get("evidence", []):
        evidence.pop("boundTo", None)
    candidate["qualityState"] = {"status": "not_assessed", "reason": "Representation/catalogue/stage migration retires every earlier favorable verdict; new evidence bindings and stage review are required."}
    protect_revision(original, candidate)
    state_dir = Path(state_dir)
    state_dir.mkdir(parents=True, exist_ok=True)
    snapshot = state_dir / ("pre-migration-revision-" + str(original.get("revision")) + "-" + digest(original)[:12] + ".json")
    if not snapshot.exists():
        snapshot.write_bytes(Path(document_path).read_bytes())
    candidate["history"] = copy.deepcopy(original.get("history", [])) + [{"at": NOW(), "kind": "explicit_generic_field_migration", "previousRevision": original.get("revision"), "previousHash": digest(original), "snapshot": snapshot.name, "changeReason": reason, "renamedFields": renamed, "protectedAliasesRetained": retained, "retiredReviewCount": len(original.get("reviews", [])), "sourcePinsUnchanged": original.get("sourcePins") == candidate.get("sourcePins")}]
    write_json(output_path, candidate)
    return {"created": str(output_path), "preservedSnapshot": str(snapshot), "renamedFields": renamed, "protectedAliasesRetained": retained, "reviewReuseAllowed": False, "nextAction": "Resolve product applicability, bind retained evidence to the new fingerprint, and obtain the seven current selected-stage reviews per item. Protected source snapshots and frozen items were preserved."}


def record_answer(state_dir, question_id, answer, answered_by, assessment="ready_for_revision", follow_up_reason=None):
    from quality_loop import record_answer as retain_answer
    return retain_answer(state_dir, question_id, answer, answered_by, assessment, follow_up_reason, api=globals())


def main(argv=None):
    import quality_loop
    import quality_tools
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalogue", default=str(Path(__file__).with_name("catalogue.json")))
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("scaffold")
    create.add_argument("--output", required=True)
    create.add_argument("--document-id", default="new-product-plan")
    create.add_argument("--author-id", default="Pending")
    create.add_argument("--mode", choices=["real", "synthetic_fixture"], default="real")
    create.add_argument("--assessment-mode", choices=["profile", "exhaustive"], default="profile")
    create.add_argument("--stage", choices=REVIEW_STAGES, default="planning")
    for name in ("check", "loop", "fingerprint"):
        cmd = commands.add_parser(name)
        cmd.add_argument("--document", required=True)
        cmd.add_argument("--trust-store")
        cmd.add_argument("--assessment-mode", choices=["profile", "exhaustive"])
        cmd.add_argument("--stage", choices=REVIEW_STAGES)
        cmd.add_argument("--allow-synthetic", action="store_true", help="Explicitly permit synthetic mechanics input; no real qualification or approval is granted.")
        if name == "fingerprint":
            cmd.add_argument("--element-id")
            cmd.add_argument("--field-id")
            cmd.add_argument("--check-id")
        if name != "fingerprint":
            cmd.add_argument("--report", required=True)
        if name == "loop":
            cmd.add_argument("--state-dir", required=True)
            cmd.add_argument("--batch-size", type=int, default=3)
            cmd.add_argument("--interactive", action="store_true")
    revise = commands.add_parser("apply-revision")
    revise.add_argument("--document", required=True)
    revise.add_argument("--candidate", required=True)
    revise.add_argument("--state-dir", required=True)
    migrate = commands.add_parser("migrate")
    migrate.add_argument("--document", required=True)
    migrate.add_argument("--output", required=True)
    migrate.add_argument("--state-dir", required=True)
    migrate.add_argument("--stage", choices=REVIEW_STAGES, default="planning")
    migrate.add_argument("--change-reason", required=True)
    answer = commands.add_parser("record-answer")
    answer.add_argument("--state-dir", required=True)
    answer.add_argument("--question-id", required=True)
    answer.add_argument("--answer-file", required=True)
    answer.add_argument("--answered-by", required=True)
    answer.add_argument("--assessment", choices=["ready_for_revision", "needs_clarification"], default="ready_for_revision")
    answer.add_argument("--follow-up-reason")
    acknowledge = commands.add_parser("acknowledge-batch")
    acknowledge.add_argument("--state-dir", required=True)
    acknowledge.add_argument("--batch-id", required=True)
    acknowledge.add_argument("--acknowledged-by", required=True)
    dismiss = commands.add_parser("dismiss-question")
    dismiss.add_argument("--state-dir", required=True)
    dismiss.add_argument("--question-id", required=True)
    dismiss.add_argument("--reason", required=True)
    dismiss.add_argument("--dismissed-by", required=True)
    quality_tools.register_commands(commands)
    args = parser.parse_args(argv)
    try:
        if args.command in {"summary", "next", "explain"}:
            print(json.dumps(quality_tools.dispatch(args, None, globals()), indent=2, ensure_ascii=False))
            return 0
        if args.command == "acknowledge-batch":
            print(json.dumps(quality_loop.acknowledge_batch(args.state_dir, args.batch_id, args.acknowledged_by, api=globals()), indent=2, ensure_ascii=False))
            return 0
        if args.command == "dismiss-question":
            print(json.dumps(quality_loop.dismiss_question(args.state_dir, args.question_id, args.reason, args.dismissed_by, api=globals()), indent=2, ensure_ascii=False))
            return 0
        if args.command == "apply-revision":
            print(json.dumps(apply_revision(args.document, args.candidate, args.state_dir), indent=2))
            return 0
        if args.command == "record-answer":
            result = record_answer(args.state_dir, args.question_id, Path(args.answer_file).read_text(encoding="utf-8"), args.answered_by, args.assessment, args.follow_up_reason)
            print(json.dumps(result, indent=2))
            return 0
        catalogue = read_json(args.catalogue)
        errors = catalogue_errors(catalogue)
        if errors:
            raise ValueError("Invalid catalogue: " + "; ".join(errors))
        if args.command in quality_tools.COMMANDS:
            print(json.dumps(quality_tools.dispatch(args, catalogue, globals()), indent=2, ensure_ascii=False))
            return 0
        if args.command == "scaffold":
            write_json(args.output, scaffold(catalogue, args.document_id, args.author_id, args.mode, args.assessment_mode, args.stage))
            print(json.dumps({"created": args.output, "status": "draft_needs_input", "catalogueHash": digest(catalogue)}))
            return 0
        if args.command == "migrate":
            print(json.dumps(migrate_document(catalogue, args.document, args.output, args.state_dir, args.stage, args.change_reason), indent=2))
            return 0
        document = read_json(args.document)
        validate_document_shape(document)
        if document.get("mode") == "synthetic_fixture" and not args.allow_synthetic:
            raise ValueError("Synthetic fixture input requires explicit --allow-synthetic. This flag authorizes only a labelled mechanics test, never real product qualification.")
        if args.assessment_mode or args.stage:
            document["assessment"] = {"mode": args.assessment_mode or "profile", **({"stage": args.stage or "planning"} if args.assessment_mode != "exhaustive" else {})}
        root = Path(args.document).resolve().parent
        trust = read_json(args.trust_store) if args.trust_store else None
        if args.command == "fingerprint":
            if args.check_id:
                print(check_subject_fingerprint(document, catalogue, args.element_id, args.field_id, args.check_id, root))
            elif args.element_id or args.field_id:
                raise ValueError("Scoped fingerprint requires --check-id; omit all target flags only for the global audit fingerprint.")
            else:
                print(subject_fingerprint(document, catalogue, root))
            return 0
        report = Checker(catalogue, document, root, trust).run()
        write_json(args.report, report)
        result = {"qualityState": report["qualityState"], "readinessState": report["readinessState"], "deliveryState": report["deliveryState"], "assurance": report["assurance"], "report": args.report}
        if args.command == "loop":
            state_dir = Path(args.state_dir)
            state_path = state_dir / "loop-state.json"
            state = read_json(state_path) if state_path.exists() else None
            packet, state = question_packet(report, document, state, args.batch_size)
            quality_loop.write_state(state_dir, state, api=globals())
            write_json(state_dir / "questions.json", packet)
            result["questionPacket"] = str(state_dir / "questions.json")
            result["loopStatus"] = packet["loopStatus"]
            result["newQuestionCount"] = packet["newQuestionCount"]
            result["pendingQuestionCount"] = packet["pendingQuestionCount"]
            result["reviewerQueueCount"] = packet["reviewerQueueCount"]
            result["repairQueueCount"] = packet["repairQueueCount"]
            result["currentBatchId"] = packet["currentBatchId"]
            result["nextBatch"] = [{key: question[key] for key in ("id", "elementId", "fieldId", "question")} | {"checksToResolve": len(question["checksToResolve"])} for question in packet["nextBatch"]]
            if args.interactive:
                respondent = input("Your registered respondent ID (answers do not grant approval): ").strip()
                for question in packet["nextBatch"]:
                    answer_text = input(question["id"] + " — " + question["question"] + "\nAnswer (blank pauses): ").strip()
                    if not answer_text:
                        break
                    record_answer(state_dir, question["id"], answer_text, respondent)
                result["nextAction"] = "Apply a verified proposed revision; then rerun. No answers were promoted to approvals."
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if report["qualityState"]["status"] in SUCCESS_STATES else 2
    except (ValueError, KeyError, TypeError, AttributeError, OSError, json.JSONDecodeError) as error:
        print(json.dumps({"qualityState": {"status": "blocked"}, "error": str(error), "noPassGranted": True}), file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
