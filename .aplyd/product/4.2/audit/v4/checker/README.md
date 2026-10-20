# Generic product-management quality checker — version 4

This offline package checks a product-management hierarchy with a small, stage-specific review contract. It supports digital products, services, physical products and internal work through the same eight levels: vision, strategy, roadmap, release goal, epic, user story, acceptance criterion and technical task. Python 3.9 or later is sufficient; the checker has no network calls, hosting, scheduler or paid dependencies.

**Default workload: seven mandatory aggregate reviews per assessed item, not a verdict for every reference rule.** One item at each of the eight levels needs 56 review verdicts. The engine adds automatic integrity checks and selects at most two advisory reference targets per hierarchy level across the entire assessed scope. Missing advisory reviews remain visibly unreviewed, do not block the stage, and create no owner questions. They never count as passed reference coverage.

Real-mode output is **advisory only**, even when a supplied trust store matches. Editable local files cannot prove a reviewer's identity, genuine independence or external authority. Documentation checks, owner approval, execution readiness, acceptance, publication and observed availability remain separate gates.

## Select the stage before reviewing

The input's `assessment` selects `mode: profile` and one of these stages:

| Stage | Evidence expected now | Evidence that stays deferred |
| --- | --- | --- |
| `discovery` | Supported problem, riskiest assumption, falsifiable experiment, bounded research and decision consequence. | A committed implementation or invented production result. |
| `planning` | Testable bounded outcome, priority rationale, attributable size uncertainty, dependencies, measures, safeguards and qualification plan. | Future executed tests, published artifact or outcome measurements. |
| `ready` | Agreed current specification, actual prerequisites and authorities, canonical team Ready checklist and relevant AI qualification plan. | A claim that work or release has happened. |
| `delivery` | Actual scoped implementation and verification evidence, canonical team Done checklist, separate authorized release and availability records where applicable. | Future outcome-learning results. |
| `learning` | Observed results against targets, uncertainty, adverse outcomes, operational/AI monitoring and a recorded strategy/roadmap decision. | A fabricated retrospective or causal conclusion unsupported by observations. |

There are five profiles, eight levels and seven gates per level: 280 gate definitions, of which only the seven for the selected stage/type run on each assessed item. Stages do not grant the next stage automatically. Changing stage changes the subject fingerprint and requires current reviews. A legacy document without `assessment` selects the planning profile with an explicit coverage warning. Unknown stages or profile modes block; they never fall back to a permissive mode.

The catalogue also retains 189 field definitions, 587 **content components** and detailed reference rules. Components have labels and stable IDs but no independent verdicts or circular “apply owning-field checks” criteria. They are merged into their owning field. The selected aggregate gate reviews the applicable contents of its required fields. Future-stage reference fields are not demanded merely because they exist in the library.

An explicitly requested `assessment.mode: exhaustive` runs all applicable detailed field, element and hierarchy reference checks. This remains an exceptional, costed review; it is not the default and does not replace safety or external approval.

## Establish context and mandatory branches

Read `../PRODUCT-CONTEXT.md`, the context intake, and `../AI-ASSURANCE.md` when applicable. Intake files are human/agent working templates; they are not automatically imported. Retain actual source snapshots, map their decisions into the checker input and catalogue fields, and pin the snapshots.

The executable input must declare:

```json
{
  "assessment": {"mode": "profile", "stage": "planning"},
  "productProfile": {
    "ai": {
      "applicability": "yes",
      "sourceIds": ["source-001"],
      "rationale": "The source requires product-runtime AI; authoring-tool AI is separate."
    },
    "personalData": {
      "applicability": "unknown",
      "sourceIds": [],
      "rationale": ""
    }
  }
}
```

Use actual source-backed `yes`, `no` or `unknown`; never copy the example's decisions. `unknown` blocks decision-dependent planning, ready, delivery and learning. Discovery may retain `unknown` only with a meaningful sourced `resolutionPlan` and rationale; the discovery gate must also verify that consequential runtime evaluation is not being undertaken. A `no` claim needs a pinned source reference and specific rationale. The reviewer must check it against every applicable protected source obligation, rather than infer exclusion from a product label.

A pinned source may additionally declare `requiredBranches: {"ai": true, "personalData": true}`. This metadata is hashed when supplied; false or unknown branch keys are invalid. A profile `no` cannot contradict a true source requirement. Missing metadata does not waive an obligation, and the checker does not infer legal truth from arbitrary prose.

