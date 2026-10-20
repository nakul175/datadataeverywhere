import { afterEach, expect, it, vi } from 'vitest';
vi.mock('server-only', () => ({}));
import { publicUrls } from '../lib/public-urls';
afterEach(() => vi.unstubAllEnvs());
it('uses the verified Aplyd task-tool default', () => {
  vi.stubEnv('TASKS_PUBLIC_URL', '');
  expect(publicUrls().tasks).toBe('https://sheethappensofficer.aplyd.org/');
});
it.each([
  'http://example.test',
  'https://example.test/?token=private',
  'https://example.test/#secret',
])('rejects unsafe public tool URL %s', (value) => {
  vi.stubEnv('TASKS_PUBLIC_URL', value);
  expect(() => publicUrls()).toThrow();
});
it('rejects credential-bearing URLs made from synthetic fixture values', () => {
  const url = new URL('https://example.test');
  url.username = 'fixture-user';
  url.password = 'fixture-only';
  vi.stubEnv('TASKS_PUBLIC_URL', url.toString());
  expect(() => publicUrls()).toThrow();
});
