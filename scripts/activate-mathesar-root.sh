#!/usr/bin/env bash
# One-time production activation from the DigitalOcean root console.
set -euo pipefail

if [[ "$(id -u)" != 0 ]]; then
  echo 'Run this script from the DigitalOcean root console.' >&2
  exit 1
fi
if [[ "${1:-}" != --deploy ]]; then
  echo 'Usage: bash scripts/activate-mathesar-root.sh --deploy' >&2
  exit 1
fi

expected_commit='bcbd48a986a2a129bd0c5cf92963170975efe7a8'
app_root='/opt/datadataeverywhere'
backup_root='/var/backups/datadataeverywhere'
unified_root='/home/deploy/datadataeverywhere'
unified_release="$unified_root/releases/bcbd48a"
release_manifest_digest='b96dd782886b27e624e84dd3b37e280eb182c820ac42cfc2f37aedff5c085c4c'
unified_uid="$(id -u deploy)"
unified_previous="$(readlink "$unified_root/current" || true)"
release_marker="$unified_root/shared/release.current"
previous_marker=''
[[ -f "$release_marker" ]] && previous_marker="$(cat "$release_marker")"

exec 9>/var/lock/datadataeverywhere-mathesar-activation.lock
flock -n 9 || { echo 'Another DataDataEverywhere activation is running.' >&2; exit 1; }

[[ -d "$app_root/.git" ]] || { echo 'Production checkout is missing.' >&2; exit 1; }
[[ -f "$unified_release/scripts/deploy-unified-user.sh" ]] || { echo 'Validated unified release is missing.' >&2; exit 1; }
[[ "$(sha256sum "$unified_release/SHA256SUMS" | cut -d ' ' -f1)" == "$release_manifest_digest" ]] || {
  echo 'Unified release manifest does not identify the validated commit.' >&2
  exit 1
}
(cd "$unified_release" && sha256sum --quiet -c SHA256SUMS) || {
  echo 'Unified release source failed byte-integrity verification.' >&2
  exit 1
}
[[ -f /etc/caddy/Caddyfile ]] || { echo 'Host Caddy configuration is missing.' >&2; exit 1; }
systemctl is-active --quiet caddy || { echo 'Host Caddy must be active.' >&2; exit 1; }
systemctl is-active --quiet docker || { echo 'Docker must be active.' >&2; exit 1; }

cd "$app_root"
[[ -z "$(git status --porcelain --untracked-files=no)" ]] || {
  echo 'Production checkout has tracked changes; refusing activation.' >&2
  exit 1
}
old_commit="$(git rev-parse HEAD)"
mkdir -p "$backup_root"
stamp="$(date -u +%Y%m%dT%H%M%SZ)"
env_backup="$backup_root/env.before-mathesar-$stamp"
caddy_backup="$backup_root/Caddyfile.before-mathesar-$stamp"
cp -p .env "$env_backup"
cp -p /etc/caddy/Caddyfile "$caddy_backup"
caddy_uid="$(stat -c '%u' /etc/caddy/Caddyfile)"
caddy_gid="$(stat -c '%g' /etc/caddy/Caddyfile)"
caddy_mode="$(stat -c '%a' /etc/caddy/Caddyfile)"
chmod 600 "$env_backup" "$caddy_backup"

rollback() {
  result=$?
  [[ $result -eq 0 ]] && return
  set +e
  cd "$app_root"
  docker compose --profile admin stop mathesar-gateway mathesar >/dev/null 2>&1
  cp -p "$env_backup" .env
  git checkout --detach "$old_commit" >/dev/null 2>&1
  if [[ -n "$unified_previous" ]]; then
    runuser -u deploy -- env HOME=/home/deploy XDG_RUNTIME_DIR="/run/user/$unified_uid" \
      ln -sfn "$unified_previous" "$unified_root/.current-next"
    mv -Tf "$unified_root/.current-next" "$unified_root/current"
    runuser -u deploy -- env HOME=/home/deploy XDG_RUNTIME_DIR="/run/user/$unified_uid" \
      systemctl --user restart datadataeverywhere.service
  fi
  if [[ -n "$previous_marker" ]]; then
    printf '%s\n' "$previous_marker" > "$release_marker"
    chown deploy:deploy "$release_marker"
    chmod 600 "$release_marker"
  else
    rm -f "$release_marker"
  fi
  cp -p "$caddy_backup" /etc/caddy/Caddyfile
  chown "$caddy_uid:$caddy_gid" /etc/caddy/Caddyfile
  chmod "$caddy_mode" /etc/caddy/Caddyfile
  caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile >/dev/null 2>&1 && systemctl reload caddy
  docker compose up -d >/dev/null 2>&1
  echo 'Activation failed; source, private environment and Caddyfile were restored.' >&2
  exit "$result"
}
trap rollback EXIT

# Capture a consistent pre-change backup using the currently deployed release.
bash scripts/backup.sh

