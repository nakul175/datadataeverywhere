import { beforeEach, describe, expect, it, vi } from 'vitest';
vi.mock('server-only', () => ({}));
const mock = vi.hoisted(() => ({
  identity: vi.fn(),
  allowed: vi.fn(),
  reserve: vi.fn(),
  context: vi.fn(),
}));
vi.mock('../lib/access', async (original) => ({
  ...(await original<object>()),
  identity: mock.identity,
  allowedTables: mock.allowed,
}));
vi.mock('../lib/budget', () => ({ reserve: mock.reserve }));
vi.mock('../lib/nocodb', () => ({ tableContext: mock.context }));
import { POST } from '../app/api/ai/context/route';
function request(tableId = 'allowed', origin = 'https://example.test') {
  return new Request('https://example.test/api/ai/context', {
    method: 'POST',
    headers: { origin, 'content-type': 'application/json' },
    body: JSON.stringify({ tableId }),
  });
}
beforeEach(() => {
  vi.clearAllMocks();
  process.env.APP_ORIGIN = 'https://example.test';
  mock.identity.mockResolvedValue('member');
  mock.allowed.mockResolvedValue([{ id: 'allowed', name: 'Table', fields: ['Id'] }]);
});
describe('Non-provider context disclosure preview', () => {
  it('refuses foreign origins and ungranted tables before reading any data', async () => {
    expect((await POST(request('allowed', 'https://other.test'))).status).toBe(403);
    expect((await POST(request('private'))).status).toBe(403);
    expect(mock.context).not.toHaveBeenCalled();
    expect(mock.reserve).not.toHaveBeenCalled();
  });
  it('uses the same bounded context reader and releases its lease', async () => {
    const release = vi.fn().mockResolvedValue(undefined);
    mock.reserve.mockResolvedValue(release);
    mock.context.mockResolvedValue({ rows: [{ Id: 1 }], rowsIncluded: 1, complete: true });
    const res = await POST(request());
    const body = await res.json();
    expect(body.providerCalled).toBe(false);
    expect(body.context.rows).toEqual([{ Id: 1 }]);
    expect(mock.reserve).toHaveBeenCalledWith('member', 32000);
    expect(release).toHaveBeenCalledOnce();
    expect(res.headers.get('cache-control')).toBe('no-store');
  });
  it('releases the lease and refuses a nested-data context', async () => {
    const release = vi.fn().mockResolvedValue(undefined);
    mock.reserve.mockResolvedValue(release);
    const { HttpError } = await import('../lib/access');
    mock.context.mockRejectedValue(new HttpError(409, 'Nested data refused'));
    expect((await POST(request())).status).toBe(409);
    expect(release).toHaveBeenCalledOnce();
  });
});
