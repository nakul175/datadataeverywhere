> **Live interface update — 20 October 2026:** The existing Aplyd server now runs the consolidated Holy Sheet! workspace at https://datadataeverywhere.aplyd.org. See [UNIFIED-WORKSPACE.md](UNIFIED-WORKSPACE.md) for its deployed service, account sign-in, AI setup, rollback and operating notes. The Docker instructions below describe the original engine/sidecar installation; rebuilding that legacy sidecar alone does not update the active native interface.

# DataDataEverywhere — production deployment bundle

For the existing `aplyd-productivity-suite` server, follow [SHARED-HOST.md](SHARED-HOST.md); it uses the host’s existing Caddy instead of starting a second proxy.

This repository contains all four requested phases. Configure your real credentials interactively; no API keys, fake passwords, stub handlers, or invented repository URLs are embedded in source.

The deployment is designed for one Ubuntu 24.04 LTS Droplet. Use 4 vCPUs / 8 GiB RAM as an initial engineering estimate, with SSD storage sized for your tables, attachments, backups, and growth. This is not a benchmark or a guarantee of 50 simultaneously running queries. Fifty named users can sign in; the AI API admits eight concurrent calls, rejecting excess calls with HTTP 429. Measure your workload before increasing limits. A single Droplet is a single failure domain and is not a highly available service.

## Layout

```text
datadataeverywhere/
├── docker-compose.yml                 # PostgreSQL, NocoDB, sidecar, Redis, Caddy
├── Caddyfile                          # HTTPS and authenticated reverse proxy
├── LICENSE                            # MIT for our own code
├── postgres/init.sh                   # Isolated DB roles and databases
├── config/access.example.json         # Empty, fail-closed access policy
├── scripts/
│   ├── configure.py                   # Prompts; generates secrets and first dashboard user
│   ├── settings.py                    # Private dotenv reader/writer
│   ├── set-secret.py                  # Changes one deployment setting without echoing it
│   ├── add-user.py                    # Individual dashboard accounts and password rotation
│   ├── grant-table.py                 # Table/column policy and grants
│   ├── pin-images.py                  # Resolves container tags to immutable digests
│   ├── backup.sh                      # Consistent backup with planned downtime
│   └── restore.sh                     # Restore to a clean Docker host
└── sidecar/
    ├── Dockerfile
    ├── package.json / package-lock.json
    ├── app/
    │   ├── layout.tsx / globals.css
    │   ├── page.tsx / chat.tsx         # Tailwind sidebar and streaming chat
    │   └── api/{chat,health}/route.ts
    ├── lib/{access,nocodb,redis,budget}.ts
    └── tests/                         # Access, context, route, and Redis concurrency tests
```

## Phase 1 — infrastructure

`docker-compose.yml` is the complete stack. PostgreSQL uses Alpine and a named volume; no PostgreSQL or Redis port is published. NocoDB's troubleshooting port is bound only to `127.0.0.1:8080`. Next.js is reachable only inside the Docker network through Caddy.

PostgreSQL is limited to 120 connections, with a 20-connection NocoDB application pool, bounded per-role connections, 512 MiB shared buffers, and conservative per-query memory. Fifty browser sessions do not each need a permanent database connection. This uses NocoDB's existing pool; it does not place metadata migrations behind PgBouncer transaction pooling. Monitor actual connection use before changing these settings. [NocoDB configuration](https://nocodb.com/docs/self-hosting/environment-variables), [PostgreSQL connection settings](https://www.postgresql.org/docs/17/runtime-config-connection.html).

`nocodb_meta` is owned by the restricted `nocodb` role and stores NocoDB-managed metadata and internal base data. `teamdata` is an optional separately owned database for externally connected PostgreSQL tables. Start with internal NocoDB bases; the extra database is available if your installed edition supports connecting an external source. Do not manually modify NocoDB's metadata schema. PostgreSQL initialization scripts run only on the first creation of an empty database volume. Changing `.env` later does not rotate existing PostgreSQL role passwords.

