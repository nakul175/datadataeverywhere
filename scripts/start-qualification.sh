#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
umask 077
node -e 'if (Number(process.versions.node.split(".")[0]) < 22) process.exit(1)'
# Deliberately separate names/volumes/network/port; never load the production .env.
available=$(awk '/MemAvailable:/ {print $2}' /proc/meminfo)
if [ "${available:-0}" -lt 3145728 ]; then
  echo 'At least 3 GiB of available memory is required before starting this isolated qualification stack.' >&2
  exit 1
fi
mkdir -p .qualification
if [ ! -f .qualification/stack.env ]; then
  python3 - <<'PY'
from pathlib import Path
import secrets
p=Path('.qualification/stack.env')
with p.open('x') as f:
    for name in ['QA_DB_PASSWORD','QA_JWT_SECRET','QA_CONNECTION_KEY','QA_ADMIN_PASSWORD']:
        f.write(name+'='+secrets.token_hex(16 if name=='QA_CONNECTION_KEY' else 32)+'\n')
p.chmod(0o600)
PY
fi
docker compose --env-file .qualification/stack.env -f docker-compose.qualification.yml -p dde-qualification config --quiet
if ! docker compose --env-file .qualification/stack.env -f docker-compose.qualification.yml -p dde-qualification up -d --wait --wait-timeout 360; then
  # This stack contains synthetic fixtures only; redact every generated secret before diagnostics.
  python3 - <<'PY'
from pathlib import Path
import subprocess
result=subprocess.run(['docker','compose','--env-file','.qualification/stack.env','-f','docker-compose.qualification.yml','-p','dde-qualification','logs','--no-color','--tail','80'],capture_output=True,text=True,timeout=30)
diagnostic=result.stdout+result.stderr
for line in Path('.qualification/stack.env').read_text().splitlines():
    if '=' in line:
        value=line.split('=',1)[1]
        if value: diagnostic=diagnostic.replace(value,'[redacted-fixture-secret]')
print(diagnostic)
PY
  exit 1
fi
echo 'Isolated qualification engine is on loopback 19080. No public proxy was changed.'
node scripts/qualify-engine.mjs
