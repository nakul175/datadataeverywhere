#!/usr/bin/env bash
set -euo pipefail
umask 077
# Run as the existing deploy account. Data engine containers are left intact.
release_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
app_root="$HOME/datadataeverywhere"
source_dir="$release_root/sidecar"
if [[ "$(id -u)" == 0 ]]; then echo 'Run as deploy, not root.' >&2; exit 1; fi
if [[ ! -f "$source_dir/package-lock.json" ]]; then echo 'Release source missing.' >&2; exit 1; fi
node_bin="$(command -v node)"
node -e 'if (Number(process.versions.node.split(".")[0]) < 22) process.exit(1)'
mkdir -p "$app_root/shared" "$app_root/shared/data" "$HOME/.config/systemd/user"
chmod 700 "$app_root" "$app_root/shared" "$app_root/shared/data"
if [[ ! -f "$app_root/shared/access.json" ]]; then printf '%s\n' '{"tables":[],"users":{}}' > "$app_root/shared/access.json"; fi
if [[ ! -f "$app_root/shared/runtime.env" ]]; then
  cat > "$app_root/shared/runtime.env" <<ENV
AUTH_MODE=nocodb
APP_ORIGIN=https://datadataeverywhere.aplyd.org
NOCODB_URL=http://127.0.0.1:8080
ACCESS_FILE=$app_root/shared/access.json
SQLITE_BUDGET_FILE=$app_root/shared/data/budget.sqlite
AI_PROVIDER=openai
USER_DAILY_TOKEN_BUDGET=500000
GLOBAL_DAILY_TOKEN_BUDGET=5000000
ENV
fi
chmod 600 "$app_root/shared/runtime.env" "$app_root/shared/access.json"
cd "$source_dir"
npm ci --ignore-scripts --cache "$app_root/npm-cache"
NEXT_TELEMETRY_DISABLED=1 NODE_OPTIONS=--max-old-space-size=1536 npm run build
cp -a public .next/standalone/public
cp -a .next/static .next/standalone/.next/static
previous="$(readlink "$app_root/current" || true)"
ln -sfn "$source_dir" "$app_root/.current-next"
mv -Tf "$app_root/.current-next" "$app_root/current"
cat > "$HOME/.config/systemd/user/datadataeverywhere.service" <<UNIT
[Unit]
Description=DataDataEverywhere unified workspace
After=network.target
[Service]
Type=simple
WorkingDirectory=$app_root/current/.next/standalone
ExecStart=$node_bin $app_root/current/.next/standalone/server.js
Environment=NODE_ENV=production
Environment=NEXT_TELEMETRY_DISABLED=1
Environment=HOSTNAME=127.0.0.1
Environment=PORT=3301
EnvironmentFile=$app_root/shared/runtime.env
Restart=on-failure
RestartSec=5
TimeoutStopSec=100
KillSignal=SIGTERM
UMask=0077
NoNewPrivileges=true
RestrictSUIDSGID=true
MemoryMax=768M
TasksMax=128
[Install]
WantedBy=default.target
UNIT
loginctl enable-linger "$(id -un)"
systemctl --user daemon-reload
systemctl --user enable datadataeverywhere.service
systemctl --user restart datadataeverywhere.service
healthy=false
for attempt in {1..30}; do
  if curl -fsS --max-time 2 http://127.0.0.1:3301/api/health > /dev/null; then healthy=true; break; fi
  sleep 1
done
if [[ "$healthy" != true ]]; then
  if [[ -n "$previous" ]]; then ln -sfn "$previous" "$app_root/.current-next"; mv -Tf "$app_root/.current-next" "$app_root/current"; systemctl --user restart datadataeverywhere.service; fi
  echo 'Release failed readiness check; previous symlink restored if available.' >&2; exit 1
fi
printf '%s\n' 'Unified app ready on 127.0.0.1:3301. Public proxy switch is a separate validated step.'
