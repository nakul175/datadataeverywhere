import 'server-only';
import { createClient } from 'redis';
const client = createClient({
  url: process.env.REDIS_URL || 'redis://redis:6379',
  // Fail this request within a bounded connect attempt; a later request can reconnect.
  socket: { connectTimeout: 3000, reconnectStrategy: false },
  disableOfflineQueue: true,
});
client.on('error', () => console.error('Budget store unavailable'));
let connecting: Promise<unknown> | undefined;
export async function redis() {
  if (!client.isOpen) {
    connecting ||= (async () => {
      let timer: ReturnType<typeof setTimeout> | undefined;
      try {
        await Promise.race([
          client.connect(),
          new Promise<never>((_, reject) => {
            timer = setTimeout(() => {
              if (client.isOpen) client.destroy();
              reject(new Error('BudgetStoreUnavailable'));
            }, 3000);
          }),
        ]);
      } finally {
        clearTimeout(timer);
        connecting = undefined;
      }
    })();
  }
  if (connecting) await connecting;
  if (!client.isReady) throw new Error('BudgetStoreUnavailable');
  return client;
}
