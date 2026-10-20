# Generic product management documentation and quality standard

Version: 3.0-generic. 10 October 2026. This framework is generic across digital, physical, service, internal/process and mixed products. It certifies neither a particular product plan nor legal/approval/readiness/delivery authority.

## Review load and certification boundary

Default assessment selects exactly seven must-pass semantic gates per item for its declared stage: discovery, planning, ready, delivery or learning. Every core structural/source/evidence/version/applicability/trust-integrity check remains mandatory. Up to two deterministic noncritical field-rule targets per hierarchy level across all assessed items are advisory samples; their verdicts are disclosed and never certify unsampled detail coverage. Exhaustive field review is optional and explicitly displays its cost. Safety, privacy, security, authorization, applicable AI assurance and protected source obligations live in unsampled gates and cannot be bypassed by sampling.

Required content components belong to their owning field. They are not separate quality checks and require no per-component verdict. The reference field rules support deeper or sampled inspection; the current-stage aggregate contract defines the mandatory semantic verdicts.

## Actual context, authority and applicability

Use pinned actual product sources and profile: users, outcomes, operating context, product type, controls, protected assets, information sensitivity, applicable safety/domain/jurisdiction obligations, actual process and authority. Unknown necessary applicability, access, rights, evidence or authority remains unresolved. AI use is yes/no/unknown with evidence; authoring-only AI is separately declared. India personal-data rules apply only when the actual context and authoritative current sources establish applicability. Do not invent dates, targets, estimates, owners, recipients, consent, approvals or clinical/industry policy.

Offline review is advisory only. Local names such as reviewer-2 cannot establish independence or authority; authoritative mode needs a reviewer registry and verification receipt administered outside the authoring agent. Quality, actual specification approval, execution readiness, acceptance, authorised publication, observed availability, user verification and outcome learning stay separate.

## Executable branch guard

Engine model productProfile.ai and productProfile.personalData carry applicability yes/no/unknown, pinned sourceIds and a specific rationale. Unknown is permitted only during bounded discovery with a sourced resolutionPlan and no consequential runtime evaluation; planning, ready, delivery and learning remain needs_input until necessary applicability is resolved. Actual pinned source objects may optionally add requiredBranches={ai:true, personalData:true}. The metadata may only assert obligations, never set false; absence is not an exclusion. A no/N/A profile cannot remove a branch explicitly required by a retained source. All branch fields still need evidence-backed aggregate review; metadata does not authenticate semantic truth.

## Canonical team Ready and Done

team-checklists.json contains one proposed reusable team Definition of Ready and one Definition of Done. The actual team authority must adopt/version them; no owner or approval is fabricated. Stories and tasks link the exact adopted canonical policy ID/version/content hash and current evidence, plus item-specific additions. Changing policy or item/evidence invalidates dependent reviews.

## Compatibility

Canonical generic field IDs replace software-only aliases. compatibility-map.json gives explicit field/check/component migration. Preserve original text and provenance, pin v3 and re-review changed content; a prior PASS is stale. Exact prototype/batch/procedure/service revisions and observed operational availability are first-class evidence. Git, CI, APIs or hosting are only actual-process examples.

## Required field content components

## Shared information field requirements

- **Identity** (`common.identity`): Define Identity.
  Required field content components: common.identity.detail_1 — Stable ID or canonical document link; common.identity.detail_2 — title; common.identity.detail_3 — element type; common.identity.detail_4 — version.
  Applicability: always. Required; apply source qualifiers.

- **Purpose** (`common.purpose`): Define Purpose.
  Required field content components: common.purpose.detail_1 — Intended outcome; common.purpose.detail_2 — people or operators served.
  Applicability: always. Required; apply source qualifiers.

- **Traceability** (`common.traceability`): Define Traceability.
  Required field content components: common.traceability.detail_1 — Parent; common.traceability.detail_2 — authoritative source IDs; common.traceability.detail_3 — relevant children; common.traceability.detail_4 — decision links; common.traceability.detail_5 — canonical record links.
  Applicability: always. Required; apply source qualifiers.

- **Boundary** (`common.boundary`): Define Boundary.
  Required field content components: common.boundary.detail_1 — Included scope; common.boundary.detail_2 — excluded scope; common.boundary.detail_3 — constraints.
  Applicability: always. Required; apply source qualifiers.

- **Responsibility** (`common.responsibility`): Define Responsibility.
  Required field content components: common.responsibility.detail_1 — Actual accountable owner or assignee; common.responsibility.detail_2 — applicable approval authority; common.responsibility.detail_3 — pending owner/authority explicitly identified.
  Applicability: always. Required; apply source qualifiers.

- **State** (`common.state`): Define State.
  Required field content components: common.state.detail_1 — Planning state; common.state.detail_2 — readiness state; common.state.detail_3 — delivery state; common.state.detail_4 — state reason; common.state.detail_5 — agreed dates/targets or explicit pending decision.
  Applicability: always. Required; apply source qualifiers.

- **Evidence** (`common.evidence`): Define Evidence.
  Required field content components: common.evidence.detail_1 — Claim links; common.evidence.detail_2 — observations; common.evidence.detail_3 — test outputs; common.evidence.detail_4 — explicitly labelled assumptions.
  Applicability: always. Required; apply source qualifiers.

- **Change history** (`common.change_history`): Define Change history.
  Required field content components: common.change_history.detail_1 — What changed; common.change_history.detail_2 — why; common.change_history.detail_3 — when; common.change_history.detail_4 — decision impact; common.change_history.detail_5 — source impact; common.change_history.detail_6 — frozen-version impact.
  Applicability: always. Required; apply source qualifiers.

- **Source provenance** (`common.source_provenance`): Define Source provenance.
  Required field content components: common.source_provenance.detail_1 — Original source or proposed supplement; common.source_provenance.detail_2 — Exact source/version reference.
  Applicability: always. Required; apply source qualifiers.

- **Approval/specification state** (`common.approval_specification_state`): Define Approval/specification state.
  Required field content components: common.approval_specification_state.detail_1 — Draft/approved/frozen revision; common.approval_specification_state.detail_2 — Applicable authority/decision evidence.
  Applicability: always. Required; apply source qualifiers.

- **Execution result** (`common.execution_result`): Define Execution result.
  Required field content components: common.execution_result.detail_1 — Not run/passed/failed/blocked/skipped; common.execution_result.detail_2 — Reason; common.execution_result.detail_3 — Evidence for observed results.
  Applicability: conditional. Required when criteria or delivery claims are involved; nonexecution is an explicit state, not fabricated evidence.

- **Actual product context and assurance applicability** (`common.context_profile`): Resolve generic obligations through the actual product profile and pinned authority sources.
  Required field content components: common.context_profile.detail_1 — Profile ID, version and content hash; product type, actual users and operating context; common.context_profile.detail_2 — AI use: yes/no/unknown, scope and factual source; authoring-only AI separately declared; common.context_profile.detail_3 — Safety, security, access, accessibility and information sensitivity with actual consequences; common.context_profile.detail_4 — Personal-data and jurisdiction applicability, governing authoritative sources and unresolved legal decisions; common.context_profile.detail_5 — AI assurance record ID/version/hash and applicable AI-01 to AI-07 evidence links; common.context_profile.detail_6 — Protected source obligations, prohibited effects and qualification/release process.
  Applicability: always. Required at the selected stage when named by a must-pass gate. Unagreed facts may be identified as pending only where that stage permits them.

- **Pinned AI assurance record and current-stage groups** (`common.ai_assurance_reference`): Apply a controlled AI assurance record across hierarchy levels when product AI is used.
  Required field content components: common.ai_assurance_reference.detail_1 — Actual AI assurance record ID, version and content hash; common.ai_assurance_reference.detail_2 — Current-stage AI-01 to AI-07 status and exact evidence locators; common.ai_assurance_reference.detail_3 — Actual product AI scope, model/prompt/configuration revision and responsible decisions; common.ai_assurance_reference.detail_4 — Dataset rights/quality, evaluation/safety/fallback, privacy/legal and monitoring obligations; common.ai_assurance_reference.detail_5 — Unresolved applicability, failed threshold or required decision with precise resume condition.
  Applicability: conditional. Required when product AI is yes; AI unknown is unresolved for a dependent decision. A no-use exclusion must cite a pinned actual source and rationale.

- **Applicable personal-data rights and governance** (`common.personal_data_controls`): Carry actual privacy/legal obligations into every stage where personal data is used.
  Required field content components: common.personal_data_controls.detail_1 — Personal-data applicability, categories, subjects, purpose and minimal necessary scope; common.personal_data_controls.detail_2 — Jurisdiction/legal applicability and current authoritative sources; actual reviewed decision; common.personal_data_controls.detail_3 — Permission/consent or other established legal basis, rights and processing boundaries as applicable; common.personal_data_controls.detail_4 — Access, retention/deletion, security, affected third parties and transfer constraints; common.personal_data_controls.detail_5 — Actual decision/approval evidence, unresolved legal facts and prohibited processing.
  Applicability: conditional. Required when actual personal-data processing is yes; unknown applicability is unresolved for a dependent decision. A no-personal-data exclusion must cite a pinned actual source and rationale.

## Product vision field requirements

- **Title/version** (`vision.title_version`): Define Title/version.
  Required field content components: vision.title_version.detail_1 — Vision title; vision.title_version.detail_2 — vision version.
  Applicability: always. Required; apply source qualifiers.

- **Accountable product owner and review authority** (`vision.owner_authority`): Define Accountable product owner and review authority.
  Required field content components: vision.owner_authority.detail_1 — Accountable product owner; vision.owner_authority.detail_2 — review authority.
  Applicability: always. Required; apply source qualifiers.

- **Source/research links** (`vision.research_sources`): Define Source/research links.
  Required field content components: vision.research_sources.detail_1 — Source links; vision.research_sources.detail_2 — research links.
  Applicability: always. Required; apply source qualifiers.

- **State and last review** (`vision.state_review`): Define State and last review.
  Required field content components: vision.state_review.detail_1 — Planning state; vision.state_review.detail_2 — last review date.
  Applicability: always. Required; apply source qualifiers.

- **Primary users and their operating context** (`vision.primary_users_context`): Define Primary users and their operating context.
  Required field content components: vision.primary_users_context.detail_1 — Primary users; vision.primary_users_context.detail_2 — their operating context.
  Applicability: always. Required; apply source qualifiers.

- **Problem or unmet need, with supporting evidence** (`vision.problem_evidence`): Define Problem or unmet need, with supporting evidence.
  Required field content components: vision.problem_evidence.detail_1 — Problem or unmet need; vision.problem_evidence.detail_2 — supporting evidence.
  Applicability: always. Required; apply source qualifiers.

- **Other affected users/operators** (`vision.affected_users`): Define Other affected users/operators.
  Required field content components: vision.affected_users.detail_1 — Other affected users; vision.affected_users.detail_2 — operators.
  Applicability: conditional. Required when people/operators other than the primary user are materially affected; a verified no-other-role finding may support N/A.

- **Vision statement** (`vision.vision_statement`): Define Vision statement.
  Required field content components: vision.vision_statement.detail_1 — People served; vision.vision_statement.detail_2 — valuable future outcome; vision.vision_statement.detail_3 — operating context.
  Applicability: always. Required; apply source qualifiers.

- **Value delivered to users and the organisation** (`vision.value`): Define Value delivered to users and the organisation.
  Required field content components: vision.value.detail_1 — User value; vision.value.detail_2 — organisational value.
  Applicability: always. Required; apply source qualifiers.

- **Principles that guide product decisions** (`vision.principles`): Define Principles that guide product decisions.
  Required field content components: vision.principles.detail_1 — Product decision principles.
  Applicability: always. Required; apply source qualifiers.

- **Boundaries and non-goals** (`vision.non_goals`): Define Boundaries and non-goals.
  Required field content components: vision.non_goals.detail_1 — Boundaries; vision.non_goals.detail_2 — non-goals.
  Applicability: always. Required; apply source qualifiers.

- **Long-term success signals** (`vision.success_signals`): Define Long-term success signals.
  Required field content components: vision.success_signals.detail_1 — Long-term success signals.
  Applicability: always. Required; apply source qualifiers.

- **For each measurable signal** (`vision.signal_measurement`): Define For each measurable signal.
  Required field content components: vision.signal_measurement.detail_1 — Signal definition; vision.signal_measurement.detail_2 — population/denominator; vision.signal_measurement.detail_3 — baseline source; vision.signal_measurement.detail_4 — measurement period; vision.signal_measurement.detail_5 — owner; vision.signal_measurement.detail_6 — pending unmeasured baseline or unagreed target.
  Applicability: conditional. Required for each measurable success signal; qualitative/nonmeasurable signals require a justified alternative observation method.

- **Assumptions requiring validation and research needed** (`vision.assumptions_research`): Define Assumptions requiring validation and research needed.
  Required field content components: vision.assumptions_research.detail_1 — Assumptions requiring validation; vision.assumptions_research.detail_2 — research needed.
  Applicability: always. Required; apply source qualifiers.

- **Review triggers and linked strategy** (`vision.review_strategy`): Define Review triggers and linked strategy.
  Required field content components: vision.review_strategy.detail_1 — Review triggers; vision.review_strategy.detail_2 — linked strategy.
  Applicability: always. Required; apply source qualifiers.

- **Change history** (`vision.change_history`): Define Change history.
  Required field content components: vision.change_history.detail_1 — Vision changes; vision.change_history.detail_2 — reasons; vision.change_history.detail_3 — revision/time; vision.change_history.detail_4 — source/decision impact.
  Applicability: always. Required; apply source qualifiers.

- **Outcome learning and strategy/roadmap feedback** (`vision.learning_feedback`): Keep product direction responsive to measured outcomes.
  Required field content components: vision.learning_feedback.detail_1 — Linked post-release or discovery review ID/version/evidence; vision.learning_feedback.detail_2 — Original target, observed result and comparable context; vision.learning_feedback.detail_3 — Uncertainty, confounders and counterevidence; vision.learning_feedback.detail_4 — Continue/change/stop decision with actual authority; vision.learning_feedback.detail_5 — Changed hypothesis, strategy choice or roadmap priority and canonical link; vision.learning_feedback.detail_6 — Next measurement/review window, actual owner and decision follow-up.
  Applicability: always. Required at the selected stage when named by a must-pass gate. Unagreed facts may be identified as pending only where that stage permits them.

## Product strategy field requirements

- **Title/version, owner, decision authority and state** (`strategy.identity_state`): Define Title/version, owner, decision authority and state.
  Required field content components: strategy.identity_state.detail_1 — Strategy title; strategy.identity_state.detail_2 — version; strategy.identity_state.detail_3 — owner; strategy.identity_state.detail_4 — decision authority; strategy.identity_state.detail_5 — state.
  Applicability: always. Required; apply source qualifiers.

- **Parent vision and authoritative source links** (`strategy.vision_sources`): Define Parent vision and authoritative source links.
  Required field content components: strategy.vision_sources.detail_1 — Parent vision; strategy.vision_sources.detail_2 — authoritative source links.
  Applicability: always. Required; apply source qualifiers.

- **User/operational problems to address first** (`strategy.priority_problems`): Define User/operational problems to address first.
  Required field content components: strategy.priority_problems.detail_1 — Problems addressed first; strategy.priority_problems.detail_2 — priority rationale.
  Applicability: always. Required; apply source qualifiers.

- **Evidence supporting the diagnosis** (`strategy.diagnosis_evidence`): Define Evidence supporting the diagnosis.
  Required field content components: strategy.diagnosis_evidence.detail_1 — Evidence supporting diagnosis.
  Applicability: always. Required; apply source qualifiers.

- **Constraints** (`strategy.constraints`): Define Constraints.
  Required field content components: strategy.constraints.detail_1 — Responsibilities; strategy.constraints.detail_2 — systems; strategy.constraints.detail_3 — capacity; strategy.constraints.detail_4 — permissions; strategy.constraints.detail_5 — resources.
  Applicability: always. Required; apply source qualifiers.

- **Priority users and use cases** (`strategy.priority_users_use_cases`): Define Priority users and use cases.
  Required field content components: strategy.priority_users_use_cases.detail_1 — Priority users; strategy.priority_users_use_cases.detail_2 — priority use cases.
  Applicability: always. Required; apply source qualifiers.

- **Strategic choices/bets, why each is worth pursuing, and alternatives/trade-offs** (`strategy.choices_tradeoffs`): Define Strategic choices/bets, why each is worth pursuing, and alternatives/trade-offs.
  Required field content components: strategy.choices_tradeoffs.detail_1 — Strategic choices/bets; strategy.choices_tradeoffs.detail_2 — reason for each; strategy.choices_tradeoffs.detail_3 — alternatives; strategy.choices_tradeoffs.detail_4 — trade-offs.
  Applicability: always. Required; apply source qualifiers.

- **What is deferred or excluded, with rationale** (`strategy.deferral`): Define What is deferred or excluded, with rationale.
  Required field content components: strategy.deferral.detail_1 — Deferred/excluded work; strategy.deferral.detail_2 — rationale.
  Applicability: always. Required; apply source qualifiers.

- **Existing components to reuse and capabilities requiring separate decisions** (`strategy.reuse_decisions`): Define Existing components to reuse and capabilities requiring separate decisions.
  Required field content components: strategy.reuse_decisions.detail_1 — Existing reusable components; strategy.reuse_decisions.detail_2 — capabilities requiring separate decisions.
  Applicability: always. Required; apply source qualifiers.

- **Dependencies and assumptions** (`strategy.dependencies_assumptions`): Define Dependencies and assumptions.
  Required field content components: strategy.dependencies_assumptions.detail_1 — Dependencies; strategy.dependencies_assumptions.detail_2 — assumptions.
  Applicability: always. Required; apply source qualifiers.

- **Outcome measures** (`strategy.outcome_measures`): Define Outcome measures.
  Required field content components: strategy.outcome_measures.detail_1 — Measure definition; strategy.outcome_measures.detail_2 — numerator/denominator where applicable; strategy.outcome_measures.detail_3 — baseline; strategy.outcome_measures.detail_4 — source; strategy.outcome_measures.detail_5 — period; strategy.outcome_measures.detail_6 — owner.
  Applicability: always. Required; apply source qualifiers.

- **Agreed targets or explicit pending decision** (`strategy.targets`): Define Agreed targets or explicit pending decision.
  Required field content components: strategy.targets.detail_1 — Agreed targets; strategy.targets.detail_2 — or explicit pending target decision.
  Applicability: always. Required; apply source qualifiers.

- **Validation/learning plan** (`strategy.validation_plan`): Define Validation/learning plan.
  Required field content components: strategy.validation_plan.detail_1 — Validation/learning plan.
  Applicability: always. Required; apply source qualifiers.

- **Conditions to continue, adjust, stop or revisit a choice** (`strategy.continue_adjust_stop`): Define Conditions to continue, adjust, stop or revisit a choice.
  Required field content components: strategy.continue_adjust_stop.detail_1 — Conditions to continue; strategy.continue_adjust_stop.detail_2 — adjust; strategy.continue_adjust_stop.detail_3 — stop; strategy.continue_adjust_stop.detail_4 — revisit choices.
  Applicability: always. Required; apply source qualifiers.

- **Linked roadmap and release goals** (`strategy.roadmap_release_links`): Define Linked roadmap and release goals.
  Required field content components: strategy.roadmap_release_links.detail_1 — Linked roadmap; strategy.roadmap_release_links.detail_2 — release goals.
  Applicability: always. Required; apply source qualifiers.

- **Open decisions and their owners** (`strategy.open_decisions`): Define Open decisions and their owners.
  Required field content components: strategy.open_decisions.detail_1 — Open decisions; strategy.open_decisions.detail_2 — decision owners.
  Applicability: always. Required; apply source qualifiers.

- **Resource/capacity commitments only if established** (`strategy.resource_commitments`): Define Resource/capacity commitments only if established.
  Required field content components: strategy.resource_commitments.detail_1 — Established resource commitments; strategy.resource_commitments.detail_2 — established capacity commitments.
  Applicability: conditional. Required when a commitment is claimed; unestablished capacity must be identified as an assumption, not an invented commitment.

- **Review triggers and change history** (`strategy.review_history`): Define Review triggers and change history.
  Required field content components: strategy.review_history.detail_1 — Review triggers; strategy.review_history.detail_2 — change history.
  Applicability: always. Required; apply source qualifiers.

- **Outcome learning and strategy/roadmap feedback** (`strategy.learning_feedback`): Keep product direction responsive to measured outcomes.
  Required field content components: strategy.learning_feedback.detail_1 — Linked post-release or discovery review ID/version/evidence; strategy.learning_feedback.detail_2 — Original target, observed result and comparable context; strategy.learning_feedback.detail_3 — Uncertainty, confounders and counterevidence; strategy.learning_feedback.detail_4 — Continue/change/stop decision with actual authority; strategy.learning_feedback.detail_5 — Changed hypothesis, strategy choice or roadmap priority and canonical link; strategy.learning_feedback.detail_6 — Next measurement/review window, actual owner and decision follow-up.
  Applicability: always. Required at the selected stage when named by a must-pass gate. Unagreed facts may be identified as pending only where that stage permits them.

