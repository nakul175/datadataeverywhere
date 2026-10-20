# Workflow and Process Orchestration Guide

Version 2.0 | Reusable operating procedure | 11 October 2026

Give this bundle to an agent together with the current product plan, repository and project access. It defines the sequence for taking one approved user story through implementation, testing, review and observed delivery. The product plan defines what to build; this playbook defines how to execute and record the work.

## The required order

Check current state → summarize evidence → select the next authorized step → execute or fix → check again. Repeat this outer loop throughout the workflow. Never skip a failed gate simply because the next step is available.

| Phase | Required output |
| --- | --- |
| 1 Inspect and resume | Fresh source, authority, status and existing evidence |
| 2 Select and freeze | One story, linked tasks, testable criteria and test plan |
| 3 Prepare and implement | Authorized environment and isolated change |
| 4 Test and repair | Actual native results, defects and new retest records |
| 5 Publish and review | Verified links, current CI and independent decision |
| 6 Release and learn | Observed version, live checks and measured follow-up |

## What this bundle establishes

The procedure is generic. Linear, GitHub, Playwright and k6 are adapter examples. Equivalent planning, source-control and runner tools can be substituted without changing the evidence or approval requirements. The supplied companion packages are pinned in PACKAGE-LOCK.json; project-specific bindings belong in the adopting repository.

This is an operating template, not an installed autonomous service or a product certification. Existing project protections, human approvals and domain requirements still apply. A checklist completion is not proof that its claims are true.

## Files to read

Start with START-HERE.md, AGENTS.md and PROJECT-CONFIG.template.json. Human reviewers use this guide; agents use PROCESS.md as the same procedure in text form. Do not load both by default. Consult the gate checklist at each transition and load templates as needed. Do not load audit history by default. For integrity checks use only audit/BUNDLE-MANIFEST.json; historical manifests never certify this version.

# Four package authority contract

Workflow version 2.0 composes the supplied Product Management 4.2, Testing and QA 1.3 and Coding and Engineering 2.1.0 distributions. Archive hashes and manifest checks are recorded in PACKAGE-LOCK.json. This version replaces the earlier standalone testing playbook as the process specification.

| Package | Owns and remains authoritative |
| --- | --- |
| Product management | Vision, priorities, release scope, epic/story/criterion/task identity, product quality and team Ready/Done |
| Testing and QA | Risk, case/version mappings, native execution records, coverage, quality and release verification |
| Coding and engineering | Architecture, implementation constraints, command execution, native adapters and technical review |
| Workflow and process | Stage routing, prerequisite checks, task allocation, handoff, tool selection and delivery reconciliation |

The workflow selects and invokes each native package; it does not copy their catalogues into a fourth standard. Obligations are conjunctive. Product scope does not waive QA or engineering rules, and engineering cannot infer product authority from prose. An unresolved conflict holds its dependent action and routes a decision to the responsible owners.

## One baseline for each story

Bind the package versions and hashes, approved product source, criterion/case versions, task links, team checklist, exception register and source revision before qualification. Keep one canonical product task key and one selected exception authority. Workflow events reference native IDs rather than allocating another backlog or replacing native status vocabulary.

## Adoption must establish real connections

The engineering distribution provides connect_bundles.py and the native_bridge.py implementation. Its README says the actual companion archives were unavailable during its construction. These newer supplied companion versions therefore require actual adapter, native command and field-map qualification; a successful file inventory does not prove compatibility.

Use the engineering connection helper first in read-only proposal mode with the actual PM 4.2 and QA 1.3 versions. Resolve missing product-owned typed task-criterion links, actual owners and native QA arguments. Review and approve the repository-specific binding before installing or executing reviewed commands. No owner, approval, command or deployment target is prefilled by this workflow package.

# Routing tools and native checks

## Invoke the owning package at the correct stage

| Stage | Native authority and invocation |
| --- | --- |
| Product check and readiness | PM checker loop → summary → next; select relevant stage and actual external trust store |
| Connection and technical planning | Engineering connect_bundles.py read-only proposal; approved integration manifest and typed task links |
| Implementation | Engineering root router, profile and reviewed commands; repository conventions and approved product task |
| Verification | QA TASK-ROUTING and risk tier; actual unit/API/browser/performance tools plus native qa_lint.py |
| PR and integration | Engineering audit and run, actual required CI, final diff review and native QA record checks |
| Release candidate | Native QA --release on complete qualification snapshot, required specialist/UAT decisions and team checklist |
| Deployment and outcomes | Authorized release mechanism, observed version/live checks and native product learning records |

