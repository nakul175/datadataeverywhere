#!/bin/sh
set -eu
# Values are passed as psql variables, never interpolated into SQL.
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres \
  --set=ncpass="$NOCODB_DB_PASSWORD" --set=teampass="$TEAM_DB_PASSWORD" <<'SQL'
CREATE ROLE nocodb LOGIN PASSWORD :'ncpass' CONNECTION LIMIT 35;
CREATE DATABASE nocodb_meta OWNER nocodb;
CREATE ROLE teamdata LOGIN PASSWORD :'teampass' CONNECTION LIMIT 55;
CREATE DATABASE teamdata OWNER teamdata;
REVOKE ALL ON DATABASE nocodb_meta FROM PUBLIC;
REVOKE ALL ON DATABASE teamdata FROM PUBLIC;
SQL
