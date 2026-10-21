#!/usr/bin/env bash
# Run this from the DigitalOcean root console. Does not grant deploy new sudo rights.
set -euo pipefail
if [ "$(id -u)" != 0 ]; then echo 'Run from a root console.' >&2; exit 1; fi
src=$(cd "$(dirname "$0")/.." && pwd)
exec 9>/var/lock/datadataeverywhere-install.lock
flock -n 9 || { echo 'Another setup process is running.' >&2; exit 1; }
if ! systemctl is-active --quiet caddy; then echo 'Existing host Caddy must be active.' >&2; exit 1; fi
# Refuse port conflicts before installing anything.
python3 - <<'PYPORT'
import socket
for port in (8080,3300,8090):
    with socket.socket() as s:
        try: s.bind(('127.0.0.1',port))
        except OSError: raise SystemExit('Required local port is occupied: '+str(port))
PYPORT
if [ "$src" != /opt/datadataeverywhere ]; then
  if [ -e /opt/datadataeverywhere ]; then
    echo '/opt/datadataeverywhere already exists. Inspect it before retrying.' >&2; exit 1
  fi
  install -d -m 700 /opt/datadataeverywhere
  cp -a "$src/." /opt/datadataeverywhere/
  chown -R root:root /opt/datadataeverywhere
fi
cd /opt/datadataeverywhere
apt-get update
apt-get install -y ca-certificates curl python3 python3-bcrypt
if ! command -v docker >/dev/null; then
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
fi
systemctl enable --now docker
if [ ! -f .env ]; then
  python3 scripts/configure.py
else
  python3 scripts/prepare-mathesar.py
fi
python3 - <<'PYENV'
import sys
sys.path.insert(0,'scripts')
from settings import load, save
values=load(); values['COMPOSE_FILE']='docker-compose.shared.yml'; save(values)
PYENV
python3 scripts/pin-images.py
docker compose config --quiet
docker compose build --pull
docker compose up -d --wait --wait-timeout 300
curl --fail --silent --show-error http://127.0.0.1:3300/api/health
python3 scripts/install-host-proxy.py
# Show status without disclosing environment variables or credentials.
docker compose ps
printf '\nDeployment installed. Verify HTTPS at:\nhttps://datadataeverywhere.aplyd.org\n'
printf 'Mathesar is internal only. Use an SSH tunnel to 127.0.0.1:8090 for administrator setup.\n'
