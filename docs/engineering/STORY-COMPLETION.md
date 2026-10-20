# Story completion implementation and qualification

Authorization record: the user requested “Complete all stories” on 20 October 2026, then explicitly requested “make an agent for yourself to act as a reviewr”. This authorizes bounded development and a separate technical reviewer; it does not fill the native owner/release approvals described below.

This is a C2 development change authorized by the owner's request to complete the backlog. Work is on `feat/story-completion`, stacked on the unmerged standards-adoption branch. Native plan, task allocation, QA mappings and independent acceptance remain draft; no release gate or exception is silently approved. Linear technical tasks APL-3001–3008 own the eight bounded changes below. Their descriptions and `.engineering/traceability.json` identify exact criterion allocation, not accepted coverage.

## Implemented development scope

| Story | Technical task | Change | Evidence boundary |
| --- | --- | --- | --- |
| DDE-48 | APL-3001 | Explicit whole-table query alongside unchanged page search/sort; schema-based text/sort allowlists and primary-key tie-break; 50-row pages | Typed contract and compiled-app synthetic test. Actual installed NocoDB compatibility still requires isolated qualification. |
| DDE-39 | APL-3002 | Refuse complex/unknown AI field types and any object/array value; authenticated bounded preview uses the same reader and no provider | Controlled refusal/preview tests. No nested sharing consent or legal/privacy approval inferred. |
| DDE-42 | APL-3003 | Coordinated stopped-service archive includes compiled app, protected runtime/access files, service unit and all SQLite state; checksummed isolated restore refuses overwrites/traversal | Unified file/SQLite restore tested locally; full PostgreSQL/NocoDB restore and recovery objectives remain pending. |
| DDE-47 | APL-3004 | Checked server-side HTTPS task/native URLs; default task host is the responding Aplyd deployment | HTTPS target checked; the modified navigation is not deployed. |
| DDE-40 | APL-3005 | Keep process liveness; add authenticated dependency readiness without provider calls or secret output | Compiled fixture checks do not certify production readiness. |
| DDE-34 | APL-3006 | Abort chat and preview work on panel/table unmount | Real provider cancellation and billing still need qualification. |
| DDE-36 | APL-3007 | Bound Redis connect/command attempts; preserve no-refund atomic reservations | Disposable Redis and SQLite tests; not a 50-user workload result. |
| DDE-38 | APL-3008 | Central provider/model readiness; explicit Anthropic model required; no guessed replacement alias | Configuration tests and stream-construction stub; no actual provider inference. |

The context reader also enforces its 100-row ceiling when an upstream ignores requested page size. Oversized workspace pages are refused rather than silently truncated. CI runs the Python recovery suite and compiled-app smoke in addition to all application tests; native readiness remains a separate required gate.

## Query API contract

`GET /api/workspace?action=records&tableId=...&scope=table` accepts optional `query`, `fieldId`, `sortId`, `direction=asc|desc` and bounded integer `offset`. `fieldId` and `sortId` are IDs from the currently authorized schema, never raw names/operators. A nonempty search requires a supported simple text field. Search text is at most 200 letters/numbers/spaces/dots/at/plus/minus/underscore; underscore is escaped as a literal LIKE character. Unknown/repeated parameters, raw filter syntax, unsupported field names/types and ambiguous keys are refused. Full-table queries require one supported primary key and add it as a deterministic tie-break.

