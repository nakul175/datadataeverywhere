import 'server-only';
import { randomUUID } from 'node:crypto';
import { redis } from './redis';
import { HttpError } from './access';
// One atomic operation: per-user RPM, daily reservation, global daily reservation,
// and expiring concurrency leases. UTC day keys survive sidecar restarts.
export const reserveLua = `
local now = tonumber(ARGV[1])
local cost = tonumber(ARGV[2])
redis.call('ZREMRANGEBYSCORE', KEYS[4], '-inf', now)
redis.call('ZREMRANGEBYSCORE', KEYS[5], '-inf', now)
if redis.call('ZCARD', KEYS[4]) >= 1 or redis.call('ZCARD', KEYS[5]) >= 8 then return 0 end
if tonumber(redis.call('GET', KEYS[1]) or '0') >= 6 then return 0 end
if tonumber(redis.call('GET', KEYS[2]) or '0') + cost > tonumber(ARGV[5]) then return 0 end
if tonumber(redis.call('GET', KEYS[3]) or '0') + cost > tonumber(ARGV[6]) then return 0 end
redis.call('INCR', KEYS[1]); redis.call('EXPIRE', KEYS[1], 120)
redis.call('INCRBY', KEYS[2], cost); redis.call('EXPIRE', KEYS[2], 172800)
redis.call('INCRBY', KEYS[3], cost); redis.call('EXPIRE', KEYS[3], 172800)
redis.call('ZADD', KEYS[4], now + 180000, ARGV[3]); redis.call('EXPIRE', KEYS[4], 240)
redis.call('ZADD', KEYS[5], now + 180000, ARGV[3]); redis.call('EXPIRE', KEYS[5], 240)
return 1
`;
export async function reserve(user: string, cost: number) {
  if (process.env.SQLITE_BUDGET_FILE)
    return (await import('./local-limits')).localReserve(user, cost);
  const r = await redis();
  const now = Date.now();
  const id = randomUUID();
  const day = new Date(now).toISOString().slice(0, 10);
  const userLease = `dde:active:user:${user}`;
  const globalLease = 'dde:active:global';
  const result = await r.withAbortSignal(AbortSignal.timeout(3000)).eval(reserveLua, {
    keys: [
      `dde:rpm:${user}:${Math.floor(now / 60000)}`,
      `dde:day:${day}:user:${user}`,
      `dde:day:${day}:global`,
      userLease,
      globalLease,
    ],
    arguments: [
      String(now),
      String(cost),
      id,
      day,
      process.env.USER_DAILY_TOKEN_BUDGET || '500000',
      process.env.GLOBAL_DAILY_TOKEN_BUDGET || '5000000',
    ],
  });
  if (Number(result) !== 1)
    throw new HttpError(429, 'Rate, concurrency, or daily token budget reached. Try later.');
  let released = false;
  return async () => {
    if (released) return;
    released = true;
    const bounded = r.withAbortSignal(AbortSignal.timeout(3000));
    await Promise.all([bounded.zRem(userLease, id), bounded.zRem(globalLease, id)]).catch(() => {});
  };
}
