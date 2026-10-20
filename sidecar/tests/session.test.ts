import { beforeEach, describe, expect, it, vi } from 'vitest';
vi.mock('server-only', () => ({}));
const mocks = vi.hoisted(() => ({ get: vi.fn(), engine: vi.fn() }));
vi.mock('next/headers', () => ({ cookies: async () => ({ get: mocks.get }) }));
vi.mock('../lib/engine', () => ({ engine: mocks.engine }));
import { currentSession } from '../lib/session';
beforeEach(() => {
  vi.clearAllMocks();
});
describe('NocoDB-backed sessions', () => {
  it('rejects a missing session', async () => {
    mocks.get.mockReturnValue(undefined);
    await expect(currentSession()).rejects.toMatchObject({ status: 401 });
    expect(mocks.engine).not.toHaveBeenCalled();
  });
  it('rejects upstream guest fallback', async () => {
    mocks.get.mockReturnValue({ value: 'invalid-token' });
    mocks.engine.mockResolvedValue({
      id: 'guest',
      email: 'guest@example.test',
      roles: { guest: true },
    });
    await expect(currentSession()).rejects.toMatchObject({ status: 401 });
  });
  it('uses a validated upstream identity rather than trusting decoded claims', async () => {
    mocks.get.mockReturnValue({ value: 'server-validated-token' });
    mocks.engine.mockResolvedValue({
      id: 'u1',
      email: 'Owner@Example.test',
      roles: { org_level_creator: true },
    });
    expect(await currentSession()).toMatchObject({ id: 'u1', email: 'owner@example.test' });
    expect(mocks.engine).toHaveBeenCalledWith('/api/v1/auth/user/me', 'server-validated-token');
  });
});
