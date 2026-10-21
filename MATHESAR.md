# Mathesar transition runbook

Mathesar is the internal PostgreSQL studio for DataDataEverywhere. It is not a second customer-facing product. The member application contains no Mathesar or NocoDB link, attribution, workspace upsell or public admin route.

## Existing installation

The PostgreSQL initialization hook creates Mathesar's metadata database on a new volume. On the existing Droplet, create/rotate that role first, then start the two internal services:

```bash
cd /opt/datadataeverywhere
python3 scripts/prepare-mathesar.py
python3 scripts/pin-images.py
docker compose config --quiet
docker compose up -d --wait mathesar mathesar-gateway
docker compose ps mathesar mathesar-gateway
```

`prepare-mathesar.py` writes a generated password to the private `.env`, passes it to `psql` through the process environment, and prints no secret. It creates only `mathesar` and `mathesar_meta`; it does not grant access to product data.

The studio services use Compose's `admin` profile, so routine application restarts do not spend memory on an administration tool. Naming both services in the command above starts that profile explicitly. Stop the studio after the administration session with `docker compose stop mathesar-gateway mathesar`.

From an administrator computer, open a tunnel using the existing SSH identity:

```bash
ssh -L 8090:127.0.0.1:8090 deploy@YOUR_DROPLET_IP
```

Then open `http://127.0.0.1:8090`. Create the first Mathesar administrator through its setup screen. Do not publish port 8090 in a firewall, reverse proxy or DNS record.

To attach product data, create a dedicated PostgreSQL role with the exact schema/table privileges approved for that administrator. Connect Mathesar to host `postgres`, port `5432`, database `teamdata`. Never use `postgres`, `mathesar`, `nocodb` or an application-owner credential for this connection. The role and grants require a production database inventory and are deliberately not guessed by this repository.

## Editing Mathesar itself

The official Mathesar source is GPLv3 and can be forked and changed. Keep the fork in a separate repository so its licence, history, dependencies and tests remain intact. The release workflow is:

1. Fork `mathesar-foundation/mathesar` at tag `0.12.0`.
2. Create a branch for the DataDataEverywhere admin-studio changes.
3. Retain GPLv3 and third-party notices and publish corresponding source when distribution requires it.
4. Build and test the fork with Mathesar's own Dockerfile and upstream test suite.
5. Push the image to a controlled registry, resolve its immutable digest, and set `MATHESAR_IMAGE` to that digest.
6. Back up `mathesar_meta`, `teamdata`, `mathesarstatic`, `mathesarmedia` and `mathesarsecrets`; test restore before upgrading production.

The repository backup and clean-host restore scripts include these Mathesar volumes. Their existing planned-downtime and empty-target rules still apply. A passing script test is not a recovery result; execute and reconcile an isolated restore before production activation.

DataDataEverywhere branding and ordinary member workflows belong in `sidecar/`. Fork Mathesar only for internal studio capabilities that cannot be delivered through configuration or the product application.

## Compatibility boundary

The current deployed app still authenticates and performs table CRUD through a private NocoDB container. NocoDB has no public Caddy host or product links after this transition, and new workspaces are disabled. Do not remove its container yet. Removal requires replacement and qualification of sessions, table metadata, records, AI context, governed feeds, invitations, backups and restoration as listed in [ADR-002](docs/architecture/ADR-002-mathesar-transition.md).
