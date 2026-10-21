import 'server-only';
import { readFileSync } from 'node:fs';
import { Client } from 'pg';
import { z } from 'zod';
import { HttpError } from '../errors';
import { engine } from '../engine';
import {
  canonical,
  hash,
  sourceSchema,
  schemaFor,
  type Source,
  type Grant,
  type Schema,
} from './contracts';
export function sources(): Source[] {
  if (process.env.FEEDS_ENABLED !== 'true')
    throw new HttpError(503, 'Governed feeds are disabled.');
  const file = process.env.FEEDS_SOURCES_FILE;
  if (!file) throw new HttpError(503, 'Reviewed feed mappings are not configured.');
  try {
    const list = z
      .array(sourceSchema)
      .max(64)
      .parse(JSON.parse(readFileSync(file, 'utf8')));
    if (new Set(list.map((s) => s.id)).size !== list.length) throw new Error();
    for (const s of list)
      if (
        new Set(s.fields.map((f) => f.id)).size !== s.fields.length ||
        new Set(s.fields.map((f) => f.column)).size !== s.fields.length
      )
        throw new Error();
    return list;
  } catch {
    throw new HttpError(503, 'Invalid reviewed feed mappings.');
  }
}
export function sourceFor(id: string) {
  const s = sources().find((s) => s.id === id);
  if (!s) throw new HttpError(403, 'Feed source is unavailable.');
  return s;
}
async function service(path: string) {
  const token = process.env.FEEDS_NOCODB_TOKEN;
  if (!token) throw new HttpError(503, 'Source authority verification is not configured.');
  // A separate metadata verification credential; this client issues GET requests only.
  const response = await fetch(new URL(path, process.env.NOCODB_URL || 'http://127.0.0.1:8080'), {
    headers: { 'xc-token': token },
    redirect: 'error',
    cache: 'no-store',
    signal: AbortSignal.timeout(10000),
  });
  if (!response.ok) throw new HttpError(403, 'Source authorization cannot be verified.');
  const body = response.body?.getReader();
  if (!body) throw new HttpError(502, 'Source authority is unavailable.');
  let size = 0;
  const parts: Uint8Array[] = [];
  try {
    while (true) {
      const { done, value } = await body.read();
      if (done) break;
      size += value.length;
      if (size > 1_000_000) throw new HttpError(503, 'Source authority response is too large.');
      parts.push(value);
    }
  } finally {
    await body.cancel().catch(() => {});
  }
  return JSON.parse(Buffer.concat(parts).toString('utf8'));
}
const simple = new Set([
  'ID',
  'SingleLineText',
  'LongText',
  'Email',
  'PhoneNumber',
  'URL',
  'Number',
  'Decimal',
  'Currency',
  'Percent',
  'Checkbox',
  'Date',
  'DateTime',
  'Duration',
  'Year',
  'SingleSelect',
]);
export async function authority(
  source: Source,
  owner: string,
  grant: Grant,
  actor?: { id: string; token: string },
  validateSchema = true,
): Promise<Schema> {
  if (actor) await engine(`/api/v2/meta/tables/${source.tableId}`, actor.token);
  const [users, meta] = await Promise.all([
    service(`/api/v2/meta/bases/${source.baseId}/users`),
    service(`/api/v2/meta/tables/${source.tableId}`),
  ]);
  const members = users.users?.list || users.users || users.list;
  if (!Array.isArray(members) || meta.base_id !== source.baseId || meta.id !== source.tableId)
    throw new HttpError(403, 'Source mapping cannot be verified.');
  const admin = (userId: string) =>
    members.some(
      (m: { id?: string; roles?: unknown }) =>
        m.id === userId &&
        (typeof m.roles === 'string'
          ? m.roles.split(',').some((r) => ['owner', 'creator'].includes(r.trim()))
          : m.roles &&
            typeof m.roles === 'object' &&
            Object.entries(m.roles).some(
              ([k, v]) => ['owner', 'creator'].includes(k) && v === true,
            )),
    );
  if (!admin(owner) || (actor && !admin(actor.id)))
    throw new HttpError(403, 'A current full-base owner or creator is required.');
  if (!validateSchema) return schemaFor(source, grant);
  if (!Array.isArray(meta.columns)) throw new HttpError(409, 'Feed schema requires review.');
  for (const fieldId of new Set([
    ...grant.fields,
    ...(grant.scope.kind === 'equals' ? [grant.scope.field] : []),
  ])) {
    const field = source.fields.find((f) => f.id === fieldId);
    const column = meta.columns.find((c: { id: string }) => c.id === fieldId);
    if (
      !field ||
      !column ||
      column.column_name !== field.column ||
      column.title !== field.title ||
      column.uidt !== field.uidt ||
      !simple.has(column.uidt)
    )
      throw new FeedSchemaError(
        fieldId,
        column
          ? {
              id: column.id,
              column: column.column_name,
              title: column.title,
              type: column.uidt,
              dt: column.dt,
            }
          : { id: fieldId, removed: true },
      );
  }
  return schemaFor(source, grant);
}
const quote = (v: string) => `"${v.replaceAll('"', '""')}"`;
const types = new Set([
  'text',
  'character varying',
  'character',
  'smallint',
  'integer',
  'bigint',
  'numeric',
  'real',
  'double precision',
  'boolean',
  'date',
  'timestamp without time zone',
  'timestamp with time zone',
  'uuid',
]);
export async function extract(
  source: Source,
  grant: Grant,
  schema: Schema,
  accept: (key: string, values: Record<string, string | null>) => void,
  signal?: AbortSignal,
) {
  const url = process.env.FEEDS_DATABASE_URL;
  if (!url) throw new HttpError(503, 'Read-only PostgreSQL connector is not configured.');
  const client = new Client({
    connectionString: url,
    connectionTimeoutMillis: 5000,
    query_timeout: 10000,
    statement_timeout: 10000,
    application_name: 'dde-readonly-feed',
  });
  client.on('error', () => {});
  const abort = () => {
    void client.end().catch(() => {});
  };
  const deadline = setTimeout(abort, 45000);
  signal?.addEventListener('abort', abort, { once: true });
  try {
    if (signal?.aborted) throw new HttpError(499, 'Export interrupted; restart.');
    await client.connect();
    await client.query('BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY');
    await assertView(client, source);
    await client.query("SET LOCAL TIME ZONE 'UTC'");
    await client.query("SET LOCAL DateStyle = 'ISO, YMD'");
    await client.query('SET LOCAL extra_float_digits = 3');
    await client.query("SET LOCAL idle_in_transaction_session_timeout = '10000ms'");
    const role = await client.query(
      'SELECT rolsuper, rolbypassrls FROM pg_roles WHERE rolname=current_user',
    );
    if (role.rows[0]?.rolsuper || role.rows[0]?.rolbypassrls)
      throw new HttpError(503, 'Connector role must not bypass source security.');
    const relation = await client.query(
      'SELECT c.relkind FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname=$1 AND c.relname=$2',
      [source.schema, source.view],
    );
    if (relation.rows[0]?.relkind !== 'v')
      throw new HttpError(409, 'Only reviewed SQL views can be exported.');
    const columns = await client.query(
      'SELECT column_name, data_type FROM information_schema.columns WHERE table_schema=$1 AND table_name=$2',
      [source.schema, source.view],
    );
    const scope = grant.scope;
    const required = [
      ...new Set([
        source.key,
        ...schema.fields.map((f) => f.column),
        ...(scope.kind === 'equals'
          ? [source.fields.find((f) => f.id === scope.field)?.column || '']
          : []),
      ]),
    ];
    for (const name of required) {
      const actual = columns.rows.find((c) => c.column_name === name);
      const mapped = source.fields.find((f) => f.column === name);
      if (!actual || !types.has(actual.data_type) || (mapped && actual.data_type !== mapped.pgType))
        throw new HttpError(409, 'SQL view schema changed; reapprove the mapping.');
    }
    const parameters: unknown[] = [];
    let where = '';
    if (scope.kind === 'equals') {
      const field = source.fields.find((f) => f.id === scope.field);
      if (!field) throw new HttpError(403, 'Row scope is not approved.');
      const values = scope.values.filter((v) => v !== null);
      parameters.push(values);
      where = ` WHERE (${quote(field.column)}::text = ANY($1::text[])${scope.values.includes(null) ? ` OR ${quote(field.column)} IS NULL` : ''})`;
    }
    const fields = schema.fields.map(
      (f, i) => `left(${quote(f.column)}::text, 8193) AS ${quote(`f${i}`)}`,
    );
    await client.query(
      `DECLARE dde_rows NO SCROLL CURSOR FOR SELECT left(${quote(source.key)}::text,1001) AS source_key, ${fields.join(',')} FROM ${quote(source.schema)}.${quote(source.view)}${where} ORDER BY ${quote(source.key)}::text COLLATE "C"`,
      parameters,
    );
    let previous: string | undefined;
    while (true) {
      if (signal?.aborted) throw new HttpError(499, 'Export interrupted; restart.');
      const page = await client.query('FETCH FORWARD 10 FROM dde_rows');
      for (const row of page.rows) {
        if (
          typeof row.source_key !== 'string' ||
          row.source_key.length > 1000 ||
          row.source_key === previous
        )
          throw new HttpError(409, 'Source keys must be unique, non-null and bounded.');
        previous = row.source_key;
        const values = Object.fromEntries(
          schema.fields.map((f, i) => [f.id, row[`f${i}`] as string | null]),
        );
        if (Object.values(values).some((v) => v !== null && Buffer.byteLength(v) > 8192))
          throw new HttpError(
            413,
            'Field value exceeds complete-export limits; narrow the approved dataset.',
          );
        accept(row.source_key, values);
      }
      if (page.rows.length < 10) break;
    }
    await client.query('COMMIT');
  } catch (e) {
    await client.query('ROLLBACK').catch(() => {});
    if (e instanceof HttpError) throw e;
    throw new HttpError(
      503,
      'Snapshot extraction failed; no complete export was published. Restart after checking the connector.',
    );
  } finally {
    clearTimeout(deadline);
    signal?.removeEventListener('abort', abort);
    await client.end().catch(() => {});
  }
}

