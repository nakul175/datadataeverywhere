# Optional AI assurance module

Edition 3.0 generic. Source review date: 10 October 2026. Module ID: `generic.ai_assurance.v3`.

This module applies to a product capability that uses AI to produce, rank, classify, predict, recommend, generate or act. It works for predictive models, generative models and systems assembled from models, retrieval, policies and tools. It does not select a provider, acquire data, transmit information, call an AI service or authorise a consequential action. The actual product determines its risks, metrics, required authority and applicable law.

The requirements below are this bundle's planning and assurance policy. They are not a claim that a regulator or standard requires this entire checklist. The cited source notes support the limited background and legal facts identified in section 7.

## 1. Choose the applicability branch

Record `document.productProfile.ai` as `{ "applicability": "yes|no|unknown", "sourceIds": [], "rationale": "...", "resolutionPlan": null }`. Record personal-data applicability separately under `document.productProfile.personalData` using the same properties. A source ID must resolve to the actual authoritative source and version. Discovery-only unknown applicability also requires a meaningful `resolutionPlan`, supporting source IDs and rationale establishing the actual scope; a blank plan does not permit advancement. AI used only to draft or review documentation is a separate authoring-tool declaration; it does not prove that the delivered product uses AI. Its handling of project information still needs the actual access, confidentiality and data permissions.

- **Yes:** identify the exact capability, release, users, effects and operating boundary. Apply the seven assurance groups to that scope at the relevant stage.
- **No:** provide authoritative evidence covering the declared scope and its relevant dependencies. A statement that an item has no AI is insufficient if its parent service uses an AI decision or output that affects it. A reviewed exclusion applies to that scope only and must be revisited when the dependency or scope changes.
- **Unknown:** retain the unknown and the question needed to resolve it. Discovery can continue with a resolution plan and bounded work that does not need the missing decision. An AI-dependent planning, readiness, delivery or learning gate remains `needs_input`; unknown never becomes an automatic exclusion or pass.

Do not assess the entire company because one capability is being changed. Reuse a pinned, current assurance record for shared unchanged components, then review the change and any affected assumptions. A record is scoped to a capability, version and environment; evidence from one cannot silently certify another.

## 2. Seven evidence groups, not hundreds of verdicts

Record one consolidated assessment per applicable group for the current stage, supported by the relevant evidence listed below. The group assessment states which subrequirements are satisfied, excluded with evidence, pending, failed or stale. A single failing must-pass subrequirement fails the group; an average cannot hide it. Record these assessments together in the scoped assurance record, and let the hierarchy's existing AI/risk stage gate review that evidence. Do not request seven additional checker verdicts for every child item or create a second tree of blocking review items. Reuse the current shared record and review each child's material impact.

The assessor can inspect representative lower-risk supporting material under the declared sampling plan. Dataset-quality bars, protected rights, source permissions, prohibited effects, safety/fallback tests, release thresholds, identity/authority controls and required monitoring responses are must-pass for their relevant stage and cannot be sampled away. Automated dataset and result checks can cover thousands of rows without requiring thousands of human verdicts.

| Group | Must-pass decision | Primary evidence |
| --- | --- | --- |
| AI-01 | Intended use, authority and risk boundary are defensible | Capability inventory, affected groups, risk register, decision/action permissions, oversight contract |
| AI-02 | Evaluation data is suitable and usable for the declared purpose | Versioned dataset manifest, provenance/rights record, slice matrix, label rubric/audit, leakage report |
| AI-03 | Evaluation proves the declared acceptance contract | Frozen metric definitions and thresholds, run manifest, raw results, per-slice analysis and regression comparison |
| AI-04 | Unsafe, wrong, uncertain and unavailable behavior is controlled | Threat/failure scenarios, red-team and fallback results, refusal behavior, override and recovery evidence |
| AI-05 | The evaluated configuration is the released configuration | Model/prompt/retrieval/tool/runtime/config pins, change record, reproducible runs, promotion and rollback evidence |
| AI-06 | Data use and legal applicability have been resolved | Data-flow map, permission/legal-basis record, retention/deletion controls, jurisdiction/current-duty analysis |
| AI-07 | Operation is monitored and learning changes decisions | Baseline and drift contract, telemetry/sample plan, alert tests, response authority, post-release review and roadmap links |

