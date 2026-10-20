import { afterAll, beforeEach, describe, expect, it, vi } from 'vitest';
vi.mock('server-only', () => ({}));
import { createClient } from 'redis';
import { reserveLua } from '../lib/budget';
// Test only on a disposable Redis instance. This suite calls FLUSHDB.
const url = process.env.TEST_REDIS_URL;
const r = url ? createClient({ url }) : undefined;
describe.skipIf(!url)('Atomic budget integration (disposable Redis)', () => {
  beforeEach(async () => { if (!r!.isOpen) await r!.connect(); await r!.flushDb(); });
  afterAll(async () => { if (r?.isOpen) await r.quit(); });
  function admit(user: string, id: string, userBudget = 10000, globalBudget = 10000, cost = 1000) {
    return r!.eval(reserveLua, { keys: [`rpm:${user}`, `day:${user}`, 'day:global', `active:${user}`, 'active:global'], arguments: [String(Date.now()), String(cost), id, 'day', String(userBudget), String(globalBudget)] });
  }
  it('admits exactly one concurrent request from the same user', async () => {
    const results = await Promise.all(Array.from({ length: 50 }, (_, i) => admit('alice', String(i))));
    expect(results.filter(x => Number(x) === 1)).toHaveLength(1); expect(await r!.get('day:global')).toBe('1000');
  });
  it('admits at most eight global concurrent requests from 50 users', async () => {
    const results = await Promise.all(Array.from({ length: 50 }, (_, i) => admit(`user${i}`, String(i), 100000, 100000)));
    expect(results.filter(x => Number(x) === 1)).toHaveLength(8);
  });
  it('rejects a request exceeding a daily budget without charging it', async () => {
    expect(Number(await admit('alice', 'a', 999))).toBe(0);
    expect(await r!.get('day:global')).toBeNull();
  });
  it('checks the global budget atomically', async () => {
    const results = await Promise.all(Array.from({ length: 50 }, (_, i) => admit(`user${i}`, String(i), 10000, 2500)));
    expect(results.filter(x => Number(x) === 1)).toHaveLength(2); expect(await r!.get('day:global')).toBe('2000');
  });
  it('rejects a seventh request in the same minute', async () => {
    for (let i = 0; i < 6; i++) {
      expect(Number(await admit('alice', String(i)))).toBe(1);
      await r!.del('active:alice'); await r!.del('active:global');
    }
    expect(Number(await admit('alice', 'seventh'))).toBe(0);
  });
  it('cleans up expired concurrency leases', async () => {
    await r!.zAdd('active:alice', { score: Date.now() - 1, value: 'dead' });
    expect(Number(await admit('alice', 'new'))).toBe(1);
  });
});
