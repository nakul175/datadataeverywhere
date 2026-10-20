import { createServer, type Socket } from 'node:net';
import { expect, it, vi } from 'vitest';
vi.mock('server-only', () => ({}));

it('bounds a silent Redis handshake and permits a fresh connection attempt', async () => {
  const peers = new Set<Socket>();
  let accepted = 0;
  const server = createServer((socket) => {
    accepted++;
    peers.add(socket);
    socket.on('close', () => peers.delete(socket));
  });
  await new Promise<void>((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', resolve);
  });
  const address = server.address();
  if (!address || typeof address === 'string') throw new Error('Missing test address');
  const previous = process.env.REDIS_URL;
  process.env.REDIS_URL = `redis://127.0.0.1:${address.port}`;
  vi.resetModules();
  try {
    const { redis } = await import('../lib/redis');
    for (let attempt = 0; attempt < 2; attempt++) {
      const started = Date.now();
      await expect(redis()).rejects.toThrow();
      expect(Date.now() - started).toBeLessThan(4500);
    }
    expect(accepted).toBe(2);
  } finally {
    if (previous === undefined) delete process.env.REDIS_URL;
    else process.env.REDIS_URL = previous;
    for (const peer of peers) peer.destroy();
    await new Promise<void>((resolve) => server.close(() => resolve()));
  }
}, 10000);
