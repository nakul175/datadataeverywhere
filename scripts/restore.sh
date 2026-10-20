#!/usr/bin/env bash
# Restore a backup on a NEW, EMPTY installation only. Do not restore over live DBs.
set -euo pipefail
cd "$(dirname "$0")/.."
read -r -p 'Absolute path to extracted backup directory: ' backup
[ -d "$backup" ] || exit 1
if [ -f "$backup/docker-compose.shared.yml" ] && ! systemctl is-active --quiet caddy; then
  echo 'Shared-host restore requires host Caddy installed and active. See SHARED-HOST.md.' >&2; exit 1
fi
(cd "$backup" && sha256sum -c SHA256SUMS)
read -r -p 'Type RESTORE-EMPTY to confirm this stack has no data to preserve: ' confirm
[ "$confirm" = RESTORE-EMPTY ] || exit 1
# Refuse existing database/data volumes, including a stopped installation.
for name in datadataeverywhere_pgdata datadataeverywhere_ncdata datadataeverywhere_redisdata; do
  if docker volume inspect "$name" >/dev/null 2>&1; then
    echo 'Existing data volume detected. Restore on a clean host or separately isolated Docker daemon.' >&2; exit 1
  fi
done
mkdir -p config caddy
install -m 600 "$backup/env" .env
install -m 644 "$backup/access.json" config/access.json
install -m 644 "$backup/users.caddy" caddy/users.caddy
cp "$backup/docker-compose.yml" "$backup/Caddyfile" .
if [ -f "$backup/docker-compose.shared.yml" ]; then cp "$backup/docker-compose.shared.yml" .; fi
# Skip init script because pg_dumpall contains roles and CREATE DATABASE statements.
docker compose run -d --name dde-restore-pg --no-deps --volume /dev/null:/docker-entrypoint-initdb.d/10-init.sh:ro postgres
for i in $(seq 1 60); do
  if docker exec dde-restore-pg pg_isready -h 127.0.0.1 -U postgres >/dev/null 2>&1; then break; fi
  sleep 2
done
# pg_dumpall includes the bootstrap postgres role; remove its CREATE line only.
sed '/^CREATE ROLE postgres;$/d' "$backup/postgres.sql" | docker exec -i dde-restore-pg psql -U postgres -v ON_ERROR_STOP=1 postgres
docker stop dde-restore-pg >/dev/null
docker rm dde-restore-pg >/dev/null
for service in nocodb redis; do
  if [ "$service" = nocodb ]; then path=/usr/app/data; else path=/data; fi
  docker compose run --rm --no-deps -T --user root --entrypoint tar "$service" -C "$path" -xzf - < "$backup/$service.tgz"
done
docker compose up -d --build --wait
if [ -f "$backup/docker-compose.shared.yml" ]; then python3 scripts/install-host-proxy.py; fi
