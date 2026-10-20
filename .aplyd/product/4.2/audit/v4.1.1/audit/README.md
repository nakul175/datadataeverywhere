# Audit records: load only on request

Normal execution starts at `../START-HERE.md`. Do not load this folder by default or use synthetic verification material as actual project evidence.

## Current packaging

`BUNDLE-MANIFEST.json` is the current 4.1 file-integrity manifest. It lists paths relative to the extracted bundle root and excludes itself. `PACKAGING-QUALIFICATION.json` records the actual packaging checks and test execution for this instruction-and-layout update. The checker, catalogue, Word guide, fixtures and executable test sources are unchanged.

## Preserved v4 evidence

`v4/` preserves historical v4 records and superseded instruction files byte-for-byte. Their original timestamps, commands, relative paths and hashes are historical observations; they are not rewritten as new 4.1 runs or authenticated product approvals. The old manifest in `v4/BUNDLE-MANIFEST.json` describes the original v4 payload, not the current 4.1 file list.

Use `RELOCATION-MAP.json` to resolve every original v4 file to its preserved location and expected hash. For a reference relative to a receipt's original directory, first join it to that original directory, then look up the resulting original bundle-root path. Some records explicitly use checker-root or bundle-root paths instead; the index documents those bases. Commands remain recorded in their original execution context.

The map includes unchanged live runtime files and separate historical copies of revised instruction files. A revised live START-HERE or README must never be compared with the original v4 hash; compare its historical copy instead. All original v4 payload bytes remain available through the map.

Original generated reports and pending-loop state are examples under `v4/checker/examples/`; normal work must create or refresh its own state with loop before reading next. Current optional test reproduction commands are in `../checker/README.md`, `../checker/verification/README.md` and `../documentation/README.md`. Unchanged harnesses write new receipts beside themselves on a working copy; preserve these separately under `runs/` when retained. They do not overwrite v4 history.

Verification establishes packaging and mechanics only. It does not authenticate owners, independent reviewers, actual product quality, approval, readiness, delivery or learning results.
