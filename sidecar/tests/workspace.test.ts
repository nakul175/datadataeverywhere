import { beforeEach, describe, expect, it, vi } from 'vitest';
vi.mock('server-only', () => ({}));
const mocks = vi.hoisted(() => ({ session: vi.fn(), engine: vi.fn(), tables: vi.fn() }));
vi.mock('../lib/session', () => ({ currentSession: mocks.session }));
vi.mock('../lib/engine', async original => ({ ...await original<object>(), engine: mocks.engine }));
vi.mock('../lib/access', async original => ({ ...await original<object>(), allowedTables: mocks.tables }));
import { GET, POST } from '../app/api/workspace/route';
const schema = { columns: [{ id: 'c1', title: 'Id', uidt: 'ID', pk: true }, { id: 'c2', title: 'Name', uidt: 'SingleLineText' }, { id: 'c3', title: 'Total', uidt: 'Formula' }] };
function request(body: unknown, origin = 'https://example.test') { return new Request('https://example.test/api/workspace', { method: 'POST', headers: { origin, 'content-type': 'application/json' }, body: JSON.stringify(body) }); }
beforeEach(() => { vi.clearAllMocks(); process.env.APP_ORIGIN = 'https://example.test'; mocks.session.mockResolvedValue({ token: 'user-only-token', id: 'u1', email: 'owner@example.test' }); mocks.tables.mockResolvedValue([]); });
describe('Workspace permission boundaries', () => {
  it('rejects cross-origin writes without reading data', async () => { const res = await POST(request({ action: 'createBase', title: 'Team' }, 'https://attacker.test')); expect(res.status).toBe(403); expect(mocks.engine).not.toHaveBeenCalled(); });
  it('projects base results without leaking connection metadata', async () => { mocks.engine.mockResolvedValue({ list: [{ id: 'b1', title: 'Team', sources: [{ password: 'secret' }] }] }); const res = await GET(new Request('https://example.test/api/workspace')); expect(await res.json()).toEqual({ bases: [{ id: 'b1', title: 'Team' }] }); expect(mocks.engine.mock.calls[0][1]).toBe('user-only-token'); });
  it('blocks calculated-field writes before record mutation', async () => { mocks.engine.mockResolvedValue(schema); const res = await POST(request({ action: 'updateRecord', tableId: 't1', id: 1, values: { Total: 500 } })); expect(res.status).toBe(400); expect(mocks.engine).toHaveBeenCalledTimes(1); });
  it('uses the current user token on schema and record writes', async () => { mocks.engine.mockResolvedValueOnce(schema).mockResolvedValueOnce({}); const res = await POST(request({ action: 'updateRecord', tableId: 't1', id: 7, values: { Name: 'Updated' } })); expect(res.status).toBe(200); expect(mocks.engine.mock.calls[1]).toEqual(['/api/v2/tables/t1/records', 'user-only-token', 'PATCH', { Name: 'Updated', Id: 7 }]); });
  it('requires upstream authorization before returning records', async () => { const { HttpError } = await import('../lib/access'); mocks.engine.mockRejectedValue(new HttpError(403, 'Role denied')); const res = await GET(new Request('https://example.test/api/workspace?action=records&tableId=private')); expect(res.status).toBe(403); expect(mocks.engine).toHaveBeenCalledTimes(1); });
  it('does not offer an arbitrary upstream proxy', async () => { const res = await GET(new Request('https://example.test/api/workspace?action=proxy&url=http://169.254.169.254')); expect(res.status).toBe(400); expect(mocks.engine).not.toHaveBeenCalled(); });
});
