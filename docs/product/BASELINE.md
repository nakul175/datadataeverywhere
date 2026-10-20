# DataDataEverywhere baseline, version 1

Status: factual adoption inventory, not a retrospectively approved product plan.
Source revision: d819af9c539d063b98b96df89ea5c54ec054c193.
Work item: https://github.com/nakul175/datadataeverywhere/issues/1.

The requested product is a self-hosted team data engine for approximately 50 users, hosted with SheetHappensOfficer on an Ubuntu DigitalOcean Droplet. PostgreSQL stores data, NocoDB supplies data management APIs and an advanced spreadsheet, and a Next.js interface combines table browsing and a read-only AI panel. The interface is branded DataDataEverywhere with the approved Holy Sheet! mascot and Aplyd colors.

Implemented scope includes account sign-in, workspace/table listing and creation, pagination, page-local search/sort, simple record creation/editing, per-user NocoDB authorization, and bounded AI context with approved-field grants and persistent rate/budget admission. The AI code exists; provider credentials and field grants are operator configuration and live provider behavior is unverified.

Advanced relations, imports, field types and user administration remain native NocoDB functions. Documents, Notion parity, task synchronization, unified login to the advanced native UI and automatic release orchestration are not implemented. A native systemd interface currently fronts the existing Docker data engine. The old Docker sidecar is retained as a rollback option.

The current live service predates standards adoption. Its operation does not establish product acceptance, 50-user capacity, disaster-recovery readiness, independent security review or compliant release approval. Those claims must be qualified with new evidence under the adopted process.

The repository owner and requesting user are nakul175. Accountable engineering, QA, security, operations and independent reviewer assignments require an actual owner decision. A native Product 4.2 plan with authoritative typed task/criterion links and a native QA qualification scope has not yet been supplied. Do not substitute the bundle's synthetic example records.
