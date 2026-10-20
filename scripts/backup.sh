#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
umask 077
mkdir -p backups
stamp=$(date -u +%Y%m%dT%H%M%SZ)
dest="backups/$stamp"
mkdir "$dest"
# Planned downtime: consistent DB + file + Redis snapshot, no new writes.
services=(sidecar nocodb redis)
service_names=$(docker compose config --services)
service_names=${service_names//$'\n'/ }
if [[ " $service_names " == *" caddy "* ]]; then services+=(caddy); fi
docker compose stop "${services[@]}"
trap 'docker compose up -d "${services[@]}" >/dev/null' EXIT
docker compose exec -T postgres pg_dumpall -U postgres > "$dest/postgres.sql"
for service in nocodb redis; do
  if [ "$service" = nocodb ]; then path=/usr/app/data; else path=/data; fi
  docker compose run --rm --no-deps -T --user root --entrypoint tar "$service" -C "$path" -czf - . > "$dest/$service.tgz"
done
cp .env "$dest/env"
cp config/access.json "$dest/access.json"
cp caddy/users.caddy "$dest/users.caddy"
cp docker-compose.yml Caddyfile "$dest/"
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
