"""Small dotenv reader/writer for operator scripts; never prints values."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
ENV = ROOT / '.env'
def load():
    values = {}
    if ENV.exists():
        for line in ENV.read_text().splitlines():
            if not line or line.startswith('#'): continue
            key, value = line.split('=', 1)
            values[key] = json.loads(value).replace('$$', '$')
    return values
def save(values):
    lines = []
    for key, value in values.items():
        if any(ord(c) < 32 for c in value): raise ValueError('Settings cannot contain control characters')
        # JSON escaping handles quotes and backslashes. $$ prevents Compose interpolation.
        lines.append(key + '=' + json.dumps(value.replace('$', '$$'), ensure_ascii=False))
    ENV.touch(mode=0o600, exist_ok=True)
    ENV.chmod(0o600)
    ENV.write_text('\n'.join(lines) + '\n')
