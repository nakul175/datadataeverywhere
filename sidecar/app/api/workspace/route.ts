import { z } from 'zod';
import { currentSession } from '@/lib/session';
import { engine, engineId, boundedBody, sameOrigin } from '@/lib/engine';
import { tableSchemaFor, checkedValues } from '@/lib/workspace';
import { allowedTables, HttpError, errorResponse } from '@/lib/access';
export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
const json = (data: unknown) => Response.json(data, { headers: { 'Cache-Control': 'no-store' } });
function listItems(data: { list?: unknown[] }) {
  if (!Array.isArray(data.list)) throw new HttpError(502, 'Unexpected list response.');
  return data.list as { id: string; title?: string; table_name?: string }[];
}
export async function GET(req: Request) {
  try {
    const session = await currentSession(); const q = new URL(req.url).searchParams;
    switch (q.get('action') || 'bases') {
      case 'bases': {
        const data = await engine('/api/v2/meta/bases/', session.token);
        return json({ bases: listItems(data).map(b => ({ id: b.id, title: b.title || 'Untitled workspace' })) });
      }
      case 'tables': {
        const data = await engine(`/api/v2/meta/bases/${engineId(q.get('baseId'))}/tables`, session.token);
        return json({ tables: listItems(data).map(t => ({ id: t.id, title: t.title || t.table_name || 'Untitled table' })) });
      }
      case 'records': {
        const id = engineId(q.get('tableId')); const offset = Number(q.get('offset') || 0);
        if (!Number.isSafeInteger(offset) || offset < 0 || offset > 10000000) throw new HttpError(400, 'Invalid page.');
        const columns = await tableSchemaFor(id, session.token);
        const data = await engine(`/api/v2/tables/${id}/records?limit=50&offset=${offset}`, session.token);
        if (!Array.isArray(data.list)) throw new HttpError(502, 'Unexpected records response.');
        // Do not forward arbitrary metadata or nested attachment URLs to the client.
        const rows = data.list.map((row: Record<string, unknown>) => Object.fromEntries(columns.map(c => [c.title, row[c.title] ?? null])));
        const approved = (await allowedTables(session.email)).find(t => t.id === id);
        const provider = process.env.AI_PROVIDER || 'openai';
        const ready = provider === 'anthropic' ? Boolean(process.env.ANTHROPIC_API_KEY) : Boolean(process.env.OPENAI_API_KEY);
        return json({ columns, rows, page: { offset, isLast: data.pageInfo?.isLastPage === true || rows.length < 50, total: Number.isSafeInteger(data.pageInfo?.totalRows) ? data.pageInfo.totalRows : null }, ai: { ready: ready && Boolean(approved), fields: approved?.fields || [], reason: !ready ? 'Your administrator needs to connect an AI provider.' : !approved ? 'This table needs approved AI fields before chatting.' : '' } });
      }
      default: throw new HttpError(400, 'Unknown workspace action.');
    }
  } catch (e) { return errorResponse(e); }
}
const name = z.string().trim().min(1).max(80).regex(/^[\p{L}\p{N} _-]+$/u, 'Use letters, numbers, spaces, dashes or underscores.');
const mutation = z.discriminatedUnion('action', [
  z.object({ action: z.literal('createBase'), title: name }).strict(),
  z.object({ action: z.literal('createTable'), baseId: z.string(), title: name }).strict(),
  z.object({ action: z.literal('createRecord'), tableId: z.string(), values: z.record(z.string(), z.unknown()) }).strict(),
  z.object({ action: z.literal('updateRecord'), tableId: z.string(), id: z.union([z.string().max(200), z.number()]), values: z.record(z.string(), z.unknown()) }).strict(),
]);
export async function POST(req: Request) {
  try {
    sameOrigin(req); const session = await currentSession();
    const parsed = mutation.safeParse(await boundedBody(req));
    if (!parsed.success) throw new HttpError(400, parsed.error.issues[0]?.message || 'Invalid change.');
    const body = parsed.data;
    if (body.action === 'createBase') {
      const data = await engine('/api/v2/meta/bases', session.token, 'POST', { title: body.title });
      return json({ id: data.id, title: data.title });
    }
    if (body.action === 'createTable') {
      const data = await engine(`/api/v2/meta/bases/${engineId(body.baseId)}/tables`, session.token, 'POST', {
        title: body.title, table_name: body.title.replace(/\s+/g, '_'), columns: [
          { title: 'Id', column_name: 'id', uidt: 'ID', dt: 'int4', pk: true, ai: true, rqd: true },
          { title: 'Title', column_name: 'title', uidt: 'SingleLineText', dt: 'text', pv: true },
          { title: 'Notes', column_name: 'notes', uidt: 'LongText', dt: 'text' },
        ],
      });
      return json({ id: data.id, title: data.title });
    }
    const id = engineId(body.tableId); const columns = await tableSchemaFor(id, session.token); const values = checkedValues(columns, body.values);
    if (body.action === 'updateRecord') {
      const keys = columns.filter(c => c.primary);
      if (keys.length !== 1) throw new HttpError(400, 'This table uses a complex record identifier. Edit it in the advanced spreadsheet.');
      await engine(`/api/v2/tables/${id}/records`, session.token, 'PATCH', { ...values, [keys[0].title]: body.id });
    } else await engine(`/api/v2/tables/${id}/records`, session.token, 'POST', values);
    return json({ ok: true });
  } catch (e) { return errorResponse(e); }
}
