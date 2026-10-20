import type { UIMessage } from 'ai';
// The UI stream adds step markers, state, and provider metadata to messages.
// Send text only; never forward those presentation/protocol fields to the API.
export function chatPayload(messages: UIMessage[], tableId: string) {
  return { tableId, messages: messages.map(message => ({
    role: message.role,
    parts: message.parts.flatMap(part => part.type === 'text' ? [{ type: 'text' as const, text: part.text }] : []),
  })).filter(message => message.parts.length > 0) };
}