COMMAND-ROUTING.md records observed native paths and CLI examples. They are templates, not shell commands to run blindly. Resolve actual repository paths, command arguments and tool versions, review code and action authority, then execute through the engineering runner when its approved profile applies. Preserve native exit semantics; a PM unresolved exit is not an engineering pass.

## Tool responsibilities

Linear or an equivalent tracker stores canonical planning and readable progress. GitHub or equivalent source control stores reviewed changes and CI evidence. Playwright executes applicable browser tests; k6 executes approved performance workloads. Existing unit/API/security tools stay in their native pipeline. Select existing tools from the project profile; do not force every tool onto every low-risk change.

The QA Low-tier fast path and engineering C0–C3 classification remain native. Record both classifications and their scoped applicability; do not equate their labels mechanically. Full release ceremony applies to release scope. Lightweight work still requires meaningful applicable tests and cannot use a risk label to bypass mandatory security or authorization controls.

The workflow checks that required tools were actually invoked, outputs belong to the candidate and their native results are retained. Missing tools, zero/all-skipped execution, failed startup or absent reports hold the relevant gate. A connector readback verifies publication only, not semantic quality or approval.

# Parallel assembly line and integration

## Allocate work from a dependency graph

Build a graph of canonical tasks and dependencies inside the selected release scope. A task is eligible only when its native readiness, authority and predecessor requirements pass. Default concurrency is one; increase it only under the project-approved capacity and environment budget. Separate independent tasks may run in parallel without marking their parent story delivered.

## Lease and isolation contract

Before assignment, the controller records a unique lease ID, canonical task ID, agent identity, exact base, branch/worktree, owned paths, dependency versions, environment/data ownership, resource budget, expiry and heartbeat. Lease acquisition must be atomic in the chosen durable backend. The controller must not claim atomicity from an ordinary JSON file.

Use isolated branches/worktrees and synthetic environments per worker. Serialize conflicting paths, schema/migration changes, shared fixtures and policy files under explicit locks. No concurrent writes to shared QA CSV registers or approval records. Workers produce separate immutable run records; one integrator validates and appends them through reviewed merges.

## Review and integrate in order

Workers hand off actual source, diff, native run IDs, artifacts, held gates and cleanup status. The reviewer uses a verified independent identity and the current candidate; self-created aliases never count. Integrate dependency order using the existing protected merge mechanism. After a base or contract change, rebase or merge safely and retest the affected integration candidate before qualification.

## Recover interrupted work

On lease expiry or agent failure, first check fresh branch, native records and environment ownership. Reassignment requires a new fenced lease/version so a returning old worker cannot publish authoritative changes. Recover through compare-and-set or equivalent controller guarantees. Release only owned resources and retain incomplete evidence. Stop new allocation when the approved budget or deadline is exhausted; this is not success.

PARALLEL-WORK.template.json specifies the required dispatch and handoff fields. This package supplies the design and review contract; it does not implement a lease server, worker scheduler or distributed locking service. The chosen backend needs concurrency and interruption tests before parallel activation.

# CI CD enforcement and activation

## Required pipeline structure

Bootstrap validates approved package pins and native bindings. PR jobs execute applicable engineering checks, actual tests and QA record checks. Integration jobs qualify the exact merge candidate. Release jobs add complete native QA release and specialist/UAT decisions. Authorized deployment jobs deliver the selected artifact; subsequent jobs observe the actual version, health and declared live journey.

An always-run aggregator evaluates every required child result for the exact candidate. Only actual successful executed checks satisfy a required check. Missing, skipped, neutral, cancelled, timed-out or unavailable children hold/fail the aggregate. The QA package explicitly requires this behavior; a green interface is insufficient. Never let a PR change its own required-check list without protected review.

## Trust and release controls

Pin policy and workflow changes under independently reviewed ownership and verified server rules. Use least privilege and keep secrets out of untrusted pull-request execution. Record required check names, reporting authority, candidate identity, workflow revision, native commands, resource limits and artifact retention. Native checkers cannot authenticate CI source, reviewers or branch-protection settings offline.

