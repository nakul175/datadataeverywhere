import 'server-only';
import { HttpError, type Table } from './access';
const MAX_ROWS = 100;
const MAX_JSON_BYTES = 24000;
async function get(path: string, signal: AbortSignal) {
  if (process.env.AUTH_MODE === 'nocodb') {
    const { currentSession } = await import('./session');
    const { engine } = await import('./engine');
    return engine(path, (await currentSession()).token, 'GET', undefined, signal);
  }
  if (!process.env.NOCODB_API_TOKEN)
    throw new HttpError(503, 'NocoDB API token has not been configured.');
  const response = await fetch(new URL(path, process.env.NOCODB_URL || 'http://nocodb:8080'), {
    headers: { 'xc-token': process.env.NOCODB_API_TOKEN },
    signal: AbortSignal.any([signal, AbortSignal.timeout(10000)]),
    cache: 'no-store',
    redirect: 'error',
  });
  if (!response.ok) throw new HttpError(502, 'Unable to read the approved NocoDB table.');
  // Bound even a misconfigured upstream; never buffer an unlimited response.
  if (!response.body) throw new HttpError(502, 'Empty NocoDB response.');
  const reader = response.body.getReader();
  const chunks: Uint8Array[] = [];
  let size = 0;
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      size += value.length;
      if (size > 2_000_000)
        throw new HttpError(
          413,
          'NocoDB response exceeds safety limit. Select fewer/smaller fields.',
        );
      chunks.push(value);
    }
  } finally {
    await reader.cancel().catch(() => {});
  }
  return JSON.parse(Buffer.concat(chunks).toString('utf8'));
}
export async function tableContext(table: Table, signal: AbortSignal) {
  const meta = await get(`/api/v2/meta/tables/${encodeURIComponent(table.id)}`, signal);
  if (!Array.isArray(meta.columns)) throw new HttpError(502, 'Unexpected NocoDB schema response.');
  const columns = meta.columns.filter(
    (c: { title?: string }) => c.title && table.fields.includes(c.title),
  );
  if (columns.length !== table.fields.length)
    throw new HttpError(
      409,
      'Approved fields changed. Ask an administrator to update access.json.',
    );
  const schema = columns.map((c: { title: string; uidt: string; dt: string; pk?: boolean }) => ({
    name: c.title,
    type: c.uidt || c.dt,
    primaryKey: Boolean(c.pk),
  }));
  if (Buffer.byteLength(JSON.stringify(schema)) > 4000)
    throw new HttpError(413, 'Schema exceeds context limit.');
  const rows: Record<string, unknown>[] = [];
  let offset = 0;
  let complete = false;
  let truncatedForSize = false;
  // A bounded first-page sample; no claim of whole-table aggregates or filtered-view equivalence.
  while (rows.length < MAX_ROWS) {
    const query = new URLSearchParams({
      limit: String(Math.min(25, MAX_ROWS - rows.length)),
      offset: String(offset),
      fields: table.fields.join(','),
    });
    const page = await get(
      `/api/v2/tables/${encodeURIComponent(table.id)}/records?${query}`,
      signal,
    );
    if (!Array.isArray(page.list)) throw new HttpError(502, 'Unexpected NocoDB row response.');
    for (const row of page.list) {
      // Defense in depth: only approved top-level columns reach the model.
      const projected = Object.fromEntries(table.fields.map((f) => [f, row[f] ?? null]));
      if (Buffer.byteLength(JSON.stringify([...rows, projected])) > MAX_JSON_BYTES) {
        truncatedForSize = true;
        break;
      }
      rows.push(projected);
    }
    offset += page.list.length;
    if (truncatedForSize) break;
    if (page.pageInfo?.isLastPage === true || page.list.length === 0) {
      complete = true;
      break;
    }
  }
  return {
    tableId: table.id,
    table: table.name,
    fetchedAt: new Date().toISOString(),
    schema,
    rows,
    rowsIncluded: rows.length,
    complete,
    truncated: !complete,
    scope:
      'Unfiltered bounded table sample; not the current NocoDB view. No attachments are downloaded.',
  };
}