## Roadmap field requirements

- **Title/version, owner, planning state and sources** (`roadmap.identity_state`): Define Title/version, owner, planning state and sources.
  Required field content components: roadmap.identity_state.detail_1 — Roadmap title; roadmap.identity_state.detail_2 — version; roadmap.identity_state.detail_3 — owner; roadmap.identity_state.detail_4 — planning state; roadmap.identity_state.detail_5 — sources.
  Applicability: always. Required; apply source qualifiers.

- **Linked vision, strategy and release-goal documents** (`roadmap.alignment_links`): Define Linked vision, strategy and release-goal documents.
  Required field content components: roadmap.alignment_links.detail_1 — Vision link; roadmap.alignment_links.detail_2 — strategy link; roadmap.alignment_links.detail_3 — release-goal document links.
  Applicability: always. Required; apply source qualifiers.

- **Now** (`roadmap.now`): Define Now.
  Required field content components: roadmap.now.detail_1 — Current horizon outcomes; roadmap.now.detail_2 — canonical records; roadmap.now.detail_3 — priority; roadmap.now.detail_4 — entry conditions.
  Applicability: always. Required; apply source qualifiers.

- **Next** (`roadmap.next`): Define Next.
  Required field content components: roadmap.next.detail_1 — Next horizon outcomes; roadmap.next.detail_2 — canonical records; roadmap.next.detail_3 — transition conditions.
  Applicability: always. Required; apply source qualifiers.

- **Later** (`roadmap.later`): Define Later.
  Required field content components: roadmap.later.detail_1 — Later horizon outcomes; roadmap.later.detail_2 — canonical records; roadmap.later.detail_3 — uncertainty.
  Applicability: always. Required; apply source qualifiers.

- **Complete release and horizon allocation with sources** (`roadmap.release_allocation`): Define Complete release and horizon allocation with sources.
  Required field content components: roadmap.release_allocation.detail_1 — Current committed release allocation; roadmap.release_allocation.detail_2 — subsequent release or horizon allocation; roadmap.release_allocation.detail_3 — complete longer-term scope allocation; roadmap.release_allocation.detail_4 — sources.
  Applicability: always. Required; apply source qualifiers.

- **Cross-release/shared epic links without duplicated issues** (`roadmap.shared_epics`): Define Cross-release/shared epic links without duplicated issues.
  Required field content components: roadmap.shared_epics.detail_1 — Cross-release epic links; roadmap.shared_epics.detail_2 — shared epic links; roadmap.shared_epics.detail_3 — no duplicated issues.
  Applicability: always. Required; apply source qualifiers.

- **Actual required predecessor outputs** (`roadmap.predecessor_outputs`): Define Actual required predecessor outputs.
  Required field content components: roadmap.predecessor_outputs.detail_1 — Actual required predecessor outputs.
  Applicability: always. Required; apply source qualifiers.

- **Design relationships that inform work but do not block every story** (`roadmap.design_relationships`): Define Design relationships that inform work but do not block every story.
  Required field content components: roadmap.design_relationships.detail_1 — Nonblocking design relationships.
  Applicability: conditional. Required where design relationships inform sequencing; no-design-dependency findings require explicit reason.

- **Evidence needed to move scope into the next horizon** (`roadmap.horizon_gate_evidence`): Define Evidence needed to move scope into the next horizon.
  Required field content components: roadmap.horizon_gate_evidence.detail_1 — Evidence to advance scope to next horizon.
  Applicability: always. Required; apply source qualifiers.

- **Capacity assumptions and uncertainty** (`roadmap.capacity_uncertainty`): Define Capacity assumptions and uncertainty.
  Required field content components: roadmap.capacity_uncertainty.detail_1 — Capacity assumptions; roadmap.capacity_uncertainty.detail_2 — uncertainty.
  Applicability: always. Required; apply source qualifiers.

- **Deferred scope and why** (`roadmap.deferred_scope`): Define Deferred scope and why.
  Required field content components: roadmap.deferred_scope.detail_1 — Deferred scope; roadmap.deferred_scope.detail_2 — rationale.
  Applicability: always. Required; apply source qualifiers.

- **Open decisions/blockers, accountable owner and precise resume condition** (`roadmap.blockers_decisions`): Define Open decisions/blockers, accountable owner and precise resume condition.
  Required field content components: roadmap.blockers_decisions.detail_1 — Open decision/blocker; roadmap.blockers_decisions.detail_2 — accountable owner; roadmap.blockers_decisions.detail_3 — precise resume condition.
  Applicability: always. Required; apply source qualifiers.

- **Change history** (`roadmap.change_history`): Define Change history.
  Required field content components: roadmap.change_history.detail_1 — Changes; roadmap.change_history.detail_2 — reason; roadmap.change_history.detail_3 — version/time; roadmap.change_history.detail_4 — affected sequence/source/gates.
  Applicability: always. Required; apply source qualifiers.

- **Sequence table: horizon/release** (`roadmap.sequence_horizon_release`): Define Sequence table: horizon/release.
  Required field content components: roadmap.sequence_horizon_release.detail_1 — Now/Next/Later or named release; roadmap.sequence_horizon_release.detail_2 — Canonical release identity.
  Applicability: always. Required; apply source qualifiers.

- **Sequence table: intended outcome** (`roadmap.sequence_outcome`): Define Sequence table: intended outcome.
  Required field content components: roadmap.sequence_outcome.detail_1 — Intended user/operator outcome.
  Applicability: always. Required; apply source qualifiers.

- **Sequence table: canonical epic/story links** (`roadmap.sequence_item_links`): Define Sequence table: canonical epic/story links.
  Required field content components: roadmap.sequence_item_links.detail_1 — Canonical epic links; roadmap.sequence_item_links.detail_2 — Canonical story/supporting-item links.
  Applicability: always. Required; apply source qualifiers.

- **Sequence table: sequencing rationale** (`roadmap.sequence_rationale`): Define Sequence table: sequencing rationale.
  Required field content components: roadmap.sequence_rationale.detail_1 — Why this outcome comes here; roadmap.sequence_rationale.detail_2 — Relevant priority/trade-off.
  Applicability: always. Required; apply source qualifiers.

- **Sequence table: dependency/decision gate** (`roadmap.sequence_gate`): Define Sequence table: dependency/decision gate.
  Required field content components: roadmap.sequence_gate.detail_1 — Concrete predecessor output or decision; roadmap.sequence_gate.detail_2 — Owner/authority; roadmap.sequence_gate.detail_3 — Observable entry condition.
  Applicability: always. Required; apply source qualifiers.

- **Sequence table: confidence** (`roadmap.sequence_confidence`): Define Sequence table: confidence.
  Required field content components: roadmap.sequence_confidence.detail_1 — Confidence assessment; roadmap.sequence_confidence.detail_2 — Supporting evidence; roadmap.sequence_confidence.detail_3 — Uncertainty and review trigger.
  Applicability: always. Required; apply source qualifiers.

- **Sequence table: agreed timing, if any** (`roadmap.sequence_timing`): Define Sequence table: agreed timing, if any.
  Required field content components: roadmap.sequence_timing.detail_1 — Agreed timing when established; roadmap.sequence_timing.detail_2 — Authority/agreement source; roadmap.sequence_timing.detail_3 — Uncertainty/review condition.
  Applicability: conditional. Required only where timing is agreed or claimed; otherwise state no timing commitment and decision context without inventing dates.

- **Outcome learning and strategy/roadmap feedback** (`roadmap.learning_feedback`): Keep product direction responsive to measured outcomes.
  Required field content components: roadmap.learning_feedback.detail_1 — Linked post-release or discovery review ID/version/evidence; roadmap.learning_feedback.detail_2 — Original target, observed result and comparable context; roadmap.learning_feedback.detail_3 — Uncertainty, confounders and counterevidence; roadmap.learning_feedback.detail_4 — Continue/change/stop decision with actual authority; roadmap.learning_feedback.detail_5 — Changed hypothesis, strategy choice or roadmap priority and canonical link; roadmap.learning_feedback.detail_6 — Next measurement/review window, actual owner and decision follow-up.
  Applicability: always. Required at the selected stage when named by a must-pass gate. Unagreed facts may be identified as pending only where that stage permits them.

## Release goal field requirements

- **Release ID/name, version, milestone link, owner and state** (`release_goal.identity_milestone`): Define Release ID/name, version, milestone link, owner and state.
  Required field content components: release_goal.identity_milestone.detail_1 — Release ID/name; release_goal.identity_milestone.detail_2 — version; release_goal.identity_milestone.detail_3 — milestone link; release_goal.identity_milestone.detail_4 — owner; release_goal.identity_milestone.detail_5 — state.
  Applicability: always. Required; apply source qualifiers.

- **Parent roadmap/strategy and authoritative sources** (`release_goal.alignment_sources`): Define Parent roadmap/strategy and authoritative sources.
  Required field content components: release_goal.alignment_sources.detail_1 — Parent roadmap; release_goal.alignment_sources.detail_2 — strategy; release_goal.alignment_sources.detail_3 — authoritative sources.
  Applicability: always. Required; apply source qualifiers.

- **Target users, operating context and end-to-end journey** (`release_goal.users_journey`): Define Target users, operating context and end-to-end journey.
  Required field content components: release_goal.users_journey.detail_1 — Target users; release_goal.users_journey.detail_2 — operating context; release_goal.users_journey.detail_3 — end-to-end journey.
  Applicability: always. Required; apply source qualifiers.

- **Usable outcome this release must deliver** (`release_goal.usable_outcome`): Define Usable outcome this release must deliver.
  Required field content components: release_goal.usable_outcome.detail_1 — Usable release outcome.
  Applicability: always. Required; apply source qualifiers.

- **Measures and agreed targets, with baseline/measurement plan** (`release_goal.measures_targets`): Define Measures and agreed targets, with baseline/measurement plan.
  Required field content components: release_goal.measures_targets.detail_1 — Measures; release_goal.measures_targets.detail_2 — agreed targets; release_goal.measures_targets.detail_3 — baseline; release_goal.measures_targets.detail_4 — measurement plan.
  Applicability: always. Required; apply source qualifiers.

- **Included canonical stories and supporting items** (`release_goal.included_items`): Define Included canonical stories and supporting items.
  Required field content components: release_goal.included_items.detail_1 — Included canonical stories; release_goal.included_items.detail_2 — included supporting items.
  Applicability: always. Required; apply source qualifiers.

- **Must-have source requirements and applicable NFRs** (`release_goal.requirements_nfrs`): Define Must-have source requirements and applicable NFRs.
  Required field content components: release_goal.requirements_nfrs.detail_1 — Must-have source requirements; release_goal.requirements_nfrs.detail_2 — applicable NFRs.
  Applicability: always. Required; apply source qualifiers.

- **Excluded/deferred scope and rationale** (`release_goal.excluded_deferred`): Define Excluded/deferred scope and rationale.
  Required field content components: release_goal.excluded_deferred.detail_1 — Excluded/deferred scope; release_goal.excluded_deferred.detail_2 — rationale.
  Applicability: always. Required; apply source qualifiers.

- **Dependencies, readiness assumptions and open decisions** (`release_goal.dependencies_decisions`): Define Dependencies, readiness assumptions and open decisions.
  Required field content components: release_goal.dependencies_decisions.detail_1 — Dependencies; release_goal.dependencies_decisions.detail_2 — readiness assumptions; release_goal.dependencies_decisions.detail_3 — open decisions.
  Applicability: always. Required; apply source qualifiers.

- **Entry** (`release_goal.entry_gate`): Define Entry.
  Required field content components: release_goal.entry_gate.detail_1 — Specification readiness; release_goal.entry_gate.detail_2 — predecessor outputs; release_goal.entry_gate.detail_3 — fixtures; release_goal.entry_gate.detail_4 — environments; release_goal.entry_gate.detail_5 — applicable approvals.
  Applicability: always. Required; apply source qualifiers.

- **Exit** (`release_goal.exit_gate`): Define Exit.
  Required field content components: release_goal.exit_gate.detail_1 — Acceptance scenarios; release_goal.exit_gate.detail_2 — regression/integration checks; release_goal.exit_gate.detail_3 — release operating readiness.
  Applicability: always. Required; apply source qualifiers.

- **Applicable product, privacy, security, domain and human approval authorities** (`release_goal.approval_authorities`): Define Applicable product, privacy, security, domain and human approval authorities.
  Required field content components: release_goal.approval_authorities.detail_1 — privacy authority where applicable; release_goal.approval_authorities.detail_2 — security authority where applicable; release_goal.approval_authorities.detail_3 — domain-specific authority where applicable; release_goal.approval_authorities.detail_4 — product and human approval authority where required; release_goal.approval_authorities.detail_5 — linked authority requirements.
  Applicability: conditional. Required for authorities demanded by the release's actual source/policy/access rules; no applicable authority requires a justified source-based reason.

- **Rollout and recovery readiness through the authorized delivery route** (`release_goal.rollout_recovery`): Define Rollout and recovery readiness through the authorized delivery route.
  Required field content components: release_goal.rollout_recovery.detail_1 — Existing authorized rollout route; release_goal.rollout_recovery.detail_2 — recovery/rollback readiness.
  Applicability: conditional. Required when a release changes an operating product, service, process or configuration; a planning-only release may have a factually reviewed exclusion.

- **Final deliverable revision and change-review reference** (`release_goal.qualified_revision_review`): Define Final deliverable revision and change-review reference.
  Required field content components: release_goal.qualified_revision_review.detail_1 — Final deliverable or configuration revision; release_goal.qualified_revision_review.detail_2 — canonical change-review or decision reference where required.
  Applicability: conditional. Required when a versioned deliverable is part of release qualification; at authoring state planned evidence and not-yet-produced output. Change-review subtype follows the supplied product profile.

- **Final-revision qualification results and independent review** (`release_goal.final_tests_review`): Define Final-revision qualification results and independent review.
  Required field content components: release_goal.final_tests_review.detail_1 — Final-revision qualification or evaluation results; release_goal.final_tests_review.detail_2 — independent review.
  Applicability: conditional. Required at declared qualification stages; before execution describe the method and explicitly unproduced results. Software build/CI and physical/service evaluation details apply only to the relevant product profile.

- **Integrated or published revision evidence** (`release_goal.published_revision`): Define Integrated or published revision evidence.
  Required field content components: release_goal.published_revision.detail_1 — Observed integrated or published revision identifier.
  Applicability: conditional. Required only where integration, publication or operating-baseline adoption is part of the declared release gate. If the declared release gate has no such stage, supply an independently justified exclusion; an uncompleted required stage stays unmet.

- **Observed operationally available revision, context and observation time** (`release_goal.available_revision`): Define Observed operationally available revision, context and observation time.
  Required field content components: release_goal.available_revision.detail_1 — Actually observed operationally available revision identifier; release_goal.available_revision.detail_2 — operating environment or delivery context; release_goal.available_revision.detail_3 — observation time.
  Applicability: conditional. Required where observed operational availability is part of the declared release gate. Integration or publication alone cannot establish user availability or justify exclusion.

- **Operational journey verification, approved evaluation context and result** (`release_goal.operational_verification`): Define Operational journey verification, approved evaluation context and result.
  Required field content components: release_goal.operational_verification.detail_1 — Required operational journey verification; release_goal.operational_verification.detail_2 — approved evaluation fixture, participant context or sample; release_goal.operational_verification.detail_3 — observed result.
  Applicability: conditional. Required where operational journey verification is demanded by the declared gate; otherwise explain the authoritative alternative evidence. No product is required to have a hosted application.

- **Unmet gates, precise blockers and resume condition** (`release_goal.unmet_gates`): Define Unmet gates, precise blockers and resume condition.
  Required field content components: release_goal.unmet_gates.detail_1 — Unmet gates; release_goal.unmet_gates.detail_2 — precise blockers; release_goal.unmet_gates.detail_3 — resume condition.
  Applicability: always. Required; apply source qualifiers.

- **Change history** (`release_goal.change_history`): Define Change history.
  Required field content components: release_goal.change_history.detail_1 — Release changes; release_goal.change_history.detail_2 — reasons; release_goal.change_history.detail_3 — revision/time; release_goal.change_history.detail_4 — source/frozen impact.
  Applicability: always. Required; apply source qualifiers.

- **Post-release outcome review and feedback** (`release_goal.post_release_review`): Compare observed release outcomes with targets and update direction.
  Required field content components: release_goal.post_release_review.detail_1 — Frozen release/target revision and exact available deliverable revision; release_goal.post_release_review.detail_2 — Actual measurement owner and agreed observation window; release_goal.post_release_review.detail_3 — Metric definition, baseline, target, denominator/population and data source; release_goal.post_release_review.detail_4 — Observed result with evidence, time/context and uncertainty; release_goal.post_release_review.detail_5 — Target-versus-result comparison, unintended effects and user feedback; release_goal.post_release_review.detail_6 — Continue/change/stop decision and actual authority; release_goal.post_release_review.detail_7 — Strategy/roadmap feedback links, improvement action owners and next review.
  Applicability: always. Required at the selected stage when named by a must-pass gate. Unagreed facts may be identified as pending only where that stage permits them.

- **AI release and monitoring controls** (`release_goal.ai_release_controls`): Apply the pinned AI assurance module at the current stage only where AI is used.
  Required field content components: release_goal.ai_release_controls.detail_1 — AI assurance record ID, version and content hash; AI use scope; release_goal.ai_release_controls.detail_2 — Dataset/slice versions, quality bar, consent/rights and held-out evaluation evidence; release_goal.ai_release_controls.detail_3 — Task-specific metric, threshold, sample size, uncertainty and critical-slice rule; release_goal.ai_release_controls.detail_4 — Safety/refusal/escalation/fallback evaluation and prohibited effects; release_goal.ai_release_controls.detail_5 — Exact model/provider configuration and prompt/retrieval/tool versions as applicable; release_goal.ai_release_controls.detail_6 — Personal-data/jurisdiction legal applicability and actual authority decisions; release_goal.ai_release_controls.detail_7 — Promotion/regression evidence, monitoring/drift threshold and rollback/fallback owner.
  Applicability: conditional. Required when scoped product AI is used or its applicability is unknown for a dependent design/readiness/release decision. Evidence-backed no-product-AI scope may justify exclusion; authoring-tool use must be declared separately.

## Epic field requirements

- **Epic ID/title, owner, state and source work package** (`epic.identity_workpackage`): Define Epic ID/title, owner, state and source work package.
  Required field content components: epic.identity_workpackage.detail_1 — Epic ID/title; epic.identity_workpackage.detail_2 — owner; epic.identity_workpackage.detail_3 — state; epic.identity_workpackage.detail_4 — source work package.
  Applicability: always. Required; apply source qualifiers.

- **Parent strategy/release goals and requirement references** (`epic.alignment_requirements`): Define Parent strategy/release goals and requirement references.
  Required field content components: epic.alignment_requirements.detail_1 — Parent strategy; epic.alignment_requirements.detail_2 — release goals; epic.alignment_requirements.detail_3 — requirement references.
  Applicability: always. Required; apply source qualifiers.

- **User/operational problem** (`epic.problem`): Define User/operational problem.
  Required field content components: epic.problem.detail_1 — User/operational problem.
  Applicability: always. Required; apply source qualifiers.

- **Coherent capability and intended outcome** (`epic.capability_outcome`): Define Coherent capability and intended outcome.
  Required field content components: epic.capability_outcome.detail_1 — Coherent capability; epic.capability_outcome.detail_2 — intended outcome.
  Applicability: always. Required; apply source qualifiers.

- **Included scope** (`epic.included_scope`): Define Included scope.
  Required field content components: epic.included_scope.detail_1 — Included scope.
  Applicability: always. Required; apply source qualifiers.

- **Excluded scope and hand-offs** (`epic.excluded_handoffs`): Define Excluded scope and hand-offs.
  Required field content components: epic.excluded_handoffs.detail_1 — Excluded scope; epic.excluded_handoffs.detail_2 — hand-offs.
  Applicability: always. Required; apply source qualifiers.

- **Shared experience, data, interface and quality contracts or decisions** (`epic.shared_contracts`): Define Shared experience, data, interface and quality contracts or decisions.
  Required field content components: epic.shared_contracts.detail_1 — Shared experience contracts where applicable; epic.shared_contracts.detail_2 — data contracts where applicable; epic.shared_contracts.detail_3 — interface contracts where applicable; epic.shared_contracts.detail_4 — quality attribute contracts where applicable; epic.shared_contracts.detail_5 — decisions.
  Applicability: conditional. Required where children share a contract or decision; each subtype is applicable only when the product profile includes it. Independent children need a justified no-shared-contract finding.

- **Linked functional stories and supporting items** (`epic.children`): Define Linked functional stories and supporting items.
  Required field content components: epic.children.detail_1 — Linked functional stories; epic.children.detail_2 — supporting items.
  Applicability: always. Required; apply source qualifiers.

- **Release allocation of those items** (`epic.release_allocation`): Define Release allocation of those items.
  Required field content components: epic.release_allocation.detail_1 — Release allocation of child items.
  Applicability: always. Required; apply source qualifiers.

