# Product context and applicability

Edition 3.0 generic. Establish the actual product, assessment scope and lifecycle stage before using the hierarchy or checker. This framework works across product and service types. It does not supply product facts, legal applicability, owners, targets, providers, release permission or an operating environment.

## 1. Establish the product and decision

- Product identity and type; the problem, desired outcomes and existing or non-product baseline.
- Primary users, affected people, operators and stakeholders; operating environment and constraints.
- Exact scope, parent records, canonical workspace, protected requirements and frozen revisions.
- Authoritative source content, version and locator, including what is current, approved, proposed or disputed.
- Lifecycle stage: `discovery`, `planning`, `ready`, `delivery` or `learning`; the particular gate being assessed now.
- Actual decision owners, expertise and bounded authority, supported by existing sources. A missing owner remains unknown.
- Existing systems, resources, dependencies, interfaces, access and approved constraints.
- Applicable accessibility, safety, privacy, security, domain, contractual and regulatory obligations, their source versions and current applicability.
- The relevant acceptance and separate quality, approval, readiness, delivery and learning conditions.
- Known unknowns, the next required question and evidence needed to resolve it.

Do not infer a technology stack, workflow, device, delivery channel, repository, service provider, budget, date or authority from this generic framework. Tasks may concern software, design, operations, manufacturing, research or verification. Use the product's actual artifact revision and operating release identifier. Compatibility mappings preserve legacy software field IDs; they do not impose software deployment on another product type.

## 2. Declare applicability explicitly

The executable assessment uses `document.productProfile.ai` and `document.productProfile.personalData`, each shaped as:

```json
{
  "applicability": "yes|no|unknown",
  "sourceIds": [],
  "rationale": "The actual scope facts and why this branch follows from them",
  "resolutionPlan": null
}
```

Set `yes` when the actual scope or a material dependency uses AI or processes personal data. Set `no` only with scope-covering authoritative evidence. An absence of information is `unknown`, not `no`. AI used in document authoring is declared separately from AI in the delivered product, and its project-data permissions still apply.

Discovery permits unresolved applicability only with a meaningful `resolutionPlan`, supporting source IDs and rationale establishing the actual scope, and a clear authorised test boundary. A blank plan or unsupported scope remains `needs_input`. Decisions in planning, readiness, delivery and learning that depend on the unknown remain `needs_input`. Apply the relevant stage requirements; do not demand live results in discovery or treat a complete test plan as an observed pass.

For actual AI use, link one scoped, versioned AI assurance record from `AI-ASSURANCE.md` and `ai-assurance.template.json`. Its seven consolidated groups cover use/authority, dataset quality, measured acceptance, safety/fallback, versioning/regression, privacy/law and monitoring/learning. They support the hierarchy's stage gates; they do not add hundreds of per-detail review verdicts.

Legal obligations are jurisdiction- and fact-dependent. The optional India DPDP review is an applicability branch with primary source references and phased commencement, not a universal condition imposed on every project. Confirm current duties and the actual release date with the responsible qualified reviewer. A template date cannot certify later compliance.

## 3. Use one team readiness and one team completion definition

Create or locate one authoritative team readiness checklist and one authoritative team completion checklist, each with ID, version, content hash, source reference, criteria and review/approval authority. User stories and tasks link to the applicable versions rather than copying separate definitions into every record. Keep outcome-specific acceptance criteria on the story; the team checklist does not replace them.

Readiness records the conditions needed to begin the intended delivery work: sufficiently resolved scope and decisions, testable criteria, required dependencies and permissions, feasible validation, relevant risks and evidence plan. Completion records the conditions needed to claim the scope complete: observed acceptance, required validation and risk controls, separate approvals, artifact/delivery evidence and required operational or learning handoff. Each criterion applies only when its factual and stage conditions exist.

Changing a checklist triggers impact analysis for linked items and makes affected old reviews stale. A checklist does not grant authority, convert planned evidence to observed evidence or collapse quality, approval, readiness and delivery into one status.

## 4. Keep discovery, priority, sizing and learning explicit

An epic identifies its riskiest material assumption, the test that could disprove it, target population, evidence, success/failure decision and effect on the proposed solution. An experiment must stay within actual data, participant, spending and action permissions.

Epics and user stories record a priority rationale that compares value, urgency, risk reduction, dependency and opportunity cost against the relevant alternatives. A priority number without its method and supporting evidence is not a rationale. Record a size estimate with the actual unit, method, range, assumptions, dependencies, confidence and estimator evidence. Estimates are forecasts, not invented commitments; unknown size remains pending where the decision requires it.

Every release has a learning review for a declared window: target, baseline and observed result; relevant denominators and uncertainty; incidents and unexpected outcomes; and a continue, improve, narrow, roll back or retire decision made within real authority. Link the decision and resulting actions back to strategy and roadmap. A successful release and a measured improvement in user outcomes remain separate facts.

## 5. Use stage gates and sampled supporting reviews

Use the small must-pass gate set for the current element and stage. The exhaustive reference catalogue supports diagnosis and deeper review; it is not an instruction to create one mandatory human verdict for every reference detail on every run. Record the supporting-sample population, selection method, seed where relevant, risk rationale, coverage and escalation rule. Sampling never removes a stage-applicable must-pass requirement, protected right, required permission, safety invariant, release target or failure that has already been observed.

Reuse current shared evidence by reference and pin. Review affected changes and assumptions rather than copying verdicts blindly. Changed content, sources, applicability, checklist or release versions make affected previous reviews stale. New evidence can reveal new questions; repeated identical unanswered questions do not count as progress.

The authoring agent cannot create its own trusted independent reviewers. Offline mode is advisory: it checks supplied claims and consistency, not identity or external authority. Where approval or independent review is required, use the team's externally established reviewer registry or review service and its actual trust mechanism. A local record naming `reviewer-2` is not that mechanism.

## 6. Map intake to the executable assessment

`product-context.template.json` and `ai-assurance.template.json` are intake aids. They are not the checker's input schema, are not automatically imported, and do not become approvals when completed. Nulls and empty required evidence remain unresolved. Preserve the filled source-backed intake for review and map relevant facts into the executable document:

1. Resolve source references to actual `sources` records and pin the authoritative content/version.
2. Map the exact scope and stage to the assessment and its `productProfile` branches.
3. Record profile/checklist/assurance versions and hashes in `common.context_profile`, `common.ai_assurance_reference`, `common.personal_data_controls` when applicable, and the relevant element fields.
4. Link the applicable team checklists, discovery tests, priority/size evidence and learning records to their catalogue fields.
5. Attach evidence to the stage's consolidated reviews and keep external approval records distinct.
6. Report passed/total must-pass gates, sampled-support coverage, unresolved questions, stale evidence and the actual quality/approval/readiness/delivery/learning statuses.

The profile cannot waive a protected requirement, overwrite the rule catalogue or create a source, owner or result. Use existing authorised access. Record accessible evidence references rather than credentials or unnecessary raw personal data.
