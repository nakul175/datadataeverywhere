import { beforeEach, describe, expect, it, vi } from 'vitest';
vi.mock('server-only', () => ({}));
const mocks = vi.hoisted(() => ({ headers: vi.fn(), readFile: vi.fn() }));
vi.mock('next/headers', () => ({ headers: mocks.headers }));
vi.mock('node:fs/promises', () => ({ readFile: mocks.readFile }));
import { identity, allowedTables } from '../lib/access';
beforeEach(() => {
  process.env.PROXY_SECRET = 'trusted-proxy-secret';
});
describe('Authentication and authorization', () => {
  it('rejects a forged identity header without the proxy secret', async () => {
    mocks.headers.mockResolvedValue(new Headers({ 'x-dde-user': 'owner' }));
    await expect(identity()).rejects.toMatchObject({ status: 401 });
  });
  it('accepts a trusted proxy identity', async () => {
    mocks.headers.mockResolvedValue(
      new Headers({ 'x-dde-user': 'owner', 'x-dde-proxy-secret': 'trusted-proxy-secret' }),
    );
    await expect(identity()).resolves.toBe('owner');
  });
  it('returns only explicitly granted tables; unknown users get none', async () => {
    mocks.readFile.mockResolvedValue(
      JSON.stringify({
        tables: [
          { id: 'one', name: 'One', fields: ['Id'] },
          { id: 'two', name: 'Two', fields: ['Id'] },
        ],
        users: { owner: ['one'] },
      }),
    );
    expect((await allowedTables('owner')).map((t) => t.id)).toEqual(['one']);
    expect(await allowedTables('stranger')).toEqual([]);
  });
});