This follows the [NocoDB v2 query contract](https://nocodb.com/apis/v2/data). Response scope is explicit; filtered totals are not inferred from an upstream unqualified count. Ordering is deterministic for a quiescent dataset; live offset pages can still shift under writes. This is not a consistent export. Existing page-local search/sort remains separate and clearly labeled.

## AI and operations contracts

`POST /api/ai/context` requires the same origin, current identity and explicit user/table/field grant as chat. It reserves 32,000 conservative units with the existing rate/concurrency/daily gate, reads the same 100-row/24,000-byte context and releases its lease. It makes no model call and returns no-store. The UI warns that a later question fetches a new sample. Complex fields and unexpected nested values fail closed; no automatic grant expansion or recursive disclosure occurs.

OpenAI uses `OPENAI_MODEL` or the existing `gpt-4o` default. Anthropic requires an explicit `ANTHROPIC_MODEL`. Both require privately configured credentials. Readiness reports configuration presence separately from provider connectivity/quality. No model is claimed available or qualified from its source default.

`GET /api/health` remains process liveness. Authenticated `/api/health/ready` checks the engine health endpoint, budget store and access-policy parse with bounded I/O. It does not certify database recovery, role semantics or provider quality. Public tool URLs require HTTPS without embedded credentials, query or fragment; `TASKS_PUBLIC_URL` defaults to `https://sheethappensofficer.aplyd.org` and `NOCODB_PUBLIC_URL` preserves the native-host default.

The unified backup helper requires Python 3.12 and a stopped service. The coordinated backup script stops/restarts only the previously active unified service around engine snapshots and refuses unknown service state. The root Docker backup and the user's shared directory must be captured together. Backup files include secrets and must be encrypted and access-controlled before offsite transfer. Restore is for a new isolated installation, requires the original service user/home/path, rejects existing app/unit/data volumes and never starts the restored user service automatically. Operator review and a full database restore drill remain mandatory.

## Isolated actual-engine qualification

`docker-compose.qualification.yml` creates a separate `dde-qualification` project, internal database network plus an engine-only HTTP bridge, new PostgreSQL/NocoDB volumes, loopback-only port 19080 and bounded memory. The qualification-only NocoDB limit is 1536 MiB with a 1024 MiB JavaScript heap; the previous 768 MiB container failed startup with a recorded V8 heap exhaustion. It never mounts production volumes or imports the production environment file. The runner refuses startup below 3 GiB available memory; this is a containment preflight, not a service-level objective. Prefer a dedicated test host.

On an approved Ubuntu test host with Docker administration, Python 3.12 and Node 22+:

```bash
bash scripts/start-qualification.sh
```

This creates private random fixture credentials in ignored `.qualification/stack.env`, starts the isolated stack, then checks actual v1 authentication, the starter schema, 257 synthetic rows, pagination, full-table filter/sort and PATCH persistence. The report is private `.quality/evidence/engine-qualification.json`. The Compose configuration has been validated with the existing server's CLI without starting containers. No actual-engine qualification result is claimed until the runner succeeds. Keep the isolated data until evidence is reviewed; do not substitute production for this test environment.

The deploy account currently cannot run Docker/root operations. No broad privilege was granted. An actual operator must execute the approved test/restore work. Production and its neighboring app are unchanged.

## Why governed feeds remain held

DDE-01–04 require explicit delegable permissions, consistent complete snapshots, resumable export, schema/change semantics and live revocation. The current NocoDB REST reader exposes paging, not an authenticated change watermark or transaction snapshot. Two equal scans, modified timestamps and webhooks alone cannot prove that relevant inserts/deletes/ABA changes were absent. Reusing the AI sample or labeling a mixed REST extraction consistent would violate the original criteria.

A viable next design is an explicitly configured PostgreSQL read-only snapshot adapter with reviewed physical table/column mapping and an effective row/delegation policy, or a source API with a qualified snapshot/change contract. Snapshot materialization must be bounded, permission checks remain live on every page, and policy/schema changes invalidate cursors. No source database credentials, RLS/delegation contract or independently reviewed access adapter has been supplied. Do not invent that authority from a UI session or silently bypass NocoDB access rules. These decisions must be resolved before implementing a purportedly complete external feed. No feed is published by this branch.

## Verification and outstanding completion gates

Run format/lint, types/build, all application tests with a disposable `TEST_REDIS_URL`, all Python tests, syntax/security/reference checks and the compiled fixture smoke. The smoke uses a local test double and manual HTTP cookie forwarding; it is not real-engine roles, browser-cookie qualification, recovery or production acceptance. Never use a production Redis URL: the integration suite deliberately flushes its disposable database.

Formal completion still needs independently verified native bindings/reviews, actual engine-role/native-feature evidence, provider keys plus approved evaluation data/targets, a representative workload/recovery contract, full restore/capacity runs and separately authorized release evidence. Existing, implemented, reviewed, merged, deployed and accepted remain separate. The implementation request does not create missing results.


## Browser qualification follow-up — APL-3018

The user requested continued completion on 20 October 2026. Extend the existing isolated qualifier with exact Playwright 1.64.1 / Chromium, production-mode compiled app cookies, synthetic invalid/valid login, pagination, full-table query, dialog focus/saving states, create/edit/reload, failure correction, mobile navigation and logout/back/re-login. No trace/video/storage-state exports or provider calls; report errors redact fixture credentials. Browser state remains ephemeral. CI installs its matching headless browser and cleans up the existing isolated engine project. This executes engineering qualification against the original criterion allocation, without inventing accessibility conformance, trusted approval, acceptance or live deployment.


## Role qualification follow-up — APL-3020

Use the version-matched official NocoDB v1 signup and v2 base-member contracts in the disposable stack. Invite-only remains enabled; the documented offline invitation token is consumed in memory because this fixture has no SMTP. Create a viewer on one base and editor on another, qualify native and compiled-app read/write/schema boundaries, then remove membership and recheck the existing session. Missing/forged sessions and separate AI grants are tested directly. Unsupported edition/API behavior is a retained failure; no license bypass, production account/role mutation or email-delivery claim. Browser qualification executes first so an unsupported invitation path does not erase independently executed evidence.

Browser qualification exposed and fixed dialog focus restoration after autofocus, unstable prefilled multiline labels and unhandled network logout failure. The focus handler captures its trigger before opening and reads saving state without restarting its lifecycle; fields have stable label IDs; logout failures retain a retry message. Partial executed checks survive test failures; screenshots are private, synthetic and password-masked. Required native gates remain intact.


## Recovery qualification follow-up — APL-3022

CI-only recovery uses explicit source `dde-qualification` and clean-target `dde-recovery-qualification` projects. A stopped compiled process supplies its real SQLite/login state; an explicit synthetic Title-only preview grant reserves 32,000 conservative units without a model. The helper snapshots the compiled interface, protected policy/runtime files, SQLite state and an exclusively created fixture unit. PostgreSQL dump and NocoDB files are captured after source writes stop, checksummed and restored to new volumes. A native-uploaded text attachment, exact records, account sign-in, restored interface reads and prior budget state are reconciled. The restored app is launched as a test process; no systemd service or host Caddy is activated.

Target volumes are refused if they exist, and cleanup requires a target-created marker. Home fixture deletion requires its generated marker and unit cleanup requires its exact content hash. Raw SQL, snapshots, generated credentials, attachment URLs, SQLite keys, private diagnostics and screenshots are excluded from uploaded evidence. Only bounded summary reports are uploaded. This exercises actual data and the unified-state helper, not the complete production backup/restore shell orchestration. Redis/legacy compatibility, SMTP delivery, host/systemd/Caddy behavior and owner-agreed recovery objectives remain distinct qualification work; elapsed time and zero loss of known fixture rows are observations only.


Native invitation compatibility finding: in this CE version mail delivery can return false without throwing, so a successful invitation response need not contain `invite_token`. The owner-only base-member listing exposes the native copy-invitation token; the fixture uses that legitimate administrator path when needed, never direct database seeding, disabled invite-only signup or a license bypass. Fixture passwords include all common character classes. Full email delivery remains unverified.
