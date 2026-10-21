# ADR-002: Mathesar as the internal PostgreSQL studio

**Status:** Accepted for development on 21 October 2026; production activation remains a separate release action.

## Decision

DataDataEverywhere will use PostgreSQL as the product data system and Mathesar 0.12.0 as an internal, self-hosted administration studio. Team members use only the branded DataDataEverywhere interface. Mathesar binds to loopback port 8090 and is reached by an administrator through an SSH tunnel; it has no public Caddy route and no member-facing link.

NocoDB remains temporarily available on the private Docker network and the shared host's loopback interface because the deployed application still uses its accounts, metadata and REST contracts. Its public virtual host, product links, attribution and workspace-creation affordance are removed. This is a compatibility phase, not the final architecture. NocoDB can be removed after native PostgreSQL authentication, table metadata, record operations, AI context and governed-feed authority replace every dependency recorded below.

## Why Mathesar

Mathesar is GPLv3 software maintained by the nonprofit Mathesar Foundation. It operates directly on PostgreSQL schemas, tables, constraints and privileges. The official source can be forked and changed; modified distributed builds must continue to satisfy GPLv3 and third-party notices. DataDataEverywhere does not depend on proprietary Mathesar features.

Mathesar's metadata is isolated in `mathesar_meta`, owned by the non-superuser `mathesar` role. Product data stays in `teamdata`. An administrator adds `teamdata` inside Mathesar using a separately reviewed PostgreSQL role; the service metadata role must not be reused as a product-data superuser.

## Transition gates

1. Mathesar starts from the pinned `mathesar/mathesar:0.12.0` image, is healthy, and is reachable only through `ssh -L 8090:127.0.0.1:8090 ...`.
2. A restricted PostgreSQL role and schema are created for the actual product-data permissions. Negative tests prove it cannot read or change excluded schemas/tables.
3. Existing NocoDB sessions and table identifiers are inventoried before any data move. The current live screenshot shows zero tables in the visible workspace, but that observation is not a database inventory.
4. Native DataDataEverywhere auth and direct PostgreSQL table APIs pass role, revocation, concurrency, backup and restore tests.
5. NocoDB is removed only after live readback proves no requests, accounts, attachments, feeds or recovery procedures depend on it.

## Code-editable development

Production uses an immutable image digest resolved from the reviewed 0.12.0 tag. To customize Mathesar, fork the official repository, retain its GPLv3 license and notices, build a new image from the reviewed commit, run its test suite, and set `MATHESAR_IMAGE` to the resulting immutable digest. Do not mount a mutable source checkout into production or use `latest`.

Branding changes to the member-facing product belong in this repository's Next.js application. Mathesar source customization is reserved for the private admin studio and must not create a second public product surface.
