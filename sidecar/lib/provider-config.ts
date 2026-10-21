import 'server-only';
import { HttpError } from './errors';

export function providerConfiguration() {
  const provider = process.env.AI_PROVIDER || 'openai';
  if (!['openai', 'anthropic'].includes(provider))
    throw new HttpError(503, 'Invalid AI provider configuration.');
  const model =
    provider === 'openai' ? process.env.OPENAI_MODEL || 'gpt-4o' : process.env.ANTHROPIC_MODEL;
  if (!model || !/^[a-zA-Z0-9._:-]{1,200}$/.test(model))
    throw new HttpError(503, 'Your administrator needs to select an explicit AI model.');
  const key = provider === 'openai' ? process.env.OPENAI_API_KEY : process.env.ANTHROPIC_API_KEY;
  if (!key) throw new HttpError(503, 'Your administrator needs to connect an AI provider.');
  return { provider, model };
}

export function aiReadiness() {
  try {
    providerConfiguration();
    return { ready: true, reason: '' };
  } catch (e) {
    return {
      ready: false,
      reason: e instanceof HttpError ? e.message : 'AI configuration is unavailable.',
    };
  }
}
