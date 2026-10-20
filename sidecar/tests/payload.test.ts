import { expect, it } from 'vitest';
import { chatPayload } from '../lib/payload';
it('keeps multi-turn streamed text but strips SDK step markers and part metadata', () => {
  const payload = chatPayload([
    { id: 'u1', role: 'user', parts: [{ type: 'text', text: 'First question' }] },
    { id: 'a1', role: 'assistant', parts: [{ type: 'step-start' }, { type: 'text', text: 'First answer', state: 'done' }] },
    { id: 'u2', role: 'user', parts: [{ type: 'text', text: 'Follow up' }] },
  ], 'table1');
  expect(payload.messages).toHaveLength(3);
  expect(payload.messages[1]).toEqual({ role: 'assistant', parts: [{ type: 'text', text: 'First answer' }] });
  expect(JSON.stringify(payload)).not.toContain('state');
  expect(JSON.stringify(payload)).not.toContain('step-start');
});
