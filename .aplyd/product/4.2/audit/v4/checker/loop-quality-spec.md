# Product-management quality gates and improvement loop

Engine contract 4.0-generic · 10 October 2026 · retained catalogue 3.0-generic

This contract defines the actual offline checker and improvement loop. It applies to products, physical goods, services and internal work. The retained catalogue specifies hierarchy fields and criteria; this edition changes review binding, clarification delivery, preservation and inspection. A framework implementation test does not qualify an actual product plan.

## 1. Results and authority stay separate

Maintain distinct records for documentation quality, specification approval, execution readiness, acceptance, authorized publication, observed availability, user verification and measured outcome learning. A proposed target is not a measurement; an integrated artifact is not observed availability. A stage conclusion grants none of the other gates.

| Result | Exact meaning |
| --- | --- |
| `stage_checks_satisfied` | All selected profile gates and mandatory integrity checks are satisfied for the current real-mode scope and stage using supplied records. The conclusion remains advisory. |
| `advisory_checks_satisfied` | All selected exhaustive reference checks and integrity checks are satisfied for a real-mode assessment. The conclusion remains advisory. |
| `synthetic_checks_satisfied` | The explicitly permitted synthetic mechanics input satisfies its selected checks. No actual product is qualified. |
| `needs_input`, `needs_revision`, `blocked` | One or more mandatory checks remain unresolved. Inspect the work lanes and precise finding rather than infer approval. |

Synthetic `check`, `loop`, `fingerprint` and evidence-binding invocation requires `--allow-synthetic`. The flag permits a labelled mechanics test only; it does not turn synthetic evidence into real evidence. No new synthetic success uses the former aspirational quality label.

`certificationGranted` is always false. Supplied readiness and delivery claims remain `supplied_unverified`; the checker grants no execution permission, business decision, legal approval, safety certification, acceptance or release authority. A locally created registry and receipt cannot authenticate a person or independent agent. Real-mode conclusions remain advisory even when every structural consistency check succeeds.

## 2. Stage-aware review budget and retained criteria

There are eight levels: vision, strategy, roadmap, release goal, epic, user story, acceptance criterion and implementation/verification task. The five stages are `discovery`, `planning`, `ready`, `delivery` and `learning`. Each stage/type selects exactly seven mandatory aggregate reviews per item. One item at each level requires 56 semantic verdicts. A partial scope must identify its assessed levels and contextual ancestors; it cannot certify omitted work.

Automatic integrity checks always run: input shape, catalogue/model pins, unique IDs, exact declared scope, protected source pins, valid parents and relationships, applicable cycle checks, field/type/alias integrity, review targets/statuses, approval references and current proof binding. Selected `requiredFieldIds` and applicable conditional branches determine the content due at that stage. Future-stage fields may remain explicitly pending; they are deferred, not passed.

The unchanged catalogue has 189 owning fields, 587 content components, 280 stage-gate definitions and 1,307 detailed reference criteria. Components are assessed within their owning field and gate, without independent component verdicts. Explicit exhaustive assessment is available but is not the default workload.

At most two deterministic noncritical reference targets per hierarchy level are sampled across the assessed scope. Selection follows stable identities rather than editable wording. Unreviewed samples remain visibly unreviewed and produce no owner questions. A failed sample requires triage: a mandatory defect blocks; an out-of-gate advisory disposition requires current independent justification, `mandatoryDefect: false` and a meaningful `scopeJustification`. Sampling never substitutes for a mandatory review or exempts safety, source integrity, access, privacy or applicable AI assurance.

## 3. Stage purpose and canonical team checklists

