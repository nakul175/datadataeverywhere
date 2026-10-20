#!/usr/bin/env python3
"""Resolve operator-selected tags to immutable digests; do not print env values."""
import subprocess
from settings import load, save
values=load()
for key in ('NODE_IMAGE','POSTGRES_IMAGE','REDIS_IMAGE','NOCODB_IMAGE','CADDY_IMAGE'):
    image=values[key]
    subprocess.run(['docker','pull',image],check=True)
    digest=subprocess.check_output(['docker','image','inspect',image,'--format','{{index .RepoDigests 0}}'],text=True).strip()
    if '@sha256:' not in digest: raise SystemExit('Could not resolve '+key)
    values[key]=digest
save(values)
print('Service image digests pinned in .env. Review and test before future upgrades.')
