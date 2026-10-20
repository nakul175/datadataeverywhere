import 'server-only';
import { createClient } from 'redis';
const client = createClient({
  url: process.env.REDIS_URL || 'redis://redis:6379',
  socket: { connectTimeout: 3000, reconnectStrategy: (retries) => Math.min(100 * retries, 3000) },
  disableOfflineQueue: true,
});
client.on('error', () => console.error('Budget store unavailable'));
let connecting: Promise<unknown> | undefined;
export async function redis() {
  if (!client.isOpen) {
    connecting ||= client.connect().finally(() => {
      connecting = undefined;
    });
    await connecting;
  }
  if (!client.isReady) throw new Error('BudgetStoreUnavailable');
  return client;
}
