# Edition 4: latest review findings, corrections and retained improvements

This release is a generic product-management framework. It contains no fixed project, organization, platform, provider, actual owner or fabricated product evidence. The previous archives remain separate historical editions. Engine/loop edition 4 retains the stage catalogue from edition 3 because its hierarchy criteria have not changed.

The latest feedback included older edition-2 measurements: 30 tests, roughly 1,534 review records, 320 questions and a 91-page guide. Edition 3 already reduced default review load and supplied separate document/review receipts. Independent reproduction nevertheless confirmed the important remaining defects against edition 3, including whole-document invalidation, skipped batches, resolved-question regression, repeated history, review-scope bypass, approved-content overwrite and malformed inputs. The corrections below address those actual defects rather than dismissing the feedback because some numbers were historical.

## 1. Scale, scoped invalidation and review routing

**Retained improvement:** Seven unsampled aggregate gates per item for the selected discovery/planning/ready/delivery/learning stage. Detailed rules are deferred reference guidance unless an exhaustive assessment is explicitly selected. Advisory samples never replace mandatory criteria or count unsampled rules as passed.

**New correction:** `scoped-v1` fingerprints bind each exact review target to its item, ancestors, declared prerequisite/reference closure, relevant alignment children, sources, governance, cited proof and referenced reviewer authority. Whole-hierarchy reviews still bind all members. Document revision numbers, change reasons and question bookkeeping do not invalidate otherwise unchanged scopes. Shared source/risk/governance changes can legitimately reopen many reviews; the checker does not pretend that every change is local.

Missing and stale verdicts now enter a reviewer queue. Explicit supported repairs have a separate lane. Only unresolved facts/evidence/decisions become owner question packets. The executing agent must inspect retained sources before requesting information; the checker does not contact anyone or dispatch review agents automatically.

**Measured evidence:** A 302-item synthetic backlog contains four upper-level items, eight epics, 40 stories, 150 acceptance criteria and 100 tasks. It uses 2,114 semantic verdicts rather than an exhaustive review matrix. A local task edit reopens eight reviews, preserving 2,106 and the unrelated branch. A smaller two-branch test shows eight of 84 reopened; its loop requests eight reviewer tasks and zero owner questions. Unrelated queue metadata creates zero stale quality reviews. Cited proof, linked prerequisites and used authority changes still invalidate the relevant scopes.

**Boundary:** The seven reviews remain real review work in an actual project. Generated favorable verdicts in these fixtures establish mechanics only. A coherent active scope and actual reviewer capacity are still needed; the framework does not guarantee semantic convergence or invent review outcomes.

## 2. Persistent question delivery, regression and bounded history

**New corrections:** Creating a batch does not mark it shown or acknowledged. The same unanswered batch remains on rerun. Explicit acknowledgement records the actual actor and advances presentation while leaving the questions awaiting answers. Read-only inspection cannot acknowledge a batch.

A resolved factual question that fails again opens a linked new occurrence automatically. Missing/stale review work routes to reviewers rather than requiring an owner to affirm a gate. Partial answers can generate repeated linked clarification; answers, acknowledgement and dismissal never clear a check.

Active state retains compact bounded histories, iteration summaries, answer records, inactive packets and batch events. Older records move to confined content-addressed archives with links and cumulative counts. Archive integrity is verified before a state write; changed history, traversal or incorrect counts are refused without replacing current state bytes.

**Evidence:** The independent loop receipt covers unanswered batch persistence, occurrence-2 regression, owner/reviewer routing, acknowledged questions still awaiting answers and malformed nested state. Across 45 context revisions, active state stabilizes at 573,772 bytes after the retention limits are reached, instead of repeatedly copying full check text. A separate 140-round regression test retains all 140 answers across active state and archives. Tampering an older archive is refused. These bounds limit working-state copies, not required clarification rounds or actual active product work.

## 3. Reviewer scope, synthetic mode and approved-content trust

**New corrections:** A quality reviewer must be distinct from every author in its actual review scope, including ancestors/context, and have rights covering every scoped item. All 28 whole-hierarchy checks now refuse both a story's own author and a different reviewer registered for only one story. Ancestor authors cannot review child gates whose binding includes that ancestor.

Synthetic assessment requires explicit `--allow-synthetic` and reports `synthetic_checks_satisfied`. It does not share a real-mode success label. Relabelling inputs or creating another reviewer name cannot authenticate a reviewer or authorize actual work. Real profile and exhaustive results remain explicitly advisory, including when supplied registry/receipt files match.

The external consistency receipt now binds the exact review set and current scoped subjects. Queue-only metadata preserves a current receipt; source/evidence/verdict/authority changes retire it. This is consistency verification, not an external identity service.

Approved, frozen and protected elements cannot be overwritten, deleted or downgraded in place by `apply-revision`; propose an amendment and preserve the prior snapshot. Meaningless approval references such as `TBD` cannot support an approved state. Actual approval authenticity and authority are still supplied and require external verification.

**Evidence:** The actual-catalogue trust receipt contains hierarchy rights/author counterexamples, ancestor-author refusal, approved rewrite refusal, approval-placeholder refusal and distinct synthetic invocation. The scale receipt checks real-mode receipt consistency after queue metadata edits, source-baseline refusal after actual source changes and the continuing unauthenticated/advisory boundary. Every report retains `certificationGranted: false`.