git fetch --quiet origin feat/story-completion
resolved="$(git rev-parse "${expected_commit}^{commit}")"
[[ "$resolved" == "$expected_commit" ]] || { echo 'Validated commit is unavailable.' >&2; exit 1; }
git checkout --detach "$expected_commit"

python3 scripts/prepare-mathesar.py
python3 scripts/pin-images.py
docker compose config --quiet
docker compose --profile admin up -d --wait --wait-timeout 300 mathesar mathesar-gateway

runuser -u deploy -- env HOME=/home/deploy XDG_RUNTIME_DIR="/run/user/$unified_uid" \
  bash "$unified_release/scripts/deploy-unified-user.sh"
[[ "$(readlink -f "$unified_root/current")" == "$unified_release/sidecar" ]] || {
  echo 'Unified release symlink does not identify the validated source.' >&2
  exit 1
}

python3 - "$caddy_backup" <<'PY'
import pathlib
import shutil
import os
import re
import stat
import subprocess
import sys

main = pathlib.Path('/etc/caddy/Caddyfile')
source = main.read_text()
replacement = pathlib.Path('/opt/datadataeverywhere/caddy/unified-site.caddy').read_text().strip()
include = 'import /etc/caddy/datadataeverywhere/site.caddy'

if source.count(include) == 1 and not re.search(
    r'(?m)^\s*(?:datadataeverywhere|nocodb\.datadataeverywhere)\.aplyd\.org\s*\{', source
):
    candidate = source.replace(include, replacement)
else:
    pattern = re.compile(
        r'(?m)^[ \t]*(datadataeverywhere\.aplyd\.org|nocodb\.datadataeverywhere\.aplyd\.org)[ \t]*\{'
    )
    matches = list(pattern.finditer(source))
    addresses = [match.group(1) for match in matches]
    if addresses.count('datadataeverywhere.aplyd.org') != 1 or addresses.count(
        'nocodb.datadataeverywhere.aplyd.org'
    ) > 1:
        raise SystemExit('Unexpected DataDataEverywhere Caddy configuration.')
    spans = []
    for match in matches:
        depth = 0
        end = None
        for index in range(match.start(), len(source)):
            char = source[index]
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0:
                    end = index + 1
                    while end < len(source) and source[end] in ' \t':
                        end += 1
                    if end < len(source) and source[end] == '\n':
                        end += 1
                    break
        if end is None:
            raise SystemExit('Could not identify an existing DataDataEverywhere Caddy block.')
        spans.append((match.start(), end, match.group(1)))
    candidate = source
    for start, end, _address in reversed(spans):
        candidate = candidate[:start] + candidate[end:]
    candidate = candidate.rstrip() + '\n\n' + replacement + '\n'

staged = pathlib.Path('/etc/caddy/Caddyfile.datadataeverywhere-next')
original_stat = main.stat()
fd = os.open(staged, os.O_WRONLY | os.O_CREAT | os.O_EXCL, stat.S_IMODE(original_stat.st_mode))
with os.fdopen(fd, 'w') as handle:
    handle.write(candidate)
os.chown(staged, original_stat.st_uid, original_stat.st_gid)
os.chmod(staged, stat.S_IMODE(original_stat.st_mode))
try:
    subprocess.run(
        ['caddy', 'validate', '--config', str(staged), '--adapter', 'caddyfile'],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    staged.replace(main)
    subprocess.run(['systemctl', 'reload', 'caddy'], check=True)
except BaseException:
    staged.unlink(missing_ok=True)
    shutil.copy2(pathlib.Path(sys.argv[1]), main)
    os.chown(main, original_stat.st_uid, original_stat.st_gid)
    os.chmod(main, stat.S_IMODE(original_stat.st_mode))
    subprocess.run(['systemctl', 'reload', 'caddy'], check=False)
    raise
PY

for path in /nocodb /dashboard; do
  code="$(curl --connect-timeout 5 --max-time 15 -fsS -o /dev/null -w '%{http_code}' "https://datadataeverywhere.aplyd.org$path" || true)"
  [[ "$code" == 404 ]] || { echo "Retired route did not return 404: $path ($code)" >&2; exit 1; }
done
native_code="$(curl --connect-timeout 5 --max-time 15 -sS -o /dev/null -w '%{http_code}' https://nocodb.datadataeverywhere.aplyd.org/ || true)"
[[ "$native_code" == 404 || "$native_code" == 000 ]] || { echo "Retired native hostname remained reachable ($native_code)." >&2; exit 1; }
curl --connect-timeout 5 --max-time 15 -fsS http://127.0.0.1:3301/api/health >/dev/null
curl --connect-timeout 5 --max-time 15 -fsS http://127.0.0.1:8090/ >/dev/null

printf '%s\n' "$expected_commit" > "$release_marker"
chown deploy:deploy "$release_marker"
chmod 600 "$release_marker"

trap - EXIT
echo "Mathesar activation complete at $expected_commit."
echo 'Member app is healthy; retired admin routes return 404; Mathesar remains loopback-only on 127.0.0.1:8090.'