Keep merge authority separate from deployment and live data authority. Define environment approval, rollback triggers, migrations, observation window and accountable operator before activation. Serial release to a shared environment prevents one candidate from replacing another during qualification. Preserve source-to-artifact-to-observed-deployment linkage.

## Activation evidence required

Before calling the assembly line enforced, demonstrate in an authorized safe repository that a deliberately failed required check prevents merge; skipped and missing required jobs cannot qualify; a changed head invalidates prior qualification; policy changes require the configured reviewer; expired leases cannot publish; and a failed live smoke holds completion and follows the approved rollback decision.

## Current delivery boundary

This bundle is a reviewed-by-author workflow specification with pinned input distributions, templates and byte-integrity checks. No product repository was adopted, companion native checkers executed, live scheduler installed, server protection changed or CI/CD activated while producing it. Those are explicit adoption stages, not implied outcomes. ACTIVATION-CHECKLIST.md records the remaining operational evidence.

# Authority and responsibilities

## Authority before action

Inspect repository instructions, product decisions, protected branches, existing pull requests and actual external status before editing. Preserve existing work and reuse only individually verified components. User authorization determines scope; an access token alone does not authorize a purchase, production write or message to another person.

Use safe reversible assumptions for wording or implementation choices and label them with rationale. Do not assume authority, user consent, acceptance, clinical policy, real-data access, an owner identity or a required human approval. Missing authority or a safety-critical decision blocks dependent work; independent safe work may continue.

## Accountability

| Role | Responsibility |
| --- | --- |
| Product decision maker | Approves scope and material criterion changes; confirms business acceptance when required |
| Implementation agent | Builds the isolated change and preserves actual results and limitations |
| Test executor | Runs frozen tests and records failures, retries and incomplete work |
| Independent reviewer | Reviews the current diff and evidence within a verified external identity |
| Release operator | Obeys protection rules and observes the delivered version and live checks |

One agent may implement and execute tests, but those actions do not establish independent review. The author cannot create a second reviewer identity and treat it as independent approval. Reviewer identity and authority must come from a trusted system or human outside the authoring agent. Offline review is advisory only.

## Four decisions remain separate

Documentation quality measures the clarity and completeness of a plan. Readiness permits implementation. Approval records a qualified reviewer or human decision. Delivery requires observed release evidence. None automatically implies the others.

UAT means acceptance by an authorized user or representative. A Playwright journey can provide evidence for UAT, but cannot manufacture the human decision. Conditional domain, privacy or safety approvals must be specified before work starts.

# Inspect select and freeze

## Step 1 Inspect and resume

Read the project configuration and current product hierarchy. Fetch fresh issue, branch, pull request and deployment status. Identify the exact source version, previous unfinished run and outstanding blocker. Compare local changes before creating a branch. Record observed facts with timestamps and links. Do not rerun a completed stage merely because a new agent starts.

## Step 2 Select one authorized story

Choose the highest-priority eligible story whose dependencies and readiness gate are satisfied. Record the release goal, epic, story and owning tasks by stable identifiers. Reuse an existing authorized branch or create an isolated branch from verified current main according to repository rules. Keep one active delivery story unless explicit parallel scope is authorized.

## Step 3 Freeze the execution contract

Record user outcome, scope and exclusions; acceptance criteria; UX and accessibility; data/API and permission rules; nonfunctional requirements (NFRs); dependency decisions; and Definition of Ready/Done versions. Each criterion needs an observable expected result and evidence method. Preserve product traceability without duplicating the same scenario under every parent.

A scenario describes a behavior and conditions. A test case specifies fixtures, actions and an oracle, which is the rule for deciding whether the result is correct. An assertion is an individual check during execution. A test run is an execution record. These units have different denominators and must never be added together as a single passed-test count.

## Required test planning

Select positive, refusal, authorization, validation/error, empty-state and recovery cases where applicable. Include regression and performance coverage based on affected behavior. Freeze dataset provenance, expected results, samples, duration, workload, thresholds, timeout and retry policy. Record each applicability decision; mandatory applicable checks cannot be sampled away.

Each case maps to stable scenario and criterion IDs and all owning stories/tasks. Deduplicate only identical preconditions, behavior, oracle and constraints; preserve every ownership link. Similar wording with different authorization, actors or environments remains separate. Contract changes need a decision record and new version before dependent results can qualify.

# Prepare and implement

## Step 4 Prepare the environment

