#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
umask 077
mkdir -p backups
stamp=$(date -u +%Y%m%dT%H%M%SZ)
dest="backups/$stamp"
mkdir "$dest"
unified_root=${UNIFIED_ROOT:-/home/deploy/datadataeverywhere}
unified_user=${UNIFIED_USER:-deploy}
unified_was_active=false
unified_ctl=()
if [ -d "$unified_root" ]; then
  unified_uid=$(id -u "$unified_user")
  if [ "$(id -u)" = "$unified_uid" ]; then
    unified_ctl=(systemctl --user)
  else
    [ "$(id -u)" = 0 ] || { echo 'Unified backup requires the service user or root.' >&2; exit 1; }
    unified_ctl=(runuser -u "$unified_user" -- env "XDG_RUNTIME_DIR=/run/user/$unified_uid" systemctl --user)
  fi
  unified_state=$("${unified_ctl[@]}" is-active datadataeverywhere 2>/dev/null || true)
  case "$unified_state" in
    active|activating|reloading) unified_was_active=true ;;
    inactive|failed) ;;
    *) echo 'Cannot establish unified service state; refusing a potentially inconsistent backup.' >&2; exit 1 ;;
  esac
fi
# Planned downtime: consistent DB + file + Redis snapshot, no new writes.
services=(sidecar nocodb redis)
service_names=$(docker compose config --services)
service_names=${service_names//$'\n'/ }
if [[ " $service_names " == *" caddy "* ]]; then services+=(caddy); fi
admin_running=$(docker compose --profile admin ps --status running --services)
if grep -qx mathesar <<<"$admin_running"; then services+=(mathesar); fi
if grep -qx mathesar-gateway <<<"$admin_running"; then services+=(mathesar-gateway); fi
cleanup() {
  result=$?
  set +e
  docker compose up -d "${services[@]}" >/dev/null || result=1
  if [ "$unified_was_active" = true ]; then "${unified_ctl[@]}" start datadataeverywhere || result=1; fi
  exit "$result"
}
trap cleanup EXIT
if [ "$unified_was_active" = true ]; then "${unified_ctl[@]}" stop datadataeverywhere; fi
docker compose stop "${services[@]}"
if [ -d "$unified_root" ]; then
  python3 scripts/unified-state.py backup --root "$unified_root" --user "$unified_user" --output "$dest"
fi
docker compose exec -T postgres pg_dumpall -U postgres > "$dest/postgres.sql"
for service in nocodb redis; do
  if [ "$service" = nocodb ]; then path=/usr/app/data; else path=/data; fi
  docker compose run --rm --no-deps -T --user root --entrypoint tar "$service" -C "$path" -czf - . > "$dest/$service.tgz"
done
for item in static:/code/static media:/code/.media secrets:/code/.secrets; do
  name=${item%%:*}; path=${item#*:}
  docker compose --profile admin run --rm --no-deps -T --user root --entrypoint tar mathesar -C "$path" -czf - . > "$dest/mathesar-$name.tgz"
done
cp .env "$dest/env"
cp config/access.json "$dest/access.json"
cp caddy/users.caddy "$dest/users.caddy"
cp docker-compose.yml Caddyfile "$dest/"
cp mathesar/Caddyfile "$dest/mathesar-Caddyfile"
if [ -f docker-compose.shared.yml ]; then cp docker-compose.shared.yml "$dest/"; fi
# Includes database passwords and provider keys. Encrypt before off-site transfer.
python3 - "$dest" <<'PYSUM'
import hashlib,sys
from pathlib import Path
folder=Path(sys.argv[1])
files=sorted(p for p in folder.iterdir() if p.is_file() and p.name!='SHA256SUMS')
(folder/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in files))
PYSUM
printf 'Backup complete: %s\n' "$dest"
