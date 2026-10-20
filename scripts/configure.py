#!/usr/bin/env python3
import getpass, json, re, secrets
from settings import ROOT, ENV, save
try:
    import bcrypt
except ImportError:
    raise SystemExit('Install python3-bcrypt first: apt-get install python3-bcrypt')
if ENV.exists(): raise SystemExit('.env exists. Use scripts/set-secret.py to update individual settings.')
email = input('NocoDB administrator email (also ACME contact): ').strip()
if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email): raise SystemExit('Invalid email')
username = input('AI dashboard administrator username: ').strip()
if not re.fullmatch(r'[a-zA-Z0-9_.-]{1,64}', username): raise SystemExit('Invalid username')
password = getpass.getpass('AI dashboard password (12–64 ASCII characters): ')
if not 12 <= len(password) <= 64 or not password.isascii(): raise SystemExit('Use 12–64 ASCII characters')
if getpass.getpass('Confirm dashboard password: ') != password: raise SystemExit('Passwords differ')
admin_password = getpass.getpass('NocoDB administrator password (12+ chars, upper/lower/number/special): ')
if len(admin_password) < 12 or not all((re.search('[A-Z]',admin_password),re.search('[a-z]',admin_password),re.search('[0-9]',admin_password),any(c in "$&+,:;=?@#'.^*()%!_-\"" for c in admin_password))):
    raise SystemExit('NocoDB password does not meet requirements')
if getpass.getpass('Confirm NocoDB password: ') != admin_password: raise SystemExit('Passwords differ')
provider = input('AI provider [openai/anthropic] (openai): ').strip() or 'openai'
if provider not in ('openai','anthropic'): raise SystemExit('Invalid provider')
key = getpass.getpass('Provider API key (blank to configure later): ')
values = {
    'NODE_IMAGE':'node:24-alpine', 'POSTGRES_IMAGE':'postgres:17-alpine', 'REDIS_IMAGE':'redis:7-alpine',
    'NOCODB_IMAGE':'nocodb/nocodb:2026.09.1', 'CADDY_IMAGE':'caddy:2-alpine',
    'POSTGRES_PASSWORD':secrets.token_hex(32), 'NOCODB_DB_PASSWORD':secrets.token_hex(32),
    'TEAM_DB_PASSWORD':secrets.token_hex(32), 'NC_AUTH_JWT_SECRET':secrets.token_hex(48),
    'NC_CONNECTION_ENCRYPT_KEY':secrets.token_hex(16), 'PROXY_SECRET':secrets.token_hex(48), 'NC_ADMIN_EMAIL':email, 'NC_ADMIN_PASSWORD':admin_password,
    'AI_PROVIDER':provider, 'OPENAI_API_KEY':key if provider=='openai' else '',
    'ANTHROPIC_API_KEY':key if provider=='anthropic' else '', 'OPENAI_MODEL':'gpt-4o', 'ANTHROPIC_MODEL':'',
    'NOCODB_API_TOKEN':'', 'USER_DAILY_TOKEN_BUDGET':'500000', 'GLOBAL_DAILY_TOKEN_BUDGET':'5000000',
    'NC_SMTP_HOST':'', 'NC_SMTP_PORT':'587', 'NC_SMTP_USERNAME':'', 'NC_SMTP_PASSWORD':'',
    'NC_SMTP_FROM':'', 'NC_SMTP_SECURE':'false',
}
save(values)
(ROOT/'caddy').mkdir(exist_ok=True)
(ROOT/'caddy/users.caddy').write_text(username + ' ' + bcrypt.hashpw(password.encode(),bcrypt.gensalt(rounds=12)).decode() + '\n')
(ROOT/'config').mkdir(exist_ok=True)
(ROOT/'config/access.json').write_text(json.dumps({'tables':[], 'users':{username:[]}}, indent=2)+'\n')
print('Configuration saved. Secrets were not printed. Keep .env out of Git.')