- **Each item has one primary epic parent; cross-epic contributors are related links** (`epic.primary_parent`): Define Each item has one primary epic parent; cross-epic contributors are related links.
  Required field content components: epic.primary_parent.detail_1 — One primary epic per item; epic.primary_parent.detail_2 — cross-epic contributors as related links.
  Applicability: always. Required; apply source qualifiers.

- **Design dependencies versus genuine completion prerequisites** (`epic.dependencies`): Define Design dependencies versus genuine completion prerequisites.
  Required field content components: epic.dependencies.detail_1 — Design dependencies; epic.dependencies.detail_2 — genuine completion prerequisites.
  Applicability: always. Required; apply source qualifiers.

- **Risks/open decisions, owners and resume conditions** (`epic.risks_decisions`): Define Risks/open decisions, owners and resume conditions.
  Required field content components: epic.risks_decisions.detail_1 — Risks; epic.risks_decisions.detail_2 — open decisions; epic.risks_decisions.detail_3 — owners; epic.risks_decisions.detail_4 — resume conditions.
  Applicability: always. Required; apply source qualifiers.

- **Epic-level success/completion boundary** (`epic.completion_boundary`): Define Epic-level success/completion boundary.
  Required field content components: epic.completion_boundary.detail_1 — Epic-level success/completion boundary.
  Applicability: always. Required; apply source qualifiers.

- **Child acceptance evidence and uncovered requirements** (`epic.child_evidence_gaps`): Define Child acceptance evidence and uncovered requirements.
  Required field content components: epic.child_evidence_gaps.detail_1 — Child acceptance evidence; epic.child_evidence_gaps.detail_2 — uncovered requirements.
  Applicability: always. Required; apply source qualifiers.

- **Accepted items / in-scope items, with denominator and scope version** (`epic.accepted_rollup`): Define Accepted items / in-scope items, with denominator and scope version.
  Required field content components: epic.accepted_rollup.detail_1 — Accepted item count; epic.accepted_rollup.detail_2 — in-scope denominator; epic.accepted_rollup.detail_3 — scope version.
  Applicability: always. Required; apply source qualifiers.

- **Remaining gaps and change history** (`epic.gaps_history`): Define Remaining gaps and change history.
  Required field content components: epic.gaps_history.detail_1 — Remaining gaps; epic.gaps_history.detail_2 — change history.
  Applicability: always. Required; apply source qualifiers.

- **Riskiest assumption, discovery test and decision** (`epic.assumption_test`): Reduce the main uncertainty before committing a capability.
  Required field content components: epic.assumption_test.detail_1 — Ranked assumptions and why this is the riskiest; epic.assumption_test.detail_2 — Falsifiable hypothesis and counter-hypothesis; epic.assumption_test.detail_3 — Authorized test population/sample and method; epic.assumption_test.detail_4 — Predeclared decision threshold, limitations and stopping conditions; epic.assumption_test.detail_5 — Actual observation/evidence when the test is due; epic.assumption_test.detail_6 — Continue, change, stop or explicitly authorized proceed-under-risk decision; source and follow-up.
  Applicability: always. Required at the selected stage when named by a must-pass gate. Unagreed facts may be identified as pending only where that stage permits them.

- **Priority rationale and trade-offs** (`epic.priority_rationale`): Explain why this item belongs ahead of alternatives.
  Required field content components: epic.priority_rationale.detail_1 — Intended outcome and affected users; epic.priority_rationale.detail_2 — Evidence of value/urgency or risk reduction; epic.priority_rationale.detail_3 — Compared alternatives including defer/do nothing; epic.priority_rationale.detail_4 — Declared scoring or decision method and input sources; no fabricated score; epic.priority_rationale.detail_5 — Dependency/sequence and opportunity-cost rationale; epic.priority_rationale.detail_6 — Actual decision owner, state and revision.
  Applicability: always. Required at the selected stage when named by a must-pass gate. Unagreed facts may be identified as pending only where that stage permits them.

- **Size range, unit and uncertainty** (`epic.size_estimate`): Support sequence and capacity decisions with an honest estimate.
  Required field content components: epic.size_estimate.detail_1 — Range or declared coarse size and unit; epic.size_estimate.detail_2 — Estimation method, assumptions and scope revision; epic.size_estimate.detail_3 — Evidence or actual estimators; pending if not yet agreed; epic.size_estimate.detail_4 — Uncertainty/confidence and main variance drivers; epic.size_estimate.detail_5 — Dependencies, exclusions and resource constraints; epic.size_estimate.detail_6 — Re-estimation trigger and decision impact.
  Applicability: always. Required at the selected stage when named by a must-pass gate. Unagreed facts may be identified as pending only where that stage permits them.

- **Capability outcome learning** (`epic.outcome_learning`): Roll up child outcomes without double-counting delivery.
  Required field content components: epic.outcome_learning.detail_1 — Original capability hypothesis and measures; epic.outcome_learning.detail_2 — Child post-release/acceptance observations and scope denominator; epic.outcome_learning.detail_3 — Actual user/operator outcome evidence; epic.outcome_learning.detail_4 — Gap, unintended consequence and uncertainty analysis; epic.outcome_learning.detail_5 — Decision and strategy/roadmap feedback links.
  Applicability: always. Required at the selected stage when named by a must-pass gate. Unagreed facts may be identified as pending only where that stage permits them.

- **AI discovery and capability validation** (`epic.ai_validation_contract`): Apply the pinned AI assurance module at the current stage only where AI is used.
  Required field content components: epic.ai_validation_contract.detail_1 — AI assurance record ID, version and content hash; AI use scope; epic.ai_validation_contract.detail_2 — Dataset/slice versions, quality bar, consent/rights and held-out evaluation evidence; epic.ai_validation_contract.detail_3 — Task-specific metric, threshold, sample size, uncertainty and critical-slice rule; epic.ai_validation_contract.detail_4 — Safety/refusal/escalation/fallback evaluation and prohibited effects; epic.ai_validation_contract.detail_5 — Exact model/provider configuration and prompt/retrieval/tool versions as applicable; epic.ai_validation_contract.detail_6 — Personal-data/jurisdiction legal applicability and actual authority decisions; epic.ai_validation_contract.detail_7 — Promotion/regression evidence, monitoring/drift threshold and rollback/fallback owner.
  Applicability: conditional. Required when scoped product AI is used or its applicability is unknown for a dependent design/readiness/release decision. Evidence-backed no-product-AI scope may justify exclusion; authoring-tool use must be declared separately.

## User story field requirements

- **Canonical story ID/title, primary epic, release and owner** (`user_story.identity_parent`): Define Canonical story ID/title, primary epic, release and owner.
  Required field content components: user_story.identity_parent.detail_1 — Canonical story ID/title; user_story.identity_parent.detail_2 — primary epic; user_story.identity_parent.detail_3 — release; user_story.identity_parent.detail_4 — owner.
  Applicability: always. Required; apply source qualifiers.

- **Source requirement IDs, original clauses/test cases and decision links** (`user_story.source_clauses`): Define Source requirement IDs, original clauses/test cases and decision links.
  Required field content components: user_story.source_clauses.detail_1 — Source requirement IDs; user_story.source_clauses.detail_2 — original clauses/test cases; user_story.source_clauses.detail_3 — decision links.
  Applicability: always. Required; apply source qualifiers.

- **Specification version and approval/readiness state** (`user_story.specification_state`): Define Specification version and approval/readiness state.
  Required field content components: user_story.specification_state.detail_1 — Specification version; user_story.specification_state.detail_2 — approval/readiness state.
  Applicability: always. Required; apply source qualifiers.

- **Context, trigger and preconditions** (`user_story.context_trigger`): Define Context, trigger and preconditions.
  Required field content components: user_story.context_trigger.detail_1 — Context; user_story.context_trigger.detail_2 — trigger; user_story.context_trigger.detail_3 — preconditions.
  Applicability: always. Required; apply source qualifiers.

- **In scope** (`user_story.in_scope`): Define In scope.
  Required field content components: user_story.in_scope.detail_1 — In-scope behaviour.
  Applicability: always. Required; apply source qualifiers.

- **Out of scope and existing behaviour to preserve** (`user_story.out_of_scope`): Define Out of scope and existing behaviour to preserve.
  Required field content components: user_story.out_of_scope.detail_1 — Out-of-scope behaviour; user_story.out_of_scope.detail_2 — existing behaviour to preserve.
  Applicability: always. Required; apply source qualifiers.

- **Main user journey and observable results** (`user_story.main_journey`): Define Main user journey and observable results.
  Required field content components: user_story.main_journey.detail_1 — Main journey; user_story.main_journey.detail_2 — observable results.
  Applicability: always. Required; apply source qualifiers.

- **Applicable waiting, absence, refusal, failure and recovery behaviour** (`user_story.adverse_behaviour`): Define Applicable waiting, absence, refusal, failure and recovery behaviour.
  Required field content components: user_story.adverse_behaviour.detail_1 — Waiting or loading behaviour where applicable; user_story.adverse_behaviour.detail_2 — empty or unavailable outcome where applicable; user_story.adverse_behaviour.detail_3 — refusal or denied behaviour where applicable; user_story.adverse_behaviour.detail_4 — failure behaviour; user_story.adverse_behaviour.detail_5 — recovery behaviour.
  Applicability: always. Required; apply source qualifiers.

- **Applicable interaction, device and accessibility requirements** (`user_story.interaction_accessibility`): Define Applicable interaction, device and accessibility requirements.
  Required field content components: user_story.interaction_accessibility.detail_1 — Applicable interaction channel or device behaviour; user_story.interaction_accessibility.detail_2 — accessibility behaviour.
  Applicability: conditional. Required for declared interaction, device or accessibility obligations; assess the actual product profile. A nonmobile channel does not waive other applicable accessibility or inclusion requirements.

- **Experience references or explicit interaction or service description** (`user_story.experience_reference`): Define Experience references or explicit interaction or service description.
  Required field content components: user_story.experience_reference.detail_1 — Experience, design or service reference; user_story.experience_reference.detail_2 — or explicit interaction or service description.
  Applicability: always. Required; apply source qualifiers.

- **Inspected existing components, processes and contracts proposed for reuse** (`user_story.inspected_components`): Define Inspected existing components, processes and contracts proposed for reuse.
  Required field content components: user_story.inspected_components.detail_1 — Actually inspected existing components or processes; user_story.inspected_components.detail_2 — verified contracts proposed for reuse.
  Applicability: conditional. Required where reuse, preservation or integration with existing components/processes is claimed or necessary. A genuinely new standalone capability may justify no existing component to reuse.

- **Applicable authoritative identity, authorization scope and accountability path** (`user_story.access_accountability`): Define Applicable authoritative identity, authorization scope and accountability path.
  Required field content components: user_story.access_accountability.detail_1 — Authoritative identity or actor entitlement where applicable; user_story.access_accountability.detail_2 — authorization or allocation scope where applicable; user_story.access_accountability.detail_3 — audit or accountability path where required.
  Applicability: conditional. Required when the journey involves authenticated identity, entitlements, protected assets, controlled actions or mandated accountability. Public or noncontrolled journeys need a factually reviewed boundary assessment, not invented accounts, servers or audit systems.

- **Inputs, operations, output and error contracts, and side effects** (`user_story.operation_contracts`): Define Inputs, operations, output and error contracts, and side effects.
  Required field content components: user_story.operation_contracts.detail_1 — Inputs; user_story.operation_contracts.detail_2 — state changes or reads/writes where applicable; user_story.operation_contracts.detail_3 — output and error contracts; user_story.operation_contracts.detail_4 — side effects.
  Applicability: conditional. Required when the journey transforms input, information, materials or state or has an external effect; digital API/schema details are conditional on actual interfaces. A no-effect observation still needs its observable result and reviewed boundary.

- **Applicable permission or policy checks, refusal behaviour and prohibited effects** (`user_story.permissions_refusal`): Define Applicable permission or policy checks, refusal behaviour and prohibited effects.
  Required field content components: user_story.permissions_refusal.detail_1 — Applicable permission or policy checks; user_story.permissions_refusal.detail_2 — refusal behaviour where applicable; user_story.permissions_refusal.detail_3 — prohibited effects.
  Applicability: conditional. Required for controlled actions, access, safety restrictions or other policy-governed effects; a public uncontrolled action may justify no permission check only with a factual authority/boundary assessment.

- **Applicable retention, disconnected operation and concurrent-use rules** (`user_story.information_continuity_coordination`): Define Applicable retention, disconnected operation and concurrent-use rules.
  Required field content components: user_story.information_continuity_coordination.detail_1 — Existing retention rules where applicable; user_story.information_continuity_coordination.detail_2 — disconnected or offline rules where applicable; user_story.information_continuity_coordination.detail_3 — concurrent-use rules where applicable; user_story.information_continuity_coordination.detail_4 — unresolved decisions.
  Applicability: conditional. Required when retained state, disconnected use, simultaneous operations or authoritative source obligations affect the journey. Unsupported offline/sync capabilities must not be invented; unknown necessary behaviour remains unresolved.

- **Applicable quality attributes, thresholds and measurement conditions** (`user_story.nfr_thresholds`): Define Applicable quality attributes, thresholds and measurement conditions.
  Required field content components: user_story.nfr_thresholds.detail_1 — Applicable authoritative quality attributes; user_story.nfr_thresholds.detail_2 — agreed or source-defined thresholds where meaningful; user_story.nfr_thresholds.detail_3 — measurement or evaluation conditions.
  Applicability: conditional. Required when authoritative or product-risk obligations demand quality attributes beyond the functional result. Each attribute and measurement subtype follows actual scope; a reviewed no-extra-obligation conclusion may justify exclusion.

- **Identified acceptance criteria using template 7** (`user_story.criteria`): Define Identified acceptance criteria using template 7.
  Required field content components: user_story.criteria.detail_1 — Identified acceptance criteria; user_story.criteria.detail_2 — template 7 detail coverage.
  Applicability: always. Required; apply source qualifiers.

- **Positive, refusal, error, authorization and recovery scenarios as applicable** (`user_story.scenario_coverage`): Define Positive, refusal, error, authorization and recovery scenarios as applicable.
  Required field content components: user_story.scenario_coverage.detail_1 — Positive; user_story.scenario_coverage.detail_2 — refusal; user_story.scenario_coverage.detail_3 — error; user_story.scenario_coverage.detail_4 — authorization; user_story.scenario_coverage.detail_5 — recovery scenarios as applicable.
  Applicability: always. Required; apply source qualifiers.

- **Approved test or evaluation context and verification mapping** (`user_story.evaluation_mapping`): Define Approved test or evaluation context and verification mapping.
  Required field content components: user_story.evaluation_mapping.detail_1 — Approved test fixtures, sample or evaluation context; user_story.evaluation_mapping.detail_2 — verification method mapping.
  Applicability: always. Required; apply source qualifiers.

- **Source criteria and proposed supplements distinguished** (`user_story.source_supplement_separation`): Define Source criteria and proposed supplements distinguished.
  Required field content components: user_story.source_supplement_separation.detail_1 — Source criteria; user_story.source_supplement_separation.detail_2 — proposed supplementary criteria.
  Applicability: always. Required; apply source qualifiers.

- **Required predecessor outputs/decisions and Ready conditions** (`user_story.ready_prerequisites`): Define Required predecessor outputs/decisions and Ready conditions.
  Required field content components: user_story.ready_prerequisites.detail_1 — Required predecessor outputs/decisions; user_story.ready_prerequisites.detail_2 — Ready conditions.
  Applicability: always. Required; apply source qualifiers.

- **Linked technical/verification tasks using template 8** (`user_story.task_links`): Define Linked technical/verification tasks using template 8.
  Required field content components: user_story.task_links.detail_1 — Linked technical tasks; user_story.task_links.detail_2 — verification tasks; user_story.task_links.detail_3 — template 8 coverage.
  Applicability: always. Required; apply source qualifiers.

- **Frozen revision and change process when qualified** (`user_story.frozen_change`): Define Frozen revision and change process when qualified.
  Required field content components: user_story.frozen_change.detail_1 — Frozen revision; user_story.frozen_change.detail_2 — change process when qualified.
  Applicability: conditional. Required when story is frozen/qualified or needs a future freeze/change process; drafts may describe planned freeze without claiming it occurred.

- **Definition of Done and required independent review and governance checks** (`user_story.done_reviews`): Define Definition of Done and required independent review and governance checks.
  Required field content components: user_story.done_reviews.detail_1 — Definition of Done; user_story.done_reviews.detail_2 — independent review; user_story.done_reviews.detail_3 — applicable governance checks.
  Applicability: always. Required; apply source qualifiers.

- **Qualified revision, actual evaluation outputs, release transition, observed availability and user verification** (`user_story.delivery_evidence`): Define Qualified revision, actual evaluation outputs, release transition, observed availability and user verification.
  Required field content components: user_story.delivery_evidence.detail_1 — Final qualified deliverable revision; user_story.delivery_evidence.detail_2 — actual evaluation outputs; user_story.delivery_evidence.detail_3 — integration or publication revision where required; user_story.delivery_evidence.detail_4 — observed operationally available revision where required; user_story.delivery_evidence.detail_5 — required user-journey verification.
  Applicability: conditional. Execution details are required only at their declared qualification or delivery stages. Authoring records planned evidence and not-yet-produced results; each subtype follows actual product profile and required future gate.

- **Criteria passed / declared criteria total, identified by criterion IDs and specification version (not task or assertion counts); blockers and exact resume condition** (`user_story.criterion_rollup_blockers`): Define Criteria passed / declared criteria total, identified by criterion IDs and specification version (not task or assertion counts); blockers and exact resume condition.
  Required field content components: user_story.criterion_rollup_blockers.detail_1 — Passed criterion IDs; user_story.criterion_rollup_blockers.detail_2 — declared total; user_story.criterion_rollup_blockers.detail_3 — specification version; user_story.criterion_rollup_blockers.detail_4 — blockers; user_story.criterion_rollup_blockers.detail_5 — resume condition.
  Applicability: always. Required; apply source qualifiers.

- **Change history** (`user_story.change_history`): Define Change history.
  Required field content components: user_story.change_history.detail_1 — Story changes; user_story.change_history.detail_2 — reasons; user_story.change_history.detail_3 — revision/time; user_story.change_history.detail_4 — source/frozen impact.
  Applicability: always. Required; apply source qualifiers.

- **User-need statement** (`user_story.story_statement`): Define User-need statement.
  Required field content components: user_story.story_statement.detail_1 — Specific actor; user_story.story_statement.detail_2 — Concrete action/outcome; user_story.story_statement.detail_3 — User value.
  Applicability: always. Required; apply source qualifiers.

- **Supporting-item and investigation variant** (`user_story.supporting_item_variant`): Define Supporting-item and investigation variant.
  Required field content components: user_story.supporting_item_variant.detail_1 — Actual operator/consumer; user_story.supporting_item_variant.detail_2 — Bounded supporting outcome/value; user_story.supporting_item_variant.detail_3 — Preserved canonical type/acceptance; user_story.supporting_item_variant.detail_4 — For investigation: question/method/evidence-backed decision output.
  Applicability: conditional. Required for canonical supporting/enabler/investigation items; functional stories use the normal actor/outcome/value statement.

- **Priority rationale and trade-offs** (`user_story.priority_rationale`): Explain why this item belongs ahead of alternatives.
  Required field content components: user_story.priority_rationale.detail_1 — Intended outcome and affected users; user_story.priority_rationale.detail_2 — Evidence of value/urgency or risk reduction; user_story.priority_rationale.detail_3 — Compared alternatives including defer/do nothing; user_story.priority_rationale.detail_4 — Declared scoring or decision method and input sources; no fabricated score; user_story.priority_rationale.detail_5 — Dependency/sequence and opportunity-cost rationale; user_story.priority_rationale.detail_6 — Actual decision owner, state and revision.
  Applicability: always. Required at the selected stage when named by a must-pass gate. Unagreed facts may be identified as pending only where that stage permits them.

- **Size range, unit and uncertainty** (`user_story.size_estimate`): Support sequence and capacity decisions with an honest estimate.
  Required field content components: user_story.size_estimate.detail_1 — Range or declared coarse size and unit; user_story.size_estimate.detail_2 — Estimation method, assumptions and scope revision; user_story.size_estimate.detail_3 — Evidence or actual estimators; pending if not yet agreed; user_story.size_estimate.detail_4 — Uncertainty/confidence and main variance drivers; user_story.size_estimate.detail_5 — Dependencies, exclusions and resource constraints; user_story.size_estimate.detail_6 — Re-estimation trigger and decision impact.
  Applicability: always. Required at the selected stage when named by a must-pass gate. Unagreed facts may be identified as pending only where that stage permits them.

- **Canonical team Definition of Ready reference and item additions** (`user_story.team_ready_reference`): Use one team-level readiness policy rather than duplicated checklists.
  Required field content components: user_story.team_ready_reference.detail_1 — Actual team policy ID, version, content hash and canonical source; user_story.team_ready_reference.detail_2 — Applicable Ready check IDs and current satisfaction evidence; user_story.team_ready_reference.detail_3 — Item-specific additions and factual exclusions; user_story.team_ready_reference.detail_4 — Actual required decisions/approvals and separate current states; user_story.team_ready_reference.detail_5 — Unmet prerequisite/blocker, actual owner and precise resume condition.
  Applicability: always. Required at the selected stage when named by a must-pass gate. Unagreed facts may be identified as pending only where that stage permits them.