Verify tool versions, dependencies, fixtures, isolated backend, safe target URLs and authorized credentials without exposing secrets. Use synthetic or explicitly approved de-identified data. Establish whether the environment is local, CI, staging or production and what it can prove. Confirm resource caps, teardown and redaction rules.

Use the project-defined readiness gate before coding. If the source, authority or oracle is missing, mark the stage held with the precise missing input. Do not turn a placeholder into a pass or invent an approval. A surrogate device/network must be labelled; it does not certify the actual target environment.

## Step 5 Implement the story and tests

Build the smallest complete user outcome, with meaningful tests and explicit scenario linkage. Reuse authoritative identity, server-side scoping and audit behavior. Avoid unrelated refactors, bulk merges and alternative databases or providers unless authorized. Preserve existing criteria and baselines.

Record changed files, rationale and any risk. Save meaningful checkpoints, then pin the exact tested source version. A dirty worktree needs a content manifest that includes changed and untracked execution inputs; otherwise it cannot claim an exact commit test. Include backend, schema, fixtures and relevant generated inputs in applicability evidence.

## Step 6 Execute relevant checks

Run the real build, static checks, unit/API/auth tests, browser journeys and approved performance tests that apply to this change. Capture command, tool version, start/end time, exit code, environment and native output. A command failing before test startup means zero product tests executed. Preserve the startup failure separately.

Use bounded timeouts and approved workloads. Do not add a paid provider, widen data permissions or remove protection rules to obtain a result. For an unexpected credential or environment failure, diagnose without printing secrets and record the exact blocker. Teardown only resources created and owned by this run.

# Runner linkage and evidence

## Playwright adapter

Annotate each relevant case with explicit scenario IDs. Preserve native case identity, expected and actual status, attempts, errors, retries, screenshots and traces when configured. Unknown IDs fail linkage; unannotated tests remain unmapped. A browser action passing with invalid linkage does not satisfy its scenario gate. A retry-then-pass remains flaky unless a separately approved policy allows qualification.

## k6 adapter

Record the approved target, model, virtual users, iterations or arrival rate, duration, samples, requests, check counts, errors and native threshold outcomes. Check successes alone do not imply a performance pass. Missing thresholds, incomplete workload, discarded slow samples or exhausted retries keep the gate held. A reporting smoke cannot certify the product load profile.

## Native and linked reports

Save raw native evidence first, then normalize it into a linked report without changing outcomes. Use a unique run ID and a new output location. Never overwrite earlier failed runs. The report must retain exact source/environment identity, tool and test-contract versions, coverage and result scope. Attach hashes and stable artifact links; identify local-only attachments explicitly.

| Record group | Required details |
| --- | --- |
| Identity | Run ID, UTC timestamps, source version, environment and runner version |
| Traceability | Release, epic, story, task, criterion, scenario and case IDs |
| Execution | Command, exits, attempts, samples, failures and incomplete work |
| Evidence | Native reports, artifact URLs, hashes, access and retention policy |
| Decision | Gate outcomes, limitations, blockers and reviewer authority |

Do not expose secrets, personal data or access tokens in reports or traces. Restrict artifact access and retention to project policy. If necessary, retain a protected original and publish a redacted derivative with its own hash and provenance. A hash proves byte equality, not truth or independent approval.

# Repair publish and review

## Step 7 Fix and retest

Classify the defect as product, test, mapping, environment or reporting failure using the actual output. Link it to the affected criterion and owning task. Preserve the failing run; implement a scoped correction; record a new source version; and run the affected checks plus justified regressions in a new run. Never increase a lint baseline or relax a performance threshold merely to pass.

A changed executable, fixture, model, prompt, criterion or environment makes relevant old evidence stale. Invalidate dependent approvals and gates, then retest the affected scope. Documentation-only changes can reuse evidence only with an explicit byte/source applicability check. Do not claim that an old green CI run belongs to a new head.

## Step 8 Publish and reconcile

Publish native artifacts to the approved evidence store and append a readable run summary in the planning system. Record failures, skipped cases, flakes and unexecuted scope. Deduplicate by the actual run ID and verify saved readback. If publication fails after execution, retain local evidence and mark publication pending; do not rerun tests solely to retry a save.

After an unknown write outcome, retrieve the existing record before retrying. Keep one canonical scenario register and reference it from tasks; avoid copying the same results into competing records. A planning document contains summaries and links, not necessarily every byte of every historical test log.