An active AI branch adds its stage-specific fields to an **unsampled mandatory gate**. Its seven assurance groups cover evaluation data and quality bars, quantitative acceptance targets, safety/refusal/fallback tests, data provenance/consent and applicable law, model/prompt/configuration versioning, operating controls, and post-launch drift/learning. The current contract and exact record/version/hash must be reviewed; the engine does not execute model evaluations or invent thresholds. An active branch's required assurance fields cannot be blanket N/A.

Safety, security, privacy, authorization, regulated or protected requirements remain in the mandatory aggregate criteria. They are not optional advisory sampling subjects. Product-specific law and policy apply only through actual context, current authoritative sources and the genuine required approval route.

## Start and run a draft

Run from the checker directory:

```sh
python3 -B quality_checker.py scaffold --output draft.json --document-id product-plan-001 --author-id author-001 --stage planning
python3 -B quality_checker.py check --document draft.json --report report.json
python3 -B quality_checker.py loop --document draft.json --report report.json --state-dir review-state --batch-size 3
```

The scaffold contains all eight elements and pending reference fields so nothing is invented. Only selected-stage required fields block the profile. Populate actual sources, actors, decisions and evidence; set authoritative source snapshots `protected: true`. Add a new source/version instead of overwriting protected material. Keep proposed content separate from approved/frozen text.

`check` writes mandatory check results, coverage, advisory samples, deferred-reference counts and the assurance boundary. `loop` adds durable deduplicated repair/question packets. A pristine eight-level pending fixture produces 59 packets against the current catalogue, not 320. These are requirements/repair/review packets, not an instruction to ask a human 59 questions: the calling agent repairs supported draft omissions and obtains independent reviews, and asks a decision owner only for missing facts, priorities, permissions or decisions.

Synthetic assessment requires explicit `--allow-synthetic`; omission returns exit `3`. Exit `0` means the declared selected checks are satisfied, with synthetic status kept distinct; inspect the report's stage, mode and assurance. Exit `2` means unresolved input, revision, stale review or quality finding. Exit `3` means malformed input or command/schema error. None grants approval or claims delivery.

Profile success is `stage_checks_satisfied`, expressly limited to the selected stage and scope. Real exhaustive success is `advisory_checks_satisfied`; all synthetic fixtures use `synthetic_checks_satisfied` and require explicit `--allow-synthetic`. Every report has `certificationGranted: false`. Real-mode loop success is `advisory_complete`; synthetic loop success is `synthetic_complete`. Neither authenticates approval.

## Review, sampling and the improvement loop

1. Preserve authoritative/frozen records and declare scope, stage, catalogue and source versions.
2. Run automatic identity, graph, scope, source, field/type, review-target and evidence-binding integrity checks.
3. Obtain the selected stage's seven distinct, reasoned aggregate reviews per item. Give the reviewer exact sources, revision, criteria and retained observations, not the author's desired verdict. The gates contain all applicable hard branches.
4. Use at most two deterministic advisory reference targets per hierarchy level. The seed uses stable document ID, stage, catalogue, element and check IDs; changing wording cannot cherry-pick a new sample. Record unreviewed targets honestly. Do not turn a small sample into an exhaustive-pass claim.
5. A failed sampled criterion requires documented triage. A mandatory/safety/source-integrity defect blocks and reopens the responsible gate. Only an independently justified `mandatoryDefect: false` with `scopeJustification` can retain a finding as an out-of-gate advisory improvement. Silently ignoring a failed sample cannot pass.
6. Repair supported gaps safely. Ask bounded owner questions for unavailable facts or actual authority decisions; do not ask users to supply reviewer verdicts. Answers are information, not automatic quality or approval.
7. Retain answers and source provenance; apply a supported proposed revision. A partial or contradictory answer produces a linked follow-up without a fixed clarification-round limit. The current unresolved batch is retained and displayed again until answered or explicitly acknowledged. Acknowledged unanswered questions remain awaiting an answer. Resolved groups reopen automatically if their checks regress.
8. Rebind evidence and independently review the selected gates after a content/source/authority/evidence/catalogue/stage change. Only targets whose substantive dependency scope changed become stale; historical snapshots remain. Revision counters and question queue bookkeeping do not invalidate substantive reviews.
9. Exit only when all selected mandatory gates and integrity checks pass. Report deferred references and advisory findings, plus separate approval/readiness/delivery/learning facts. No average, timeout or iteration cap creates success.

A finite invocation pauses as `needs_input`, `needs_revision`, `blocked` or `blocked_no_progress` when required information is unavailable. It resumes from persisted state; a resource pause is not quality success.