- **Canonical team Definition of Done reference and item additions** (`user_story.team_done_reference`): Use one team-level completion policy with distinct delivery evidence.
  Required field content components: user_story.team_done_reference.detail_1 — Actual team policy ID, version, content hash and canonical source; user_story.team_done_reference.detail_2 — Applicable Done check IDs and current evidence at final revision; user_story.team_done_reference.detail_3 — Item-specific additions and explicitly justified scope; user_story.team_done_reference.detail_4 — Separate quality, approval, acceptance, release and observed-availability states; user_story.team_done_reference.detail_5 — Outcome-learning hand-off, actual owner and window; user_story.team_done_reference.detail_6 — Unmet gate/blocker and precise resume condition.
  Applicability: always. Required at the selected stage when named by a must-pass gate. Unagreed facts may be identified as pending only where that stage permits them.

- **Story outcome feedback** (`user_story.outcome_learning`): Turn actual user experience into a product decision.
  Required field content components: user_story.outcome_learning.detail_1 — Original user outcome and acceptance revision; user_story.outcome_learning.detail_2 — Observed experience/result after availability; user_story.outcome_learning.detail_3 — Comparable target or qualitative learning question; user_story.outcome_learning.detail_4 — Unexpected effects and feedback evidence; user_story.outcome_learning.detail_5 — Decision, linked epic/strategy/roadmap follow-up and actual owner.
  Applicability: always. Required at the selected stage when named by a must-pass gate. Unagreed facts may be identified as pending only where that stage permits them.

- **AI acceptance and fallback contract** (`user_story.ai_acceptance_contract`): Apply the pinned AI assurance module at the current stage only where AI is used.
  Required field content components: user_story.ai_acceptance_contract.detail_1 — AI assurance record ID, version and content hash; AI use scope; user_story.ai_acceptance_contract.detail_2 — Dataset/slice versions, quality bar, consent/rights and held-out evaluation evidence; user_story.ai_acceptance_contract.detail_3 — Task-specific metric, threshold, sample size, uncertainty and critical-slice rule; user_story.ai_acceptance_contract.detail_4 — Safety/refusal/escalation/fallback evaluation and prohibited effects; user_story.ai_acceptance_contract.detail_5 — Exact model/provider configuration and prompt/retrieval/tool versions as applicable; user_story.ai_acceptance_contract.detail_6 — Personal-data/jurisdiction legal applicability and actual authority decisions; user_story.ai_acceptance_contract.detail_7 — Promotion/regression evidence, monitoring/drift threshold and rollback/fallback owner.
  Applicability: conditional. Required when scoped product AI is used or its applicability is unknown for a dependent design/readiness/release decision. Evidence-backed no-product-AI scope may justify exclusion; authoring-tool use must be declared separately.

## Acceptance criterion field requirements

- **Criterion ID and owning item** (`acceptance_criterion.identity_owner`): Define Criterion ID and owning item.
  Required field content components: acceptance_criterion.identity_owner.detail_1 — Stable criterion ID; acceptance_criterion.identity_owner.detail_2 — owning canonical story/supporting item.
  Applicability: always. Required; apply source qualifiers.

- **Source reference/provenance** (`acceptance_criterion.source_provenance`): Define Source reference/provenance.
  Required field content components: acceptance_criterion.source_provenance.detail_1 — Original source clause reference; acceptance_criterion.source_provenance.detail_2 — or proposed supplementary criterion.
  Applicability: always. Required; apply source qualifiers.

- **Approval/specification state** (`acceptance_criterion.approval_state`): Define Approval/specification state.
  Required field content components: acceptance_criterion.approval_state.detail_1 — Draft/approved/frozen revision; acceptance_criterion.approval_state.detail_2 — authority; acceptance_criterion.approval_state.detail_3 — decision evidence.
  Applicability: always. Required; apply source qualifiers.

- **Scenario kind** (`acceptance_criterion.scenario_kind`): Define Scenario kind.
  Required field content components: acceptance_criterion.scenario_kind.detail_1 — Positive/refusal/error/authorization/recovery/applicable NFR kind.
  Applicability: always. Required; apply source qualifiers.

- **Given** (`acceptance_criterion.given`): Define Given.
  Required field content components: acceptance_criterion.given.detail_1 — Actor; acceptance_criterion.given.detail_2 — identity or entitlement where applicable; acceptance_criterion.given.detail_3 — initial product, process, information or material state; acceptance_criterion.given.detail_4 — preconditions.
  Applicability: always. Required; apply source qualifiers.

- **When** (`acceptance_criterion.when`): Define When.
  Required field content components: acceptance_criterion.when.detail_1 — Concrete action; acceptance_criterion.when.detail_2 — or event.
  Applicability: always. Required; apply source qualifiers.

- **Then** (`acceptance_criterion.then`): Define Then.
  Required field content components: acceptance_criterion.then.detail_1 — Observable result; acceptance_criterion.then.detail_2 — relevant product, process, asset or information state the actor observes.
  Applicability: always. Required; apply source qualifiers.

- **Prohibited effects** (`acceptance_criterion.prohibited_effects`): Define Prohibited effects.
  Required field content components: acceptance_criterion.prohibited_effects.detail_1 — Prohibited writes; acceptance_criterion.prohibited_effects.detail_2 — disclosures; acceptance_criterion.prohibited_effects.detail_3 — other effects.
  Applicability: conditional. Required where an action could cause unintended access, disclosure or side effects; no-effect cases need an explicit boundary assessment.

- **Measurement conditions** (`acceptance_criterion.measurement`): Define Measurement conditions.
  Required field content components: acceptance_criterion.measurement.detail_1 — Source threshold; acceptance_criterion.measurement.detail_2 — timing; acceptance_criterion.measurement.detail_3 — profile; acceptance_criterion.measurement.detail_4 — device; acceptance_criterion.measurement.detail_5 — environment as applicable.
  Applicability: conditional. Required for quantitative, timing, device or NFR conditions; qualitative outcomes use observable rubrics rather than invented numerical targets.

- **Approved evaluation context and verification method identifier** (`acceptance_criterion.evaluation_method`): Define Approved evaluation context and verification method identifier.
  Required field content components: acceptance_criterion.evaluation_method.detail_1 — Approved test fixture, sample, simulation or participant context; acceptance_criterion.evaluation_method.detail_2 — verification method; acceptance_criterion.evaluation_method.detail_3 — test or evaluation identifier.
  Applicability: always. Required; apply source qualifiers.

- **Expected evidence** (`acceptance_criterion.expected_evidence`): Define Expected evidence.
  Required field content components: acceptance_criterion.expected_evidence.detail_1 — Expected evidence artifact/observation.
  Applicability: always. Required; apply source qualifiers.

- **Actual execution** (`acceptance_criterion.actual_execution`): Define Actual execution.
  Required field content components: acceptance_criterion.actual_execution.detail_1 — Not run/passed/failed/blocked/skipped; acceptance_criterion.actual_execution.detail_2 — reason where needed.
  Applicability: always. Required; apply source qualifiers.

- **Observed evidence** (`acceptance_criterion.observed_evidence`): Define Observed evidence.
  Required field content components: acceptance_criterion.observed_evidence.detail_1 — Original output or observation link; acceptance_criterion.observed_evidence.detail_2 — final artifact or procedure revision; acceptance_criterion.observed_evidence.detail_3 — environment or evaluation context; acceptance_criterion.observed_evidence.detail_4 — observation time.
  Applicability: conditional. Required when executed/observed result is claimed; not-run explicitly records no evidence yet and planned evidence requirement.

- **Unresolved gap or blocker and resume condition** (`acceptance_criterion.gap_resume`): Define Unresolved gap or blocker and resume condition.
  Required field content components: acceptance_criterion.gap_resume.detail_1 — Unresolved gap/blocker; acceptance_criterion.gap_resume.detail_2 — resume condition.
  Applicability: conditional. Required while an unresolved gap exists; clean state records a reviewed no-open-gap finding rather than inventing blockers.

- **AI dataset, metric and threshold measurement** (`acceptance_criterion.ai_evaluation_measurement`): Apply the pinned AI assurance module at the current stage only where AI is used.
  Required field content components: acceptance_criterion.ai_evaluation_measurement.detail_1 — AI assurance record ID, version and content hash; AI use scope; acceptance_criterion.ai_evaluation_measurement.detail_2 — Dataset/slice versions, quality bar, consent/rights and held-out evaluation evidence; acceptance_criterion.ai_evaluation_measurement.detail_3 — Task-specific metric, threshold, sample size, uncertainty and critical-slice rule; acceptance_criterion.ai_evaluation_measurement.detail_4 — Safety/refusal/escalation/fallback evaluation and prohibited effects; acceptance_criterion.ai_evaluation_measurement.detail_5 — Exact model/provider configuration and prompt/retrieval/tool versions as applicable; acceptance_criterion.ai_evaluation_measurement.detail_6 — Personal-data/jurisdiction legal applicability and actual authority decisions; acceptance_criterion.ai_evaluation_measurement.detail_7 — Promotion/regression evidence, monitoring/drift threshold and rollback/fallback owner.
  Applicability: conditional. Required when scoped product AI is used or its applicability is unknown for a dependent design/readiness/release decision. Evidence-backed no-product-AI scope may justify exclusion; authoring-tool use must be declared separately.

## Implementation or verification task field requirements

- **Task ID/title, task type, actual assignee/owner, state** (`technical_task.identity_type`): Define Task ID/title, task type, actual assignee/owner, state.
  Required field content components: technical_task.identity_type.detail_1 — Task ID/title; technical_task.identity_type.detail_2 — task type; technical_task.identity_type.detail_3 — actual assignee/owner; technical_task.identity_type.detail_4 — state.
  Applicability: always. Required; apply source qualifiers.

- **Primary parent** (`technical_task.parent_owner`): Define Primary parent.
  Required field content components: technical_task.parent_owner.detail_1 — Primary parent story/supporting item or existing task; technical_task.parent_owner.detail_2 — canonical owning item link when nested.
  Applicability: always. Required; apply source qualifiers.

- **Source requirement and acceptance-criterion IDs** (`technical_task.source_criteria`): Define Source requirement and acceptance-criterion IDs.
  Required field content components: technical_task.source_criteria.detail_1 — Source requirement IDs; technical_task.source_criteria.detail_2 — acceptance-criterion IDs.
  Applicability: always. Required; apply source qualifiers.

- **Bounded technical or verification result and why it is needed** (`technical_task.bounded_result`): Define Bounded technical or verification result and why it is needed.
  Required field content components: technical_task.bounded_result.detail_1 — Bounded technical/verification result; technical_task.bounded_result.detail_2 — why needed.
  Applicability: always. Required; apply source qualifiers.

- **Relevant components or processes, exact contracts and specification revision** (`technical_task.components_contracts`): Define Relevant components or processes, exact contracts and specification revision.
  Required field content components: technical_task.components_contracts.detail_1 — Relevant components or processes; technical_task.components_contracts.detail_2 — exact contracts; technical_task.components_contracts.detail_3 — source/specification revision.
  Applicability: always. Required; apply source qualifiers.

- **Required data/fixtures, approved environment and access** (`technical_task.data_environment_access`): Define Required data/fixtures, approved environment and access.
  Required field content components: technical_task.data_environment_access.detail_1 — Required data/fixtures; technical_task.data_environment_access.detail_2 — approved environment; technical_task.data_environment_access.detail_3 — access.
  Applicability: always. Required; apply source qualifiers.

- **Concrete predecessor output/decision links** (`technical_task.predecessors`): Define Concrete predecessor output/decision links.
  Required field content components: technical_task.predecessors.detail_1 — Concrete predecessor output links; technical_task.predecessors.detail_2 — decision links.
  Applicability: always. Required; apply source qualifiers.

- **Native completion blockers only where an output is genuinely required** (`technical_task.native_blockers`): Define Native completion blockers only where an output is genuinely required.
  Required field content components: technical_task.native_blockers.detail_1 — Native completion blockers where genuinely required.
  Applicability: conditional. Required where concrete completion prerequisites exist; a reviewed no-prerequisite finding allows no blocker edges.

- **Components, artifacts, procedures or interfaces affected** (`technical_task.affected_components`): Define Components, artifacts, procedures or interfaces affected.
  Required field content components: technical_task.affected_components.detail_1 — Affected components or operating processes; technical_task.affected_components.detail_2 — artifacts or procedures; technical_task.affected_components.detail_3 — interfaces.
  Applicability: always. Required; apply source qualifiers.

- **Work steps sufficient for execution** (`technical_task.work_steps`): Define Work steps sufficient for execution.
  Required field content components: technical_task.work_steps.detail_1 — Executable work steps.
  Applicability: always. Required; apply source qualifiers.

- **Applicable experience, information, interface, authorization and quality impacts** (`technical_task.impacts`): Define Applicable experience, information, interface, authorization and quality impacts.
  Required field content components: technical_task.impacts.detail_1 — Experience impacts where applicable; technical_task.impacts.detail_2 — information or material state impacts where applicable; technical_task.impacts.detail_3 — interface or contract impacts where applicable; technical_task.impacts.detail_4 — authorization or policy impacts where applicable; technical_task.impacts.detail_5 — quality attribute impacts where applicable.
  Applicability: always. Required; apply source qualifiers.

- **Out of scope and behaviours to preserve** (`technical_task.exclusions_preservation`): Define Out of scope and behaviours to preserve.
  Required field content components: technical_task.exclusions_preservation.detail_1 — Out-of-scope work; technical_task.exclusions_preservation.detail_2 — behaviour to preserve.
  Applicability: always. Required; apply source qualifiers.

- **For a spike** (`technical_task.spike_plan`): Define For a spike.
  Required field content components: technical_task.spike_plan.detail_1 — Research question; technical_task.spike_plan.detail_2 — method; technical_task.spike_plan.detail_3 — bounded effort if agreed; technical_task.spike_plan.detail_4 — decision evidence.
  Applicability: conditional. Required for spike/investigation tasks; implementation-only tasks require a reasoned not-a-spike finding.

- **Reviewable deliverables** (`technical_task.deliverables`): Define Reviewable deliverables.
  Required field content components: technical_task.deliverables.detail_1 — Reviewable deliverables.
  Applicability: always. Required; apply source qualifiers.

- **Verification cases and expected results mapped to parent criteria** (`technical_task.verification_cases`): Define Verification cases and expected results mapped to parent criteria.
  Required field content components: technical_task.verification_cases.detail_1 — Verification cases; technical_task.verification_cases.detail_2 — expected results; technical_task.verification_cases.detail_3 — parent-criterion mapping.
  Applicability: always. Required; apply source qualifiers.

- **Required qualification checks and independent review** (`technical_task.qualification_review`): Define Required qualification checks and independent review.
  Required field content components: technical_task.qualification_review.detail_1 — Required qualification checks, evaluations or builds/tests/CI where applicable; technical_task.qualification_review.detail_2 — independent review.
  Applicability: conditional. Required when declared qualification requires checks and review; specific builds/CI or other evaluation methods follow product type and actual scope. No fabricated software evidence is needed for nonsoftware work.

- **Definition of Done** (`technical_task.done`): Define Definition of Done.
  Required field content components: technical_task.done.detail_1 — Definition of Done.
  Applicability: always. Required; apply source qualifiers.

- **Actual output evidence, final revision, review reference and evaluation results** (`technical_task.actual_outputs`): Define Actual output evidence, final revision, review reference and evaluation results.
  Required field content components: technical_task.actual_outputs.detail_1 — Actual output/evidence links; technical_task.actual_outputs.detail_2 — final deliverable revision and review/change reference where applicable; technical_task.actual_outputs.detail_3 — executed evaluation results.
  Applicability: conditional. Required when output or completion is claimed; before execution distinguish planned output from not-yet-produced evidence and state the appropriate future evidence contract.

- **Integration, availability and operational-verification evidence within task scope** (`technical_task.release_verification`): Define Integration, availability and operational-verification evidence within task scope.
  Required field content components: technical_task.release_verification.detail_1 — Integration or publication evidence where required; technical_task.release_verification.detail_2 — observed availability evidence where required; technical_task.release_verification.detail_3 — operational or user-verification evidence where required.
  Applicability: conditional. Required only when these stages are part of the task's declared scope; not owning a stage does not waive the parent release's required gate. The product profile defines applicable stage types.

- **Blocker, owner and exact resume condition** (`technical_task.blocker_owner_resume`): Define Blocker, owner and exact resume condition.
  Required field content components: technical_task.blocker_owner_resume.detail_1 — Blocker; technical_task.blocker_owner_resume.detail_2 — owner; technical_task.blocker_owner_resume.detail_3 — exact resume condition.
  Applicability: always. Required; apply source qualifiers.

- **Remaining work and change history** (`technical_task.remaining_history`): Define Remaining work and change history.
  Required field content components: technical_task.remaining_history.detail_1 — Remaining work; technical_task.remaining_history.detail_2 — change history.
  Applicability: always. Required; apply source qualifiers.

- **Canonical team Definition of Ready reference and item additions** (`technical_task.team_ready_reference`): Use one team-level readiness policy rather than duplicated checklists.
  Required field content components: technical_task.team_ready_reference.detail_1 — Actual team policy ID, version, content hash and canonical source; technical_task.team_ready_reference.detail_2 — Applicable Ready check IDs and current satisfaction evidence; technical_task.team_ready_reference.detail_3 — Item-specific additions and factual exclusions; technical_task.team_ready_reference.detail_4 — Actual required decisions/approvals and separate current states; technical_task.team_ready_reference.detail_5 — Unmet prerequisite/blocker, actual owner and precise resume condition.
  Applicability: always. Required at the selected stage when named by a must-pass gate. Unagreed facts may be identified as pending only where that stage permits them.

- **Canonical team Definition of Done reference and item additions** (`technical_task.team_done_reference`): Use one team-level completion policy with distinct delivery evidence.
  Required field content components: technical_task.team_done_reference.detail_1 — Actual team policy ID, version, content hash and canonical source; technical_task.team_done_reference.detail_2 — Applicable Done check IDs and current evidence at final revision; technical_task.team_done_reference.detail_3 — Item-specific additions and explicitly justified scope; technical_task.team_done_reference.detail_4 — Separate quality, approval, acceptance, release and observed-availability states; technical_task.team_done_reference.detail_5 — Outcome-learning hand-off, actual owner and window; technical_task.team_done_reference.detail_6 — Unmet gate/blocker and precise resume condition.
  Applicability: always. Required at the selected stage when named by a must-pass gate. Unagreed facts may be identified as pending only where that stage permits them.

- **AI artifact, evaluation and version evidence** (`technical_task.ai_artifact_evidence`): Apply the pinned AI assurance module at the current stage only where AI is used.
  Required field content components: technical_task.ai_artifact_evidence.detail_1 — AI assurance record ID, version and content hash; AI use scope; technical_task.ai_artifact_evidence.detail_2 — Dataset/slice versions, quality bar, consent/rights and held-out evaluation evidence; technical_task.ai_artifact_evidence.detail_3 — Task-specific metric, threshold, sample size, uncertainty and critical-slice rule; technical_task.ai_artifact_evidence.detail_4 — Safety/refusal/escalation/fallback evaluation and prohibited effects; technical_task.ai_artifact_evidence.detail_5 — Exact model/provider configuration and prompt/retrieval/tool versions as applicable; technical_task.ai_artifact_evidence.detail_6 — Personal-data/jurisdiction legal applicability and actual authority decisions; technical_task.ai_artifact_evidence.detail_7 — Promotion/regression evidence, monitoring/drift threshold and rollback/fallback owner.
  Applicability: conditional. Required when scoped product AI is used or its applicability is unknown for a dependent design/readiness/release decision. Evidence-backed no-product-AI scope may justify exclusion; authoring-tool use must be declared separately.

## Mandatory stage gates

## Discovery stage

Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.

### Product vision

