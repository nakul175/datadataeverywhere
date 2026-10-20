import { z } from 'zod';
import { currentSession } from '@/lib/session';
import { boundedBody, sameOrigin } from '@/lib/engine';
import { errorResponse, HttpError } from '@/lib/access';
import { FeedService } from '@/lib/feeds/service';
import { authority, sources } from '@/lib/feeds/source';
import { id } from '@/lib/feeds/contracts';
export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
const json = (v: unknown) =>
  Response.json(v, { headers: { 'Cache-Control': 'no-store', 'Referrer-Policy': 'no-referrer' } });
export async function GET(req: Request) {
  let release: (() => void) | undefined;
  try {
    const actor = await currentSession();
    const q = new URL(req.url).searchParams;
    const service = new FeedService();
    release = service.store.admit();
    if (q.get('action') === 'history') {
      const after = Number(q.get('after') || 0);
      if (!Number.isSafeInteger(after) || after < 0)
        throw new HttpError(400, 'Invalid history cursor.');
      return json(await service.history(id.parse(q.get('id')), actor, after));
    }
    const available = [];
    for (const source of sources()) {
      const grant = {
        source: source.id,
        owner: actor.id,
        consumer: 'source-discovery',
        expiresAt: new Date(Date.now() + 60000).toISOString(),
        fields: source.fields.map((f) => f.id),
        scope: { kind: 'all' as const, confirmed: true as const },
      };
      try {
        await authority(source, actor.id, grant, actor);
        available.push({
          id: source.id,
          baseId: source.baseId,
          tableId: source.tableId,
          fields: source.fields,
        });
      } catch {}
    }
    return json({ sources: available, feeds: await service.list(actor), owner: actor.id });
  } catch (e) {
    return errorResponse(e);
  } finally {
    release?.();
  }
}
const command = z.discriminatedUnion('action', [
  z.object({ action: z.literal('create'), grant: z.unknown() }).strict(),
  z.object({ action: z.enum(['pause', 'resume', 'revoke', 'rotate', 'snapshot']), id }).strict(),
]);
export async function POST(req: Request) {
  let release: (() => void) | undefined;
  try {
    sameOrigin(req);
    const actor = await currentSession();
    const body = command.parse(await boundedBody(req));
    const service = new FeedService();
    release = service.store.admit();
    if (body.action === 'create') return json(await service.create(body.grant, actor));
    if (body.action === 'snapshot') return json(await service.build(body.id, actor, req.signal));
    return json(await service.lifecycle(body.id, body.action, actor));
  } catch (e) {
    return errorResponse(e);
  } finally {
    release?.();
  }
}