```sh
python3 -B quality_checker.py record-answer --state-dir review-state --question-id Q-EXAMPLE --answer-file answer.txt --answered-by owner-001
python3 -B quality_checker.py record-answer --state-dir review-state --question-id Q-EXAMPLE --answer-file answer.txt --answered-by owner-001 --assessment needs_clarification --follow-up-reason 'The specific release boundary is still unresolved.'
python3 -B quality_checker.py apply-revision --document draft.json --candidate candidate.json --state-dir review-state
```

A candidate retains `documentId`, increments `revision` exactly once and supplies meaningful `changeReason`. The revision helper refuses protected source/field deletion or change, and approved/frozen/protected element overwrite. It saves the prior snapshot. A manual edit outside the helper cannot be prevented; real use therefore needs an externally held source baseline and actual review, not local re-pinning alone.

## Input, evidence and reviewer contract

The JSON model retains schema version `1.0`; catalogue version is separately `3.0-generic`.

- Identity: `documentId`, positive `revision`, actual `authorId`, `mode` (`real` or `synthetic_fixture`), exact `catalogueHash`, `assessment` and explicit `productProfile` branches.
- Scope: `full_hierarchy` or justified `partial`, exact assessed `includedElementTypes`, and optional contextual ancestors. Contextual ancestors are retained but not claimed as assessed.
- Elements: stable ID/type/parent, author/source/dependency links, separate originality/approval state and fields keyed by canonical IDs. Unknown/wrong-level fields, alias conflicts and invalid types block. Required stage values cannot be unresolved placeholders. Future-stage placeholders remain deferred.
- Sources: exact retained text/version/originality/approval/protected state and exact source pins. Optional `requiredBranches` is additionally bound. A hash provides self-consistency, not truth or authority.
- Evidence: retained content or a confined local asset, description/origin, content hash, subject binding and explicit fixture provenance and exact scoped-v1 target bindings. A URL alone is not observed proof; asset traversal and resolved symlink escapes are refused.
- Reviews: exactly one current verdict per selected aggregate gate (`fieldId: null`), unique ID, reviewer, declared independence, bindingVersion scoped-v1, exact target subjectFingerprint, evidence IDs and gate-specific rationale. Whole-hierarchy reviewers must be distinct from every assessed item author and cover the entire assessed scope. Optional reference reviews name their owning field/check. In explicit exhaustive mode conditional whole-field N/A additionally requires exact current N/A reviews for each covered reference check. In profile mode an allowed required conditional-field exclusion must supply source-backed `scopeJustification` and be evaluated in the gate review; always-required/protected or active AI/person-data branch fields cannot be exempted.
- Separate records: `approvalRecords`, `readinessState`, `deliveryState` and actual canonical Ready/Done checklist references. Readiness and delivery claims are wrapped as supplied/unverified. The checker does not run evaluations, fulfill checklists, authorize work, publish or observe users.

```sh
python3 -B quality_checker.py fingerprint --document draft.json
```

The global fingerprint identifies the full document for audit. Each review binds an exact scoped-v1 target fingerprint: its item, ancestors, declared prerequisites/design references, direct children for alignment criteria, cited sources, referenced evidence and relevant reviewer authority. Whole-hierarchy criteria bind the whole declared scope. Unrelated sibling and queue-only edits preserve current reviews. Verdicts, binding arrays and queue bookkeeping are excluded from target hashes to avoid cycles. Preserve replaced reviews and their evidence in retained history.

Real mode requires a separately supplied `--trust-store review-profiles.json` with the exact catalogue/source pins, registered authority objects and one current verification receipt containing exact sorted active review hashes, verification method, verifier ID and locatable verification record. The verification receipt uses bindingVersion scoped-v1 and subjectFingerprint from review_set_fingerprint, with exact sorted active review hashes. This review-set binding survives queue-only changes and rejects changed substantive subjects or verdicts. The engine validates shape, separation and matching bytes. **An author can fabricate all those local files. This remains advisory and cannot authenticate independence.** A real authoritative gate needs an externally administered registry and verification boundary outside the authoring agent. Reviewer authority never confers business, legal, safety or release approval.

## Compatibility and migration

`compatibility-map.json` maps former software-shaped field, reference-check and component IDs to generic names. Legacy fields are accepted through canonical aliases without silently changing their contents. Supplying legacy and canonical values that differ blocks until an actual authority resolves the conflict.

Use the explicit migration to adopt the new catalogue/profile:

```sh
python3 -B quality_checker.py migrate --document legacy.json --output current.json --state-dir migration-history --stage planning --change-reason 'Adopt generic fields and stage review while preserving original source content.'
```