| Stage | Mandatory review purpose | Boundary |
| --- | --- | --- |
| Discovery | Establish the important problem and test the riskiest assumption using a falsifiable, bounded experiment and decision consequence. | A hypothesis and planned experiment remain unproven. |
| Planning | Define a bounded, testable outcome, sourced priority, attributable sizing uncertainty, dependencies, measures and qualification route. | Unagreed facts remain open before dependent commitments; future results stay planned. |
| Ready | Establish specification, actual prerequisites, authority and the applicable canonical Ready checklist. | Documentation and checklist text do not create permission. |
| Delivery | Compare actual output and validation against criteria and the canonical Done checklist; separately retain publication and availability evidence. | Task counts and integration cannot establish acceptance or observed delivery. |
| Learning | Compare measured results with targets and baselines; inspect uncertainty, adverse effects and drift; record continue/adjust/stop and strategy/roadmap follow-through. | A missed target is not rewritten as success or proof of causation. |

A team adopts one versioned Ready checklist and one versioned Done checklist with actual owner, policy ID, version/hash, applicability, evidence and decision authority. Stories and tasks link to these records and add justified item-specific conditions. Supplied checklist templates are proposed standards, not adopted policies or fulfilled conditions.

## 4. Conditional AI and personal-information assurance

Map retained source facts into `productProfile.ai` and `productProfile.personalData`. Each declares `applicability: yes|no|unknown`, pinned `sourceIds` and a meaningful `rationale`. Intake is not automatically imported. Unknown applicability blocks dependent planning, ready, delivery and learning decisions. Discovery unknown requires a sourced `resolutionPlan` and appropriately bounded activity, rather than consequential unqualified runtime use.

Optional `source.requiredBranches` may assert only `ai: true` and/or `personalData: true`. The metadata is source-hashed. Contradictory exclusions block in profile and exhaustive modes; protected source metadata cannot be removed through revision. Missing metadata is not proof of exclusion, and arbitrary source prose still requires semantic review.

An active AI branch requires stage-appropriate evidence covering purpose/risk/authority; versioned evaluation data, quality, rights, representativeness and leakage controls; agreed measurable thresholds and reproducible results when due; safety/refusal/fallback/escalation; model/prompt/configuration/tool/retrieval versions; privacy and applicable jurisdictional duties; and monitoring, drift, response ownership, rollback and learning. These obligations stay in the unsampled assurance gate. Required active fields cannot be blanket N/A.

No owner, provider, threshold, result, consent or legal interpretation is invented. Authoring-tool AI and product-runtime AI remain separate. The conditional AI module retains dated primary legal sources, including India where actually applicable; applying teams must recheck currency and commencement. This checker neither runs model evaluations nor determines legal compliance.

## 5. Scoped review and evidence binding

Every active review uses `bindingVersion: scoped-v1` and the exact fingerprint for its `(elementId, fieldId, checkId)` target. Aggregate profile reviews use `fieldId: null`. A legacy whole-document fingerprint is audit metadata and cannot serve as current review proof. Use the supplied scoped-fingerprint and binding helpers rather than reimplement hashing.

The deterministic binding includes:

- Exact catalogue, document identity, mode, author, assessment stage, declared scope and shared product-profile decisions.
- The complete target item, its ancestors and the transitive closure of explicit completion prerequisites and design references.
- Direct children and their context for alignment checks: dimensions `traceability`, `consistency`, `nonredundancy` or `completeness`, and gate IDs ending `.01`.
- Relevant source snapshots/pins, including shared profile source references, and applicable approval records.
- Evidence actually referenced by the matching review, including retained content/local-asset bytes, description, origin, kind and synthetic designation.
- The reviewer authority profiles actually referenced by that review.

Whole-hierarchy reviews bind all retained members, including contextual ancestors. Source, scope, catalogue, shared risk or governance changes may legitimately reopen many reviews. The closure is deliberately conservative; it does not infer arbitrary undeclared semantic dependencies from prose. Declare genuine relationships and have alignment reviews inspect omissions.

Document-level revision numbers, change reasons, answer/question bookkeeping and `questionDecisionVersions` do not alter scoped quality bindings. Unused evidence or reviewer additions do not invalidate unrelated reviews. Changing a local item, cited source, proof or reviewer authority reopens its actual dependent scopes. Keep old reviews as history; do not copy an old favorable verdict onto a new fingerprint.

