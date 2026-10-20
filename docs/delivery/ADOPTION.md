# APLYD delivery adoption: DataDataEverywhere

Work item: https://github.com/nakul175/datadataeverywhere/issues/1.
Date: 20 October 2026. State: implemented proposal; independent review and activation pending.

## Scope and authority

The repository owner asked to apply APLYD Delivery System 1.0 after the initial application deployment. This authorizes adoption work, not invented historic approvals, new product features, a production redeployment or a compliant-release certificate. Product baseline d819af9c539d063b98b96df89ea5c54ec054c193 and the deployed architecture are preserved.

Engineering classification is C2 because this introduces development dependencies and changes multi-module delivery controls. Proposed QA tier is Medium: an incorrect report/gate could permit a material regression (impact 3, plausible likelihood 2, score 6). CI has no deployment or secret access; independent review of controls remains required. These classifications are an implementation assessment, not a recorded specialist acceptance.

## Supplied package adoption

The supplied master archive passed its 381-file byte-integrity check before use. The native engineering installer was run first in dry-run mode, then applied. It added the immutable Engineering 2.1.0 core and staged conflicts for README, .gitignore and .env.example instead of overwriting them. Existing app instructions in sidecar/AGENTS.md remain intact. Root AGENTS.md is the one composition router.

Product 4.2, Testing 1.3 and Workflow 2.0 references remain byte-identical under versioned .aplyd paths. The master archive and original companion ZIPs are not republished; hashes and the unchanged extracted references are recorded in .aplyd/delivery-lock.json. The engineering core has its own native manifest. Bundle examples/audits are reference material only, not current project records, test evidence or approvals. Root application MIT licensing does not add a license grant to separately supplied standards or their third-party material.

The engineering connection helper was run on these actual native packages. Explicit selection points to the real project QA registers and current PM catalogue. It correctly reports missing product records, typed relationships and owners; no synthetic PM example was selected. Its proposal is not installed as approved integration.

## Repository controls

- One root router, contribution rules, PR template and verified repository-owner CODEOWNERS entries.
- Repository-specific draft profile and command definitions; one canonical adoption work item and one selected exception authority.
- Factual product baseline, architecture decision, proposed Ready/Done, gap register and recovery handover.
- Exact Biome 2.5.15 formatting and initial lint rules, existing type/build checks, both npm audits, a bounded pattern-based secret scanner and immutable reference checks.
- CI runs all 33 application tests with disposable Redis and rejects empty, failed or skipped test reports. Four separate delivery-control tests cover false-summary, all-skipped, failing and actual-passing reports.
- Pinned official GitHub Action revisions, read-only tokens, no pull_request_target, no production deployment, bounded execution, 14-day synthetic report retention and an always-run aggregate that only accepts success from every child.

Source formatting is mechanical. The only application configuration change fixes the output tracing root so the new root development lockfile does not relocate the standalone server artifact expected by Docker/systemd. Production files and processes were not changed by this adoption.

## Evidence and truthful status

Local checks passed: reference integrity (265 reference files plus the 34-file native engineering core), pattern scan with no findings, formatting, lint, types, production build, both npm audits, Python/shell syntax, 33/33 application tests and 4/4 delivery-control tests. An earlier run with Redis unset passed 27 and skipped six; it is preserved and does not qualify. The report gate rejects that incomplete run. The full rerun executed all 33 with no skips. The standalone server remains at .next/standalone/server.js.

Native engineering audit is BLOCKED because configuration approval, assigned roles, native PM/QA integration and server evidence are incomplete. Native QA structural lint accepts the empty planning register format; that means zero qualified product evidence, not release readiness. Native QA release validation fails for missing criteria pins, evidence and complete scope. Product qualification cannot run on an absent real plan/trusted reviewer store. CI retains these holds and deliberately fails the aggregate rather than weakening a gate.

## Activation boundary

GitHub readback before adoption found Actions enabled, main unprotected and no repository rulesets. This PR does not install branch protection, schedule agents or deploy anything. A red workflow alone does not prevent merge on an unprotected branch. Native staged combined workflow remains a reference proposal; the repository-specific delivery workflow is the actual proposed CI implementation.

Before full activation: assign accountable roles and an independent reviewer; approve the native plan/criterion links, QA mappings, proposed team checklist and command profile; qualify the actual native adapters; review and configure server-required checks and protected policy ownership; prove failed/skipped/missing checks cannot merge and a changed head invalidates qualification; then separately qualify release/deployment/live-version controls. See GAPS.md. Parallelism remains one worker and no distributed lease guarantees are claimed.

Private local native evidence is retained under .aplyd/evidence and excluded from Git. The PR CI publishes only selected synthetic JUnit and native structured reports for 14 days. Actual external review, UAT, production load, restore, provider evaluation and release observations require new evidence and are not claimed here.
