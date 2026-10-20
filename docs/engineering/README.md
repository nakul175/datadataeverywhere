# Engineering entry point

Read the root AGENTS.md, .engineering/repository.json and docs/delivery/ADOPTION.md. The APLYD Engineering 2.1.0 core is immutable under .aplyd/engineering/2.1.0. Product 4.2, Testing 1.3 and Workflow 2.0 references are unchanged and pinned by .aplyd/delivery-lock.json.

The profile is deliberately draft: adoption work is authorized by GitHub #1, but independent configuration approval, native product/QA bindings and server protection are not established. Do not set approval fields merely to make the audit pass. Current application facts live in docs/product/BASELINE.md and docs/architecture/ADR-001-existing-system.md. The one exception authority is .governance/exceptions.json; no exceptions are approved.

Development checks use the root npm package for Biome and the existing sidecar npm package for types/build/tests. The workflow runs a disposable Redis instance so all integration tests execute. Native audit and QA record gates are additional obligations, not replaced by code tests. Logs are source-bound and retained separately from assertions about review or release.
