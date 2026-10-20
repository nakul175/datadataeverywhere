# Verifying the Word guide

The Word guide retains its edition-4 field, criterion and operating reference text. Engine 4.2 adds catalogue-identity enforcement without changing those criteria. The current execution addendum is in `../START-HERE.md`, `../AGENTS.md` and `../checker/README.md`; use those instructions for the fixed identity and working sequence.

Optional verification only; normal agents use relevant guide sections on demand.
Preserved content, test and visual receipts are under `../audit/v4/documentation/`.
Do not load them by default. Resolve historical paths through `../audit/RELOCATION-MAP.json`.

From this directory, run `python3 verify_guide.py`. Python's standard library is sufficient. The command reads the actual Word OOXML, catalogue, source standard and AI module; it prints a JSON receipt and does not modify or create files. It works from any current directory. Optional `--document`, `--catalogue`, `--source` and `--ai` arguments select alternate input files for inspection.

The verifier checks all 189 field IDs in their own table rows, all 587 component labels and their exact owning-field/applicability cell, all 56 mapped base criteria, all five shared stage clauses and the conditional assurance suffix. It reconstructs all 280 stage criteria from the text actually present in Word and compares them with the catalogue. It also checks all 14 AI source headings as actual headings, with exact punctuation, and verifies the catalogue's source content pin. The receipt records SHA-256 hashes of the actual four input files and Word document XML.

Exit 0 means this content check passed, 2 means content differs, and 3 means an input was malformed. A pass establishes this exact content representation. It does not establish semantic correctness, visual readability, independent approval, readiness or delivery. Visual review has separate page-image receipts.

Run the negative tests with `python3 -m unittest discover -s tests -v`. Tests alter temporary copies of actual Word XML to prove that missing field rows, component labels, criterion fragments and heading punctuation are refused. They also test source pin changes, malformed Word input and read-only execution. They never change the bundled document or its sources.
