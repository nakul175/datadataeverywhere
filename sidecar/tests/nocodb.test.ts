import { beforeEach, afterEach, describe, expect, it, vi } from 'vitest';
vi.mock('server-only', () => ({}));
import { tableContext } from '../lib/nocodb';
const table = { id: 'm123', name: 'Orders', fields: ['Id', 'Total'] };
const meta = {
  columns: [
    { title: 'Id', uidt: 'ID', pk: true },
    { title: 'Total', uidt: 'Number' },
    { title: 'Secret', uidt: 'Text' },
  ],
};
beforeEach(() => {
  process.env.NOCODB_API_TOKEN = 'test-token';
  process.env.NOCODB_URL = 'http://nocodb:8080';
});
afterEach(() => vi.unstubAllGlobals());
describe('NocoDB context boundaries', () => {
  it('projects approved columns and strips unapproved schema/rows', async () => {
    const fetcher = vi
      .fn()
      .mockResolvedValueOnce(Response.json(meta))
      .mockResolvedValueOnce(
        Response.json({
          list: [{ Id: 1, Total: 12, Secret: 'private' }],
          pageInfo: { isLastPage: true },
        }),
      );
    vi.stubGlobal('fetch', fetcher);
    const context = await tableContext(table, new AbortController().signal);
    expect(context.rows).toEqual([{ Id: 1, Total: 12 }]);
    expect(JSON.stringify(context)).not.toContain('Secret');
    expect(context.complete).toBe(true);
    expect(fetcher.mock.calls[1][0].searchParams.get('fields')).toBe('Id,Total');
    expect(fetcher.mock.calls[0][1].headers).toEqual({ 'xc-token': 'test-token' });
  });
  it('paginates but never includes more than 100 rows', async () => {
    let page = 0;
    vi.stubGlobal(
      'fetch',
      vi.fn(async (url: URL) =>
        url.pathname.includes('/meta/')
          ? Response.json(meta)
          : Response.json({
              list: Array.from({ length: 25 }, (_, i) => ({ Id: page * 25 + i, Total: 1 })),
              pageInfo: { isLastPage: ++page === 20 },
            }),
      ),
    );
    const context = await tableContext(table, new AbortController().signal);
    expect(context.rows).toHaveLength(100);
    expect(context.truncated).toBe(true);
    expect(page).toBe(4);
  });
  it('caps JSON bytes and reports truncation', async () => {
    vi.stubGlobal(
      'fetch',
      vi
        .fn()
        .mockResolvedValueOnce(Response.json(meta))
        .mockResolvedValueOnce(
          Response.json({
            list: [{ Id: 1, Total: 'x'.repeat(30000) }],
            pageInfo: { isLastPage: true },
          }),
        ),
    );
    const context = await tableContext(table, new AbortController().signal);
    expect(context.rows).toHaveLength(0);
    expect(context.truncated).toBe(true);
  });
  it('fails closed when the approved schema has changed', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(Response.json({ columns: [{ title: 'Id' }] })),
    );
    await expect(tableContext(table, new AbortController().signal)).rejects.toMatchObject({
      status: 409,
    });
  });
  it('rejects oversized upstream response bodies', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response('x'.repeat(2_000_001))));
    await expect(tableContext(table, new AbortController().signal)).rejects.toMatchObject({
      status: 413,
    });
  });
});
