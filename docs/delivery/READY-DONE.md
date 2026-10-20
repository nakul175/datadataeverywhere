# Proposed Ready and Done checklist, version 1

Status: proposed for owner review. This is not a recorded owner approval.

Before implementation: identify the actual work item and source revision; define observable acceptance and exclusions; classify engineering and QA risk separately; freeze relevant criterion/case versions; identify dependencies, data/environment ownership and runnable verification. Unknown critical authority holds the dependent action.

Before merge: pass actual format/lint/types/build/dependency/secrets/tests and applicable native PM/QA/engineering checks on the final head; publish source-linked evidence; preserve skipped/failed/flaky results; obtain an independent authorized review and any required owner decisions. Missing or skipped required checks cannot satisfy the aggregate gate.

Before release: identify the immutable artifact and source; obtain release authority; record migrations, rollback, resource and data bounds; run the applicable native release assessment; serialize changes to shared production. Observe the deployed version and declared live journey. Merge, deployment, acceptance and outcome learning are distinct states.

AI changes additionally require versioned prompt/model/context and adversarial evaluation, approved data provenance and privacy scope, budget enforcement, fallback behavior and an actual provider run in the authorized environment. No live provider result is claimed by mock tests.

There is one exception register: .governance/exceptions.json. It is empty because no exceptions have been approved. Parallelism remains one worker; no atomic lease backend or parallel controller is qualified.
