#!/usr/bin/env python3
import getpass, json, re
import bcrypt
from settings import ROOT
username=input('Dashboard username: ').strip()
if not re.fullmatch(r'[a-zA-Z0-9_.-]{1,64}', username): raise SystemExit('Invalid username')
password=getpass.getpass('Dashboard password (12–64 ASCII characters): ')
if not 12<=len(password)<=64 or not password.isascii(): raise SystemExit('Invalid password')
if getpass.getpass('Confirm password: ')!=password: raise SystemExit('Passwords differ')
f=ROOT/'config/access.json'; cfg=json.loads(f.read_text())
allowed=input('Approved table IDs (comma-separated; blank gives no table access): ').strip()
ids=[s.strip() for s in allowed.split(',') if s.strip()]
if any(t not in {x['id'] for x in cfg['tables']} for t in ids): raise SystemExit('Unknown table ID. Register it with grant-table.py first.')
users=ROOT/'caddy/users.caddy'
entries=[s for s in users.read_text().splitlines() if s.split()[0]!=username]
entries.append(username+' '+bcrypt.hashpw(password.encode(),bcrypt.gensalt(rounds=12)).decode())
users.write_text('\n'.join(entries)+'\n')
cfg['users'][username]=ids; f.write_text(json.dumps(cfg,indent=2)+'\n')
print('User saved. Reload Caddy: docker compose exec caddy caddy reload --config /etc/caddy/Caddyfile')