## 4. Agent usability and helper safety

**New corrections:** Agents use `summary`, `next` and targeted `explain <checkId>` before inspecting relevant source/evidence locations. They no longer need to read the entire detailed report into a single prompt. Questions identify the element, affected field/check, precise gap and declared decision owner; an absent owner stays unresolved.

Scoped `fingerprint`, `bind-evidence`, `review-hashes` and `trust-template` remove the need to reimplement canonical hashing. Binding writes a separate result, verifies the actual proof bytes and target, and creates no verdict or approval. The trust template is incomplete by design. Read-only helpers do not mutate documents, questions or acknowledgement. Output paths cannot overwrite source documents.

**Measured evidence:** Independent helper verification executes 17 actual CLI commands with 30 passing assertions. On the 302-item fixture, `summary` returns 2,220 bytes for a 9,226,723-byte detailed report. The observed summary time is approximately 0.059 seconds and the actual check approximately 5.44 seconds in the qualification environment. These are observations, not universal performance targets. The full report remains available for traceable detailed inspection.

## 5. Input robustness, portability and specification alignment

**New corrections:** Malformed top-level lists, wrong container types, invalid targets and malformed loop state are refused through controlled errors. Assessment malformed-input/unsafe-operation refusal uses exit 3 rather than a Python traceback. Unresolved `TBD by product owner` and `Owner: TBD` fail presence; a meaningful confirmed absence beginning `None —` is not automatically rejected.

Rulebook reads and writes explicitly use UTF-8. Parent and completion-prerequisite cycles report their exact path. `dependencyIds` means completion prerequisites; `designDependencyIds` means nonblocking references. Both affect review context, but design-reference cycles are permitted. Actual readiness/completion is not inferred from either relationship declaration.

The operating contract now names the executable result states, actual scoped binding, queues, acknowledgement/regression behavior, preservation rules, helper boundaries and current qualification evidence. Word generation must preserve human field labels and their punctuation. Document coverage and every-page visual review are independent evidence; a successful generation command is not a visual-review receipt.

**Evidence:** Controlled malformed-input, placeholder, cycle-path and design-reference tests are in the trust receipt. Helper and UTF-8 behaviors have regression coverage. The current root qualification record retains 95 tests with zero failures and 17 runs with expected exits. Document evidence is separately referenced from edition qualification.

## 6. Eight earlier improvements retained

The engine changes preserve the prior catalogue's substantive product-management improvements:

| Earlier finding | Retained contract |
| --- | --- |
| Excessive review load | Seven stage-relevant mandatory gates per item, bounded advisory sampling and explicit exhaustive opt-in. Unsampled obligations are not certified. |
| Circular detail criteria | 587 components within 189 owning fields; zero independent component verdicts. The owning gate assesses applicable required content. |
| Missing AI assurance | Conditional evaluation-data quality/rights, actual quantitative targets, safety/refusal/fallback, privacy and applicable law, model/prompt/configuration versioning, monitoring/drift/rollback and learning. Active assurance obligations cannot be sampled or blanket-exempted. |
| Learning stops at launch | Measured outcome comparison, uncertainty/adverse-effect review and continue/adjust/stop decisions feeding strategy and roadmap. |
| Missing discovery/priority/size | Riskiest epic assumption, falsifiable test and decision consequence; epic/story priority rationale, alternatives and attributable range sizing with uncertainty. |
| Fake independent identity | Externally governed reviewer administration is required for authoritative decisions; editable offline profiles remain advisory and unauthenticated. |
| Software-only fields | Thirteen generic field mappings with legacy compatibility; conflicting aliases block, and migration preserves originals while retiring old favorable reviews. |
| No shared Ready/Done definitions | One proposed canonical versioned Ready checklist and one Done checklist, referenced by stories/tasks; actual adoption, owner and fulfillment remain unverified until supplied. |

The conditional AI module distinguishes authoring-tool AI from runtime AI and includes dated primary references for applicable jurisdictions. It never invents targets, experiments, accuracy, consent, legal conclusions, providers or operating owners. Applying teams must establish actual context and recheck source currency.

## 7. Evidence, limits and handoff

- `checker/qualification-runs.json` and `checker/test-execution.txt`: current implementation pins, 95 tests and 17 root runs.
- `checker/independent-engine-review.json`: compact v4 independent review summary and exact evidence references.
- `checker/verification/`: portable actual-catalogue scope, loop, trust and scale harnesses with 42 passing assertions; portable helper acceptance with 30 passing assertions and 17 observed CLI commands. Receipts pin the executed modules and describe their synthetic/advisory boundaries.
- `QUALIFICATION.json`, document coverage/page-review records and `BUNDLE-MANIFEST.json`: separate edition and document qualification and exact package bytes.

No test count, output hash, local receipt or successful command establishes actual product quality, genuine independent identity, business approval, readiness, delivery or measured outcomes. Those require actual project sources and external authority. Preserve the original archive and its qualification evidence; use a working copy for new observations.

Give an executing agent the complete bundle, `START-HERE.md`, actual product context and access to the canonical project workspace. Use the Word guide for human review and the current catalogue/operating contract for exact checks. The loop continues supported repair, independent re-review and necessary clarification until its selected gates are satisfied, or pauses with precise unmet facts/authority and a resume condition. It never converts lack of progress or elapsed time into approval.
