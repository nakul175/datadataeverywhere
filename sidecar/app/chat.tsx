'use client';
import { useEffect, useMemo, useState } from 'react';
import { useChat } from '@ai-sdk/react';
import { DefaultChatTransport } from 'ai';
import { chatPayload } from '@/lib/payload';
type Table = { id: string; name: string };
export default function Chat({ user, tables }: { user: string; tables: Table[] }) {
  const [table, setTable] = useState(tables[0]?.id || '');
  return <ChatSession key={table} user={user} tables={tables} table={table} select={setTable} />;
}
function ChatSession({
  user,
  tables,
  table,
  select,
}: {
  user: string;
  tables: Table[];
  table: string;
  select: (id: string) => void;
}) {
  const [input, setInput] = useState('');
  const transport = useMemo(
    () =>
      new DefaultChatTransport({
        api: '/api/chat',
        prepareSendMessagesRequest: ({ messages }) => ({ body: chatPayload(messages, table) }),
      }),
    [table],
  );
  const { messages, sendMessage, status, error, stop, setMessages, clearError } = useChat({
    transport,
  });
  useEffect(
    () => () => {
      void stop();
    },
    [stop],
  );
  const busy = status === 'submitted' || status === 'streaming';
  return (
    <main className="min-h-screen md:grid md:grid-cols-[280px_1fr]">
      <aside className="border-b border-slate-800 bg-[#10191f] p-7 md:min-h-screen md:border-r">
        <a href="/" className="text-xl font-bold tracking-tight">
          DataData<span className="text-teal-300">Everywhere</span>
          <span className="mt-1 block text-[11px] font-normal uppercase tracking-[.3em] text-slate-500">
            Team data engine
          </span>
        </a>
        <div className="my-10 h-px bg-slate-800" />
        <p className="mb-3 text-xs uppercase tracking-widest text-slate-400">Workspace context</p>
        <label htmlFor="table" className="mb-2 block text-sm text-slate-300">
          Active table
        </label>
        <select
          id="table"
          value={table}
          disabled={busy}
          onChange={(e) => select(e.target.value)}
          className="w-full rounded-xl border border-slate-700 bg-slate-900 p-3 text-sm"
        >
          {!tables.length && <option value="">No approved tables</option>}
          {tables.map((t) => (
            <option key={t.id} value={t.id}>
              {t.name}
            </option>
          ))}
        </select>
        <p className="mt-4 text-xs leading-6 text-slate-500">
          Answers use up to 100 rows and approved columns. This selection is independent of your
          open spreadsheet view. Changing tables starts a fresh chat.
        </p>
        <button
          type="button"
          disabled={busy}
          onClick={() => {
            setMessages([]);
            clearError();
            setInput('');
          }}
          className="mt-4 block w-full rounded-xl border border-slate-700 px-4 py-3 text-left text-sm"
        >
          New conversation
        </button>
        <p className="mt-10 text-xs text-slate-500">
          Signed in as <span className="text-slate-300">{user}</span>
        </p>
      </aside>
      <section className="mx-auto flex min-h-[90vh] w-full max-w-4xl flex-col px-6 py-8 md:px-12">
        <header className="flex items-center justify-between border-b border-slate-800 pb-6">
          <span className="text-sm text-slate-400">
            AI analyst /{' '}
            <span className="text-slate-200">
              {tables.find((t) => t.id === table)?.name || 'Setup required'}
            </span>
          </span>
          <span className="rounded-full bg-teal-400/10 px-3 py-1 text-xs text-teal-300">
            Read only
          </span>
        </header>
        <div className="flex-1 space-y-6 py-10" aria-live="polite" aria-relevant="additions text">
          {!messages.length && (
            <div className="py-14">
              <p className="mb-4 text-xs uppercase tracking-[.3em] text-teal-300">
                Clarity starts here
              </p>
              <h1 className="text-4xl font-semibold leading-tight md:text-5xl">
                Your data.
                <br />A better conversation.
              </h1>
              <p className="mt-6 max-w-lg leading-7 text-slate-400">
                Ask about trends, missing values, and patterns in your selected table. Only approved
                fields are sent to your configured AI provider.
              </p>
              {!tables.length && (
                <p className="mt-5 text-amber-300">
                  Ask an administrator to approve a table and grant your username access.
                </p>
              )}
            </div>
          )}
          {messages.map((message) => (
            <article
              key={message.id}
              className={`rounded-2xl border p-5 ${message.role === 'user' ? 'ml-8 border-slate-700 bg-slate-800/60' : 'mr-8 border-teal-900/60 bg-[#101c20]'}`}
            >
              <p className="mb-3 text-xs uppercase tracking-widest text-slate-500">
                {message.role === 'user' ? 'You' : 'DataData analyst'}
              </p>
              <div className="whitespace-pre-wrap text-sm leading-7">
                {message.parts.map((part, i) =>
                  part.type === 'text' ? <span key={i}>{part.text}</span> : null,
                )}
              </div>
            </article>
          ))}
          {status === 'submitted' && (
            <p className="animate-pulse text-sm text-teal-300">Reading your table sample…</p>
          )}
          {error && (
            <p
              role="alert"
              className="rounded-xl border border-red-900 bg-red-950/40 p-4 text-sm text-red-200"
            >
              {error.message}
            </p>
          )}
        </div>
        <form
          onSubmit={async (e) => {
            e.preventDefault();
            if (!input.trim() || busy || !table) return;
            const text = input;
            setInput('');
            await sendMessage({ text });
          }}
          className="sticky bottom-0 bg-[#0b1014] py-4"
        >
          <label htmlFor="question" className="sr-only">
            Ask about the table
          </label>
          <div className="rounded-2xl border border-slate-700 bg-slate-900 p-3">
            <textarea
              id="question"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="What should I know about this table?"
              rows={2}
              maxLength={10000}
              disabled={!table || busy}
              className="w-full resize-none bg-transparent p-2 text-sm outline-none"
            />
            <div className="flex items-center justify-between">
              <p className="px-2 text-xs text-slate-500">
                Bounded sample · verify important results
              </p>
              {busy ? (
                <button
                  type="button"
                  onClick={() => stop()}
                  className="rounded-lg bg-slate-700 px-5 py-2 text-sm"
                >
                  Stop
                </button>
              ) : (
                <button
                  disabled={!table || !input.trim()}
                  className="rounded-lg bg-teal-300 px-5 py-2 text-sm font-semibold text-slate-950"
                >
                  Ask ↗
                </button>
              )}
            </div>
          </div>
        </form>
      </section>
    </main>
  );
}
