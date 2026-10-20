#!/usr/bin/env python3
import json, re
from settings import ROOT
f=ROOT/'config/access.json'; cfg=json.loads(f.read_text())
table=input('NocoDB table ID: ').strip()
if not re.fullmatch(r'[a-zA-Z0-9_-]{1,100}',table): raise SystemExit('Invalid table ID')
name=input('Display name: ').strip()
fields=[s.strip() for s in input('Approved field titles (comma-separated, exact case; include primary key): ').split(',') if s.strip()]
users=[s.strip() for s in input('Dashboard usernames to grant access (comma-separated): ').split(',') if s.strip()]
if not name or len(name)>100 or not 1<=len(fields)<=30 or len(fields)!=len(set(fields)) or any(len(s)>200 for s in fields): raise SystemExit('Invalid name or fields')
if any(u not in cfg['users'] for u in users): raise SystemExit('Unknown dashboard username')
cfg['tables']=[t for t in cfg['tables'] if t['id']!=table]+[{'id':table,'name':name,'fields':fields}]
for u in users:
    if table not in cfg['users'][u]: cfg['users'][u].append(table)
f.write_text(json.dumps(cfg,indent=2)+'\n')
print('Table registered and grants applied. Reload the dashboard page; server checks access on every request.')