async function assertView(client: Client, source: Source) {
  const result = await client.query(
    `SELECT c.relkind, pg_get_viewdef(c.oid,true) AS definition,
    has_table_privilege(c.oid,'SELECT') AS readable,
    has_table_privilege(c.oid,'INSERT,UPDATE,DELETE,TRUNCATE,REFERENCES,TRIGGER') AS writable,
    r.rolsuper,r.rolbypassrls FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
    JOIN pg_roles r ON r.rolname=current_user WHERE n.nspname=$1 AND c.relname=$2`,
    [source.schema, source.view],
  );
  const row = result.rows[0];
  if (
    !row ||
    row.relkind !== 'v' ||
    !row.readable ||
    row.writable ||
    row.rolsuper ||
    row.rolbypassrls
  )
    throw new HttpError(403, 'Reviewed view is unavailable to the restricted connector role.');
  const cols = await client.query(
    'SELECT column_name,data_type FROM information_schema.columns WHERE table_schema=$1 AND table_name=$2',
    [source.schema, source.view],
  );
  for (const field of source.fields) {
    const actual = cols.rows.find((c) => c.column_name === field.column);
    if (!actual || actual.data_type !== field.pgType || !types.has(actual.data_type))
      throw new FeedSchemaError(field.id, { type: actual?.data_type || 'unavailable' });
  }
  if (hash(row.definition) !== source.viewDefinitionHash)
    throw new HttpError(
      409,
      'SQL view definition changed; pause and reapprove the source mapping.',
    );
}
export async function verifyView(source: Source) {
  const url = process.env.FEEDS_DATABASE_URL;
  if (!url) throw new HttpError(503, 'Read-only PostgreSQL connector is not configured.');
  const client = new Client({
    connectionString: url,
    connectionTimeoutMillis: 5000,
    query_timeout: 5000,
    statement_timeout: 5000,
  });
  client.on('error', () => {});
  const deadline = setTimeout(() => {
    void client.end().catch(() => {});
  }, 12000);
  try {
    await client.connect();
    await assertView(client, source);
  } catch (e) {
    if (e instanceof HttpError) throw e;
    throw new HttpError(503, 'Source view authorization cannot be verified.');
  } finally {
    clearTimeout(deadline);
    await client.end().catch(() => {});
  }
}

export class FeedSchemaError extends HttpError {
  readonly change: { version: string; fields: string[]; migration: string };
  constructor(field: string | string[], observed: unknown, reason?: string) {
    const fields = Array.isArray(field) ? field : [field];
    super(
      409,
      reason ||
        `Schema changed for approved field ${fields.join(',')}; pause and reapprove the mapping.`,
    );
    this.change = {
      version: hash(canonical(observed)),
      fields,
      migration:
        'Review the changed field and create a newly approved grant. Existing consumers remain paused.',
    };
  }
}
