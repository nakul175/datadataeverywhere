#!/usr/bin/env python3
"""Create or rotate Mathesar's private metadata role on an existing stack."""

import re
import secrets
import subprocess

from settings import load, save


values = load()
if not values:
    raise SystemExit("Run configure.py first")

password = values.get("MATHESAR_DB_PASSWORD") or secrets.token_hex(32)
if not re.fullmatch(r"[0-9a-f]{64}", password):
    raise SystemExit("MATHESAR_DB_PASSWORD must be the generated 64-character hex value")
values["MATHESAR_DB_PASSWORD"] = password
values.setdefault("MATHESAR_IMAGE", "mathesar/mathesar:0.12.0")
save(values)

sql = rf"""\set mathesarpass {password}
\set ON_ERROR_STOP on
SELECT CASE
  WHEN EXISTS (SELECT FROM pg_roles WHERE rolname = 'mathesar')
    THEN format('ALTER ROLE mathesar LOGIN PASSWORD %L CONNECTION LIMIT 20', :'mathesarpass')
  ELSE format('CREATE ROLE mathesar LOGIN PASSWORD %L CONNECTION LIMIT 20', :'mathesarpass')
END \gexec
SELECT 'CREATE DATABASE mathesar_meta OWNER mathesar'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mathesar_meta') \gexec
ALTER DATABASE mathesar_meta OWNER TO mathesar;
REVOKE ALL ON DATABASE mathesar_meta FROM PUBLIC;
"""
subprocess.run(
    [
        "docker",
        "compose",
        "exec",
        "-T",
        "postgres",
        "psql",
        "--username",
        "postgres",
        "--dbname",
        "postgres",
    ],
    input=sql,
    text=True,
    check=True,
)
print("Mathesar metadata role and database are ready. No secret was printed.")
