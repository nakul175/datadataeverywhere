"""Generate explicitly synthetic mechanics fixtures against the current catalogue."""
import importlib.util
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "tests"))
from test_checker import fixture

spec = importlib.util.spec_from_file_location("qc", BASE / "quality_checker.py")
qc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qc)
catalogue = qc.read_json(BASE / "catalogue.json")
if qc.catalogue_errors(catalogue):
    raise SystemExit("Catalogue is incomplete/invalid; do not generate fixtures yet.")
_, passing = fixture(catalogue, assessment_mode="profile")
qc.write_json(BASE / "examples" / "synthetic-pass.json", passing)
pending = qc.scaffold(catalogue, "SYNTHETIC-PENDING-FIXTURE", "fixture-author", "synthetic_fixture")
qc.write_json(BASE / "examples" / "synthetic-pending.json", pending)
failing = qc.read_json(BASE / "examples" / "synthetic-pass.json")
changed_task = next(element for element in failing["elements"] if element["elementType"] == "technical_task")
changed_field = next(field_id for field_id in changed_task["fields"] if field_id.startswith("technical_task."))
changed_task["fields"][changed_field]["value"] += " Material local task scope changed. Only this task and its direct parent alignment review must reopen; unrelated reviews remain eligible."
qc.write_json(BASE / "examples" / "synthetic-stale.json", failing)
_, exhaustive = fixture(catalogue, assessment_mode="exhaustive")
qc.write_json(BASE / "examples" / "synthetic-exhaustive-pass.json", exhaustive)
for stage in qc.REVIEW_STAGES:
    _, stage_fixture = fixture(catalogue, assessment_mode="profile", stage=stage)
    qc.write_json(BASE / "examples" / ("synthetic-" + stage + "-pass.json"), stage_fixture)
print("Generated explicitly SYNTHETIC stage, pending, stale and exhaustive mechanics fixtures. Stage fixtures have 56 mandatory generated test verdicts, not real semantic assessment. No actual product record was certified.")
