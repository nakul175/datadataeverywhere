#!/usr/bin/env python3
import getpass, sys
from settings import load, save
allowed = {'OPENAI_API_KEY','ANTHROPIC_API_KEY','ANTHROPIC_MODEL','AI_PROVIDER','NOCODB_API_TOKEN',
 'NC_SMTP_HOST','NC_SMTP_PORT','NC_SMTP_USERNAME','NC_SMTP_PASSWORD','NC_SMTP_FROM','NC_SMTP_SECURE',
 'USER_DAILY_TOKEN_BUDGET','GLOBAL_DAILY_TOKEN_BUDGET'}
if len(sys.argv)!=2 or sys.argv[1] not in allowed:
    raise SystemExit('Usage: python3 scripts/set-secret.py KEY\nAllowed keys: '+', '.join(sorted(allowed)))
values=load()
if not values: raise SystemExit('Run configure.py first')
key=sys.argv[1]; value=getpass.getpass('New value for '+key+': ')
if key=='AI_PROVIDER' and value not in ('openai','anthropic'): raise SystemExit('Invalid provider')
if key.endswith('_TOKEN_BUDGET') and (not value.isdigit() or not 1000<=int(value)<=100_000_000): raise SystemExit('Budget must be an integer between 1000 and 100000000')
values[key]=value; save(values)
print('Setting updated. Recreate the affected container to apply it.')