- **gate.vision.discovery.01 — Outcome and traceability**: The direction names actual users/operators, their problem and a durable outcome; parent/source links resolve to current authoritative evidence rather than a feature inventory. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.identity, common.traceability, vision.primary_users_context, vision.problem_evidence, vision.vision_statement.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.discovery.02 — Scope and context**: Operating context, affected people, non-goals and decision principles distinguish in-scope outcomes from exclusions without waiving protected requirements. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.boundary, vision.primary_users_context, vision.non_goals.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.discovery.03 — Discovery and evidence**: Claims and assumptions are distinguished; relevant research has population, method, source and limitations, and the most important remaining uncertainty has a falsifiable research/decision plan. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.evidence, common.source_provenance, vision.problem_evidence, vision.assumptions_research.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.discovery.04 — Measures and verification**: Success signals describe observable user/organization outcomes; each relevant measure has definition, population, method and review horizon, with agreed targets or explicit pending decision. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: vision.success_signals.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.discovery.05 — Priority, size and dependencies**: The chosen direction explains value and major alternatives/trade-offs and connects to strategy; resource or timing commitments are sourced, and pending feasibility decisions remain visible. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: vision.value.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.discovery.06 — Applicable assurance and controls**: The actual profile identifies AI, affected rights, safety, security, access, privacy and accessibility applicability; scope/principles protect these obligations and prohibited effects. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, vision.principles.
  Conditional fields: {"ai": ["common.ai_assurance_reference"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.discovery.07 — Governance and learning**: Actual product ownership/review authority, version and state are distinct from approval and delivery; review triggers connect observed learning to a decision and canonical strategy/roadmap updates. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.state, common.change_history, vision.state_review, vision.review_strategy.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Product strategy

- **gate.strategy.discovery.01 — Outcome and traceability**: Each strategic choice resolves to the vision and an evidenced priority problem/user outcome; sources distinguish established facts from proposed bets. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.identity, common.traceability, strategy.vision_sources, strategy.priority_problems.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.discovery.02 — Scope and context**: Priority users/use cases, constraints, exclusions and reuse decisions bound the strategy and identify affected operators and prohibited scope expansion. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.boundary, strategy.constraints, strategy.deferral.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.discovery.03 — Discovery and evidence**: Diagnosis and major bets have cited evidence, counterevidence and limitations; the validation plan can disprove the riskiest choice and has a predeclared continue/change/stop rule. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.evidence, common.source_provenance, strategy.diagnosis_evidence, strategy.validation_plan.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.discovery.04 — Measures and verification**: Outcome measures, baseline and agreed targets define population, method and horizon; pending target decisions are explicit before the stage that depends on them. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: strategy.outcome_measures.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.discovery.05 — Priority, size and dependencies**: Choice and sequencing rationale compare meaningful alternatives and opportunity cost; dependencies, capacity/resource assumptions and uncertainty support any actual commitment. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: strategy.choices_tradeoffs, strategy.dependencies_assumptions.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.discovery.06 — Applicable assurance and controls**: Applicable assurance obligations, including product AI and personal-data jurisdiction, constrain strategic choices; unsafe or unauthorized benefits cannot justify bypassing required controls. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, strategy.constraints.
  Conditional fields: {"ai": ["common.ai_assurance_reference"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.discovery.07 — Governance and learning**: Actual decision authority and change state are explicit; observed discovery/release learning drives a recorded continue/change/stop decision and strategy/roadmap feedback, with actual follow-up owner. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.state, common.change_history, strategy.identity_state, strategy.open_decisions.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Roadmap

- **gate.roadmap.discovery.01 — Outcome and traceability**: Canonical roadmap outcomes and items resolve to current strategy and release goals; no duplicate backlog competes with the owning records. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.identity, common.traceability, roadmap.alignment_links, roadmap.sequence_outcome.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.discovery.02 — Scope and context**: Now/Next/Later and release allocation bound a versioned scope; deferrals, shared contributors and confidence distinguish intended direction from agreed commitments. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.boundary, roadmap.now, roadmap.later.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.discovery.03 — Discovery and evidence**: Evidence gates for horizon movement reference the highest-risk assumptions and actual discovery outputs; an untested hypothesis is not presented as an established predecessor result. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.evidence, common.source_provenance, roadmap.horizon_gate_evidence.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.discovery.04 — Measures and verification**: Each allocated outcome has a linked release measure and review window or explicit pending decision; progress denominators and evidence describe outcomes without counting duplicate items. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: roadmap.sequence_outcome.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.discovery.05 — Priority, size and dependencies**: Sequence rationale reflects child priority/size ranges, genuine predecessor outputs and capacity uncertainty; estimates/timing are sourced and confidence is explicit, not invented. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: roadmap.sequence_rationale, roadmap.capacity_uncertainty.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.discovery.06 — Applicable assurance and controls**: Assurance, approval and access prerequisites appear as actual dependency/decision gates, including AI evaluation/privacy/fallback where applicable; a horizon label never waives a safety obligation. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, roadmap.sequence_gate.
  Conditional fields: {"ai": ["common.ai_assurance_reference"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.discovery.07 — Governance and learning**: Actual roadmap authority, blockers and precise resume conditions are current; measured learning changes priority/allocation or records a no-change rationale with a next decision and owner. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.state, common.change_history, roadmap.identity_state, roadmap.blockers_decisions.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Release goal

- **gate.release_goal.discovery.01 — Outcome and traceability**: The release identifies actual users and an end-to-end usable outcome traceable to strategy/roadmap; included canonical items collectively deliver that outcome. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.identity, common.traceability, release_goal.alignment_sources, release_goal.usable_outcome.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.discovery.02 — Scope and context**: In-scope and deferred items, operating context and preserved behaviour form a single versioned release boundary; dependencies and readiness assumptions are explicit. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.boundary, release_goal.users_journey, release_goal.excluded_deferred.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.discovery.03 — Discovery and evidence**: Value/readiness claims cite actual predecessor/discovery evidence with limitations; unresolved assumptions are tracked to an actual decision and exact resume condition. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.evidence, common.source_provenance, release_goal.dependencies_decisions.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.discovery.04 — Measures and verification**: Outcome targets, baseline/population/method and acceptance evidence are predeclared; entry and exit requirements are testable and do not conflate tests, acceptance, release and availability. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: release_goal.measures_targets.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.discovery.05 — Priority, size and dependencies**: Scope and sequence fit sourced epic/story priority and size/capacity assumptions; release dependencies, resource constraints and uncertain timing are explicit before any commitment. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: release_goal.dependencies_decisions.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.discovery.06 — Applicable assurance and controls**: Actual product/privacy/security/domain approval route, NFRs, recovery and applicable AI controls are specified; required dataset rights, measured thresholds, safety/fallback and monitoring gates cannot be sampled away. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, release_goal.requirements_nfrs.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "release_goal.ai_release_controls"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.discovery.07 — Governance and learning**: The release retains separate quality, approval, readiness, acceptance, authorized publication and observed-availability evidence; actual outcome review ownership/window and strategy/roadmap feedback survive go-live. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.state, common.change_history, release_goal.identity_milestone, release_goal.unmet_gates.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Epic

- **gate.epic.discovery.01 — Outcome and traceability**: One coherent capability addresses an evidenced user/operator problem and traces to current strategy/release requirements; its scope is not a collection of unrelated tasks. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.identity, common.traceability, epic.alignment_requirements, epic.problem, epic.capability_outcome.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.discovery.02 — Scope and context**: Included/excluded scope and hand-offs are explicit; canonical children have one primary parent and cross-epic contributions use related links rather than duplicate acceptance counts. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.boundary, epic.included_scope, epic.excluded_handoffs.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.discovery.03 — Discovery and evidence**: The riskiest assumption is ranked by consequence/uncertainty and has a falsifiable test, authorized method/sample, predeclared decision threshold, observed result when due and documented continue/change/stop or bounded authorized risk decision. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.evidence, common.source_provenance, epic.assumption_test.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.discovery.04 — Measures and verification**: The capability completion/outcome boundary has observable measures and child acceptance mapping; uncovered source requirements, unsuccessful children and scope denominators remain visible. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: epic.completion_boundary.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.discovery.05 — Priority, size and dependencies**: Priority compares meaningful alternatives and opportunity cost; size is a sourced range/coarse unit with scope, method, uncertainty and dependencies, and true prerequisites are separated from design relationships. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: epic.priority_rationale, epic.size_estimate.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.discovery.06 — Applicable assurance and controls**: Shared experience/information/interface/quality contracts carry actual applicable access, safety, privacy, accessibility and AI requirements into children; no critical obligation falls between epics or into advisory-only samples. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, epic.risks_decisions.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "epic.ai_validation_contract"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.discovery.07 — Governance and learning**: Actual epic owner/authority, revision, readiness/completion and gaps are distinct; accepted children alone do not prove capability value, and outcome learning feeds strategy/roadmap with an actual owner and next review. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.state, common.change_history, epic.identity_workpackage, epic.gaps_history.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### User story

- **gate.user_story.discovery.01 — Outcome and traceability**: One bounded user/operator need and observable outcome resolves to its canonical epic/release and original source clauses; supporting/investigation items use their explicit variant rather than invented end-user value. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.identity, common.traceability, user_story.identity_parent, user_story.story_statement, user_story.source_clauses.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.discovery.02 — Scope and context**: Trigger/preconditions, main journey, in/out of scope, preserved behaviour and affected users/operators are explicit; the experience can be understood without guessing. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.boundary, user_story.context_trigger, user_story.in_scope, user_story.out_of_scope.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.discovery.03 — Discovery and evidence**: Evidence and inspected reuse sources support the need/design; unresolved assumptions/decisions retain exact source, actual owner and resume condition, and source criteria are distinguished from proposed supplements. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.evidence, common.source_provenance, user_story.source_supplement_separation.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.discovery.04 — Measures and verification**: Identified criteria define observable positive/adverse/refusal/failure/authorization/recovery outcomes as applicable; every criterion maps to an approved evaluation context and expected evidence, with measurable thresholds where required. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: user_story.main_journey.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.discovery.05 — Priority, size and dependencies**: Priority follows sourced outcome, urgency/risk and alternatives; size is an attributable range/coarse unit with method, uncertainty, scope and dependencies, supporting a feasible bounded item. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: user_story.priority_rationale, user_story.size_estimate.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.discovery.06 — Applicable assurance and controls**: Actual operation contracts and side effects, access/accountability, refusal, information continuity, accessibility and NFRs cover applicable risks; AI acceptance metrics/slices, safety/fallback, rights/versioning and monitoring use the pinned module. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, user_story.permissions_refusal, user_story.interaction_accessibility.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "user_story.ai_acceptance_contract"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.discovery.07 — Governance and learning**: Canonical team Ready/Done versions and item-specific additions are linked; quality, specification approval, execution readiness, criterion acceptance and delivery are distinct, with final revision and outcome-learning hand-off current. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.state, common.change_history, user_story.specification_state, user_story.ready_prerequisites.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Acceptance criterion

- **gate.acceptance_criterion.discovery.01 — Outcome and traceability**: Criterion ID and owning item resolve to exact source provenance/current specification; a proposed supplement is distinguished from a protected original requirement. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.identity, common.traceability, acceptance_criterion.identity_owner, acceptance_criterion.source_provenance.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.discovery.02 — Scope and context**: Given/When/Then identify one scenario, trigger, expected observable result and applicable prohibited effects without implementation guesses or hidden side effects. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.boundary, acceptance_criterion.scenario_kind, acceptance_criterion.given, acceptance_criterion.when, acceptance_criterion.then.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.discovery.03 — Discovery and evidence**: The intended scenario and evaluation design use relevant source/risk evidence and an authorized reproducible context; missing facts or unavailable test inputs remain unresolved rather than guessed. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.evidence, common.source_provenance, acceptance_criterion.source_provenance.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.discovery.04 — Measures and verification**: Measurement defines method, units, threshold, sample/population and uncertainty where relevant; expected evidence can distinguish pass/fail, and AI metrics use fixed dataset/slice/model/prompt revisions. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: acceptance_criterion.expected_evidence.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.discovery.05 — Priority, size and dependencies**: The criterion maps to the owning item priority/risk and feasible verification method; any fixture/sample or predecessor constraint is explicit, and one result is not double-counted across competing criterion IDs. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: acceptance_criterion.evaluation_method.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.discovery.06 — Applicable assurance and controls**: The criterion covers its applicable safety/privacy/access/authorization/fallback obligation and prohibited effects; actual AI accuracy and critical-slice/safety thresholds are independently required when this criterion claims AI behaviour. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, acceptance_criterion.prohibited_effects.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "acceptance_criterion.ai_evaluation_measurement"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.discovery.07 — Governance and learning**: Specification approval, not-run/planned execution, observed result and accepted state remain separate; evidence is bound to the current criterion/revision and a failed/skipped/blocked result has a precise follow-up. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.state, common.change_history, acceptance_criterion.approval_state, acceptance_criterion.gap_resume.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Implementation or verification task

- **gate.technical_task.discovery.01 — Outcome and traceability**: One bounded implementation/design/operational/manufacturing/verification result has a canonical parent and exact source/criterion links; completing it must contribute to the parent outcome. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.identity, common.traceability, technical_task.parent_owner, technical_task.bounded_result.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.discovery.02 — Scope and context**: Affected components/processes and exact contracts/specification revision, exclusions and preserved behaviour bound the change; work steps and deliverables are reviewable in the actual product process. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.boundary, technical_task.components_contracts, technical_task.exclusions_preservation.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.discovery.03 — Discovery and evidence**: Work/reuse/spike claims cite inspected sources and falsifiable investigation where relevant; required evaluation inputs/access and unresolved decisions remain explicit without fabricated facts. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.evidence, common.source_provenance, technical_task.data_environment_access.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.discovery.04 — Measures and verification**: Verification cases and expected outputs map to parent acceptance criteria and actual product qualification method; no mirror-only demonstration substitutes for the declared user/operating requirement. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: technical_task.verification_cases.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.discovery.05 — Priority, size and dependencies**: Sequence relies on actual predecessor outputs and native completion blockers; parent priority/size and task effort/resource uncertainty support a feasible scope without invented commitments. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: technical_task.predecessors.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.discovery.06 — Applicable assurance and controls**: Impacts cover applicable experience, information, interface, access, safety and quality; evaluation access is authorized and AI artifact/held-out/safety/version/promotion evidence meets the pinned module when applicable. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, technical_task.impacts.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "technical_task.ai_artifact_evidence"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.discovery.07 — Governance and learning**: Actual task owner/state and canonical team Ready/Done versions are current; task completion, parent acceptance and release/availability remain distinct, and actual outputs plus learning/follow-up are handed to the owning story/release. Discovery stage: qualify the problem, highest-risk assumption, evidence and next decision. Clearly label proposed metrics/estimates/controls as hypotheses and identify unresolved decisions; do not require future build, release or measured launch results. If a present discovery test is required by source or a commitment depends on it, inspect its actual evidence or keep that decision blocked.
  Current-stage required fields: common.state, common.change_history, technical_task.identity_type, technical_task.blocker_owner_resume.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

## Planning stage

Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.

### Product vision

- **gate.vision.planning.01 — Outcome and traceability**: The direction names actual users/operators, their problem and a durable outcome; parent/source links resolve to current authoritative evidence rather than a feature inventory. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.identity, common.traceability, vision.primary_users_context, vision.problem_evidence, vision.vision_statement.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.planning.02 — Scope and context**: Operating context, affected people, non-goals and decision principles distinguish in-scope outcomes from exclusions without waiving protected requirements. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.boundary, vision.primary_users_context, vision.principles, vision.non_goals.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.planning.03 — Discovery and evidence**: Claims and assumptions are distinguished; relevant research has population, method, source and limitations, and the most important remaining uncertainty has a falsifiable research/decision plan. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.evidence, common.source_provenance, vision.research_sources, vision.problem_evidence, vision.assumptions_research.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.planning.04 — Measures and verification**: Success signals describe observable user/organization outcomes; each relevant measure has definition, population, method and review horizon, with agreed targets or explicit pending decision. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: vision.success_signals, vision.signal_measurement.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.planning.05 — Priority, size and dependencies**: The chosen direction explains value and major alternatives/trade-offs and connects to strategy; resource or timing commitments are sourced, and pending feasibility decisions remain visible. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: vision.value, vision.review_strategy.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.planning.06 — Applicable assurance and controls**: The actual profile identifies AI, affected rights, safety, security, access, privacy and accessibility applicability; scope/principles protect these obligations and prohibited effects. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, vision.principles, vision.non_goals.
  Conditional fields: {"ai": ["common.ai_assurance_reference"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.planning.07 — Governance and learning**: Actual product ownership/review authority, version and state are distinct from approval and delivery; review triggers connect observed learning to a decision and canonical strategy/roadmap updates. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.state, common.change_history, vision.owner_authority, vision.state_review, vision.review_strategy.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Product strategy

- **gate.strategy.planning.01 — Outcome and traceability**: Each strategic choice resolves to the vision and an evidenced priority problem/user outcome; sources distinguish established facts from proposed bets. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.identity, common.traceability, strategy.vision_sources, strategy.priority_problems, strategy.choices_tradeoffs.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.planning.02 — Scope and context**: Priority users/use cases, constraints, exclusions and reuse decisions bound the strategy and identify affected operators and prohibited scope expansion. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.boundary, strategy.priority_users_use_cases, strategy.constraints, strategy.deferral.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.planning.03 — Discovery and evidence**: Diagnosis and major bets have cited evidence, counterevidence and limitations; the validation plan can disprove the riskiest choice and has a predeclared continue/change/stop rule. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.evidence, common.source_provenance, strategy.diagnosis_evidence, strategy.validation_plan, strategy.continue_adjust_stop.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.planning.04 — Measures and verification**: Outcome measures, baseline and agreed targets define population, method and horizon; pending target decisions are explicit before the stage that depends on them. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: strategy.outcome_measures, strategy.targets.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.planning.05 — Priority, size and dependencies**: Choice and sequencing rationale compare meaningful alternatives and opportunity cost; dependencies, capacity/resource assumptions and uncertainty support any actual commitment. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: strategy.choices_tradeoffs, strategy.dependencies_assumptions, strategy.open_decisions.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.planning.06 — Applicable assurance and controls**: Applicable assurance obligations, including product AI and personal-data jurisdiction, constrain strategic choices; unsafe or unauthorized benefits cannot justify bypassing required controls. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, strategy.constraints, strategy.choices_tradeoffs.
  Conditional fields: {"ai": ["common.ai_assurance_reference"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.planning.07 — Governance and learning**: Actual decision authority and change state are explicit; observed discovery/release learning drives a recorded continue/change/stop decision and strategy/roadmap feedback, with actual follow-up owner. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.state, common.change_history, strategy.identity_state, strategy.roadmap_release_links, strategy.review_history.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Roadmap

- **gate.roadmap.planning.01 — Outcome and traceability**: Canonical roadmap outcomes and items resolve to current strategy and release goals; no duplicate backlog competes with the owning records. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.identity, common.traceability, roadmap.alignment_links, roadmap.sequence_outcome, roadmap.sequence_item_links.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.planning.02 — Scope and context**: Now/Next/Later and release allocation bound a versioned scope; deferrals, shared contributors and confidence distinguish intended direction from agreed commitments. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.boundary, roadmap.now, roadmap.next, roadmap.later, roadmap.deferred_scope.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.planning.03 — Discovery and evidence**: Evidence gates for horizon movement reference the highest-risk assumptions and actual discovery outputs; an untested hypothesis is not presented as an established predecessor result. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.evidence, common.source_provenance, roadmap.horizon_gate_evidence, roadmap.predecessor_outputs.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.planning.04 — Measures and verification**: Each allocated outcome has a linked release measure and review window or explicit pending decision; progress denominators and evidence describe outcomes without counting duplicate items. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: roadmap.sequence_outcome, roadmap.release_allocation, roadmap.sequence_gate.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.planning.05 — Priority, size and dependencies**: Sequence rationale reflects child priority/size ranges, genuine predecessor outputs and capacity uncertainty; estimates/timing are sourced and confidence is explicit, not invented. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: roadmap.sequence_rationale, roadmap.capacity_uncertainty, roadmap.sequence_confidence, roadmap.predecessor_outputs.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.planning.06 — Applicable assurance and controls**: Assurance, approval and access prerequisites appear as actual dependency/decision gates, including AI evaluation/privacy/fallback where applicable; a horizon label never waives a safety obligation. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, roadmap.sequence_gate, roadmap.horizon_gate_evidence.
  Conditional fields: {"ai": ["common.ai_assurance_reference"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.planning.07 — Governance and learning**: Actual roadmap authority, blockers and precise resume conditions are current; measured learning changes priority/allocation or records a no-change rationale with a next decision and owner. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.state, common.change_history, roadmap.identity_state, roadmap.blockers_decisions, roadmap.change_history.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Release goal

- **gate.release_goal.planning.01 — Outcome and traceability**: The release identifies actual users and an end-to-end usable outcome traceable to strategy/roadmap; included canonical items collectively deliver that outcome. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.identity, common.traceability, release_goal.alignment_sources, release_goal.users_journey, release_goal.usable_outcome, release_goal.included_items.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.planning.02 — Scope and context**: In-scope and deferred items, operating context and preserved behaviour form a single versioned release boundary; dependencies and readiness assumptions are explicit. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.boundary, release_goal.included_items, release_goal.excluded_deferred, release_goal.dependencies_decisions.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.planning.03 — Discovery and evidence**: Value/readiness claims cite actual predecessor/discovery evidence with limitations; unresolved assumptions are tracked to an actual decision and exact resume condition. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.evidence, common.source_provenance, release_goal.dependencies_decisions, release_goal.unmet_gates.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.planning.04 — Measures and verification**: Outcome targets, baseline/population/method and acceptance evidence are predeclared; entry and exit requirements are testable and do not conflate tests, acceptance, release and availability. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: release_goal.measures_targets, release_goal.entry_gate, release_goal.exit_gate.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.planning.05 — Priority, size and dependencies**: Scope and sequence fit sourced epic/story priority and size/capacity assumptions; release dependencies, resource constraints and uncertain timing are explicit before any commitment. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: release_goal.included_items, release_goal.dependencies_decisions.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.planning.06 — Applicable assurance and controls**: Actual product/privacy/security/domain approval route, NFRs, recovery and applicable AI controls are specified; required dataset rights, measured thresholds, safety/fallback and monitoring gates cannot be sampled away. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, release_goal.requirements_nfrs, release_goal.approval_authorities, release_goal.rollout_recovery.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "release_goal.ai_release_controls"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.planning.07 — Governance and learning**: The release retains separate quality, approval, readiness, acceptance, authorized publication and observed-availability evidence; actual outcome review ownership/window and strategy/roadmap feedback survive go-live. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.state, common.change_history, release_goal.identity_milestone, release_goal.unmet_gates, release_goal.change_history, release_goal.post_release_review.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Epic

- **gate.epic.planning.01 — Outcome and traceability**: One coherent capability addresses an evidenced user/operator problem and traces to current strategy/release requirements; its scope is not a collection of unrelated tasks. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.identity, common.traceability, epic.alignment_requirements, epic.problem, epic.capability_outcome.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.planning.02 — Scope and context**: Included/excluded scope and hand-offs are explicit; canonical children have one primary parent and cross-epic contributions use related links rather than duplicate acceptance counts. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.boundary, epic.included_scope, epic.excluded_handoffs, epic.children, epic.primary_parent.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.planning.03 — Discovery and evidence**: The riskiest assumption is ranked by consequence/uncertainty and has a falsifiable test, authorized method/sample, predeclared decision threshold, observed result when due and documented continue/change/stop or bounded authorized risk decision. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.evidence, common.source_provenance, epic.assumption_test, epic.risks_decisions.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.planning.04 — Measures and verification**: The capability completion/outcome boundary has observable measures and child acceptance mapping; uncovered source requirements, unsuccessful children and scope denominators remain visible. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: epic.completion_boundary, epic.child_evidence_gaps, epic.accepted_rollup.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.planning.05 — Priority, size and dependencies**: Priority compares meaningful alternatives and opportunity cost; size is a sourced range/coarse unit with scope, method, uncertainty and dependencies, and true prerequisites are separated from design relationships. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: epic.priority_rationale, epic.size_estimate, epic.dependencies.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.planning.06 — Applicable assurance and controls**: Shared experience/information/interface/quality contracts carry actual applicable access, safety, privacy, accessibility and AI requirements into children; no critical obligation falls between epics or into advisory-only samples. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, epic.shared_contracts, epic.risks_decisions.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "epic.ai_validation_contract"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.planning.07 — Governance and learning**: Actual epic owner/authority, revision, readiness/completion and gaps are distinct; accepted children alone do not prove capability value, and outcome learning feeds strategy/roadmap with an actual owner and next review. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.state, common.change_history, epic.identity_workpackage, epic.gaps_history.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### User story

- **gate.user_story.planning.01 — Outcome and traceability**: One bounded user/operator need and observable outcome resolves to its canonical epic/release and original source clauses; supporting/investigation items use their explicit variant rather than invented end-user value. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.identity, common.traceability, user_story.identity_parent, user_story.story_statement, user_story.source_clauses.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.planning.02 — Scope and context**: Trigger/preconditions, main journey, in/out of scope, preserved behaviour and affected users/operators are explicit; the experience can be understood without guessing. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.boundary, user_story.context_trigger, user_story.in_scope, user_story.out_of_scope, user_story.main_journey.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.planning.03 — Discovery and evidence**: Evidence and inspected reuse sources support the need/design; unresolved assumptions/decisions retain exact source, actual owner and resume condition, and source criteria are distinguished from proposed supplements. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.evidence, common.source_provenance, user_story.inspected_components, user_story.source_supplement_separation, user_story.ready_prerequisites.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.planning.04 — Measures and verification**: Identified criteria define observable positive/adverse/refusal/failure/authorization/recovery outcomes as applicable; every criterion maps to an approved evaluation context and expected evidence, with measurable thresholds where required. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: user_story.criteria, user_story.scenario_coverage, user_story.evaluation_mapping, user_story.nfr_thresholds.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.planning.05 — Priority, size and dependencies**: Priority follows sourced outcome, urgency/risk and alternatives; size is an attributable range/coarse unit with method, uncertainty, scope and dependencies, supporting a feasible bounded item. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: user_story.priority_rationale, user_story.size_estimate, user_story.ready_prerequisites.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.planning.06 — Applicable assurance and controls**: Actual operation contracts and side effects, access/accountability, refusal, information continuity, accessibility and NFRs cover applicable risks; AI acceptance metrics/slices, safety/fallback, rights/versioning and monitoring use the pinned module. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, user_story.operation_contracts, user_story.permissions_refusal, user_story.interaction_accessibility, user_story.nfr_thresholds.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "user_story.ai_acceptance_contract"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.planning.07 — Governance and learning**: Canonical team Ready/Done versions and item-specific additions are linked; quality, specification approval, execution readiness, criterion acceptance and delivery are distinct, with final revision and outcome-learning hand-off current. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.state, common.change_history, user_story.specification_state, user_story.team_ready_reference, user_story.team_done_reference.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Acceptance criterion

- **gate.acceptance_criterion.planning.01 — Outcome and traceability**: Criterion ID and owning item resolve to exact source provenance/current specification; a proposed supplement is distinguished from a protected original requirement. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.identity, common.traceability, acceptance_criterion.identity_owner, acceptance_criterion.source_provenance, acceptance_criterion.approval_state.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.planning.02 — Scope and context**: Given/When/Then identify one scenario, trigger, expected observable result and applicable prohibited effects without implementation guesses or hidden side effects. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.boundary, acceptance_criterion.scenario_kind, acceptance_criterion.given, acceptance_criterion.when, acceptance_criterion.then, acceptance_criterion.prohibited_effects.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.planning.03 — Discovery and evidence**: The intended scenario and evaluation design use relevant source/risk evidence and an authorized reproducible context; missing facts or unavailable test inputs remain unresolved rather than guessed. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.evidence, common.source_provenance, acceptance_criterion.source_provenance, acceptance_criterion.evaluation_method.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.planning.04 — Measures and verification**: Measurement defines method, units, threshold, sample/population and uncertainty where relevant; expected evidence can distinguish pass/fail, and AI metrics use fixed dataset/slice/model/prompt revisions. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: acceptance_criterion.measurement, acceptance_criterion.expected_evidence.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.planning.05 — Priority, size and dependencies**: The criterion maps to the owning item priority/risk and feasible verification method; any fixture/sample or predecessor constraint is explicit, and one result is not double-counted across competing criterion IDs. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: acceptance_criterion.identity_owner, acceptance_criterion.evaluation_method, acceptance_criterion.gap_resume.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.planning.06 — Applicable assurance and controls**: The criterion covers its applicable safety/privacy/access/authorization/fallback obligation and prohibited effects; actual AI accuracy and critical-slice/safety thresholds are independently required when this criterion claims AI behaviour. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, acceptance_criterion.prohibited_effects, acceptance_criterion.measurement.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "acceptance_criterion.ai_evaluation_measurement"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.planning.07 — Governance and learning**: Specification approval, not-run/planned execution, observed result and accepted state remain separate; evidence is bound to the current criterion/revision and a failed/skipped/blocked result has a precise follow-up. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.state, common.change_history, acceptance_criterion.approval_state, acceptance_criterion.gap_resume.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Implementation or verification task

- **gate.technical_task.planning.01 — Outcome and traceability**: One bounded implementation/design/operational/manufacturing/verification result has a canonical parent and exact source/criterion links; completing it must contribute to the parent outcome. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.identity, common.traceability, technical_task.parent_owner, technical_task.source_criteria, technical_task.bounded_result.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.planning.02 — Scope and context**: Affected components/processes and exact contracts/specification revision, exclusions and preserved behaviour bound the change; work steps and deliverables are reviewable in the actual product process. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.boundary, technical_task.components_contracts, technical_task.affected_components, technical_task.exclusions_preservation, technical_task.deliverables.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.planning.03 — Discovery and evidence**: Work/reuse/spike claims cite inspected sources and falsifiable investigation where relevant; required evaluation inputs/access and unresolved decisions remain explicit without fabricated facts. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.evidence, common.source_provenance, technical_task.data_environment_access, technical_task.work_steps.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.planning.04 — Measures and verification**: Verification cases and expected outputs map to parent acceptance criteria and actual product qualification method; no mirror-only demonstration substitutes for the declared user/operating requirement. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: technical_task.verification_cases, technical_task.qualification_review.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.planning.05 — Priority, size and dependencies**: Sequence relies on actual predecessor outputs and native completion blockers; parent priority/size and task effort/resource uncertainty support a feasible scope without invented commitments. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: technical_task.predecessors, technical_task.native_blockers, technical_task.work_steps.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.planning.06 — Applicable assurance and controls**: Impacts cover applicable experience, information, interface, access, safety and quality; evaluation access is authorized and AI artifact/held-out/safety/version/promotion evidence meets the pinned module when applicable. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, technical_task.impacts, technical_task.data_environment_access.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "technical_task.ai_artifact_evidence"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.planning.07 — Governance and learning**: Actual task owner/state and canonical team Ready/Done versions are current; task completion, parent acceptance and release/availability remain distinct, and actual outputs plus learning/follow-up are handed to the owning story/release. Planning stage: require a bounded testable plan, sourced priority/dependency rationale and honestly attributed size uncertainty where relevant. Unagreed targets/owners/estimates may remain explicitly pending only before a dependent commitment, approval or ready decision; record the exact unresolved decision and evidence needed. Future execution/launch results remain planned, never fabricated.
  Current-stage required fields: common.state, common.change_history, technical_task.identity_type, technical_task.team_ready_reference, technical_task.team_done_reference.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

## Ready stage

Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.

### Product vision

- **gate.vision.ready.01 — Outcome and traceability**: The direction names actual users/operators, their problem and a durable outcome; parent/source links resolve to current authoritative evidence rather than a feature inventory. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.identity, common.traceability, vision.primary_users_context, vision.problem_evidence, vision.vision_statement.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.ready.02 — Scope and context**: Operating context, affected people, non-goals and decision principles distinguish in-scope outcomes from exclusions without waiving protected requirements. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.boundary, vision.primary_users_context, vision.principles, vision.non_goals.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.ready.03 — Discovery and evidence**: Claims and assumptions are distinguished; relevant research has population, method, source and limitations, and the most important remaining uncertainty has a falsifiable research/decision plan. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.evidence, common.source_provenance, vision.research_sources, vision.problem_evidence, vision.assumptions_research.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.ready.04 — Measures and verification**: Success signals describe observable user/organization outcomes; each relevant measure has definition, population, method and review horizon, with agreed targets or explicit pending decision. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: vision.success_signals, vision.signal_measurement.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.ready.05 — Priority, size and dependencies**: The chosen direction explains value and major alternatives/trade-offs and connects to strategy; resource or timing commitments are sourced, and pending feasibility decisions remain visible. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: vision.value, vision.review_strategy.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.ready.06 — Applicable assurance and controls**: The actual profile identifies AI, affected rights, safety, security, access, privacy and accessibility applicability; scope/principles protect these obligations and prohibited effects. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, vision.principles, vision.non_goals.
  Conditional fields: {"ai": ["common.ai_assurance_reference"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.ready.07 — Governance and learning**: Actual product ownership/review authority, version and state are distinct from approval and delivery; review triggers connect observed learning to a decision and canonical strategy/roadmap updates. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.state, common.change_history, vision.owner_authority, vision.state_review, vision.review_strategy.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Product strategy

- **gate.strategy.ready.01 — Outcome and traceability**: Each strategic choice resolves to the vision and an evidenced priority problem/user outcome; sources distinguish established facts from proposed bets. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.identity, common.traceability, strategy.vision_sources, strategy.priority_problems, strategy.choices_tradeoffs.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.ready.02 — Scope and context**: Priority users/use cases, constraints, exclusions and reuse decisions bound the strategy and identify affected operators and prohibited scope expansion. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.boundary, strategy.priority_users_use_cases, strategy.constraints, strategy.deferral.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.ready.03 — Discovery and evidence**: Diagnosis and major bets have cited evidence, counterevidence and limitations; the validation plan can disprove the riskiest choice and has a predeclared continue/change/stop rule. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.evidence, common.source_provenance, strategy.diagnosis_evidence, strategy.validation_plan, strategy.continue_adjust_stop.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.ready.04 — Measures and verification**: Outcome measures, baseline and agreed targets define population, method and horizon; pending target decisions are explicit before the stage that depends on them. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: strategy.outcome_measures, strategy.targets.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.ready.05 — Priority, size and dependencies**: Choice and sequencing rationale compare meaningful alternatives and opportunity cost; dependencies, capacity/resource assumptions and uncertainty support any actual commitment. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: strategy.choices_tradeoffs, strategy.dependencies_assumptions, strategy.open_decisions.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.ready.06 — Applicable assurance and controls**: Applicable assurance obligations, including product AI and personal-data jurisdiction, constrain strategic choices; unsafe or unauthorized benefits cannot justify bypassing required controls. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, strategy.constraints, strategy.choices_tradeoffs.
  Conditional fields: {"ai": ["common.ai_assurance_reference"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.ready.07 — Governance and learning**: Actual decision authority and change state are explicit; observed discovery/release learning drives a recorded continue/change/stop decision and strategy/roadmap feedback, with actual follow-up owner. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.state, common.change_history, strategy.identity_state, strategy.roadmap_release_links, strategy.review_history.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Roadmap

- **gate.roadmap.ready.01 — Outcome and traceability**: Canonical roadmap outcomes and items resolve to current strategy and release goals; no duplicate backlog competes with the owning records. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.identity, common.traceability, roadmap.alignment_links, roadmap.sequence_outcome, roadmap.sequence_item_links.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.ready.02 — Scope and context**: Now/Next/Later and release allocation bound a versioned scope; deferrals, shared contributors and confidence distinguish intended direction from agreed commitments. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.boundary, roadmap.now, roadmap.next, roadmap.later, roadmap.deferred_scope.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.ready.03 — Discovery and evidence**: Evidence gates for horizon movement reference the highest-risk assumptions and actual discovery outputs; an untested hypothesis is not presented as an established predecessor result. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.evidence, common.source_provenance, roadmap.horizon_gate_evidence, roadmap.predecessor_outputs.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.ready.04 — Measures and verification**: Each allocated outcome has a linked release measure and review window or explicit pending decision; progress denominators and evidence describe outcomes without counting duplicate items. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: roadmap.sequence_outcome, roadmap.release_allocation, roadmap.sequence_gate.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.ready.05 — Priority, size and dependencies**: Sequence rationale reflects child priority/size ranges, genuine predecessor outputs and capacity uncertainty; estimates/timing are sourced and confidence is explicit, not invented. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: roadmap.sequence_rationale, roadmap.capacity_uncertainty, roadmap.sequence_confidence, roadmap.predecessor_outputs, roadmap.release_allocation, roadmap.sequence_timing.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.ready.06 — Applicable assurance and controls**: Assurance, approval and access prerequisites appear as actual dependency/decision gates, including AI evaluation/privacy/fallback where applicable; a horizon label never waives a safety obligation. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, roadmap.sequence_gate, roadmap.horizon_gate_evidence.
  Conditional fields: {"ai": ["common.ai_assurance_reference"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.ready.07 — Governance and learning**: Actual roadmap authority, blockers and precise resume conditions are current; measured learning changes priority/allocation or records a no-change rationale with a next decision and owner. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.state, common.change_history, roadmap.identity_state, roadmap.blockers_decisions, roadmap.change_history.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Release goal

- **gate.release_goal.ready.01 — Outcome and traceability**: The release identifies actual users and an end-to-end usable outcome traceable to strategy/roadmap; included canonical items collectively deliver that outcome. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.identity, common.traceability, release_goal.alignment_sources, release_goal.users_journey, release_goal.usable_outcome, release_goal.included_items.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.ready.02 — Scope and context**: In-scope and deferred items, operating context and preserved behaviour form a single versioned release boundary; dependencies and readiness assumptions are explicit. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.boundary, release_goal.included_items, release_goal.excluded_deferred, release_goal.dependencies_decisions.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.ready.03 — Discovery and evidence**: Value/readiness claims cite actual predecessor/discovery evidence with limitations; unresolved assumptions are tracked to an actual decision and exact resume condition. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.evidence, common.source_provenance, release_goal.dependencies_decisions, release_goal.unmet_gates.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.ready.04 — Measures and verification**: Outcome targets, baseline/population/method and acceptance evidence are predeclared; entry and exit requirements are testable and do not conflate tests, acceptance, release and availability. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: release_goal.measures_targets, release_goal.entry_gate, release_goal.exit_gate.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.ready.05 — Priority, size and dependencies**: Scope and sequence fit sourced epic/story priority and size/capacity assumptions; release dependencies, resource constraints and uncertain timing are explicit before any commitment. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: release_goal.included_items, release_goal.dependencies_decisions.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.ready.06 — Applicable assurance and controls**: Actual product/privacy/security/domain approval route, NFRs, recovery and applicable AI controls are specified; required dataset rights, measured thresholds, safety/fallback and monitoring gates cannot be sampled away. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, release_goal.requirements_nfrs, release_goal.approval_authorities, release_goal.rollout_recovery.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "release_goal.ai_release_controls"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.ready.07 — Governance and learning**: The release retains separate quality, approval, readiness, acceptance, authorized publication and observed-availability evidence; actual outcome review ownership/window and strategy/roadmap feedback survive go-live. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.state, common.change_history, release_goal.identity_milestone, release_goal.unmet_gates, release_goal.change_history, release_goal.post_release_review.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Epic

- **gate.epic.ready.01 — Outcome and traceability**: One coherent capability addresses an evidenced user/operator problem and traces to current strategy/release requirements; its scope is not a collection of unrelated tasks. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.identity, common.traceability, epic.alignment_requirements, epic.problem, epic.capability_outcome.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.ready.02 — Scope and context**: Included/excluded scope and hand-offs are explicit; canonical children have one primary parent and cross-epic contributions use related links rather than duplicate acceptance counts. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.boundary, epic.included_scope, epic.excluded_handoffs, epic.children, epic.primary_parent.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.ready.03 — Discovery and evidence**: The riskiest assumption is ranked by consequence/uncertainty and has a falsifiable test, authorized method/sample, predeclared decision threshold, observed result when due and documented continue/change/stop or bounded authorized risk decision. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.evidence, common.source_provenance, epic.assumption_test, epic.risks_decisions.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.ready.04 — Measures and verification**: The capability completion/outcome boundary has observable measures and child acceptance mapping; uncovered source requirements, unsuccessful children and scope denominators remain visible. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: epic.completion_boundary, epic.child_evidence_gaps, epic.accepted_rollup.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.ready.05 — Priority, size and dependencies**: Priority compares meaningful alternatives and opportunity cost; size is a sourced range/coarse unit with scope, method, uncertainty and dependencies, and true prerequisites are separated from design relationships. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: epic.priority_rationale, epic.size_estimate, epic.dependencies.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.ready.06 — Applicable assurance and controls**: Shared experience/information/interface/quality contracts carry actual applicable access, safety, privacy, accessibility and AI requirements into children; no critical obligation falls between epics or into advisory-only samples. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, epic.shared_contracts, epic.risks_decisions.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "epic.ai_validation_contract"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.ready.07 — Governance and learning**: Actual epic owner/authority, revision, readiness/completion and gaps are distinct; accepted children alone do not prove capability value, and outcome learning feeds strategy/roadmap with an actual owner and next review. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.state, common.change_history, epic.identity_workpackage, epic.gaps_history.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### User story

- **gate.user_story.ready.01 — Outcome and traceability**: One bounded user/operator need and observable outcome resolves to its canonical epic/release and original source clauses; supporting/investigation items use their explicit variant rather than invented end-user value. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.identity, common.traceability, user_story.identity_parent, user_story.story_statement, user_story.source_clauses.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.ready.02 — Scope and context**: Trigger/preconditions, main journey, in/out of scope, preserved behaviour and affected users/operators are explicit; the experience can be understood without guessing. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.boundary, user_story.context_trigger, user_story.in_scope, user_story.out_of_scope, user_story.main_journey.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.ready.03 — Discovery and evidence**: Evidence and inspected reuse sources support the need/design; unresolved assumptions/decisions retain exact source, actual owner and resume condition, and source criteria are distinguished from proposed supplements. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.evidence, common.source_provenance, user_story.inspected_components, user_story.source_supplement_separation, user_story.ready_prerequisites.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.ready.04 — Measures and verification**: Identified criteria define observable positive/adverse/refusal/failure/authorization/recovery outcomes as applicable; every criterion maps to an approved evaluation context and expected evidence, with measurable thresholds where required. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: user_story.criteria, user_story.scenario_coverage, user_story.evaluation_mapping, user_story.nfr_thresholds.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.ready.05 — Priority, size and dependencies**: Priority follows sourced outcome, urgency/risk and alternatives; size is an attributable range/coarse unit with method, uncertainty, scope and dependencies, supporting a feasible bounded item. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: user_story.priority_rationale, user_story.size_estimate, user_story.ready_prerequisites.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.ready.06 — Applicable assurance and controls**: Actual operation contracts and side effects, access/accountability, refusal, information continuity, accessibility and NFRs cover applicable risks; AI acceptance metrics/slices, safety/fallback, rights/versioning and monitoring use the pinned module. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, user_story.operation_contracts, user_story.permissions_refusal, user_story.interaction_accessibility, user_story.nfr_thresholds.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "user_story.ai_acceptance_contract"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.ready.07 — Governance and learning**: Canonical team Ready/Done versions and item-specific additions are linked; quality, specification approval, execution readiness, criterion acceptance and delivery are distinct, with final revision and outcome-learning hand-off current. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.state, common.change_history, user_story.specification_state, user_story.team_ready_reference, user_story.team_done_reference.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Acceptance criterion

- **gate.acceptance_criterion.ready.01 — Outcome and traceability**: Criterion ID and owning item resolve to exact source provenance/current specification; a proposed supplement is distinguished from a protected original requirement. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.identity, common.traceability, acceptance_criterion.identity_owner, acceptance_criterion.source_provenance, acceptance_criterion.approval_state.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.ready.02 — Scope and context**: Given/When/Then identify one scenario, trigger, expected observable result and applicable prohibited effects without implementation guesses or hidden side effects. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.boundary, acceptance_criterion.scenario_kind, acceptance_criterion.given, acceptance_criterion.when, acceptance_criterion.then, acceptance_criterion.prohibited_effects.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.ready.03 — Discovery and evidence**: The intended scenario and evaluation design use relevant source/risk evidence and an authorized reproducible context; missing facts or unavailable test inputs remain unresolved rather than guessed. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.evidence, common.source_provenance, acceptance_criterion.source_provenance, acceptance_criterion.evaluation_method.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.ready.04 — Measures and verification**: Measurement defines method, units, threshold, sample/population and uncertainty where relevant; expected evidence can distinguish pass/fail, and AI metrics use fixed dataset/slice/model/prompt revisions. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: acceptance_criterion.measurement, acceptance_criterion.expected_evidence.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.ready.05 — Priority, size and dependencies**: The criterion maps to the owning item priority/risk and feasible verification method; any fixture/sample or predecessor constraint is explicit, and one result is not double-counted across competing criterion IDs. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: acceptance_criterion.identity_owner, acceptance_criterion.evaluation_method, acceptance_criterion.gap_resume.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.ready.06 — Applicable assurance and controls**: The criterion covers its applicable safety/privacy/access/authorization/fallback obligation and prohibited effects; actual AI accuracy and critical-slice/safety thresholds are independently required when this criterion claims AI behaviour. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, acceptance_criterion.prohibited_effects, acceptance_criterion.measurement.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "acceptance_criterion.ai_evaluation_measurement"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.ready.07 — Governance and learning**: Specification approval, not-run/planned execution, observed result and accepted state remain separate; evidence is bound to the current criterion/revision and a failed/skipped/blocked result has a precise follow-up. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.state, common.change_history, acceptance_criterion.approval_state, acceptance_criterion.gap_resume.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Implementation or verification task

- **gate.technical_task.ready.01 — Outcome and traceability**: One bounded implementation/design/operational/manufacturing/verification result has a canonical parent and exact source/criterion links; completing it must contribute to the parent outcome. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.identity, common.traceability, technical_task.parent_owner, technical_task.source_criteria, technical_task.bounded_result.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.ready.02 — Scope and context**: Affected components/processes and exact contracts/specification revision, exclusions and preserved behaviour bound the change; work steps and deliverables are reviewable in the actual product process. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.boundary, technical_task.components_contracts, technical_task.affected_components, technical_task.exclusions_preservation, technical_task.deliverables.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.ready.03 — Discovery and evidence**: Work/reuse/spike claims cite inspected sources and falsifiable investigation where relevant; required evaluation inputs/access and unresolved decisions remain explicit without fabricated facts. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.evidence, common.source_provenance, technical_task.data_environment_access, technical_task.work_steps.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.ready.04 — Measures and verification**: Verification cases and expected outputs map to parent acceptance criteria and actual product qualification method; no mirror-only demonstration substitutes for the declared user/operating requirement. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: technical_task.verification_cases, technical_task.qualification_review.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.ready.05 — Priority, size and dependencies**: Sequence relies on actual predecessor outputs and native completion blockers; parent priority/size and task effort/resource uncertainty support a feasible scope without invented commitments. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: technical_task.predecessors, technical_task.native_blockers, technical_task.work_steps.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.ready.06 — Applicable assurance and controls**: Impacts cover applicable experience, information, interface, access, safety and quality; evaluation access is authorized and AI artifact/held-out/safety/version/promotion evidence meets the pinned module when applicable. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, technical_task.impacts, technical_task.data_environment_access.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "technical_task.ai_artifact_evidence"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.ready.07 — Governance and learning**: Actual task owner/state and canonical team Ready/Done versions are current; task completion, parent acceptance and release/availability remain distinct, and actual outputs plus learning/follow-up are handed to the owning story/release. Ready stage: the item can proceed through the declared actual process with the required scope/targets, feasible estimate/dependencies, evaluation access, controls and actual authority decisions resolved. Apply the canonical team Ready policy where linked. Quality PASS cannot grant approval: any independent human/business/legal/safety approval or access decision remains a separate prerequisite, and an unresolved required prerequisite blocks ready.
  Current-stage required fields: common.state, common.change_history, technical_task.identity_type, technical_task.team_ready_reference, technical_task.team_done_reference.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

## Delivery stage

Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.

### Product vision

- **gate.vision.delivery.01 — Outcome and traceability**: The direction names actual users/operators, their problem and a durable outcome; parent/source links resolve to current authoritative evidence rather than a feature inventory. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.identity, common.traceability, vision.primary_users_context, vision.problem_evidence, vision.vision_statement.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.delivery.02 — Scope and context**: Operating context, affected people, non-goals and decision principles distinguish in-scope outcomes from exclusions without waiving protected requirements. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.boundary, vision.primary_users_context, vision.principles, vision.non_goals.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.delivery.03 — Discovery and evidence**: Claims and assumptions are distinguished; relevant research has population, method, source and limitations, and the most important remaining uncertainty has a falsifiable research/decision plan. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.evidence, common.source_provenance, vision.research_sources, vision.problem_evidence, vision.assumptions_research.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.delivery.04 — Measures and verification**: Success signals describe observable user/organization outcomes; each relevant measure has definition, population, method and review horizon, with agreed targets or explicit pending decision. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: vision.success_signals, vision.signal_measurement.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.delivery.05 — Priority, size and dependencies**: The chosen direction explains value and major alternatives/trade-offs and connects to strategy; resource or timing commitments are sourced, and pending feasibility decisions remain visible. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: vision.value, vision.review_strategy.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.delivery.06 — Applicable assurance and controls**: The actual profile identifies AI, affected rights, safety, security, access, privacy and accessibility applicability; scope/principles protect these obligations and prohibited effects. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, vision.principles, vision.non_goals.
  Conditional fields: {"ai": ["common.ai_assurance_reference"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.delivery.07 — Governance and learning**: Actual product ownership/review authority, version and state are distinct from approval and delivery; review triggers connect observed learning to a decision and canonical strategy/roadmap updates. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.state, common.change_history, vision.owner_authority, vision.state_review, vision.review_strategy.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Product strategy

- **gate.strategy.delivery.01 — Outcome and traceability**: Each strategic choice resolves to the vision and an evidenced priority problem/user outcome; sources distinguish established facts from proposed bets. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.identity, common.traceability, strategy.vision_sources, strategy.priority_problems, strategy.choices_tradeoffs.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.delivery.02 — Scope and context**: Priority users/use cases, constraints, exclusions and reuse decisions bound the strategy and identify affected operators and prohibited scope expansion. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.boundary, strategy.priority_users_use_cases, strategy.constraints, strategy.deferral.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.delivery.03 — Discovery and evidence**: Diagnosis and major bets have cited evidence, counterevidence and limitations; the validation plan can disprove the riskiest choice and has a predeclared continue/change/stop rule. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.evidence, common.source_provenance, strategy.diagnosis_evidence, strategy.validation_plan, strategy.continue_adjust_stop.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.delivery.04 — Measures and verification**: Outcome measures, baseline and agreed targets define population, method and horizon; pending target decisions are explicit before the stage that depends on them. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: strategy.outcome_measures, strategy.targets.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.delivery.05 — Priority, size and dependencies**: Choice and sequencing rationale compare meaningful alternatives and opportunity cost; dependencies, capacity/resource assumptions and uncertainty support any actual commitment. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: strategy.choices_tradeoffs, strategy.dependencies_assumptions, strategy.open_decisions.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.delivery.06 — Applicable assurance and controls**: Applicable assurance obligations, including product AI and personal-data jurisdiction, constrain strategic choices; unsafe or unauthorized benefits cannot justify bypassing required controls. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, strategy.constraints, strategy.choices_tradeoffs.
  Conditional fields: {"ai": ["common.ai_assurance_reference"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.delivery.07 — Governance and learning**: Actual decision authority and change state are explicit; observed discovery/release learning drives a recorded continue/change/stop decision and strategy/roadmap feedback, with actual follow-up owner. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.state, common.change_history, strategy.identity_state, strategy.roadmap_release_links, strategy.review_history.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Roadmap

- **gate.roadmap.delivery.01 — Outcome and traceability**: Canonical roadmap outcomes and items resolve to current strategy and release goals; no duplicate backlog competes with the owning records. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.identity, common.traceability, roadmap.alignment_links, roadmap.sequence_outcome, roadmap.sequence_item_links.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.delivery.02 — Scope and context**: Now/Next/Later and release allocation bound a versioned scope; deferrals, shared contributors and confidence distinguish intended direction from agreed commitments. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.boundary, roadmap.now, roadmap.next, roadmap.later, roadmap.deferred_scope.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.delivery.03 — Discovery and evidence**: Evidence gates for horizon movement reference the highest-risk assumptions and actual discovery outputs; an untested hypothesis is not presented as an established predecessor result. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.evidence, common.source_provenance, roadmap.horizon_gate_evidence, roadmap.predecessor_outputs.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.delivery.04 — Measures and verification**: Each allocated outcome has a linked release measure and review window or explicit pending decision; progress denominators and evidence describe outcomes without counting duplicate items. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: roadmap.sequence_outcome, roadmap.release_allocation, roadmap.sequence_gate.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.delivery.05 — Priority, size and dependencies**: Sequence rationale reflects child priority/size ranges, genuine predecessor outputs and capacity uncertainty; estimates/timing are sourced and confidence is explicit, not invented. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: roadmap.sequence_rationale, roadmap.capacity_uncertainty, roadmap.sequence_confidence, roadmap.predecessor_outputs.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.delivery.06 — Applicable assurance and controls**: Assurance, approval and access prerequisites appear as actual dependency/decision gates, including AI evaluation/privacy/fallback where applicable; a horizon label never waives a safety obligation. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, roadmap.sequence_gate, roadmap.horizon_gate_evidence.
  Conditional fields: {"ai": ["common.ai_assurance_reference"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.delivery.07 — Governance and learning**: Actual roadmap authority, blockers and precise resume conditions are current; measured learning changes priority/allocation or records a no-change rationale with a next decision and owner. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.state, common.change_history, roadmap.identity_state, roadmap.blockers_decisions, roadmap.change_history.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Release goal

- **gate.release_goal.delivery.01 — Outcome and traceability**: The release identifies actual users and an end-to-end usable outcome traceable to strategy/roadmap; included canonical items collectively deliver that outcome. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.identity, common.traceability, release_goal.alignment_sources, release_goal.users_journey, release_goal.usable_outcome, release_goal.included_items.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.delivery.02 — Scope and context**: In-scope and deferred items, operating context and preserved behaviour form a single versioned release boundary; dependencies and readiness assumptions are explicit. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.boundary, release_goal.included_items, release_goal.excluded_deferred, release_goal.dependencies_decisions.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.delivery.03 — Discovery and evidence**: Value/readiness claims cite actual predecessor/discovery evidence with limitations; unresolved assumptions are tracked to an actual decision and exact resume condition. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.evidence, common.source_provenance, release_goal.dependencies_decisions, release_goal.unmet_gates.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.delivery.04 — Measures and verification**: Outcome targets, baseline/population/method and acceptance evidence are predeclared; entry and exit requirements are testable and do not conflate tests, acceptance, release and availability. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: release_goal.measures_targets, release_goal.entry_gate, release_goal.exit_gate.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.delivery.05 — Priority, size and dependencies**: Scope and sequence fit sourced epic/story priority and size/capacity assumptions; release dependencies, resource constraints and uncertain timing are explicit before any commitment. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: release_goal.included_items, release_goal.dependencies_decisions.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.delivery.06 — Applicable assurance and controls**: Actual product/privacy/security/domain approval route, NFRs, recovery and applicable AI controls are specified; required dataset rights, measured thresholds, safety/fallback and monitoring gates cannot be sampled away. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, release_goal.requirements_nfrs, release_goal.approval_authorities, release_goal.rollout_recovery.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "release_goal.ai_release_controls"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.delivery.07 — Governance and learning**: The release retains separate quality, approval, readiness, acceptance, authorized publication and observed-availability evidence; actual outcome review ownership/window and strategy/roadmap feedback survive go-live. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.state, common.change_history, release_goal.identity_milestone, release_goal.unmet_gates, release_goal.change_history, release_goal.qualified_revision_review, release_goal.final_tests_review, release_goal.published_revision, release_goal.available_revision, release_goal.operational_verification, release_goal.post_release_review.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Epic

- **gate.epic.delivery.01 — Outcome and traceability**: One coherent capability addresses an evidenced user/operator problem and traces to current strategy/release requirements; its scope is not a collection of unrelated tasks. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.identity, common.traceability, epic.alignment_requirements, epic.problem, epic.capability_outcome.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.delivery.02 — Scope and context**: Included/excluded scope and hand-offs are explicit; canonical children have one primary parent and cross-epic contributions use related links rather than duplicate acceptance counts. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.boundary, epic.included_scope, epic.excluded_handoffs, epic.children, epic.primary_parent.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.delivery.03 — Discovery and evidence**: The riskiest assumption is ranked by consequence/uncertainty and has a falsifiable test, authorized method/sample, predeclared decision threshold, observed result when due and documented continue/change/stop or bounded authorized risk decision. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.evidence, common.source_provenance, epic.assumption_test, epic.risks_decisions.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.delivery.04 — Measures and verification**: The capability completion/outcome boundary has observable measures and child acceptance mapping; uncovered source requirements, unsuccessful children and scope denominators remain visible. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: epic.completion_boundary, epic.child_evidence_gaps, epic.accepted_rollup.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.delivery.05 — Priority, size and dependencies**: Priority compares meaningful alternatives and opportunity cost; size is a sourced range/coarse unit with scope, method, uncertainty and dependencies, and true prerequisites are separated from design relationships. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: epic.priority_rationale, epic.size_estimate, epic.dependencies.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.delivery.06 — Applicable assurance and controls**: Shared experience/information/interface/quality contracts carry actual applicable access, safety, privacy, accessibility and AI requirements into children; no critical obligation falls between epics or into advisory-only samples. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, epic.shared_contracts, epic.risks_decisions.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "epic.ai_validation_contract"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.delivery.07 — Governance and learning**: Actual epic owner/authority, revision, readiness/completion and gaps are distinct; accepted children alone do not prove capability value, and outcome learning feeds strategy/roadmap with an actual owner and next review. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.state, common.change_history, epic.identity_workpackage, epic.gaps_history.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### User story

- **gate.user_story.delivery.01 — Outcome and traceability**: One bounded user/operator need and observable outcome resolves to its canonical epic/release and original source clauses; supporting/investigation items use their explicit variant rather than invented end-user value. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.identity, common.traceability, user_story.identity_parent, user_story.story_statement, user_story.source_clauses.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.delivery.02 — Scope and context**: Trigger/preconditions, main journey, in/out of scope, preserved behaviour and affected users/operators are explicit; the experience can be understood without guessing. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.boundary, user_story.context_trigger, user_story.in_scope, user_story.out_of_scope, user_story.main_journey.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.delivery.03 — Discovery and evidence**: Evidence and inspected reuse sources support the need/design; unresolved assumptions/decisions retain exact source, actual owner and resume condition, and source criteria are distinguished from proposed supplements. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.evidence, common.source_provenance, user_story.inspected_components, user_story.source_supplement_separation, user_story.ready_prerequisites.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.delivery.04 — Measures and verification**: Identified criteria define observable positive/adverse/refusal/failure/authorization/recovery outcomes as applicable; every criterion maps to an approved evaluation context and expected evidence, with measurable thresholds where required. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: user_story.criteria, user_story.scenario_coverage, user_story.evaluation_mapping, user_story.nfr_thresholds.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.delivery.05 — Priority, size and dependencies**: Priority follows sourced outcome, urgency/risk and alternatives; size is an attributable range/coarse unit with method, uncertainty, scope and dependencies, supporting a feasible bounded item. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: user_story.priority_rationale, user_story.size_estimate, user_story.ready_prerequisites.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.delivery.06 — Applicable assurance and controls**: Actual operation contracts and side effects, access/accountability, refusal, information continuity, accessibility and NFRs cover applicable risks; AI acceptance metrics/slices, safety/fallback, rights/versioning and monitoring use the pinned module. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, user_story.operation_contracts, user_story.permissions_refusal, user_story.interaction_accessibility, user_story.nfr_thresholds.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "user_story.ai_acceptance_contract"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.delivery.07 — Governance and learning**: Canonical team Ready/Done versions and item-specific additions are linked; quality, specification approval, execution readiness, criterion acceptance and delivery are distinct, with final revision and outcome-learning hand-off current. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.state, common.change_history, user_story.specification_state, user_story.team_ready_reference, user_story.team_done_reference, user_story.delivery_evidence, user_story.criterion_rollup_blockers.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Acceptance criterion

- **gate.acceptance_criterion.delivery.01 — Outcome and traceability**: Criterion ID and owning item resolve to exact source provenance/current specification; a proposed supplement is distinguished from a protected original requirement. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.identity, common.traceability, acceptance_criterion.identity_owner, acceptance_criterion.source_provenance, acceptance_criterion.approval_state.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.delivery.02 — Scope and context**: Given/When/Then identify one scenario, trigger, expected observable result and applicable prohibited effects without implementation guesses or hidden side effects. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.boundary, acceptance_criterion.scenario_kind, acceptance_criterion.given, acceptance_criterion.when, acceptance_criterion.then, acceptance_criterion.prohibited_effects.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.delivery.03 — Discovery and evidence**: The intended scenario and evaluation design use relevant source/risk evidence and an authorized reproducible context; missing facts or unavailable test inputs remain unresolved rather than guessed. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.evidence, common.source_provenance, acceptance_criterion.source_provenance, acceptance_criterion.evaluation_method.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.delivery.04 — Measures and verification**: Measurement defines method, units, threshold, sample/population and uncertainty where relevant; expected evidence can distinguish pass/fail, and AI metrics use fixed dataset/slice/model/prompt revisions. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: acceptance_criterion.measurement, acceptance_criterion.expected_evidence.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.delivery.05 — Priority, size and dependencies**: The criterion maps to the owning item priority/risk and feasible verification method; any fixture/sample or predecessor constraint is explicit, and one result is not double-counted across competing criterion IDs. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: acceptance_criterion.identity_owner, acceptance_criterion.evaluation_method, acceptance_criterion.gap_resume.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.delivery.06 — Applicable assurance and controls**: The criterion covers its applicable safety/privacy/access/authorization/fallback obligation and prohibited effects; actual AI accuracy and critical-slice/safety thresholds are independently required when this criterion claims AI behaviour. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, acceptance_criterion.prohibited_effects, acceptance_criterion.measurement.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "acceptance_criterion.ai_evaluation_measurement"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.delivery.07 — Governance and learning**: Specification approval, not-run/planned execution, observed result and accepted state remain separate; evidence is bound to the current criterion/revision and a failed/skipped/blocked result has a precise follow-up. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.state, common.change_history, acceptance_criterion.approval_state, acceptance_criterion.gap_resume, acceptance_criterion.actual_execution, acceptance_criterion.observed_evidence.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Implementation or verification task

- **gate.technical_task.delivery.01 — Outcome and traceability**: One bounded implementation/design/operational/manufacturing/verification result has a canonical parent and exact source/criterion links; completing it must contribute to the parent outcome. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.identity, common.traceability, technical_task.parent_owner, technical_task.source_criteria, technical_task.bounded_result.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.delivery.02 — Scope and context**: Affected components/processes and exact contracts/specification revision, exclusions and preserved behaviour bound the change; work steps and deliverables are reviewable in the actual product process. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.boundary, technical_task.components_contracts, technical_task.affected_components, technical_task.exclusions_preservation, technical_task.deliverables.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.delivery.03 — Discovery and evidence**: Work/reuse/spike claims cite inspected sources and falsifiable investigation where relevant; required evaluation inputs/access and unresolved decisions remain explicit without fabricated facts. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.evidence, common.source_provenance, technical_task.data_environment_access, technical_task.work_steps.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.delivery.04 — Measures and verification**: Verification cases and expected outputs map to parent acceptance criteria and actual product qualification method; no mirror-only demonstration substitutes for the declared user/operating requirement. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: technical_task.verification_cases, technical_task.qualification_review.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.delivery.05 — Priority, size and dependencies**: Sequence relies on actual predecessor outputs and native completion blockers; parent priority/size and task effort/resource uncertainty support a feasible scope without invented commitments. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: technical_task.predecessors, technical_task.native_blockers, technical_task.work_steps.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.delivery.06 — Applicable assurance and controls**: Impacts cover applicable experience, information, interface, access, safety and quality; evaluation access is authorized and AI artifact/held-out/safety/version/promotion evidence meets the pinned module when applicable. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, technical_task.impacts, technical_task.data_environment_access.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "technical_task.ai_artifact_evidence"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.delivery.07 — Governance and learning**: Actual task owner/state and canonical team Ready/Done versions are current; task completion, parent acceptance and release/availability remain distinct, and actual outputs plus learning/follow-up are handed to the owning story/release. Delivery stage: inspect original final-revision evaluation outputs against frozen expected results, required current independent review and actual authorized delivery observations within item scope. Distinguish qualified, accepted, integrated/published, available and user-verified states; fail or retain precise blockers for missing/failed evidence. A software SHA/CI/hosting mechanism is required only if the actual product process uses it.
  Current-stage required fields: common.state, common.change_history, technical_task.identity_type, technical_task.team_ready_reference, technical_task.team_done_reference, technical_task.actual_outputs, technical_task.release_verification.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

## Learning stage

Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.

### Product vision

- **gate.vision.learning.01 — Outcome and traceability**: The direction names actual users/operators, their problem and a durable outcome; parent/source links resolve to current authoritative evidence rather than a feature inventory. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.identity, common.traceability, vision.primary_users_context, vision.problem_evidence, vision.vision_statement.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.learning.02 — Scope and context**: Operating context, affected people, non-goals and decision principles distinguish in-scope outcomes from exclusions without waiving protected requirements. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.boundary, vision.primary_users_context, vision.principles, vision.non_goals.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.learning.03 — Discovery and evidence**: Claims and assumptions are distinguished; relevant research has population, method, source and limitations, and the most important remaining uncertainty has a falsifiable research/decision plan. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.evidence, common.source_provenance, vision.research_sources, vision.problem_evidence, vision.assumptions_research.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.learning.04 — Measures and verification**: Success signals describe observable user/organization outcomes; each relevant measure has definition, population, method and review horizon, with agreed targets or explicit pending decision. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: vision.success_signals, vision.signal_measurement.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.learning.05 — Priority, size and dependencies**: The chosen direction explains value and major alternatives/trade-offs and connects to strategy; resource or timing commitments are sourced, and pending feasibility decisions remain visible. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: vision.value, vision.review_strategy.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.learning.06 — Applicable assurance and controls**: The actual profile identifies AI, affected rights, safety, security, access, privacy and accessibility applicability; scope/principles protect these obligations and prohibited effects. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, vision.principles, vision.non_goals.
  Conditional fields: {"ai": ["common.ai_assurance_reference"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.vision.learning.07 — Governance and learning**: Actual product ownership/review authority, version and state are distinct from approval and delivery; review triggers connect observed learning to a decision and canonical strategy/roadmap updates. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.state, common.change_history, vision.owner_authority, vision.state_review, vision.review_strategy, vision.learning_feedback.
  Conditional fields: {}.
  Evidence: Current Product vision revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Product strategy

- **gate.strategy.learning.01 — Outcome and traceability**: Each strategic choice resolves to the vision and an evidenced priority problem/user outcome; sources distinguish established facts from proposed bets. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.identity, common.traceability, strategy.vision_sources, strategy.priority_problems, strategy.choices_tradeoffs.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.learning.02 — Scope and context**: Priority users/use cases, constraints, exclusions and reuse decisions bound the strategy and identify affected operators and prohibited scope expansion. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.boundary, strategy.priority_users_use_cases, strategy.constraints, strategy.deferral.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.learning.03 — Discovery and evidence**: Diagnosis and major bets have cited evidence, counterevidence and limitations; the validation plan can disprove the riskiest choice and has a predeclared continue/change/stop rule. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.evidence, common.source_provenance, strategy.diagnosis_evidence, strategy.validation_plan, strategy.continue_adjust_stop.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.learning.04 — Measures and verification**: Outcome measures, baseline and agreed targets define population, method and horizon; pending target decisions are explicit before the stage that depends on them. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: strategy.outcome_measures, strategy.targets.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.learning.05 — Priority, size and dependencies**: Choice and sequencing rationale compare meaningful alternatives and opportunity cost; dependencies, capacity/resource assumptions and uncertainty support any actual commitment. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: strategy.choices_tradeoffs, strategy.dependencies_assumptions, strategy.open_decisions.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.learning.06 — Applicable assurance and controls**: Applicable assurance obligations, including product AI and personal-data jurisdiction, constrain strategic choices; unsafe or unauthorized benefits cannot justify bypassing required controls. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, strategy.constraints, strategy.choices_tradeoffs.
  Conditional fields: {"ai": ["common.ai_assurance_reference"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.strategy.learning.07 — Governance and learning**: Actual decision authority and change state are explicit; observed discovery/release learning drives a recorded continue/change/stop decision and strategy/roadmap feedback, with actual follow-up owner. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.state, common.change_history, strategy.identity_state, strategy.roadmap_release_links, strategy.review_history, strategy.learning_feedback.
  Conditional fields: {}.
  Evidence: Current Product strategy revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Roadmap

- **gate.roadmap.learning.01 — Outcome and traceability**: Canonical roadmap outcomes and items resolve to current strategy and release goals; no duplicate backlog competes with the owning records. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.identity, common.traceability, roadmap.alignment_links, roadmap.sequence_outcome, roadmap.sequence_item_links.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.learning.02 — Scope and context**: Now/Next/Later and release allocation bound a versioned scope; deferrals, shared contributors and confidence distinguish intended direction from agreed commitments. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.boundary, roadmap.now, roadmap.next, roadmap.later, roadmap.deferred_scope.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.learning.03 — Discovery and evidence**: Evidence gates for horizon movement reference the highest-risk assumptions and actual discovery outputs; an untested hypothesis is not presented as an established predecessor result. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.evidence, common.source_provenance, roadmap.horizon_gate_evidence, roadmap.predecessor_outputs.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.learning.04 — Measures and verification**: Each allocated outcome has a linked release measure and review window or explicit pending decision; progress denominators and evidence describe outcomes without counting duplicate items. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: roadmap.sequence_outcome, roadmap.release_allocation, roadmap.sequence_gate.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.learning.05 — Priority, size and dependencies**: Sequence rationale reflects child priority/size ranges, genuine predecessor outputs and capacity uncertainty; estimates/timing are sourced and confidence is explicit, not invented. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: roadmap.sequence_rationale, roadmap.capacity_uncertainty, roadmap.sequence_confidence, roadmap.predecessor_outputs.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.learning.06 — Applicable assurance and controls**: Assurance, approval and access prerequisites appear as actual dependency/decision gates, including AI evaluation/privacy/fallback where applicable; a horizon label never waives a safety obligation. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, roadmap.sequence_gate, roadmap.horizon_gate_evidence.
  Conditional fields: {"ai": ["common.ai_assurance_reference"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.roadmap.learning.07 — Governance and learning**: Actual roadmap authority, blockers and precise resume conditions are current; measured learning changes priority/allocation or records a no-change rationale with a next decision and owner. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.state, common.change_history, roadmap.identity_state, roadmap.blockers_decisions, roadmap.change_history, roadmap.learning_feedback.
  Conditional fields: {}.
  Evidence: Current Roadmap revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Release goal

- **gate.release_goal.learning.01 — Outcome and traceability**: The release identifies actual users and an end-to-end usable outcome traceable to strategy/roadmap; included canonical items collectively deliver that outcome. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.identity, common.traceability, release_goal.alignment_sources, release_goal.users_journey, release_goal.usable_outcome, release_goal.included_items.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.learning.02 — Scope and context**: In-scope and deferred items, operating context and preserved behaviour form a single versioned release boundary; dependencies and readiness assumptions are explicit. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.boundary, release_goal.included_items, release_goal.excluded_deferred, release_goal.dependencies_decisions.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.learning.03 — Discovery and evidence**: Value/readiness claims cite actual predecessor/discovery evidence with limitations; unresolved assumptions are tracked to an actual decision and exact resume condition. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.evidence, common.source_provenance, release_goal.dependencies_decisions, release_goal.unmet_gates.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.learning.04 — Measures and verification**: Outcome targets, baseline/population/method and acceptance evidence are predeclared; entry and exit requirements are testable and do not conflate tests, acceptance, release and availability. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: release_goal.measures_targets, release_goal.entry_gate, release_goal.exit_gate.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.learning.05 — Priority, size and dependencies**: Scope and sequence fit sourced epic/story priority and size/capacity assumptions; release dependencies, resource constraints and uncertain timing are explicit before any commitment. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: release_goal.included_items, release_goal.dependencies_decisions.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.learning.06 — Applicable assurance and controls**: Actual product/privacy/security/domain approval route, NFRs, recovery and applicable AI controls are specified; required dataset rights, measured thresholds, safety/fallback and monitoring gates cannot be sampled away. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, release_goal.requirements_nfrs, release_goal.approval_authorities, release_goal.rollout_recovery.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "release_goal.ai_release_controls"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.release_goal.learning.07 — Governance and learning**: The release retains separate quality, approval, readiness, acceptance, authorized publication and observed-availability evidence; actual outcome review ownership/window and strategy/roadmap feedback survive go-live. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.state, common.change_history, release_goal.identity_milestone, release_goal.unmet_gates, release_goal.change_history, release_goal.post_release_review.
  Conditional fields: {}.
  Evidence: Current Release goal revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Epic

- **gate.epic.learning.01 — Outcome and traceability**: One coherent capability addresses an evidenced user/operator problem and traces to current strategy/release requirements; its scope is not a collection of unrelated tasks. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.identity, common.traceability, epic.alignment_requirements, epic.problem, epic.capability_outcome.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.learning.02 — Scope and context**: Included/excluded scope and hand-offs are explicit; canonical children have one primary parent and cross-epic contributions use related links rather than duplicate acceptance counts. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.boundary, epic.included_scope, epic.excluded_handoffs, epic.children, epic.primary_parent.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.learning.03 — Discovery and evidence**: The riskiest assumption is ranked by consequence/uncertainty and has a falsifiable test, authorized method/sample, predeclared decision threshold, observed result when due and documented continue/change/stop or bounded authorized risk decision. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.evidence, common.source_provenance, epic.assumption_test, epic.risks_decisions.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.learning.04 — Measures and verification**: The capability completion/outcome boundary has observable measures and child acceptance mapping; uncovered source requirements, unsuccessful children and scope denominators remain visible. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: epic.completion_boundary, epic.child_evidence_gaps, epic.accepted_rollup.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.learning.05 — Priority, size and dependencies**: Priority compares meaningful alternatives and opportunity cost; size is a sourced range/coarse unit with scope, method, uncertainty and dependencies, and true prerequisites are separated from design relationships. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: epic.priority_rationale, epic.size_estimate, epic.dependencies.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.learning.06 — Applicable assurance and controls**: Shared experience/information/interface/quality contracts carry actual applicable access, safety, privacy, accessibility and AI requirements into children; no critical obligation falls between epics or into advisory-only samples. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, epic.shared_contracts, epic.risks_decisions.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "epic.ai_validation_contract"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.epic.learning.07 — Governance and learning**: Actual epic owner/authority, revision, readiness/completion and gaps are distinct; accepted children alone do not prove capability value, and outcome learning feeds strategy/roadmap with an actual owner and next review. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.state, common.change_history, epic.identity_workpackage, epic.gaps_history, epic.outcome_learning.
  Conditional fields: {}.
  Evidence: Current Epic revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### User story

- **gate.user_story.learning.01 — Outcome and traceability**: One bounded user/operator need and observable outcome resolves to its canonical epic/release and original source clauses; supporting/investigation items use their explicit variant rather than invented end-user value. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.identity, common.traceability, user_story.identity_parent, user_story.story_statement, user_story.source_clauses.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.learning.02 — Scope and context**: Trigger/preconditions, main journey, in/out of scope, preserved behaviour and affected users/operators are explicit; the experience can be understood without guessing. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.boundary, user_story.context_trigger, user_story.in_scope, user_story.out_of_scope, user_story.main_journey.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.learning.03 — Discovery and evidence**: Evidence and inspected reuse sources support the need/design; unresolved assumptions/decisions retain exact source, actual owner and resume condition, and source criteria are distinguished from proposed supplements. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.evidence, common.source_provenance, user_story.inspected_components, user_story.source_supplement_separation, user_story.ready_prerequisites.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.learning.04 — Measures and verification**: Identified criteria define observable positive/adverse/refusal/failure/authorization/recovery outcomes as applicable; every criterion maps to an approved evaluation context and expected evidence, with measurable thresholds where required. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: user_story.criteria, user_story.scenario_coverage, user_story.evaluation_mapping, user_story.nfr_thresholds.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.learning.05 — Priority, size and dependencies**: Priority follows sourced outcome, urgency/risk and alternatives; size is an attributable range/coarse unit with method, uncertainty, scope and dependencies, supporting a feasible bounded item. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: user_story.priority_rationale, user_story.size_estimate, user_story.ready_prerequisites.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.learning.06 — Applicable assurance and controls**: Actual operation contracts and side effects, access/accountability, refusal, information continuity, accessibility and NFRs cover applicable risks; AI acceptance metrics/slices, safety/fallback, rights/versioning and monitoring use the pinned module. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, user_story.operation_contracts, user_story.permissions_refusal, user_story.interaction_accessibility, user_story.nfr_thresholds.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "user_story.ai_acceptance_contract"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.user_story.learning.07 — Governance and learning**: Canonical team Ready/Done versions and item-specific additions are linked; quality, specification approval, execution readiness, criterion acceptance and delivery are distinct, with final revision and outcome-learning hand-off current. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.state, common.change_history, user_story.specification_state, user_story.team_ready_reference, user_story.team_done_reference, user_story.outcome_learning.
  Conditional fields: {}.
  Evidence: Current User story revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Acceptance criterion

- **gate.acceptance_criterion.learning.01 — Outcome and traceability**: Criterion ID and owning item resolve to exact source provenance/current specification; a proposed supplement is distinguished from a protected original requirement. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.identity, common.traceability, acceptance_criterion.identity_owner, acceptance_criterion.source_provenance, acceptance_criterion.approval_state.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.learning.02 — Scope and context**: Given/When/Then identify one scenario, trigger, expected observable result and applicable prohibited effects without implementation guesses or hidden side effects. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.boundary, acceptance_criterion.scenario_kind, acceptance_criterion.given, acceptance_criterion.when, acceptance_criterion.then, acceptance_criterion.prohibited_effects.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.learning.03 — Discovery and evidence**: The intended scenario and evaluation design use relevant source/risk evidence and an authorized reproducible context; missing facts or unavailable test inputs remain unresolved rather than guessed. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.evidence, common.source_provenance, acceptance_criterion.source_provenance, acceptance_criterion.evaluation_method.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.learning.04 — Measures and verification**: Measurement defines method, units, threshold, sample/population and uncertainty where relevant; expected evidence can distinguish pass/fail, and AI metrics use fixed dataset/slice/model/prompt revisions. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: acceptance_criterion.measurement, acceptance_criterion.expected_evidence.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.learning.05 — Priority, size and dependencies**: The criterion maps to the owning item priority/risk and feasible verification method; any fixture/sample or predecessor constraint is explicit, and one result is not double-counted across competing criterion IDs. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: acceptance_criterion.identity_owner, acceptance_criterion.evaluation_method, acceptance_criterion.gap_resume.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.learning.06 — Applicable assurance and controls**: The criterion covers its applicable safety/privacy/access/authorization/fallback obligation and prohibited effects; actual AI accuracy and critical-slice/safety thresholds are independently required when this criterion claims AI behaviour. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, acceptance_criterion.prohibited_effects, acceptance_criterion.measurement.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "acceptance_criterion.ai_evaluation_measurement"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.acceptance_criterion.learning.07 — Governance and learning**: Specification approval, not-run/planned execution, observed result and accepted state remain separate; evidence is bound to the current criterion/revision and a failed/skipped/blocked result has a precise follow-up. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.state, common.change_history, acceptance_criterion.approval_state, acceptance_criterion.gap_resume, acceptance_criterion.actual_execution, acceptance_criterion.observed_evidence.
  Conditional fields: {}.
  Evidence: Current Acceptance criterion revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

### Implementation or verification task

- **gate.technical_task.learning.01 — Outcome and traceability**: One bounded implementation/design/operational/manufacturing/verification result has a canonical parent and exact source/criterion links; completing it must contribute to the parent outcome. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.identity, common.traceability, technical_task.parent_owner, technical_task.source_criteria, technical_task.bounded_result.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.learning.02 — Scope and context**: Affected components/processes and exact contracts/specification revision, exclusions and preserved behaviour bound the change; work steps and deliverables are reviewable in the actual product process. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.boundary, technical_task.components_contracts, technical_task.affected_components, technical_task.exclusions_preservation, technical_task.deliverables.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.learning.03 — Discovery and evidence**: Work/reuse/spike claims cite inspected sources and falsifiable investigation where relevant; required evaluation inputs/access and unresolved decisions remain explicit without fabricated facts. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.evidence, common.source_provenance, technical_task.data_environment_access, technical_task.work_steps.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.learning.04 — Measures and verification**: Verification cases and expected outputs map to parent acceptance criteria and actual product qualification method; no mirror-only demonstration substitutes for the declared user/operating requirement. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: technical_task.verification_cases, technical_task.qualification_review.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.learning.05 — Priority, size and dependencies**: Sequence relies on actual predecessor outputs and native completion blockers; parent priority/size and task effort/resource uncertainty support a feasible scope without invented commitments. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: technical_task.predecessors, technical_task.native_blockers, technical_task.work_steps.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.learning.06 — Applicable assurance and controls**: Impacts cover applicable experience, information, interface, access, safety and quality; evaluation access is authorized and AI artifact/held-out/safety/version/promotion evidence meets the pinned module when applicable. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning. Unsampled conditional assurance: resolve product AI yes/no/unknown from the pinned actual context. If AI is used, AI-01 to AI-07 in the pinned module apply at their current-stage requirements: dataset quality/rights, predeclared overall and critical-slice metrics/thresholds, observed safety/refusal/fallback, exact model/prompt/configuration revision, applicable personal-data/jurisdiction decisions and monitoring/drift/rollback. An evidence-backed no-use exclusion must not waive other applicable obligations. Unknown applicability or absent required rights/results is unresolved, never N/A.
  Current-stage required fields: common.context_profile, technical_task.impacts, technical_task.data_environment_access.
  Conditional fields: {"ai": ["common.ai_assurance_reference", "technical_task.ai_artifact_evidence"], "personalData": ["common.personal_data_controls"]}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

- **gate.technical_task.learning.07 — Governance and learning**: Actual task owner/state and canonical team Ready/Done versions are current; task completion, parent acceptance and release/availability remain distinct, and actual outputs plus learning/follow-up are handed to the owning story/release. Learning stage: after the agreed observation period compare actual outcomes with the original target/hypothesis under compatible metric/population definitions; retain uncertainty, counterevidence and unintended effects. Record a sourced continue/change/stop decision, actual owner, canonical strategy/roadmap feedback or explicit no-change rationale, and next measurement. A future/pending review does not claim completed learning.
  Current-stage required fields: common.state, common.change_history, technical_task.identity_type, technical_task.team_ready_reference, technical_task.team_done_reference, technical_task.actual_outputs, technical_task.blocker_owner_resume.
  Conditional fields: {}.
  Evidence: Current Implementation or verification task revision; explicit applicable field components and pinned authoritative sources. Exact evidence locators and stage-specific decision/evaluation/observation records; no invented facts or substituted future results.

## AI assurance and post-release learning

ai-assurance.json defines seven conditional assurance groups; AI-01 scope/authority, AI-02 dataset quality/rights, AI-03 measurable evaluation, AI-04 safety/fallback, AI-05 versions/promotion, AI-06 privacy/legal applicability, AI-07 monitoring/learning. An actual AI record is pinned by ID/version/content hash and mapped to common.context_profile and relevant AI fields. This intake is not automatically accepted engine input. Use current authoritative legal sources and actual reviewed applicability; no template can approve legal compliance.

Learning remains active after availability: compare actual results to original targets, disclose uncertainty/unintended effects, record a continue/change/stop decision, and feed canonical strategy/roadmap records with actual owners and a next review. A go-live announcement or process retrospective is insufficient.
