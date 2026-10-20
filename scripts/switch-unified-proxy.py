import pathlib, subprocess, time, os, urllib.request
main = pathlib.Path('/etc/caddy/Caddyfile')
old = main.read_text()
expected = 'import /etc/caddy/datadataeverywhere/site.caddy'
if old.count(expected) != 1 or 'datadataeverywhere.aplyd.org {' in old:
    raise SystemExit('Unexpected Caddy configuration; refusing automatic replacement.')
# Check the new app locally before changing any public routes.
for path in ['/api/health', '/signin']:
    with urllib.request.urlopen('http://127.0.0.1:3301' + path, timeout=5) as res:
        if res.status != 200: raise SystemExit('New app readiness failed.')
addition = '''# DataDataEverywhere unified workspace; native data engine remains on 8080.
datadataeverywhere.aplyd.org {
  encode zstd gzip
  header {
    Strict-Transport-Security "max-age=31536000"
    X-Content-Type-Options "nosniff"
    Referrer-Policy "same-origin"
    X-Frame-Options "DENY"
    X-Robots-Tag "noindex, nofollow"
  }
  request_body {
    max_size 64KB
  }
  @native path /nocodb /nocodb/*
  redir @native https://nocodb.datadataeverywhere.aplyd.org 302
  reverse_proxy 127.0.0.1:3301 {
    flush_interval -1
  }
}
nocodb.datadataeverywhere.aplyd.org {
  encode zstd gzip
  header X-Content-Type-Options "nosniff"
  reverse_proxy 127.0.0.1:8080
}
'''
new = old.replace(expected, addition)
folder = pathlib.Path.home() / 'datadataeverywhere/shared'
backup = folder / ('Caddyfile.before-unified-' + time.strftime('%Y%m%d%H%M%S'))
backup.write_text(old); backup.chmod(0o600)
# Only use the account's explicitly allowed Caddy management commands.
def write(text):
    subprocess.run(['sudo', '-n', '/usr/bin/tee', '/etc/caddy/Caddyfile'], input=text, text=True, stdout=subprocess.DEVNULL, check=True)
def validate():
    return subprocess.run(['sudo', '-n', '/usr/bin/caddy', 'validate', '--config', '/etc/caddy/Caddyfile'], capture_output=True, text=True)
write(new)
check = validate()
if check.returncode:
    write(old)
    print(check.stderr[-3000:])
    raise SystemExit('New proxy configuration failed validation; original restored without reloading.')
reload = subprocess.run(['sudo', '-n', '/usr/bin/systemctl', 'reload', 'caddy'], capture_output=True, text=True)
if reload.returncode:
    write(old)
    subprocess.run(['sudo', '-n', '/usr/bin/systemctl', 'reload', 'caddy'], capture_output=True, check=False)
    raise SystemExit('Proxy reload failed; original restored.')
print('Caddy validated and reloaded. Existing SheetHappensOfficer blocks preserved byte-for-byte.')
print('Rollback file: ' + str(backup))
