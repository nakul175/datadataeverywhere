#!/usr/bin/env python3
"""Verify the bundled Word guide against actual catalogue and source bytes.

Pure standard library, read only. The JSON receipt goes to stdout; no document,
source, receipt or other file is created or modified. Exit 0 means this content
check passed, 2 means content did not match, and 3 means an input was malformed.
This checks OOXML text and structure, not visual layout or semantic correctness.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
import zipfile


W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
STAGES = ("discovery", "planning", "ready", "delivery", "learning")
EXPECTED_COUNTS = {
    "fields": 189, "components": 587, "stageCriteria": 280,
    "baseCriteria": 56, "stageClauses": 5, "conditionalAssuranceClauses": 1,
}


class ReadOnlyArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(json.dumps({"status": "malformed_input", "readOnly": True,
                          "error": message}, ensure_ascii=False, indent=2))
        raise SystemExit(3)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def paragraph_text(paragraph):
    """Read visible Word run/hyperlink text, preserving tabs and line breaks."""
    pieces = []
    for node in paragraph.iter():
        if node.tag == W + "t":
            pieces.append(node.text or "")
        elif node.tag == W + "tab":
            pieces.append("\t")
        elif node.tag in (W + "br", W + "cr"):
            pieces.append("\n")
    return "".join(pieces)


def cell_text(cell):
    return "\n".join(paragraph_text(p) for p in cell.findall(W + "p"))


def actual_word(document_bytes):
    import io
    with zipfile.ZipFile(io.BytesIO(document_bytes)) as archive:
        members = [entry for entry in archive.infolist()
                   if entry.filename == "word/document.xml"]
        if len(members) != 1:
            raise ValueError("Word archive must contain one word/document.xml")
        if members[0].file_size > 30 * 1024 * 1024:
            raise ValueError("word/document.xml exceeds the verification size limit")
        xml_bytes = archive.read(members[0])
    root = ET.fromstring(xml_bytes)
    body = root.find(W + "body")
    if body is None:
        raise ValueError("Word OOXML has no supported document body")
    paragraphs = [paragraph_text(p) for p in body.findall(W + "p")]
    headings = []
    for p in body.findall(W + "p"):
        style = p.find(W + "pPr/" + W + "pStyle")
        if style is not None and style.get(W + "val") in ("Heading2", "Heading3"):
            headings.append(paragraph_text(p))
    rows = []
    for table in body.iter(W + "tbl"):
        for row in table.findall(W + "tr"):
            rows.append([cell_text(cell) for cell in row.findall(W + "tc")])
    return paragraphs, headings, rows, sha256(xml_bytes)


def expected_criteria(catalogue):
    bases, stages, suffixes, targets = {}, {}, set(), {}
    checks = catalogue["profileChecks"]
    if not isinstance(checks, list):
        raise ValueError("catalogue.profileChecks must be a list")
    for check in checks:
        if not isinstance(check, dict):
            raise ValueError("Every profile criterion must be an object")
        criterion = check["passCriterion"]
        stage = check["profile_stage"]
        check_id = check["id"]
        if stage not in STAGES or not isinstance(criterion, str):
            raise ValueError("Invalid profile stage or passCriterion")
        match = re.fullmatch(r"gate\.([a-z_]+)\.([a-z]+)\.(0[1-7])", check_id)
        if not match or match.group(1) != check["element"] or match.group(2) != stage:
            raise ValueError("Invalid criterion identity: " + str(check_id))
        base, separator, tail = criterion.partition(stage.title() + " stage:")
        if not separator or not base.strip():
            raise ValueError("Criterion cannot be decomposed: " + check_id)
        clause, assurance_marker, assurance = (separator + tail).partition(
            " Unsampled conditional assurance:")
        suffix = (assurance_marker.strip() + assurance) if assurance_marker else ""
        if suffix:
            if match.group(3) != "06":
                raise ValueError("Conditional assurance found outside criterion 06")
            suffixes.add(suffix)
        elif match.group(3) == "06":
            raise ValueError("Criterion 06 lacks its conditional assurance clause")
        key = (match.group(1), match.group(3))
        if key in bases and bases[key] != base.strip():
            raise ValueError("Base criterion differs between stages")
        if stage in stages and stages[stage] != clause.strip():
            raise ValueError("Stage clause differs between criteria")
        if check_id in targets:
            raise ValueError("Duplicate profile criterion: " + check_id)
        bases[key], stages[stage] = base.strip(), clause.strip()
        rebuilt = " ".join(part for part in (base.strip(), clause.strip(), suffix) if part)
        if rebuilt != criterion or check.get("pass_criteria", criterion) != criterion:
            raise ValueError("Catalogue criterion reconstruction differs: " + check_id)
        targets[check_id] = (key, stage, bool(suffix), criterion)
    return bases, stages, suffixes, targets


def verify(document_path, catalogue_path, source_path, ai_path):
    paths = {"document": document_path, "catalogue": catalogue_path,
             "source": source_path, "ai": ai_path}
    raw = {name: Path(path).read_bytes() for name, path in paths.items()}
    catalogue = json.loads(raw["catalogue"].decode("utf-8"))
    if not isinstance(catalogue, dict) or not isinstance(catalogue.get("fields"), list):
        raise ValueError("Catalogue must be an object with a fields list")
    fields = catalogue["fields"]
    field_ids, component_ids = [], []
    for field in fields:
        if not isinstance(field, dict) or not isinstance(field.get("details"), list):
            raise ValueError("Every catalogue field must have a details list")
        field_ids.append(field["id"])
        for detail in field["details"]:
            if not isinstance(detail, dict) or not isinstance(detail.get("label"), str):
                raise ValueError("Every component must have an ID and label")
            component_ids.append(detail["id"])
    if len(set(field_ids)) != len(field_ids) or len(set(component_ids)) != len(component_ids):
        raise ValueError("Catalogue field and component IDs must be unique")
    bases, stages, suffixes, targets = expected_criteria(catalogue)
    counts = {"fields": len(fields), "components": len(component_ids),
              "stageCriteria": len(targets), "baseCriteria": len(bases),
              "stageClauses": len(stages), "conditionalAssuranceClauses": len(suffixes)}
    failures = []
    if counts != EXPECTED_COUNTS:
        failures.append({"kind": "edition_counts", "expected": EXPECTED_COUNTS,
                         "actual": counts})
    source_pin = catalogue.get("source", {}).get("contentSha256")
    if source_pin != sha256(raw["source"]):
        failures.append({"kind": "catalogue_source_pin", "expected": source_pin,
                         "actual": sha256(raw["source"])})
    paragraphs, headings, rows, xml_hash = actual_word(raw["document"])
    field_passed = component_passed = 0
    for field in fields:
        matching = [row for row in rows if row and field["id"] in row[0].splitlines()]
        if len(matching) != 1 or len(matching[0]) != 2:
            failures.append({"kind": "field_row", "fieldId": field["id"],
                             "matchingRows": len(matching)})
            continue
        row = matching[0]
        expected_left = "\n".join((field["label"], field["id"],
                                  field["requiredness"]["policy"]))
        expected_right = "; ".join(d["label"] for d in field["details"]) + (
            "\nApplicability: " + field["requiredness"]["condition"])
        if row[0] != expected_left:
            failures.append({"kind": "field_identity", "fieldId": field["id"]})
        else:
            field_passed += 1
        if row[1] != expected_right:
            failures.append({"kind": "field_components_or_applicability",
                             "fieldId": field["id"]})
        for detail in field["details"]:
            if detail["label"] in row[1]:
                component_passed += 1
            else:
                failures.append({"kind": "component_label", "fieldId": field["id"],
                                 "componentId": detail["id"]})
    actual_bases = {}
    nonempty = [p for p in paragraphs if p]
    for index, paragraph in enumerate(nonempty):
        match = re.fullmatch(r"ID pattern gate\.([a-z_]+)\.STAGE\.(0[1-7])", paragraph)
        if not match:
            continue
        key = match.groups()
        previous = nonempty[index - 1] if index else ""
        if key in actual_bases or not previous.startswith("Level criterion "):
            failures.append({"kind": "base_mapping", "level": key[0], "gate": key[1]})
            continue
        actual_bases[key] = previous.removeprefix("Level criterion ")
    actual_stages = {}
    for stage in STAGES:
        matching = [p for p in paragraphs if p.startswith(stage.title() + " stage:")]
        if len(matching) == 1:
            actual_stages[stage] = matching[0]
        else:
            failures.append({"kind": "stage_clause", "stage": stage,
                             "matchingParagraphs": len(matching)})
    actual_suffixes = [p for p in paragraphs if p.startswith("Unsampled conditional assurance:")]
    actual_suffix = actual_suffixes[0] if len(actual_suffixes) == 1 else ""
    if set(actual_suffixes) != suffixes or len(actual_suffixes) != 1:
        failures.append({"kind": "conditional_assurance_clause"})
    for key, expected in bases.items():
        if actual_bases.get(key) != expected:
            failures.append({"kind": "base_criterion", "level": key[0], "gate": key[1]})
    if set(actual_bases) != set(bases):
        failures.append({"kind": "base_identity_set"})
    for stage, expected in stages.items():
        if actual_stages.get(stage) != expected:
            failures.append({"kind": "stage_clause_text", "stage": stage})
    reconstructed = []
    for check_id, (key, stage, needs_suffix, expected) in targets.items():
        parts = (actual_bases.get(key, ""), actual_stages.get(stage, ""),
                 actual_suffix if needs_suffix else "")
        if " ".join(part for part in parts if part) == expected:
            reconstructed.append(check_id)
        else:
            failures.append({"kind": "stage_criterion_reconstruction", "checkId": check_id})
    ai_headings = [re.sub(r"^#{2,3} ", "", line) for line in raw["ai"].decode("utf-8").splitlines()
                   if re.match(r"^#{2,3} ", line)]
    missing_headings = [heading for heading in ai_headings if heading not in headings]
    for heading in missing_headings:
        failures.append({"kind": "ai_heading_exact_punctuation", "heading": heading})
    return {
        "schemaVersion": "1.0", "bundleEdition": "4.0-generic",
        "catalogueVersion": catalogue.get("catalogueVersion"),
        "status": "passed" if not failures else "failed", "readOnly": True,
        "method": "Actual OOXML owning field rows, base/ID-pattern paragraph associations, shared stage and assurance paragraphs, and Heading2/3 paragraphs; no authoring text cache is trusted.",
        "scopeLimit": "Content integrity and exact catalogue representation only; does not grant semantic quality, visual-layout approval, product approval, readiness or delivery.",
        "pins": {name: {"fileName": Path(paths[name]).name, "sha256": sha256(data)}
                 for name, data in raw.items()},
        "wordDocumentXmlSha256": xml_hash,
        "catalogueSourcePinMatches": source_pin == sha256(raw["source"]),
        "expectedCounts": EXPECTED_COUNTS, "actualCatalogueCounts": counts,
        "verified": {"fieldIdsInTheirOwningRows": field_passed,
                     "componentLabelsInTheirOwningRows": component_passed,
                     "baseCriteriaInMappedParagraphs": sum(actual_bases.get(k) == v for k, v in bases.items()),
                     "sharedStageClauses": sum(actual_stages.get(k) == v for k, v in stages.items()),
                     "conditionalAssuranceClauses": int(set(actual_suffixes) == suffixes and len(actual_suffixes) == 1),
                     "exactStageCriteriaReconstructedFromWord": len(reconstructed),
                     "aiSourceHeadingsWithExactPunctuation": len(ai_headings) - len(missing_headings)},
        "aiSourceHeadingCount": len(ai_headings),
        "reconstructedCriterionIds": reconstructed, "failures": failures,
    }


def main(argv=None):
    root = Path(__file__).resolve().parent
    parser = ReadOnlyArgumentParser(description=__doc__)
    parser.add_argument("--document", type=Path, default=root / "Generic Product Management Operating Framework.docx")
    parser.add_argument("--catalogue", type=Path, default=root.parent / "checker/catalogue.json")
    parser.add_argument("--source", type=Path, default=root.parent / "checker/source-standard.md")
    parser.add_argument("--ai", type=Path, default=root.parent / "AI-ASSURANCE.md")
    args = parser.parse_args(argv)
    try:
        receipt = verify(args.document, args.catalogue, args.source, args.ai)
    except (OSError, ValueError, KeyError, TypeError, AttributeError, UnicodeError, ET.ParseError,
            zipfile.BadZipFile, RuntimeError) as exc:
        print(json.dumps({"status": "malformed_input", "readOnly": True,
                          "error": str(exc)}, ensure_ascii=False, indent=2))
        return 3
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0 if receipt["status"] == "passed" else 2


if __name__ == "__main__":
    sys.exit(main())
