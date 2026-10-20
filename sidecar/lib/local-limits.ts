import 'server-only';
import { DatabaseSync } from 'node:sqlite';
import { mkdirSync, chmodSync } from 'node:fs';
import { dirname } from 'node:path';
import { createHash, randomUUID } from 'node:crypto';
import { HttpError } from './errors';
let database: DatabaseSync | undefined;
function db() {
  if (database) return database;
  const path = process.env.SQLITE_BUDGET_FILE;
  if (!path) throw new HttpError(503, 'Budget storage is not configured.');
  mkdirSync(dirname(path), { recursive: true, mode: 0o700 });
  const d = new DatabaseSync(path); chmodSync(path, 0o600);
  d.exec(`PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000;
    CREATE TABLE IF NOT EXISTS usage (key TEXT PRIMARY KEY, amount INTEGER NOT NULL, expires INTEGER NOT NULL);
    CREATE TABLE IF NOT EXISTS leases (id TEXT PRIMARY KEY, owner TEXT NOT NULL, expires INTEGER NOT NULL);`);
  database = d; return d;
}
function transaction<T>(fn: (d: DatabaseSync) => T): T {
  const d = db(); d.exec('BEGIN IMMEDIATE');
  try { const result = fn(d); d.exec('COMMIT'); return result; } catch (e) { d.exec('ROLLBACK'); throw e; }
}
const denied = () => new HttpError(429, 'Rate, concurrency, or daily token budget reached. Try later.');
function positiveLimit(value: string | undefined, fallback: number) {
  const n = value === undefined ? fallback : Number(value);
  if (!Number.isSafeInteger(n) || n < 1) throw new HttpError(503, 'Invalid budget configuration.'); return n;
}
export async function localReserve(user: string, cost: number) {
  if (!Number.isSafeInteger(cost) || cost < 1) throw denied();
  const now = Date.now(); const id = randomUUID(); const day = new Date(now).toISOString().slice(0, 10);
  const key = createHash('sha256').update(user).digest('hex');
  transaction(d => {
    d.prepare('DELETE FROM leases WHERE expires <= ?').run(now);
    d.prepare('DELETE FROM usage WHERE expires <= ?').run(now);
    const active = d.prepare('SELECT count(*) AS n FROM leases').get() as { n: number };
    const mine = d.prepare('SELECT count(*) AS n FROM leases WHERE owner = ?').get(key) as { n: number };
    if (active.n >= 8 || mine.n >= 1) throw denied();
    const quotas = [
      [`rpm:${key}:${Math.floor(now / 60000)}`, 1, 6, now + 120000],
      [`day:${day}:${key}`, cost, positiveLimit(process.env.USER_DAILY_TOKEN_BUDGET, 500000), now + 172800000],
      [`day:${day}:global`, cost, positiveLimit(process.env.GLOBAL_DAILY_TOKEN_BUDGET, 5000000), now + 172800000],
    ] as const;
    for (const [k, amount, max, expires] of quotas) {
      const old = (d.prepare('SELECT amount FROM usage WHERE key = ?').get(k) as { amount: number } | undefined)?.amount || 0;
      if (old + amount > max) throw denied();
      d.prepare('INSERT INTO usage VALUES (?, ?, ?) ON CONFLICT(key) DO UPDATE SET amount = excluded.amount, expires = excluded.expires').run(k, old + amount, expires);
    }
    d.prepare('INSERT INTO leases VALUES (?, ?, ?)').run(id, key, now + 180000);
  });
  let released = false;
  return async () => { if (released) return; released = true; db().prepare('DELETE FROM leases WHERE id = ?').run(id); };
}
export async function loginAdmission(identity: string) {
  // Server-wide + hashed email limits persist across restarts. No passwords stored here.
  const now = Date.now(); const hash = createHash('sha256').update(identity.toLowerCase()).digest('hex');
  transaction(d => {
    d.prepare('DELETE FROM usage WHERE expires <= ?').run(now);
    for (const [key, max] of [[`login:${hash}:${Math.floor(now / 60000)}`, 6], [`login:global:${Math.floor(now / 60000)}`, 120]] as const) {
      const count = (d.prepare('SELECT amount FROM usage WHERE key = ?').get(key) as { amount: number } | undefined)?.amount || 0;
      if (count >= max) throw new HttpError(429, 'Too many sign-in attempts. Try again in a minute.');
      d.prepare('INSERT INTO usage VALUES (?, ?, ?) ON CONFLICT(key) DO UPDATE SET amount = excluded.amount').run(key, count + 1, now + 120000);
    }
  });
}
