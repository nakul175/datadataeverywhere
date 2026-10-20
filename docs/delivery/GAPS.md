# Adoption and release gaps

All entries are pending, not approved exceptions. Work item: GitHub #1.

| Gap | Current evidence | Required action/authority |
| --- | --- | --- |
| Native product plan and typed criterion links | Conversation-derived factual baseline only | Product owner supplies/reviews native Product 4.2 records and criteria |
| Native QA scope, cases and immutable runs | Existing tests and validation notes; no approved native release scope | Assigned QA owner qualifies mappings and criteria pins |
| Engineering/QA/security/operations role assignment | Repository owner is known; specialist roles unassigned | Owner records actual accountable people |
| Configuration and independent review | Adoption profile deliberately remains draft | Authorized independent review of the exact PR head |
| Merge protection | GitHub readback found main unprotected and no rulesets | Review named checks and activate/prove server enforcement |
| Automated deployment and live version linkage | Manual user-service release with rollback | Review an authorized release mechanism and observed artifact identity |
| Capacity and recovery | Budget concurrency tests exist; no 50-user E2E test or restore drill | Agree workload and recovery objectives, execute approved tests |
| AI qualification | Provider keys and table grants pending | Operator configures credentials privately; owner approves evaluation scope |
| Comprehensive lint/security coverage | Initial targeted TypeScript rules and pattern-based secret scanning | Expand with reviewed Python/shell/security tooling; do not claim complete coverage |

An expected native audit failure is retained as a failure. It is not an exception or a green release gate. Adoption documentation and reference integrity alone cannot satisfy these gaps. The original deployed version remains a legacy baseline, not retrospectively certified.
