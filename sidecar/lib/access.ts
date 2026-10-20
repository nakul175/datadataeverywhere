import 'server-only';
import { readFile } from 'node:fs/promises';
import { timingSafeEqual } from 'node:crypto';
import { headers } from 'next/headers';
import { z } from 'zod';
import { HttpError } from './errors';
export { HttpError } from './errors';
export const tableSchema = z.object({
  id: z.string().regex(/^[a-zA-Z0-9_-]{1,100}$/),
  name: z.string().min(1).max(100),
  fields: z.array(z.string().min(1).max(200)).min(1).max(30),
});
const configSchema = z.object({
  tables: z.array(tableSchema),
  users: z.record(z.string().min(1).max(254), z.array(z.string())),
});
export type Table = z.infer<typeof tableSchema>;
export async function identity() {
  if (process.env.AUTH_MODE === 'nocodb') return (await (await import('./session')).currentSession()).email;
  const h = await headers();
  const actual = Buffer.from(h.get('x-dde-proxy-secret') || '');
  const expected = Buffer.from(process.env.PROXY_SECRET || '');
  if (!expected.length || actual.length !== expected.length || !timingSafeEqual(actual, expected)) {
    throw new HttpError(401, 'Authentication required.');
  }
  const user = h.get('x-dde-user');
  if (!user || !/^[a-zA-Z0-9_.-]{1,64}$/.test(user)) throw new HttpError(401, 'Authentication required.');
  return user;
}
export async function allowedTables(user: string) {
  const cfg = configSchema.parse(JSON.parse(await readFile(process.env.ACCESS_FILE || '/app/config/access.json', 'utf8')));
  const allowed = cfg.users[user] || [];
  return cfg.tables.filter(t => allowed.includes(t.id));
}
export function errorResponse(error: unknown) {
  const known = error instanceof HttpError;
  // Do not log provider/NocoDB response bodies or table content.
  if (!known) console.error('Request failed:', error instanceof Error ? error.name : 'UnknownError');
  return Response.json({ error: known ? error.message : 'Service unavailable. Contact your administrator.' }, {
    status: known ? error.status : 503,
    headers: { 'Cache-Control': 'no-store', ...(known && error.status === 429 ? { 'Retry-After': '60' } : {}) },
  });
}
