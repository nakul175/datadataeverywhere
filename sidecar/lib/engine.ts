import 'server-only';
import { HttpError } from './errors';
export function engineId(value: unknown): string {
  if (typeof value !== 'string' || !/^[a-zA-Z0-9_-]{1,100}$/.test(value))
    throw new HttpError(400, 'Invalid data identifier.');
  return value;
}
// This client is exclusively server-side. Tokens and database connection metadata never reach the browser.
export async function engine(
  path: string,
  token?: string,
  method = 'GET',
  body?: unknown,
  signal?: AbortSignal,
) {
  const res = await fetch(new URL(path, process.env.NOCODB_URL || 'http://127.0.0.1:8080'), {
    method,
    headers: {
      ...(token ? { 'xc-auth': token } : {}),
      ...(body === undefined ? {} : { 'content-type': 'application/json' }),
    },
    body: body === undefined ? undefined : JSON.stringify(body),
    cache: 'no-store',
    redirect: 'error',
    signal: signal
      ? AbortSignal.any([signal, AbortSignal.timeout(15000)])
      : AbortSignal.timeout(15000),
  });
  if (!res.ok) {
    if (res.status === 401) throw new HttpError(401, 'Please sign in again.');
    if (res.status === 403)
      throw new HttpError(403, 'Your workspace role does not allow this action.');
    if (res.status === 404)
      throw new HttpError(404, 'This item is unavailable or you do not have access.');
    if (res.status === 429) throw new HttpError(429, 'Too many requests. Please try in a minute.');
    if (res.status === 400 || res.status === 422)
      throw new HttpError(
        400,
        'The workspace could not save this change. Check the field values and required fields.',
      );
    throw new HttpError(502, 'The data engine is temporarily unavailable.');
  }
  if (!res.body) throw new HttpError(502, 'Empty data engine response.');
  const reader = res.body.getReader();
  const parts: Uint8Array[] = [];
  let length = 0;
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      length += value.length;
      if (length > 2_000_000)
        throw new HttpError(
          413,
          'This response is too large. Use the advanced spreadsheet for large attachments.',
        );
      parts.push(value);
    }
  } finally {
    await reader.cancel().catch(() => {});
  }
  try {
    return JSON.parse(Buffer.concat(parts).toString('utf8'));
  } catch {
    throw new HttpError(502, 'Unexpected data engine response.');
  }
}
export function sameOrigin(req: Request) {
  if (!process.env.APP_ORIGIN || req.headers.get('origin') !== process.env.APP_ORIGIN)
    throw new HttpError(403, 'Invalid request origin.');
  if (!req.headers.get('content-type')?.startsWith('application/json'))
    throw new HttpError(415, 'JSON required.');
}
export async function boundedBody(req: Request) {
  const reader = req.body?.getReader();
  if (!reader) throw new HttpError(400, 'Request body required.');
  const parts: Uint8Array[] = [];
  let length = 0;
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      length += value.length;
      if (length > 64000) throw new HttpError(413, 'Request is too large.');
      parts.push(value);
    }
  } finally {
    await reader.cancel().catch(() => {});
  }
  try {
    return JSON.parse(Buffer.concat(parts).toString('utf8'));
  } catch {
    throw new HttpError(400, 'Invalid JSON.');
  }
}
