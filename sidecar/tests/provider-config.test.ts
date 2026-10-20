import { afterEach, describe, expect, it, vi } from 'vitest';
vi.mock('server-only', () => ({}));
import { aiReadiness, providerConfiguration } from '../lib/provider-config';
afterEach(() => vi.unstubAllEnvs());
describe('Explicit provider readiness', () => {
  it('does not infer connectivity from a configured OpenAI key', () => {
    vi.stubEnv('AI_PROVIDER', 'openai');
    vi.stubEnv('OPENAI_API_KEY', 'local-fixture-only');
    vi.stubEnv('OPENAI_MODEL', '');
    expect(providerConfiguration()).toEqual({ provider: 'openai', model: 'gpt-4o' });
    expect(aiReadiness().ready).toBe(true);
  });
  it('requires an explicit Anthropic model instead of a guessed model alias', () => {
    vi.stubEnv('AI_PROVIDER', 'anthropic');
    vi.stubEnv('ANTHROPIC_API_KEY', 'local-fixture-only');
    vi.stubEnv('ANTHROPIC_MODEL', '');
    expect(aiReadiness().ready).toBe(false);
    vi.stubEnv('ANTHROPIC_MODEL', 'configured-model-id');
    expect(providerConfiguration().model).toBe('configured-model-id');
  });
  it.each(['unknown', 'https://other-provider.test'])(
    'fails closed for provider %s',
    (provider) => {
      vi.stubEnv('AI_PROVIDER', provider);
      expect(aiReadiness().ready).toBe(false);
    },
  );
  it('does not expose a present credential in readiness metadata', () => {
    vi.stubEnv('AI_PROVIDER', 'openai');
    vi.stubEnv('OPENAI_API_KEY', 'local-fixture-only');
    expect(JSON.stringify(aiReadiness())).not.toContain('local-fixture-only');
  });
});