An offline checker verifies document consistency and supplied evidence claims. It does not verify reviewer identity, authenticate external approvals or certify the actual AI system. Local identities created by the authoring agent do not establish independence. Promotion and approval require the external authority mechanism declared by the team.

## 3. Group criteria and evidence

### AI-01 — Intended use, authority and risk

The record identifies what the capability does, who relies on it, what it may change, where it operates and where it must not be used. It separates draft information, recommendations, decisions and actions. It names relevant affected users, operators and groups without collecting unnecessary personal information. It compares the proposed AI behavior to the existing or non-AI baseline and explains why AI is appropriate for the tested problem.

The risk register covers plausible incorrect, incomplete, misleading, biased, unsafe, privacy-invasive and unavailable outcomes, plus misuse and dependency failure. Each material risk has a plausible trigger, affected party, consequence, severity/likelihood rationale, mitigation, residual-risk decision and evidence requirement. Risk classification is justified by the capability's effects; the agent cannot invent a safe classification or an acceptance authority.

If tools or external effects exist, identify their allowed inputs, scope, permissions, confirmations, reversibility and stop conditions. Test that model text cannot enlarge authority, that untrusted content cannot issue instructions, and that missing permission prevents the effect. Define human review or override at the actual decision point, including operator competence, accessible explanation, response time, escalation and what happens when the operator is unavailable. A human approval button alone is not evidence of effective oversight.

**Pass for planning:** the scope, risks and authority are explicit with actual sources; unresolved risks have a bounded discovery test and cannot be bypassed by declaring the document complete. **Pass for delivery:** observed control tests and the actual required risk decision cover the release. No unapproved provider, data transfer or consequential tool action is implied by this module.

### AI-02 — Evaluation dataset quality and rights

Maintain an immutable or versioned dataset manifest: dataset ID/version/hash, date and source range, intended task, population, item count, selection method, known exclusions, permitted uses, provenance, rights/consent or other established permission, and retention/access restrictions. Link record-level provenance where necessary without putting raw personal data into planning documents. Distinguish original, transformed, anonymised, pseudonymised and synthetic records; synthetic data cannot by itself prove performance on a real target population.

Before evaluating, define the dataset quality bar. It states required coverage and minimum useful counts for relevant slices, label validity and completeness thresholds, allowed duplication/error rates, acceptable representativeness gaps, and statistical adequacy for the decision. Set these values from the actual use and risk; a missing value is `target_pending`, not a default pass. Relevant slices can include languages/dialects, user groups, environments, devices, input lengths/quality, rare but costly errors and adversarial conditions. Do not collect protected or sensitive characteristics merely because the template mentions slices; use justified, authorised and minimised measures.

Separate training, tuning, prompt development and retrieval construction from frozen acceptance evaluation. Document split method, entity/time boundaries, exact and near-duplicate checks, contamination limitations and restricted test access. If a hosted model's training data is unknown, record that limitation and the mitigations; do not claim that leakage has been disproved. When test data is used to repair a model or prompt, move it to development, create a fresh protected evaluation set and retain the old benchmark for regression.

Version the annotation rubric with positive, negative, ambiguous and borderline examples, definitions of error severity and adjudication rules. Record annotator qualifications, independence where relevant, disagreement rates, adjudicated cases and an independently selected label audit with its sample method, observed errors and quality-bar decision. An AI judge needs its own validated rubric, version, human calibration and failure analysis; one model grading itself is not independent evidence.

**Pass for ready:** the dataset and its use permissions meet the frozen quality bar or explicitly bounded discovery-only limits. **Pass for delivery:** the evaluated dataset version, audit and leakage findings are recorded; important coverage or rights gaps are unresolved failures, even if the aggregate score is high.

