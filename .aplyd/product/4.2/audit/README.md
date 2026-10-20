# Audit records: load only on request

Normal execution starts at `../START-HERE.md`. Do not load this folder by default or use synthetic verification material as actual project evidence.

## Current packaging

For integrity checks use only `BUNDLE-MANIFEST.json`; historical manifests describe their original editions. The current manifest lists paths relative to the extracted bundle root and excludes itself. `QUALIFICATION.json` records the actual 4.2 regression, original-bypass reproduction and blocked-counterexample evidence. Engine 4.2 adds fixed criterion-identity enforcement; the catalogue, Word guide and loop implementation are unchanged.

The catalogue identity is visible outside this folder in `../STANDARD-IDENTITY.json` and the entry instructions. It is pinned independently in checker code. Do not weaken criteria to obtain a pass. A matching local file hash does not authorise a changed standard or authenticate a reviewer.

## Preserved v4 evidence

`v4/` preserves historical v4 records and superseded files byte-for-byte. `v4.1.1/` preserves the prior packaging records and changed files from the immediate predecessor. Their original timestamps, commands, relative paths and hashes are historical observations; they are not rewritten as 4.2 runs or authenticated product approvals. Historical manifests describe only their own original editions.

Use `RELOCATION-MAP.json` to resolve every original v4 file to its preserved location and expected hash. For a reference relative to a receipt's original directory, first join it to that original directory, then look up the resulting original bundle-root path. Some records explicitly use checker-root or bundle-root paths instead; the index documents those bases. Commands remain recorded in their original execution context.

The map includes unchanged live runtime files and separate historical copies of revised instruction files. A revised live START-HERE or README must never be compared with the original v4 hash; compare its historical copy instead. All original v4 payload bytes remain available through the map.

`PREVIOUS-EDITION-MAP.json` separately resolves every original v4.1.1 payload file. The current v4 relocation map also routes old engine/test pins to their preserved copies when live code has changed. Historical successful reports remain historical; assess a plan again with the current pinned checker before claiming a current result.

Original generated reports and pending-loop state are examples under `v4/checker/examples/`; normal work must create or refresh its own state with loop before reading next. Current optional test reproduction commands are in `../checker/README.md`, `../checker/verification/README.md` and `../documentation/README.md`. Unchanged harnesses write new receipts beside themselves on a working copy; preserve these separately under `runs/` when retained. They do not overwrite v4 history.

Verification establishes packaging and mechanics only. It does not authenticate owners, independent reviewers, actual product quality, approval, readiness, delivery or learning results.
