"""Independent CLI helper audit; generated fixture verdicts are mechanics only."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

OUT = Path(__file__).resolve().parent
BASE = OUT.parent
spec = importlib.util.spec_from_file_location("audit_qc", BASE / "quality_checker.py")
qc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qc)
catalogue = qc.read_json(BASE / "catalogue.json")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def state_hashes(directory):
    return {str(path.relative_to(directory)): sha(path) for path in directory.rglob("*") if path.is_file()}


def synthetic_scale(original):
    """Same 302-item distribution as the independently reviewed scale fixture."""
    document = copy.deepcopy(original)
    document.update(documentId="SYNTHETIC-302-HELPER-AUDIT", elements=[], evidence=[], reviews=[])
    templates = {item["elementType"]: item for item in original["elements"]}
    counts = {"vision": 1, "strategy": 1, "roadmap": 1, "release_goal": 1, "epic": 8, "user_story": 40, "acceptance_criterion": 150, "technical_task": 100}
    eid = lambda kind, index: kind + "-%03d" % index
    selection = qc.assessment_selection(catalogue, document)
    for kind, count in counts.items():
        for index in range(1, count + 1):
            item = copy.deepcopy(templates[kind])
            item["id"] = eid(kind, index)
            parent = None if kind == "vision" else eid({"strategy": "vision", "roadmap": "strategy", "release_goal": "roadmap", "epic": "release_goal", "user_story": "epic", "acceptance_criterion": "user_story", "technical_task": "user_story"}[kind], (index - 1) // 5 + 1 if kind == "user_story" else (index - 1) % 40 + 1 if kind in {"acceptance_criterion", "technical_task"} else 1)
            item["parentId"] = parent
            if "common.id" in item["fields"]:
                item["fields"]["common.id"]["value"] = item["id"]
            document["elements"].append(item)
            artifact = {"id": "proof-" + item["id"], "kind": "mechanics_fixture", "description": "SYNTHETIC generated fixture for CLI performance only.", "origin": "Independent local helper audit", "syntheticFixture": True, "content": {"label": "SYNTHETIC TEST ONLY", "item": item["id"]}, "bindings": []}
            artifact["contentHash"] = qc.evidence_hash(artifact, ".")
            document["evidence"].append(artifact)
            for gate in selection["checks"][kind]:
                document["reviews"].append({"id": "review-%04d" % len(document["reviews"]), "elementId": item["id"], "fieldId": None, "checkId": gate["id"], "status": "passed", "reviewerId": "fixture-reviewer", "independent": True, "evidenceIds": [artifact["id"]], "rationale": "SYNTHETIC generated test verdict; no actual semantic review or product qualification."})
    checker = qc.Checker(catalogue, document)
    evidence = {item["id"]: item for item in document["evidence"]}
    for review in document["reviews"]:
        target = {key: review.get(key) for key in ("elementId", "fieldId", "checkId")}
        fingerprint = qc.digest(checker.scoped_payload(tuple(target.values())))
        review.update(bindingVersion="scoped-v1", subjectFingerprint=fingerprint)
        evidence[review["evidenceIds"][0]]["bindings"].append({**target, "bindingVersion": "scoped-v1", "subjectFingerprint": fingerprint})
    return document


def main():
    runs, assertions = [], {}
    original = qc.read_json(BASE / "examples" / "synthetic-planning-pass.json")
    with tempfile.TemporaryDirectory(prefix="v4-helper-audit-") as temporary:
        work = Path(temporary)
        document_path, report_path = work / "document.json", work / "report.json"
        qc.write_json(document_path, original)
        original_hash = sha(document_path)
        def run(name, arguments, expected=0):
            command = [sys.executable, str(BASE / "quality_checker.py"), "--catalogue", str(BASE / "catalogue.json"), *map(str, arguments)]
            started = time.perf_counter()
            result = subprocess.run(command, text=True, capture_output=True)
            runs.append({"name": name, "command": [str(value).replace(str(work), "<temporary-audit-directory>") for value in arguments], "exitCode": result.returncode, "expectedExitCode": expected, "seconds": round(time.perf_counter() - started, 4), "stdoutBytes": len(result.stdout.encode()), "stderrBytes": len(result.stderr.encode()), "stdoutSha256": hashlib.sha256(result.stdout.encode()).hexdigest(), "stderrSha256": hashlib.sha256(result.stderr.encode()).hexdigest()})
            assertions[name + "Exit"] = result.returncode == expected and "Traceback" not in result.stderr
            return result
        run("deniedSynthetic", ["check", "--document", document_path, "--report", work / "denied.json"], 3)
        run("labelledSynthetic", ["check", "--document", document_path, "--report", report_path, "--allow-synthetic"])
        report = qc.read_json(report_path)
        assertions["fixtureStatusIsDistinct"] = report["qualityState"]["status"] == "synthetic_checks_satisfied" and not report["qualityState"]["certificationGranted"]
        before = sha(report_path)
        summary = run("summary", ["summary", "--report", report_path])
        assertions["summaryReadOnly"] = before == sha(report_path) and original_hash == sha(document_path)
        assertions["summaryCompact"] = len(summary.stdout.encode()) < 12000 and "checks" not in json.loads(summary.stdout)
        review = original["reviews"][0]
        explain = run("explain", ["explain", review["elementId"] + ":" + review["checkId"], "--report", report_path])
        explanation = json.loads(explain.stdout)
        assertions["explainExactCriterion"] = explanation["checkId"] == review["checkId"] and explanation["passCriterion"] and explanation["inspectionOnly"]
        fingerprint = run("scopedFingerprint", ["fingerprint", "--document", document_path, "--element-id", review["elementId"], "--check-id", review["checkId"], "--allow-synthetic"])
        assertions["scopedFingerprintMatchesCore"] = fingerprint.stdout.strip() == qc.check_subject_fingerprint(original, catalogue, review["elementId"], None, review["checkId"], work)
        run("unknownFingerprint", ["fingerprint", "--document", document_path, "--check-id", "invented", "--allow-synthetic"], 3)
        hashes_result = run("reviewHashes", ["review-hashes", "--document", document_path])
        hashes = json.loads(hashes_result.stdout)
        assertions["reviewHashesExactNoStamp"] = hashes["reviewHashes"] == sorted(qc.digest(item) for item in original["reviews"]) and hashes["reviewSetFingerprint"] == qc.review_set_fingerprint(original, catalogue, work) and sha(document_path) == original_hash
        run("hashesCannotOverwriteSource", ["review-hashes", "--document", document_path, "--output", document_path], 3)
        assertions["hashesSourcePreserved"] = sha(document_path) == original_hash
        run("trustTemplate", ["trust-template", "--document", document_path, "--output", work / "trust.json"])
        trust = qc.read_json(work / "trust.json")
        assertions["trustTemplateIsIncomplete"] = trust["reviewVerifications"] == [] and not trust["certificationGranted"] and not trust["authorityCreatedByThisHelper"] and sha(document_path) == original_hash
        bind_args = ["bind-evidence", "--document", document_path, "--evidence-id", original["evidence"][0]["id"], "--element-id", review["elementId"], "--check-id", review["checkId"], "--output", work / "bound.json"]
        run("bindSyntheticDenied", bind_args, 3)
        bind = run("bindEvidence", [*bind_args, "--allow-synthetic"])
        bound = qc.read_json(work / "bound.json")
        result = json.loads(bind.stdout)
        selected = next(item for item in bound["evidence"][0]["bindings"] if item["elementId"] == review["elementId"] and item["checkId"] == review["checkId"])
        assertions["bindExactContentAndTarget"] = bound["evidence"][0]["contentHash"] == qc.evidence_hash(bound["evidence"][0], work) and selected["subjectFingerprint"] == qc.check_subject_fingerprint(bound, catalogue, review["elementId"], None, review["checkId"], work)
        assertions["bindCreatesNoVerdictsOrApproval"] = original_hash == sha(document_path) and bound["reviews"] == original["reviews"] and result["reviewsCreated"] == 0 and result["reviewsApproved"] == 0 and not result["certificationGranted"]
        bad_args = list(bind_args); bad_args[bad_args.index("--check-id") + 1] = "invented"; bad_args[bad_args.index("--output") + 1] = work / "bad-bind.json"
        run("bindUnknownTargetDenied", [*bad_args, "--allow-synthetic"], 3)
        assertions["invalidBindWritesNothing"] = not (work / "bad-bind.json").exists()
        pending = qc.scaffold(catalogue, "SYNTHETIC-HELPER-PENDING", "fixture-author", "synthetic_fixture")
        qc.write_json(work / "pending.json", pending)
        run("pendingLoop", ["loop", "--document", work / "pending.json", "--report", work / "pending-report.json", "--state-dir", work / "state", "--allow-synthetic"], 2)
        state_before = state_hashes(work / "state")
        run("nextReadOnly", ["next", "--state-dir", work / "state"])
        assertions["nextDoesNotAcknowledgeOrMutate"] = state_before == state_hashes(work / "state")
        # Actual CLI on a release-sized fixture; inspection outputs remain small.
        scale = synthetic_scale(original)
        qc.write_json(work / "scale.json", scale)
        run("scaleCheck", ["check", "--document", work / "scale.json", "--report", work / "scale-report.json", "--allow-synthetic"])
        scale_summary = run("scaleSummary", ["summary", "--report", work / "scale-report.json"])
        scale_hashes = run("scaleReviewHashes", ["review-hashes", "--document", work / "scale.json"])
        assertions["scaleSummaryStillCompact"] = len(scale_summary.stdout.encode()) < 12000
        metrics = {"elements": len(scale["elements"]), "generatedFixtureVerdicts": len(scale["reviews"]), "reportFileBytes": (work / "scale-report.json").stat().st_size, "summaryStdoutBytes": len(scale_summary.stdout.encode()), "reviewHashesStdoutBytes": len(scale_hashes.stdout.encode()), "syntheticOnly": True}
    receipt = {"schemaVersion": "1.0", "generatedAt": qc.NOW(), "scope": "Independent actual-CLI helper acceptance; mechanical hashes, routing, source preservation and output scale. This is not a product-quality or reviewer-authentication certification.", "commandPathNormalization": "Ephemeral arguments under the generated temporary test directory are replaced with <temporary-audit-directory>; exit codes, byte counts, output hashes and timings are observations of actual unnormalized CLI execution.", "verificationScriptSha256": sha(Path(__file__)), "pins": {name: sha(BASE / name) for name in ("quality_checker.py", "quality_tools.py", "quality_loop.py", "catalogue.json")}, "assertions": assertions, "allAssertionsPassed": all(assertions.values()), "metrics": metrics, "runs": runs}
    qc.write_json(OUT / "helper-review.json", receipt)
    print(json.dumps({"allAssertionsPassed": receipt["allAssertionsPassed"], "assertions": len(assertions), "metrics": metrics, "failedAssertions": [key for key, value in assertions.items() if not value]}, indent=2))
    return 0 if receipt["allAssertionsPassed"] else 1


if __name__ == "__main__":
    sys.exit(main())
