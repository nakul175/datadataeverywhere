# ADR-001: Preserve the deployed architecture during standards adoption

Date: 2026-10-20. Status: factual retrospective record; future changes require review.

The deployed interface is Next.js App Router with React, Tailwind, the Vercel AI SDK and NocoDB REST APIs. PostgreSQL, NocoDB and Redis remain in the original Docker stack. Host Caddy provides HTTPS. The consolidated interface runs as a deploy-owned systemd user service on loopback 3301; the previous sidecar stays on loopback 3300 for rollback.

Account authentication uses the installed NocoDB v1 authentication endpoints. The application holds the upstream JWT in a Secure, HttpOnly, SameSite=Lax cookie and validates it with NocoDB. It uses that user's token for record/schema operations. AI admission additionally uses a server-owned field allowlist and persistent SQLite transactions. The legacy Docker sidecar uses Redis admission.

Trust boundaries: browser to Caddy; Caddy to loopback interface; interface to local NocoDB; NocoDB to PostgreSQL; interface to a configured external AI provider. No browser receives database credentials or an API provider secret. Approved table fields and questions leave the server only when the operator configures and enables the AI route.

Operational limitations include a single-host failure domain, upstream access-token expiry without refresh rotation, unverified production record writes, no measured 50-user load profile, no restore drill, no provider evaluation, and no currently qualified release pipeline. This adoption PR changes process and development checks, not the deployed service or data model.
