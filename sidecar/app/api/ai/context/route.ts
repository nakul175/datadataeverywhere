import { z } from 'zod';
import { identity, allowedTables, HttpError, errorResponse } from '@/lib/access';
import { boundedBody, sameOrigin } from '@/lib/engine';
import { tableContext } from '@/lib/nocodb';
import { reserve } from '@/lib/budget';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

export async function POST(req: Request) {
  let release: (() => Promise<void>) | undefined;
  try {
    sameOrigin(req);
    const user = await identity();
    const body = z
      .object({ tableId: z.string().regex(/^[a-zA-Z0-9_-]{1,100}$/) })
      .strict()
      .safeParse(await boundedBody(req));
    if (!body.success) throw new HttpError(400, 'Select one approved table.');
    const table = (await allowedTables(user)).find((t) => t.id === body.data.tableId);
    if (!table) throw new HttpError(403, 'Table access denied.');
    // The same rate/concurrency gate bounds previews; no provider request is made.
    release = await reserve(user, 32000);
    const context = await tableContext(
      table,
      AbortSignal.any([req.signal, AbortSignal.timeout(15000)]),
    );
    return Response.json(
      {
        context,
        providerCalled: false,
        notice:
          'This is a bounded preview at the displayed time. A question fetches a fresh sample. Nested/attachment fields are refused. Preview reserves 32,000 conservative budget units.',
      },
      { headers: { 'Cache-Control': 'no-store' } },
    );
  } catch (e) {
    return errorResponse(e);
  } finally {
    try {
      await release?.();
    } catch {
      console.error('AI preview lease cleanup failed');
    }
  }
}