Two separate Redis containers keep cache eviction separate from budget accounting. The budget store uses persistent AOF with `appendfsync always` and `noeviction`; calls fail closed if it becomes unavailable. The NocoDB cache is disposable. Back up PostgreSQL and NocoDB's attachment volume together.

Service versions start from explicit major tags and a NocoDB release tag; `pin-images.py` resolves all five base/service images to immutable digests in your private `.env` before first deployment. npm dependencies have exact versions and a committed lockfile. Security upgrades are deliberate: update selected versions, regenerate pins/lockfile, test, and back up before deployment.

## Phase 2 — AI sidecar

The Next.js App Router service uses the Vercel AI SDK `useChat`, `DefaultChatTransport`, `streamText`, and its UI message stream. Caddy flushes streaming responses without proxy buffering. [AI SDK stream protocol](https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol).

The server, never the browser, holds the NocoDB service token. It calls:

```text
GET /api/v2/meta/tables/{approvedTableId}
GET /api/v2/tables/{approvedTableId}/records?limit=25&offset=0&fields=...
```

It paginates at most four 25-row pages, includes only explicitly approved field titles, strips other response fields, and inserts raw JSON into the system prompt. Limits: 100 rows, 24,000 UTF-8 bytes of rows, 4,000 bytes of schema, 2 MB per upstream response, 64 KB incoming body, 20 conversation messages, and 1,024 output tokens. Oversized individual rows may yield an empty sample. Completeness is reported conservatively. Changing columns fails closed until the operator updates the policy. [NocoDB Meta API](https://nocodb.com/apis/v2/meta).

The selector identifies the sidecar's active table. It does not track another browser tab's selection, NocoDB view filters, row-level roles, or hidden UI columns. There is no supported cross-tab selection bridge included here. Every grant is table-wide over the approved columns. The NocoDB token's permissions and dashboard grants are separate controls: the operator must align them. For different row-level access, add server-enforced filters or a per-user NocoDB credential design before granting that table. Lookup, JSON, and linked-record columns can themselves contain sensitive nested values; approve those only when their full contents may be sent to the AI provider.

Dashboard authentication uses one Caddy Basic Auth account per person over HTTPS. Caddy replaces identity headers and supplies an independent proxy secret. No Next.js port is exposed, and the application verifies that secret. This is deliberately separate from NocoDB's own sign-in. Basic Auth is suitable for this small internal baseline; there is no SSO, MFA, or unified logout in this bundle. Keep a separate dashboard username per person. The app checks the live policy on every request.

Only user/assistant text is accepted. Client-supplied system messages, attachments, tool calls, arbitrary NocoDB URLs, write operations, and model selection are rejected or unavailable. Table cells are explicitly treated as untrusted data, though prompt instructions cannot mathematically prevent every malicious-cell influence. No model tools or write access exist. Answers are rendered as escaped plain text, not HTML. Conversation history stays in the browser session and is not stored by this app. Approved table data and messages are sent to the configured external provider.

### Providers

The default is **GPT-4o**, using `openai.chat('gpt-4o')`. Availability depends on your provider account; no live provider call was made while preparing this bundle. [Official GPT-4o model documentation](https://developers.openai.com/api/docs/models/gpt-4o).

**Claude 3.5 Sonnet retired on October 28, 2025**, so it is not a deployable Anthropic API target. The optional Anthropic configuration defaults to `claude-sonnet-5-5`, currently listed as its replacement; change `ANTHROPIC_MODEL` to an active model you have access to. This is an explicit substitution for the retired model, not a claim that 3.5 still works. [Anthropic model lifecycle](https://platform.claude.com/docs/en/about-claude/model-deprecations).

```bash
python3 scripts/set-secret.py AI_PROVIDER
python3 scripts/set-secret.py ANTHROPIC_API_KEY
python3 scripts/set-secret.py ANTHROPIC_MODEL
docker compose up -d --force-recreate sidecar
```

For the first command, enter `anthropic`. To return to OpenAI, set `AI_PROVIDER` to `openai` and configure `OPENAI_API_KEY`. Model choice is controlled by the server, not the user.

### Budget protection

Redis Lua atomically enforces:

- Six admissions per user per fixed UTC minute; fixed-window boundaries allow a short burst across adjacent windows.
- One in-flight request per user and eight globally; additional calls receive 429 rather than queueing.
- 500,000 reserved token units per user per UTC day and 5,000,000 globally by default.
- A 90-second request timeout, 180-second expiring concurrency leases, zero automatic provider retries, and no autonomous tool loops.

Reservations count incoming UTF-8 bytes plus a maximum context allowance, framing margin, and output allowance. This is intentionally a conservative token upper-bound estimate for these text-only calls, not exact tokenizer billing. A typical short call reserves roughly 40,000 units even if fewer tokens are billed. Failures and aborted calls keep their reservation; concurrency leases are released. This prevents concurrent overspend races and restart-based resets but can reject users earlier than their actual usage would suggest. Tune budgets with measured usage. Daily token budgets do not guarantee a dollar cap across models/prices; set provider-side usage controls and billing alerts too. Persist and back up Redis; restoring an older budget snapshot restores older counters.

## Phase 3 — Caddy and SSL

The supplied `Caddyfile` maps:

| URL | Destination |
| --- | --- |
| `https://datadataeverywhere.aplyd.org/` | Authenticated AI sidecar |
| `https://datadataeverywhere.aplyd.org/nocodb` | Redirect to NocoDB host |
| `https://datadataeverywhere.aplyd.org/dashboard` | Redirect to NocoDB host |
| `https://nocodb.datadataeverywhere.aplyd.org/` | NocoDB, with its native authentication |

DNS names are case-insensitive, so this is your requested `DataDataEverywhere.aplyd.org` domain. A separate NocoDB hostname avoids collisions between its `/api`, dashboard, and asset paths and Next.js routes. `NC_DASHBOARD_URL` changes a dashboard path; it is not a universal prefix for every API/asset. Do not simply strip `/nocodb` and expect a complete subpath installation.

Caddy obtains and renews public certificates automatically. Leave TCP 80 and 443 open and preserve the Caddy data volume. UDP 443 enables HTTP/3 but is optional. TLS only works after both DNS names resolve publicly to the Droplet and any CAA rules permit the issuer. Caddy normally uses Let's Encrypt and can fall back to another supported issuer. [Caddy automatic HTTPS](https://caddyserver.com/docs/automatic-https), [streaming proxy](https://caddyserver.com/docs/caddyfile/directives/reverse_proxy), [Basic Auth](https://caddyserver.com/docs/caddyfile/directives/basic_auth).

## Phase 4 — deployment runbook

### 1. Create the Droplet and DNS

Create an **Ubuntu 24.04 LTS x86-64** Droplet in DigitalOcean with your SSH public key. Start with 4 vCPUs / 8 GiB RAM, then adjust based on measurements. Attach a DigitalOcean Cloud Firewall allowing inbound SSH TCP 22 from your administration IP, TCP 80/443 from the Internet, and optionally UDP 443. Allow outbound traffic for package downloads, DNS, ACME, SMTP, and provider APIs. Do not open 3000, 5432, 6379, or 8080.

At the authoritative DNS provider for `aplyd.org`, create these two A records using the real public IPv4 address from the Droplet console:

```text
Name: datadataeverywhere          Type: A    Value: your Droplet's actual IPv4
Name: nocodb.datadataeverywhere   Type: A    Value: the same IPv4
```

These values are account-specific; no server address can be inferred from the domain. Remove stale AAAA records unless the Droplet is also configured for that IPv6 address. Use DNS-only mode initially if your DNS provider offers an HTTP proxy.

### 2. Transfer the bundle and initialize Git

Run these commands in a local **Bash** terminal. The prompts consume your real file path and IP, so no fake repository URL or address needs replacing. Select the downloaded `datadataeverywhere.tar.gz` archive. Use a new directory for this release:

```bash
bash
read -r -p 'Absolute path to datadataeverywhere.tar.gz: ' RELEASE
read -r -p 'Droplet public IPv4: ' DROPLET_IP
LOCAL_RELEASE=$(mktemp -d)
tar -xzf "$RELEASE" -C "$LOCAL_RELEASE"
cd "$LOCAL_RELEASE/datadataeverywhere"
git init -b main
git add .
# Uses your existing Git identity, or prompts you to configure one below.
if ! git config user.name >/dev/null; then
  read -r -p 'Git author name: ' GIT_AUTHOR
  git config user.name "$GIT_AUTHOR"
fi
if ! git config user.email >/dev/null; then
  read -r -p 'Git author email: ' GIT_EMAIL
  git config user.email "$GIT_EMAIL"
fi
git commit -m 'Initial DataDataEverywhere deployment'
ssh "root@$DROPLET_IP" 'mkdir -p /opt/datadataeverywhere'
git archive --format=tar HEAD | ssh "root@$DROPLET_IP" 'tar -xf - -C /opt/datadataeverywhere'
ssh "root@$DROPLET_IP"
```

Verify the SSH host fingerprint against your provider console on first connection. If you already use a Git host, you may instead push this source to your real repository and clone it on the server. Keep `.env`, `config/access.json`, `caddy/users.caddy`, and backups out of Git; the supplied `.gitignore` does so.

### 3. Install Docker on the fresh Ubuntu host

The following commands run as `root` on the Droplet. The package repository follows [Docker's Ubuntu installation instructions](https://docs.docker.com/engine/install/ubuntu/).

```bash
apt-get update
apt-get upgrade -y
apt-get install -y ca-certificates curl git python3 python3-bcrypt dnsutils ufw unattended-upgrades
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
. /etc/os-release
cat > /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: ${UBUNTU_CODENAME:-$VERSION_CODENAME}
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
systemctl enable --now docker
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 443/udp
ufw --force enable
cd /opt/datadataeverywhere
docker version
docker compose version
```

The Cloud Firewall is the public perimeter. Docker-published ports can bypass ordinary UFW forwarding rules; this stack publishes only Caddy and the loopback-bound NocoDB troubleshooting port. Keep the Cloud Firewall restrictions even with UFW enabled. If the OS upgrade requires a reboot, reboot now, reconnect over SSH, and return to `/opt/datadataeverywhere`.

### 4. Generate deployment settings, then start

```bash
cd /opt/datadataeverywhere
python3 scripts/configure.py
python3 scripts/pin-images.py
docker compose config --quiet
dig +short datadataeverywhere.aplyd.org A
dig +short nocodb.datadataeverywhere.aplyd.org A
```

Verify both lookups equal the Droplet IP before proceeding. `configure.py` asks for separate dashboard and NocoDB administrator passwords, creates the first individual dashboard account, generates cryptographic database/proxy/JWT/encryption secrets, and writes `.env` mode 0600. API credentials can be entered now or left blank until the next step. No plaintext secret is printed.

```bash
docker compose build --pull
docker compose run --rm --no-deps caddy caddy validate --config /etc/caddy/Caddyfile
docker compose up -d --wait --wait-timeout 240
docker compose ps
docker compose logs --tail 100 caddy
curl -I https://datadataeverywhere.aplyd.org/
curl -I https://nocodb.datadataeverywhere.aplyd.org/
```

An unauthenticated dashboard request should return **401 over valid HTTPS**. NocoDB should present its login page or redirect to it. A Docker health check does not prove DNS or public certificate issuance; verify HTTPS in your browser as well. Do not use `curl -k` to hide certificate errors. If Caddy cannot issue a certificate, check both DNS records, stale AAAA records, Cloud Firewall ports, CAA records, and whether another service already occupies 80/443.

### 5. Set up NocoDB and grant a table

1. Open `https://nocodb.datadataeverywhere.aplyd.org` and sign in with the NocoDB email/password you entered. Create your workspace/base and a table using NocoDB's UI. A useful initial table is `Orders` with `Id`, `Customer`, `Amount`, and `Status` columns.
2. In NocoDB's account/API-token settings, create a dedicated token for the sidecar. Prefer a separate service account with read-only access to only the required bases, and use token scopes if the installed edition supports them. The bundle makes only GET requests; a broad administrator token would still have administrator power if stolen.
3. Get the real table ID from NocoDB's table/API documentation. Review which fields may be sent to your provider. Include a primary key field in the approved list if answers should cite records. Never infer table IDs from display names.
4. Run the commands below. Enter the actual token at the hidden prompt; then enter the actual table ID, exact field titles, and the dashboard username created during setup.

```bash
cd /opt/datadataeverywhere
python3 scripts/set-secret.py NOCODB_API_TOKEN
python3 scripts/set-secret.py OPENAI_API_KEY
python3 scripts/grant-table.py
docker compose up -d --force-recreate sidecar
```

If the API key was already entered during setup, omit the second command. If using Anthropic, set `ANTHROPIC_API_KEY` instead and select `anthropic` as described in Phase 2. Reload the dashboard, select your approved table, and ask a question. The first real response is your provider integration smoke test and can incur API charges.

### 6. Onboard the team

Configure your actual SMTP service for NocoDB invitations/password recovery. Port 587 with STARTTLS normally uses `NC_SMTP_SECURE=false`; port 465 normally uses `true`. Keep certificate verification enabled. Then invite your team from NocoDB, using its native roles. Delivery also depends on your SMTP provider, sender verification, and Droplet outbound-mail policy.

```bash
python3 scripts/set-secret.py NC_SMTP_HOST
python3 scripts/set-secret.py NC_SMTP_PORT
python3 scripts/set-secret.py NC_SMTP_USERNAME
python3 scripts/set-secret.py NC_SMTP_PASSWORD
python3 scripts/set-secret.py NC_SMTP_FROM
python3 scripts/set-secret.py NC_SMTP_SECURE
docker compose up -d --force-recreate nocodb
```

Create a distinct dashboard identity for each of your 50 users; each run prompts for its password and approved table IDs. Do not distribute one shared dashboard password, since budgets and grants depend on individual usernames.

```bash
python3 scripts/add-user.py
docker compose exec caddy caddy reload --config /etc/caddy/Caddyfile
```

The script also rotates existing users' dashboard passwords. To revoke someone, remove their line from `caddy/users.caddy` and their mapping from `config/access.json`, then reload Caddy; revoke their NocoDB membership separately. New table definitions and grants are read on every request without a sidecar rebuild. Reopen or reload the page to refresh the selector. The same approved field list applies to everyone granted that table.

Optional external PostgreSQL source: use host `postgres`, port `5432`, database `teamdata`, username `teamdata`, and the generated `TEAM_DB_PASSWORD` from your restricted `.env`. Copy that value only into NocoDB's server-side source configuration. There is no public database endpoint. Do not use the `postgres` superuser. If your installed edition does not offer external database connections, use internal bases, which are already stored in PostgreSQL.

### 7. Verify security and operations

```bash
docker compose ps
docker compose exec postgres psql -U postgres -c 'SELECT datname, usename, count(*) FROM pg_stat_activity GROUP BY datname, usename;'
docker compose exec redis redis-cli INFO persistence
docker compose exec redis redis-cli INFO memory
docker stats --no-stream
ss -lnt
```

From an outside machine, database and Redis ports must be closed. Verify that an ungranted dashboard user sees no tables, and that a direct POST for an ungranted ID gets 403. Send concurrent requests only in a test environment and confirm 429 responses. A user can query approved fields even if the corresponding column is hidden in their spreadsheet UI, so review server policy directly.

Health checks restart neither healthy nor unhealthy processes by themselves; `restart: unless-stopped` restarts exited containers. Alert on unhealthy containers, disk pressure, backup failures, certificate errors, and provider failures using your team's monitoring. Do not leave health failures unnoticed. Load test representative tables and attachment sizes before onboarding the full team.

### 8. Back up and restore

The backup helper briefly stops public access and application writes, dumps all PostgreSQL databases/roles, archives attachments and budget Redis, and copies settings/access policy. Run in Bash from the repository root:

```bash
bash scripts/backup.sh
```

It writes a timestamped directory under `backups/` with checksums. The directory contains credentials and personal data. Encrypt it with your team's approved backup tooling and copy it to a separate host/object store. Backups kept only on the Droplet do not protect against loss of that Droplet. Schedule the command in your existing operations system at a frequency matching your recovery objectives. The backup is a consistency snapshot, not point-in-time recovery; writes after it will be lost if you restore it.

On a clean replacement Ubuntu host, install Docker and transfer the same source release and backup directory. Ensure no `datadataeverywhere_*` data volumes exist, enter the extracted backup directory when prompted, then run:

```bash
cd /opt/datadataeverywhere
bash scripts/restore.sh
```

The restore helper refuses to overwrite an existing stack's data volumes. It restores roles/databases, attachments, budget counters, and secrets before starting services. Caddy gets fresh certificates; it may encounter issuer rate limits after repeated disaster-recovery drills. Point both DNS names at the replacement server when ready. Test recovery in an isolated environment before relying on the backup workflow. Never run `docker compose down -v` on production unless your explicit intention is to delete its data volumes.

### 9. Develop and upgrade

The host needs Docker only. To run source checks without a local Node installation, use the pinned Node image through Docker in the `sidecar` directory, or install Node.js 24 locally and run:

```bash
cd sidecar
npm ci
npm run typecheck
npm test
npm run build
```

The ordinary test command skips six real-Redis integration tests unless `TEST_REDIS_URL` is set. To run them with an isolated disposable Redis, on a development machine with Node 24 and Docker:

```bash
docker run -d --rm --name dde-budget-test -p 127.0.0.1:16379:6379 redis:7-alpine
TEST_REDIS_URL=redis://127.0.0.1:16379/15 npm test
docker stop dde-budget-test
```

**Never point this test at production Redis: the integration suite runs FLUSHDB.** It submits 50 concurrent admissions, verifies global/per-user limits and atomic budgets, checks the request cap, and tests stale-lease recovery.

For updates, commit source changes to your real Git remote, pull the reviewed commit on the server, keep private runtime configuration, back up, build, and restart. Use these commands inside an existing clone of your real repository:

```bash
git pull --ff-only
bash scripts/backup.sh
docker compose build --pull
docker compose up -d --wait --wait-timeout 240
```

The initial transfer uses `git archive` and is intentionally not a server-side Git clone. To establish one later, clone your actual remote into a separate directory and copy the ignored deployment files there under root-only control before starting it with the same Compose project name. Do not run two copies concurrently. Code rollback alone cannot reverse a NocoDB schema migration; restore a tested pre-upgrade backup when a migration prevents rollback.

## Licensing and validation

Our sidecar and deployment source are MIT licensed. Current NocoDB uses a Sustainable Use License, so the entire stack should not be represented as wholly OSI-open-source. Its license describes internal business use and distribution restrictions; review the exact pinned version's terms for your intended release. Redis, PostgreSQL, Caddy, Next.js, and dependencies retain their respective licenses. [NocoDB license](https://github.com/nocodb/nocodb/blob/develop/LICENSE.md).

See `VALIDATION.md` for checks actually performed and remaining deployment checks. Infrastructure configuration and scripts are supplied for review and deployment; no Droplet, DNS zone, production credentials, or live provider access was used during preparation.