Evidence must have its actual content hash and exactly one current target binding. A URL alone is a reference, not retained observation. Local assets are confined to the input directory. Duplicate, stale, unknown or legacy global-only bindings fail. Updating hashes does not review the evidence or create approval.

The supplied real-mode verification receipt uses `bindingVersion: scoped-v1`, the exact review-set fingerprint and exact review hashes. Its identity covers current verdicts and their current semantic subjects. Queue/audit metadata changes preserve a still-current receipt; changed subjects, verdicts or cited proof retire it. The external source baseline must still match retained source pins. A matching editable file proves consistency, not registry provenance or independence.

## 6. Reviewer rights, preservation and relationship semantics

A reviewer must be distinct from the document author and every author in that review's actual scoped context. Its declared rights must cover every scoped element, or explicitly cover all elements. A one-story registration cannot review a whole hierarchy; an ancestor author cannot review a child gate that binds that ancestor. Real mode additionally requires matching separately supplied profiles. The offline advisory boundary still applies.

Reviews are unique, current, meaningful and proof-backed. Statuses are `passed`, permitted `not_applicable`, `missing`, `failed`, `stale` and `invalid`. A mandatory unresolved result blocks regardless of other green results. No averaging, rounding, timeout or iteration limit creates success. N/A requires an actually permitted, sourced exclusion and does not remove protected or active assurance obligations.

`apply-revision` preserves document identity, increments the revision exactly once, requires a meaningful reason and retains a prior snapshot. Original protected sources, protected fields and approved/frozen/protected elements cannot be overwritten, deleted or downgraded in place. Propose a separate amendment. An approval reference must be meaningful; `TBD` cannot support an approved state. These guards preserve supplied approvals; they do not authenticate them.

`parentId` establishes hierarchy. `dependencyIds` identifies completion prerequisites; `designDependencyIds` identifies nonblocking design/reference relationships. Both require valid different existing targets and both affect scoped review binding. Parent and completion-prerequisite cycles block and report the exact cycle path. Design-reference cycles are permitted and do not authorize completion. Actual prerequisite fulfillment and completion authority remain separate evidence and decisions.

## 7. Persistent work lanes and actual question delivery

The loop separates three lanes:

| Lane | Work requested |
| --- | --- |
| `reviewerQueue` | Missing or stale independent verdicts and proof-bound re-review. No user is asked to rubber-stamp the absent review. |
| `repairQueue` | Explicit supported author repairs and dismissed-but-unresolved findings. A queue disposition is not a pass. |
| Owner questions | Actual unavailable facts, evidence or decisions. The question names the element, affected fields/check, gap, criterion and declared decision owner. An absent owner stays unresolved. |

The executing agent inspects retained sources and repairs supported gaps before requesting information. It contacts users or reviewers only through an actually authorized channel. The checker creates requests; it neither dispatches agents nor sends external messages.

Creating `nextBatch` is not acknowledgement. The same outstanding batch and `currentBatchId` remain visible on rerun until answers, explicit acknowledgement, current resolution or supersession. After a batch has actually been shown, `acknowledge-batch` records the identifiable actor and advances presentation; acknowledged but unanswered questions remain in `awaitingAnswerIds`/`awaitingAnswers`. Read-only `next` does not acknowledge anything.

`record-answer` retains respondent and answer as information. It does not satisfy checks or grant authority. Incomplete answers use `needs_clarification` with a precise reason and linked follow-up. If a resolved factual question later fails, a new occurrence is created automatically with `regressionOf`; manual question-version edits are unnecessary. A solved fact awaiting independent review is `awaiting_review`, not silently resolved. A removed assessment target may be superseded without being passed.

`dismiss-question` retains the failed check and records a queue disposition for repair. Dismissal, acknowledgement, silence and elapsed time cannot clear a finding. Default question batches are small; clarification rounds have no fixed limit.

## 8. Bounded state and verified history

Active state retains at most eight compact context records per question, 32 iteration summaries, 128 answer records, 64 inactive question packets and 64 batch events. Answer references inside a packet are also bounded. Actual active unresolved work can scale with the declared product scope; this is not a cap on needed questions or clarification rounds.

