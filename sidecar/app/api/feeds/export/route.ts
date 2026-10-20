import { z } from 'zod';
import { sources } from '@/lib/feeds/source';
import { FeedService } from '@/lib/feeds/service';
import { HttpError, errorResponse } from '@/lib/access';
import { id } from '@/lib/feeds/contracts';
export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
const query = z
  .object({
    feed: id,
    snapshot: id.optional(),
    cursor: z.string().max(2000).optional(),
    before: id.optional(),
  })
  .strict();
export async function GET(req: Request) {
  let release: (() => void) | undefined;
  try {
    sources();
    const url = new URL(req.url);
    if ([...url.searchParams.keys()].some((k) => url.searchParams.getAll(k).length !== 1))
      throw new HttpError(400, 'Repeated export parameters refused.');
    const q = query.safeParse(Object.fromEntries(url.searchParams));
    if (!q.success) throw new HttpError(400, 'Unsupported export parameters.');
    const header = req.headers.get('authorization');
    if (!header?.startsWith('Bearer ')) throw new HttpError(401, 'Feed credential required.');
    const { feed, ...input } = q.data;
    const service = new FeedService();
    release = service.store.admit();
    return Response.json(await service.page(feed, header.slice(7), input, req.signal), {
      headers: { 'Cache-Control': 'no-store', 'Referrer-Policy': 'no-referrer' },
    });
  } catch (e) {
    return errorResponse(e);
  } finally {
    release?.();
  }
}
