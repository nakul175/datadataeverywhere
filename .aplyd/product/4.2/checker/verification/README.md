# Independent checker counterexamples and scale evidence

Optional verification only: do not load this directory or `../../audit/` by default.
The preserved v4 receipts now live in `../../audit/v4/checker/verification/`.
Use `../../audit/RELOCATION-MAP.json` to resolve their original paths.

These portable harnesses use only the current catalogue, checker, clarification loop and explicitly synthetic fixtures shipped in this bundle. They contain no actual product plans, users, decisions, approvals or delivered outcomes. Generated favorable verdicts set up mechanics tests; they are not semantic quality reviews.

Run from the `checker` directory using a working copy of the bundle:

```text
python verification/audit_scoped_bindings.py
python verification/audit_loop_v4.py
python verification/audit_trust_v4.py
python verification/benchmark_v4.py
python verification/audit_helpers_v4.py
```

The compact receipts preserved under `audit/v4/checker/verification/` record the original v4 qualification run. Running an unchanged harness on a working copy writes a fresh receipt beside the harness; this is a new observation and does not replace the preserved historical receipt. Move fresh records into `audit/runs/` if retaining them; do not load them into normal agent context. Preserve the original archive and its manifest as the original qualification record; compare newly observed results against that record. The harnesses read the framework and fixture files without changing them. Temporary loop state and CLI documents are confined to temporary directories and are removed after testing.

| Harness | Counterexamples and positive controls | Assertions |
| --- | --- | --- |
| `audit_scoped_bindings.py` | Two separate branches, local and parent edits, declared prerequisites and design references, removed dependency links, unused and cited proof, authority changes, duplicate evidence bindings, legacy binding refusal | 11 |
| `audit_loop_v4.py` | Unacknowledged batch persistence, explicit acknowledgement, resolved-question regression, reviewer routing, answers without passes, 45 context revisions, bounded state, verified archives, historic archive tampering, malformed nested loop state | 11 |
| `audit_trust_v4.py` | Complete hierarchy author separation and authority coverage, ancestor authors, approved content preservation, unresolved approval references, meaningful absence, exact cycle paths, design reference semantics, explicit synthetic invocation and controlled malformed-input results | 13 |
| `benchmark_v4.py` | 302-item/2,114-verdict scale, scoped leaf invalidation, preserved unrelated branches, real-mode advisory receipt consistency after queue metadata changes, changed original source refusal | 7 |
| `audit_helpers_v4.py` | 17 actual CLI commands: precise scoped/evidence hashes, compact summary, read-only next, exact criterion explanation, explicit synthetic permission, invalid-target refusals, source preservation, zero generated review verdicts, incomplete trust template, and 302-item helper output sizes | 30 |

All 72 assertions must pass. Each receipt pins the checker and catalogue actually used; the loop receipt also pins the clarification module. `helper-review.json` additionally pins the helper module and its portable harness. Its recorded CLI arguments replace the generated temporary directory with `<temporary-audit-directory>`; output hashes, timings, exit codes and byte counts come from the actual unnormalized execution. Timings and file sizes are measured observations in the qualification environment, not promised response-time targets for another machine or product.

The real-mode receipt test deliberately constructs labelled, offline test data. A matching receipt proves structural consistency only. The test requires the result to remain advisory, identities unauthenticated, and certification absent. No synthetic test is promoted to real product approval, readiness or delivery.