### AI-03 — Acceptance metrics and observed results

For each user outcome, define the metric, eligible unit, denominator, numerator, exclusions, scoring rubric, threshold operator/value, measurement window, required slices and uncertainty method. Prefer task success and costly-error rates over a generic accuracy score when those better represent the risk. Classification may require precision/recall and separate false-positive/false-negative limits; generation may require supported correctness, grounded citations, completeness and usefulness; action systems may require successful authorised action and unauthorised-effect rates. Measure refusal false positives and failures to refuse, and calibration/abstention when decisions depend on uncertainty. Do not treat a model's self-reported confidence as calibrated probability without validation.

Use a frozen acceptance statement such as: “On dataset `[ID/version/hash]`, configuration `[release-manifest]` achieves `[metric] >= [X]% on `[eligible N]` examples, with `[per-slice thresholds]`, `[uncertainty rule]` and `[safety/error limits]`.” Every bracket is an actual project value or an explicit unresolved question. There is no universal acceptable X%. Targets must be agreed before results are used to decide acceptance; a changed target requires a versioned decision and review.

Attach a reproducible run manifest, input/result references, evaluated artifact pins, raw or appropriately protected row-level outcomes, aggregate and per-slice numerators/denominators, confidence intervals or justified uncertainty treatment, error analysis, latency/resource/cost measurements when material, and comparison with baseline and previous approved version. Record repeated-run count, seeds or stochastic settings when relevant. Do not average away a mandatory failed slice. An empty denominator is not 100%; an insufficient sample is inconclusive. Results from a provider's benchmark are contextual evidence, not proof of the product's own outcome.

**Pass for ready:** metrics, thresholds, dataset and evaluation procedure are frozen and reviewable. **Pass for delivery:** current observed results meet every must-pass target for the declared scope and configuration; `target_pending`, missing runs, unresolved failures or a stale artifact remain blocked. Quality pass and actual release approval remain separate.

### AI-04 — Safety, refusal, fallback and recovery

Define product-specific prohibited and bounded outcomes from actual policy, rights, contracts and risk decisions. Build a finite, versioned scenario set covering ordinary success, harmful or disallowed requests, ambiguous intent, insufficient context, incorrect/unsupported output, uncertainty, unavailable/slow dependency, malformed output, stale retrieval and inaccessible sources. For relevant generative or tool systems, also cover prompt injection in user/retrieved/tool content, privilege escalation, sensitive-data disclosure, fabricated citations, poisoned content and tool parameters, repeated or multi-step misuse, and cross-user information leakage.

Each scenario specifies the expected allowed result, refusal/degradation, safe alternative, human escalation or halt; observable evidence and severity; and the threshold or invariant used to judge it. Include false refusals on valid work so safety controls do not silently make the capability unusable. Red-team cases are selected by risk and exposure, not merely by convenience. Record coverage limitations and residual risks; passing a finite suite does not prove that failure is impossible.

Test fallback end to end. It must preserve the existing authorisation boundary, describe what the user can do next and avoid making uncertain output appear verified. A fallback may be a safe non-AI path, a qualified human queue, retry with limits or a halt. Its feasibility, operator capacity, accessibility and time limits must be evidenced. Test degraded operation, cancellation, duplicate effects, partial completion, recovery and rollback where relevant. Logs contain sufficient evidence for diagnosis without retaining unnecessary sensitive inputs.

**Pass for delivery:** every applicable must-pass risk scenario and fallback/control assertion passes on the actual release configuration, required independent assessment and risk decisions exist, and unresolved prohibited behavior stops advancement. A successful nominal accuracy test cannot substitute for this evidence.

### AI-05 — Versioning, regression and promotion

Pin the model identity and revision or immutable snapshot where available; prompt/system instruction/template hash; preprocessing and postprocessing; policy/guardrail configuration; retrieval corpus/version, index, embedding and ranking configuration; tool schemas, permissions and code; runtime, dependencies and material settings; dataset, rubric, judge and evaluation procedure; and the released artifact/configuration manifest. Do not put credentials in the manifest. Where a vendor exposes only a mutable model alias, record that limitation, observable version signals, the change-detection plan and a narrower claim of reproducibility.

For each material change, identify the affected capabilities, risks, slices and baseline. Run the required regression suite against a frozen baseline and acceptance contract, inspect failures and retain exact run provenance. The actual promotion authority decides against predeclared thresholds; missing or failing required evidence prevents promotion. A prompt-only change can alter behavior and must not bypass this gate. Component changes that affect authorisation, privacy, safety or the evaluated population require the corresponding evidence to be refreshed.

Define rollback or halt to an actually available, previously qualified version or safe operational path. Test that the rollback restores the relevant configuration and data compatibility without new unauthorised effects. Record who can execute it, triggering conditions and confirmation evidence. Evaluation results must identify the same candidate manifest as the release; observed operating identity must identify the same approved manifest. An approved candidate and an observed operating version are distinct facts.

**Pass for delivery:** traceability connects the accepted tests, candidate, approval and observed release; each required regression and rollback test is current. Configuration or evidence changes invalidate affected prior reviews. If a dependency cannot be pinned, its uncertainty and operational controls are explicitly accepted within real authority rather than hidden behind a hash.

### AI-06 — Data permissions, privacy and law

Create a data-flow inventory for collection, evaluation, training/fine tuning, retrieval, inference, tool effects, output, telemetry and human review. Identify data categories, people or entities concerned, source, purpose, actual permission/legal basis, recipients/processors, locations, access, security, retention, withdrawal/deletion handling and approved reuse. Permission to deliver a service is not automatically permission to train a model. A licence is not automatically data-protection permission, and removing direct names is not proof of irreversible anonymity.

Record applicable jurisdictions, the relevant entity's role, scope facts, current official sources/versions, effective dates, exemptions that actually apply and the accountable qualified decision. Establish notices, consent or another applicable basis from that decision rather than assuming consent is always the only basis. If children or individuals with a lawful guardian are in scope, obtain the required qualified applicability decision before collecting or evaluating their information. Avoid unnecessary collection, maintain purpose limits, test access/erasure/withdrawal flows that the product actually requires, and record legally required retention exceptions. Resolve provider reuse/training, subprocessors, cross-border processing, deletion propagation, logging and breach/rights response obligations from actual contracts and current law.

**India branch:** complete an applicability and commencement review using the primary references in section 7. Distinguish obligations already in force, scheduled obligations and product policy adopted before commencement. Do not label all DPDP processing obligations effective on 10 October 2026, and do not label the product compliant because a checklist exists. Record other presently applicable privacy/security/sectoral duties and contractual obligations; a future DPDP commencement date does not itself authorise an otherwise impermissible use.

**Pass for ready:** proposed data uses, collection and evaluation have confirmed permissions and controls suitable for the intended work. **Pass for delivery:** the actual flows and relevant tests match the permitted purpose, applicable current duties and planned obligations for the release date; an unresolved required permission, legal interpretation or data-use decision remains `needs_input`. This module supplies a legal-review workflow, not a legal opinion for a particular product.

### AI-07 — Monitoring, incidents and product learning

Before release, declare the monitored population, accepted version and baseline, signal definitions, collection permissions, sample/cadence, minimum usable counts, thresholds, observation lag, dashboards or reports, and actual response owners/authority. Cover relevant input distribution and missingness, output/behavior distribution, task outcomes, costly errors, refusals and abstention, safety/privacy/security incidents, performance by important slices, user complaints/overrides, latency/availability and material resource costs. Statistical drift is a warning signal; it is not automatically proof of a quality loss. A stable input distribution is not proof that performance remains good.

When labels arrive late or are unavailable, state proxy limitations and the safe operating boundary. Select and audit permitted output samples, correlate incidents with exact configuration and retain enough protected evidence to reproduce failure. Unknown targets, missing owners, disabled telemetry, inadequate sample sizes and failed alerts are visible pending states, never green. Test alert delivery and the actual response path, including operator absence. Define warning, escalation, narrowed exposure, safe fallback, rollback or halt conditions and decision time limits from actual risk and authority.

Create an observed post-release review for a declared window and population. Compare target, baseline and actual numerator/denominator per outcome and relevant slice; record incidents, uncertainty, confounders and unexpected harms/benefits. Choose continue, improve, narrow, roll back or retire with rationale and real decision authority. Link resulting hypothesis updates and actions to strategy, roadmap, release goals and owned backlog records; an incident response does not replace product-learning review. Update the risk register and add new failures to an authorised regression set while keeping acceptance evaluation independent of tuning.

**Pass for delivery:** monitoring, alerting, fallback/response and a scheduled learning review are configured and tested. **Pass for learning:** observed data and the post-release decision are present, and resulting strategy/roadmap actions are traceable. Go-live is not evidence that outcomes improved.

## 4. Stage-specific evidence

| Stage | Evidence required now | Evidence not claimed yet |
| --- | --- | --- |
| Discovery | Applicability branch; intended use and material unknowns; riskiest assumption and bounded test; proposed data permissions and safety boundary before the test | Accepted production accuracy, executed promotion or observed post-release outcomes |
| Planning | AI-01 risk/authority contract; proposed AI-02/03 dataset, metrics and quality bars; planned AI-04 controls; AI-06 applicability and permitted discovery/data uses; viable AI-07 measurement plan | Passing runs or live observations that have not happened |
| Ready | Frozen evaluation/dataset/rubric/threshold contract; required permissions; version/control/test plan; required reviewers and authority; feasible monitoring/response plan | Release pass merely because the plan is complete |
| Delivery | Current AI-02 dataset quality, AI-03 measured targets, AI-04 observed safety/fallback, AI-05 candidate-to-release traceability/regression, AI-06 actual data controls, AI-07 tested monitoring and response; actual separate approvals | Success of a future outcome window |
| Learning | Versioned observations and post-release target comparison; drift/incident decisions; revised hypotheses, risk controls and strategy/roadmap actions | A delayed or empty sample as proof of success |

Reuse prior group evidence only when its scope, pins, stage, source authority, freshness and assumptions still cover the present decision. Changes trigger impact analysis and refresh affected group reviews. A low-risk documentation change does not require an unrelated entire model retest, but the exception must be evidenced and must not mask a behavioral, data or authority change.

## 5. Record structure and hierarchy mapping

`ai-assurance.template.json` is an intake and evidence index, not a checker input, an executable test runner or an approval. Blank/null values are deliberate unresolved values. It has seven groups containing consolidated claims, evidence references and stage/status. Fill a single capability record and link shared current evidence; avoid copying the same narrative into every child issue.

Map the record into `common.context_profile`, `common.ai_assurance_reference` and, where personal data applies, `common.personal_data_controls`, using source IDs, content pins, element field values and review evidence in the existing structured checker model. The following catalogue fields receive the relevant subset:

| Hierarchy element | Mapping |
| --- | --- |
| Vision | Intended value, affected people and limits; link context rather than inventing AI as the vision |
| Strategy | AI/non-AI rationale, major risk assumptions, outcome metrics and `strategy.learning_feedback` |
| Roadmap | Discovery/assurance dependencies, learning checkpoints and `roadmap.learning_feedback` |
| Release goal | `release_goal.ai_release_controls`, exact acceptance thresholds, promotion/operation distinction, `release_goal.post_release_review` |
| Epic | `epic.assumption_test`, `epic.ai_validation_contract`, coverage and risk of the bounded capability |
| User story | `user_story.ai_acceptance_contract`, outcome/error/fallback scenarios and linked team readiness/completion checklists |
| Acceptance criterion | `acceptance_criterion.ai_evaluation_measurement`, metric contract, dataset/config pins and actual results |
| Technical task | `technical_task.ai_artifact_evidence`, implementation/evaluation/monitoring artifact evidence and linked team checklists |

The context profile records the assurance record ID, version, content hash, stage, scope and seven group evidence links. An external reviewer checks those links and the current stage requirements. No new provider or model call is needed to use the module. Credentials and unnecessary raw evaluation data do not belong in the product-management package.

## 6. Questions and loop exit

Ask the smallest decision-making question that resolves the next blocked must-pass group. A question names the missing fact, why this stage needs it, acceptable evidence, actual decision authority if known, and which records will change. Questions may recur when a later answer exposes a new material uncertainty; the same unanswered question is not repeatedly emitted as a new question. Consolidate related dataset or metric requests into an evidence contract rather than generating one question per detail.

The loop can revise prose, restructure evidence and propose options within authorised scope. It cannot invent the dataset, target, owner, permission, review, observed result or approval; lower a threshold after observing failures without a legitimate versioned decision; treat an agent-created reviewer ID as trusted; or call external services because an intake field mentions them.

Exit the current stage only when every applicable must-pass group is current and satisfied, reviewed exclusions have evidence, unresolved required answers are closed, selected supporting samples pass, and the actual separate quality, approval, readiness and delivery conditions are accurately reported. Report `blocked` or `needs_input` with the exact question when information is missing. A documentation-quality result is not a production-performance or legal-compliance certification.

## 7. Primary source notes and currency

These notes were checked against primary official publications on 10 October 2026. Recheck them for the project's actual jurisdiction and release date. The detailed operating criteria above are the bundle's authored policy, not verbatim requirements attributed to these publications.

**AI background.** NIST describes its AI Risk Management Framework as voluntary and intended to support consideration of trustworthiness during design, development, use and evaluation. The official site says AI RMF 1.0 is undergoing revision; this module uses the published 1.0 as a reference, not an assumed final future revision. [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework).

NIST's published Generative AI Profile is a voluntary cross-sector companion. Its measurement guidance addresses evaluation in conditions resembling use, data provenance, limitations, safety, privacy, bias and continuing monitoring. It supplies context for the module's lifecycle approach and does not set universal numeric accuracy targets. [NIST AI 600-1, July 2024](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf).

**India: applicability and phased commencement.** Section 3 of the enacted DPDP Act describes digital personal-data processing in India and processing outside India connected to offering goods or services to people in India, subject to the Act's scope and exclusions. Applicability still requires the project's facts and the operative text. [DPDP Act 2023, section 3](https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf).

The 13 November 2025 commencement notification stages the Act's provisions: an initial institutional/other group starts on publication, section 6(9) and section 27(1)(d) after one year, and the specified main processing/rights/enforcement group after eighteen months. The calculated anniversaries are 13 November 2026 and 13 May 2027; these dates are a computation from the notification, not a blanket statement that every provision commences then. [G.S.R. 843(E)](https://www.meity.gov.in/static/uploads/2025/11/c56ceae6c383460ca69577428d36828b.pdf).

Rule 1 starts rules 1, 2 and 17–21 on publication, rule 4 after one year, and rules 3, 5–16, 22 and 23 after eighteen months. Read the final Rules with the December 2025 corrigendum, which corrects the wording of commencement references and other passages. [G.S.R. 846(E), rule 1](https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf), [G.S.R. 892(E), corrigendum](https://www.meity.gov.in/static/uploads/2025/12/3c7ebbae0e5456f493f486e6845df86b.pdf).

The October 2026 Removal of Difficulties Order makes textual changes in sections 9(1) and 10(2)(c)(ii) and states that the Order starts on its Gazette publication. Read it with the Act and separate commencement notification; the Order is not a blanket acceleration of the main processing obligations. [S.O. 5458(E), Gazette dated 6 October 2026](https://www.meity.gov.in/static/uploads/2026/10/daf495a7b5798a3dfa72a944b51fc176.pdf).

For adoption, the responsible qualified reviewer records exact current provisions, commencement, factual applicability and any other applicable duties. Preserve the authoritative document/version and review date in the project's sources; a copied date in this generic template cannot establish compliance at a later date.