Older information is preserved in content-addressed `loop-archive` records with a previous-record link and cumulative record count. Current state keeps the archive head. Historic contexts retain digests and locators instead of copying the entire check text repeatedly. Before state writes, the loop verifies the confined archive chain's filenames, content hashes, links and counts. Tampering or traversal is refused before replacing current state bytes. This is local integrity checking, not authenticated provenance.

Archive paths and referenced evidence must remain available on resume. Preserve the archive together with current state. A resource interruption pauses dependent work with an explicit resume condition; it does not constitute an answer or quality exit.

## 9. Executable improvement sequence

1. Declare actual scope/stage, preserve sources and approved originals, resolve applicability and inspect compact integrity findings.
2. Inspect `summary`, then `next` and targeted `explain`; read exact source/evidence locations for the relevant checks rather than load every reference row into one prompt.
3. Obtain reasoned independent review for selected gates. Triage sampled defects and all applicable hard obligations.
4. Repair supported content, assign required reviewer work and ask only unresolved necessary facts or decisions. Preserve the current unacknowledged batch.
5. Retain actual answers and acknowledgement separately. Ask linked clarification as often as required; never infer an answer or authority from elapsed time.
6. Apply a supported versioned amendment/revision with preserved originals. Compute exact target bindings, retain proof and obtain actual independent verdicts.
7. Recheck affected scopes. Count resolved mandatory findings, supported facts and authority separately from prose growth, timestamps and regenerated verdicts.
8. Remain in `needs_input`, `needs_review`, `needs_revision`, `blocked` or `blocked_no_progress` with precise outstanding work and resume conditions when necessary. Continue safe independent work without crossing unresolved dependencies.
9. Exit only when every selected mandatory gate and integrity check is satisfied with current bindings and no untriaged mandatory finding. Record stage, scope, revision, deferred reference denominator, sample coverage and advisory/synthetic assurance.
10. Obtain separate actual approval/readiness/acceptance/publication/availability decisions and evidence. At the learning window, compare outcomes with targets and feed justified changes into strategy, roadmap and subsequent planning.

## 10. Helpers, input failures and qualification evidence

`summary`, `next` and `explain <checkId>` provide bounded inspection. `fingerprint --check-id` computes an exact existing review target. `bind-evidence` computes proof bytes and scoped bindings into a separate output without granting a verdict. `review-hashes` computes existing review hashes; `trust-template` creates an expressly incomplete external-verification template. Helpers do not fabricate reviewers, owners, independent verdicts, evidence truth, approval or delivery; inspection exit 0 means the helper executed successfully, not that the product passed.

Malformed documents, unknown targets, conflicting aliases and invalid operations produce controlled refusal. Assessment exit 0 means only the stated checks are satisfied; exit 2 means mandatory work remains; malformed input/unsafe operations use exit 3. The retained source/check files and generated rulebooks use UTF-8. Canonical generic fields accept 13 legacy field aliases, but conflicts block. Explicit migration preserves originals and retires old favorable reviews; a rename never transfers a pass.

Qualification retains exact module/source pins, commands, expected exit codes, actual output hashes and evidence locations. The current implementation record is 95 tests with zero failures and 17 root qualification runs. Independent portable verification adds 42 scope/loop/trust/scale assertions and 30 helper assertions, all observed passing. Document source coverage and per-page visual review are separate evidence, not inferred from a compiler or generator exit.

Measured synthetic evidence: 302 items require 2,114 semantic verdicts; one leaf edit reopens eight and preserves 2,106. The helper audit measured a 2,220-byte summary for a 9,226,723-byte report. A 45-edit loop test stabilizes active state after the declared retention limits; a 140-round test retains every answer through active records and verified archives. These are mechanics and usability observations, not a semantic quality assessment or a performance guarantee.

See `qualification-runs.json`, `test-execution.txt`, `independent-engine-review.json`, `verification/README.md` and the pinned receipts. The complete bundle remains a generic operating template. Each actual project must provide its own sources, facts, authority, independent review, qualification evidence and observed outcomes.
