# Deployment on aplyd-productivity-suite

The shared host has an existing systemd Caddy service and the Sheet Happens Officer production/staging apps on ports 3000, 3001, and 3101–3108. Use `docker-compose.shared.yml`, which omits the standalone Caddy container and publishes the new sidecar on 127.0.0.1:3300 and NocoDB on 127.0.0.1:8080. It does not publish PostgreSQL or Redis.

Both application DNS names must point to the Droplet’s public IPv4 address. DNS alone does not make the application available; the containers and host routes must be installed.

The existing `deploy` SSH account can manage the SHO service but cannot install packages or edit host Caddy. The installer must be run once by an administrator in a root console. It does not grant that account additional privileges.

Run this in the DigitalOcean **root** Web Console after reviewing the staged source:

```bash
bash /home/deploy/datadataeverywhere-staging/scripts/bootstrap-shared-host.sh
```

The installer copies the release into root-owned `/opt/datadataeverywhere`, checks for port conflicts, installs official Docker packages, prompts for administrator credentials, pins images, builds and starts five containers, validates a Caddy configuration that retains existing sites, and reloads Caddy gracefully. The original Caddy configuration is backed up under `/var/backups/datadataeverywhere`. It does not run a full OS upgrade or restart the existing SHO application.

During setup, choose your own dashboard username and separate NocoDB administrator password. You may leave the provider key blank and configure it later. Do not send credentials in chat. After setup, the dashboard should return HTTP 401 without a dashboard login; NocoDB should show its native login page.

All subsequent administration commands run as root from `/opt/datadataeverywhere`. `.env` selects `docker-compose.shared.yml`, so normal `docker compose` commands target the shared-host stack. Do not start the standalone Caddy container from `docker-compose.yml` on this host.

After creating a dedicated NocoDB service token and table, run:

```bash
cd /opt/datadataeverywhere
python3 scripts/set-secret.py NOCODB_API_TOKEN
python3 scripts/set-secret.py OPENAI_API_KEY
python3 scripts/grant-table.py
docker compose up -d --force-recreate sidecar
```

To add/rotate a dashboard user, run `python3 scripts/add-user.py`, then `python3 scripts/install-host-proxy.py`. On this host the latter copies the new password hashes to Caddy and gracefully reloads it. The standalone instruction to `docker compose exec caddy ...` does not apply here. SMTP setup and NocoDB-native team invitations remain as described in README.md.

The existing live Caddy configuration must never be replaced wholesale by the bundle's standalone Caddyfile. Keep deployments and their volumes separate. Monitor memory and disk as users and attachments grow.

`backup.sh` stops only this stack's application services; host Caddy and the existing SHO app remain running. It preserves the shared manifest. For a shared-host restore, install and activate host Caddy first (or restore the Droplet backup), then use the normal restore helper on clean DDE volumes. The helper reinstalls only DDE's virtual hosts, retaining other host routes. The shared-host installer and restore integration have been syntax/configuration checked but have not yet run under root on this server.
