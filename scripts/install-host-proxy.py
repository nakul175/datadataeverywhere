#!/usr/bin/env python3
"""Run as root: add DDE hosts to the existing Caddy without replacing other sites."""
import grp, os, shutil, subprocess, time
from pathlib import Path
from settings import ROOT, load
if os.geteuid() != 0: raise SystemExit('Run from a root console')
values = load()
for key in ('PROXY_SECRET','NC_ADMIN_EMAIL'):
    if not values.get(key): raise SystemExit('Missing deployment configuration: '+key)
main = Path('/etc/caddy/Caddyfile')
if not main.is_file(): raise SystemExit('An existing host Caddy installation is required')
original = main.read_text()
include = 'import /etc/caddy/datadataeverywhere/site.caddy'
if include not in original and 'datadataeverywhere.aplyd.org' in original:
    raise SystemExit('These hosts already exist in Caddy. Review their configuration before installing.')
folder = Path('/etc/caddy/datadataeverywhere')
folder.mkdir(mode=0o750, exist_ok=True)
gid = grp.getgrnam('caddy').gr_gid
os.chown(folder,0,gid); folder.chmod(0o750)
source = (ROOT/'Caddyfile').read_text()
source = source[source.index('datadataeverywhere.aplyd.org {'):]
source = source.replace('/etc/caddy/users/users.caddy','/etc/caddy/datadataeverywhere/users.caddy')
source = source.replace('sidecar:3000','127.0.0.1:3300').replace('nocodb:8080','127.0.0.1:8080')
source = source.replace('{$PROXY_SECRET}',values['PROXY_SECRET'])
site = folder/'site.caddy'; users = folder/'users.caddy'
old_site = site.read_bytes() if site.exists() else None
old_users = users.read_bytes() if users.exists() else None
backup = Path('/var/backups/datadataeverywhere')
backup.mkdir(mode=0o700,parents=True,exist_ok=True); backup.chmod(0o700)
shutil.copy2(main,backup/('Caddyfile.'+time.strftime('%Y%m%dT%H%M%SZ',time.gmtime())))
try:
    site.write_text(source)
    shutil.copyfile(ROOT/'caddy/users.caddy',users)
    for f in (site,users): os.chown(f,0,gid); f.chmod(0o640)
    if include not in original: main.write_text(original.rstrip()+'\n\n'+include+'\n')
    result = subprocess.run(['caddy','validate','--config',str(main),'--adapter','caddyfile'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    if result.returncode: raise RuntimeError('Caddy validation failed; original configuration restored')
    subprocess.run(['systemctl','reload','caddy'],check=True)
except BaseException:
    main.write_text(original)
    for f,data in ((site,old_site),(users,old_users)):
        if data is None: f.unlink(missing_ok=True)
        else: f.write_bytes(data)
    subprocess.run(['systemctl','reload','caddy'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    raise
print('Host proxy installed. Existing Caddy sites retained; graceful reload completed.')