## Step 9 Review the final change

Create or update the isolated pull request with the final scope, current source and validation limits. Complete actual required continuous integration (CI) checks for that exact head and obtain independent review and required human/domain approval. Inspect the final diff and raw evidence, including refusals and failure history. Respect branch protection and do not bypass checks.

A local pass, documentation check, author self-review or advisory checklist cannot grant independent approval. If a required reviewer, CI or UAT is unavailable, the qualified release decision stays held. Publish the precise blocker and safe next action rather than asserting completion.

# Release verify and learn

## Step 10 Release through the authorized path

Merge or release only the isolated qualified change when all required checks and approvals apply to the current source. Record the actual released version and release event. Respect existing hosting and rollback policy. A merged commit is not evidence that hosting has updated; a successful deployment event is not evidence that the user journey works.

## Step 11 Observe live delivery

Use authorized existing access to verify the exact running version and perform the declared synthetic live smoke. Record URL/environment, observed version, actor/role, actions, result and timestamp. Temporary role or permission changes require their own authorization and guaranteed restoration; record restoration even after failure. Avoid real recipients and real patient data.

If access, version observation or the required journey is blocked, report merge/release and live verification separately. Mark the story Done only after its declared Definition of Done and acceptance gate are satisfied. Tasks may finish independently without granting story or epic completion.

## Step 12 Learn and select the next story

Compare measured release outcomes against the frozen business and operational targets at the agreed review date. Record actual adoption, outcome, failures and support signals; separate missing data from a measured zero. Feed findings into assumptions, strategy, roadmap, priority and future tests. Obtain the required decision for material plan changes.

Proceed to the next eligible story only after the current delivery gate or an explicitly authorized handoff. A future measurement window may remain pending if the project Definition of Done separates delivery from outcome validation. Do not claim a future metric as measured.

## AI features when applicable

Version the model, prompt, tools and evaluation dataset with the source. Freeze representative and adversarial cases, consent/provenance, accuracy and safety targets, refusal/fallback behavior and privacy constraints. Include approved human review, drift monitoring and rollback triggers. Verify applicable legal requirements with the qualified project authority. Do not invent thresholds or legal clearance; an AI gate stays held until required inputs and actual evaluations exist.

# Gates status and handoff

## Seven readiness checks

All applicable checks must be satisfied before implementation: 1 authorized scope; 2 clear user outcome and boundaries; 3 traceable measurable criteria; 4 resolved critical dependencies and authority; 5 versioned fixtures, oracles and NFR workload; 6 safe runnable environment; 7 linked owning tasks and approved Ready/Done definitions. A justified non-applicable decision is recorded, not silently omitted.

## Seven delivery checks

All applicable checks must be satisfied before story completion: 1 current implementation/source identified; 2 declared applicable tests actually pass with complete workloads; 3 required CI passes on final head; 4 evidence published and read back; 5 independent and required human approvals valid; 6 exact release and live journey observed; 7 Done checklist and outstanding limitations reconciled. Outcome-learning gates apply when the project explicitly includes them in Done.

## Blocker and resume rules

On a blocker, record the held gate, actual error, source/environment, safe work completed, required decision or access and next authorized action. Stop dependent transitions while continuing useful authorized independent work. No fixed number of questions guarantees truth. Ask again when new missing decisions arise; safe labelled recommendations may proceed within authorization.

At handoff, provide the source version, branch/PR, active story and task IDs, completed steps, actual run IDs, evidence links, stale evidence, unresolved gates, environment ownership, cleanup state and next action. The receiving agent checks fresh external state before resuming. Never restart the entire workflow automatically.

## Progress report

Use separate rows for epics, user stories, tasks, criteria, cases, assertions, performance workload, CI, release and observed hosting. Give total and completed counts with their source/time and result scope. Unknown totals remain unknown. State one active story, current gate, exact source and blocker in plain language. Do not add browser cases, k6 checks and assertions into one inflated total.

## Maintaining this template

Policy changes require explicit owner decisions and a new version. Do not weaken criteria to obtain a pass. Rehash a changed bundle only after its authorized change is reviewed; the in-bundle manifest checks integrity, while an externally pinned digest establishes provenance. This playbook specifies behavior; it is not an automated semantic or approval checker.