Migration writes a separate document and exact prior snapshot, preserves source text/pins, increments revision, and retires all active old reviews/evidence bindings. Unprotected keys can be renamed; protected fields/frozen elements retain their old keys and use the alias view. No favorable old report survives repinning. Resolve new applicability decisions and obtain current selected-stage reviews before using a migrated report.

## Verify the implementation locally

```sh
python3 -B -m unittest discover -s tests -v
python3 -B examples/generate_fixtures.py
python3 -B quality_checker.py check --document examples/synthetic-pass.json --allow-synthetic --report examples/pass-report.json
python3 -B quality_checker.py check --document examples/synthetic-stale.json --allow-synthetic --report examples/stale-report.json
python3 -B quality_checker.py loop --document examples/synthetic-pending.json --allow-synthetic --report examples/pending-report.json --state-dir examples/pending-loop
python3 -B quality_checker.py check --document examples/synthetic-exhaustive-pass.json --allow-synthetic --report examples/exhaustive-report.json
```

All generated fixtures and their deliberately generated verdicts are SYNTHETIC mechanics tests. They do not establish semantic quality for a real product. Tests cover false-pass attempts, protected sources, source/evidence/catalogue/stage invalidation, N/A abuse, graph and target integrity, questions and unlimited follow-ups, reduced workload, deferred-stage evidence, sampling limits/escalation, AI applicability, alias conflicts, protected migration and advisory reviewer authentication.

`render_rulebooks.py` creates readable local reference inputs under `publication/`; it does not publish to any external system. Read `loop-quality-spec.md`, the Word specification, AI module and context templates for the full operating process. No command in this package updates a backlog, contacts recipients or launches a product.

## Compact inspection and exact binding helpers

Inspect the summary, the retained next batch and one exact criterion instead of dumping the full catalogue or report into an agent context:

```sh
python3 -B quality_checker.py summary --report report.json --state-dir review-state
python3 -B quality_checker.py next --state-dir review-state --queue all --limit 3
python3 -B quality_checker.py explain gate.user_story.planning.04 --report report.json --element-id story-001
```

Inspection does not acknowledge messages, mutate state or grant quality. `next` distinguishes owner, reviewer and repair lanes. Read the exact selected source and evidence after locating the finding. A current failed review retains its actual rationale; missing or stale verdicts go to reviewer work instead of owner questions. Questions name the affected fields, gap and decision owner if supplied; an unresolved owner stays explicit.

```sh
python3 -B quality_checker.py acknowledge-batch --state-dir review-state --batch-id BATCH-ID --acknowledged-by actor-001
python3 -B quality_checker.py dismiss-question --state-dir review-state --question-id QUESTION-ID --reason 'Supported draft repair delegated; retain the failed criterion.' --dismissed-by actor-001
```

Only acknowledge a batch after actual delivery or deliberate navigation. Acknowledgement is not an answer or a pass. Dismissal retains the failed criterion in repair work. A finite run does not silently skip unresolved work.

The live state retains at most eight compact context snapshots per question, 32 iterations, 64 closed questions and 128 answers. Earlier records move to confined content-addressed archive chains. Hashes, links and cumulative counts are verified before state mutation. Total retained audit history can grow with actual activity; repeated unchanged runs do not copy full criterion text into history.

```sh
python3 -B quality_checker.py fingerprint --document draft.json --element-id story-001 --check-id gate.user_story.planning.04
python3 -B quality_checker.py bind-evidence --document draft.json --evidence-id evidence-001 --element-id story-001 --check-id gate.user_story.planning.04 --output draft-bound.json
python3 -B quality_checker.py review-hashes --document draft-bound.json --output review-hashes.json
python3 -B quality_checker.py trust-template --document draft-bound.json --output review-profiles-draft.json
```

Populate the appointed reviewer ID and referenced evidence IDs in the review target skeleton before computing its scoped hash, because those actual dependencies are part of the subject. The binding helper updates only an existing retained evidence record in a separate candidate beside the source. It never invents proof, repins a catalogue, changes verdicts or appoints a reviewer. The trust template is incomplete and contains no review verification receipt. Old global-only bindings cannot establish a current scoped review. Explicit adoption/migration retains previous records and requires current target reviews.

`dependencyIds` are completion prerequisites with a valid acyclic order. `designDependencyIds` are reference relationships and may be cyclic; referenced content still affects scoped review validity. The graph reports exact parent or blocking cycle paths. These relation records do not prove prerequisite completion or grant readiness; actual readiness remains separately evidenced.
