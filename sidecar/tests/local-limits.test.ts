import { afterAll, beforeAll, describe, expect, it, vi } from 'vitest';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
vi.mock('server-only', () => ({}));
import { localReserve, loginAdmission } from '../lib/local-limits';
const dir = mkdtempSync(join(tmpdir(), 'dde-limits-'));
beforeAll(() => {
  process.env.SQLITE_BUDGET_FILE = join(dir, 'limits.sqlite');
  process.env.GLOBAL_DAILY_TOKEN_BUDGET = '5000000';
  process.env.USER_DAILY_TOKEN_BUDGET = '500000';
});
afterAll(() => {
  delete process.env.SQLITE_BUDGET_FILE;
  delete process.env.USER_DAILY_TOKEN_BUDGET;
  delete process.env.GLOBAL_DAILY_TOKEN_BUDGET;
  rmSync(dir, { recursive: true, force: true });
});
describe('Persistent local budget admission', () => {
  it('admits only one concurrent request per user', async () => {
    const results = await Promise.allSettled(
      Array.from({ length: 12 }, () => localReserve('concurrent', 100)),
    );
    expect(results.filter((r) => r.status === 'fulfilled')).toHaveLength(1);
    for (const result of results) if (result.status === 'fulfilled') await result.value();
  });
  it('caps global concurrency at eight users', async () => {
    const results = await Promise.allSettled(
      Array.from({ length: 50 }, (_, i) => localReserve(`worker${i}`, 100)),
    );
    expect(results.filter((r) => r.status === 'fulfilled')).toHaveLength(8);
    for (const result of results) if (result.status === 'fulfilled') await result.value();
  });
  it('keeps daily reservations after completion, including repeated releases', async () => {
    const release = await localReserve('daily', 490000);
    await release();
    await release();
    await expect(localReserve('daily', 10001)).rejects.toMatchObject({ status: 429 });
  });
  it('limits repeated sign-in attempts', async () => {
    for (let i = 0; i < 6; i++) await loginAdmission('login@example.test');
    await expect(loginAdmission('LOGIN@example.test')).rejects.toMatchObject({ status: 429 });
  });
});
