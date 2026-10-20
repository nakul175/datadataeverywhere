'use client';
import { useEffect, useMemo, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useChat } from '@ai-sdk/react';
import { DefaultChatTransport } from 'ai';
import { chatPayload } from '@/lib/payload';
import type { Column } from '@/lib/workspace';
import { Brand, Mascot } from './brand';
type Item = { id: string; title: string };
type Data = {
  columns: Column[];
  rows: Record<string, unknown>[];
  page: { offset: number; isLast: boolean; total: number | null };
  ai: { ready: boolean; fields: string[]; reason: string };
};
function display(value: unknown): string {
  if (value === null || value === undefined) return '';
  if (typeof value === 'boolean') return value ? '✓' : '—';
  if (typeof value === 'object') return JSON.stringify(value);
  return String(value);
}
async function api(query: Record<string, string> | object, mutate = false) {
  const res = await fetch(
    mutate
      ? '/api/workspace'
      : `/api/workspace?${new URLSearchParams(query as Record<string, string>)}`,
    mutate
      ? {
          method: 'POST',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify(query),
        }
      : { cache: 'no-store' },
  );
  const body = await res.json();
  if (!res.ok) {
    if (res.status === 401) window.location.assign('/signin');
    throw new Error(body.error || 'Unable to load your workspace.');
  }
  return body;
}
export default function Workspace({
  user,
  nocodbUrl,
}: {
  user: { email: string; name: string };
  nocodbUrl: string;
}) {
  const [bases, setBases] = useState<Item[]>([]);
  const [base, setBase] = useState('');
  const [tables, setTables] = useState<Item[]>([]);
  const [table, setTable] = useState('');
  const [data, setData] = useState<Data | null>(null);
  const [offset, setOffset] = useState(0);
  const [query, setQuery] = useState('');
  const [sort, setSort] = useState('');
  const [descending, setDescending] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [chatOpen, setChatOpen] = useState(false);
  const [refresh, setRefresh] = useState(0);
  const [navOpen, setNavOpen] = useState(false);
  const [modal, setModal] = useState<'createBase' | 'createTable' | 'record' | null>(null);
  const [edit, setEdit] = useState<Record<string, unknown> | null>(null);
  const [saving, setSaving] = useState(false);
  const [modalError, setModalError] = useState('');
  const router = useRouter();
  useEffect(() => {
    setChatOpen(window.matchMedia('(min-width: 901px)').matches);
  }, []);
  useEffect(() => {
    let live = true;
    setError('');
    api({ action: 'bases' })
      .then((d) => {
        if (!live) return;
        setBases(d.bases);
        setBase((old) => old || d.bases[0]?.id || '');
      })
      .catch((e) => live && setError(e.message))
      .finally(() => live && setLoading(false));
    return () => {
      live = false;
    };
  }, [refresh]);
  useEffect(() => {
    if (!base) return;
    let live = true;
    setLoading(true);
    setTables([]);
    setTable('');
    setData(null);
    setError('');
    api({ action: 'tables', baseId: base })
      .then((d) => {
        if (!live) return;
        setTables(d.tables);
        setTable(d.tables[0]?.id || '');
        setOffset(0);
      })
      .catch((e) => live && setError(e.message))
      .finally(() => live && setLoading(false));
    return () => {
      live = false;
    };
  }, [base, refresh]);
  useEffect(() => {
    if (!modal) return;
    const previous = document.activeElement as HTMLElement | null;
    const dialog = document.querySelector<HTMLElement>('[role=dialog]');
    const focusables = () =>
      Array.from(
        dialog?.querySelectorAll<HTMLElement>(
          'button:not(:disabled),input:not(:disabled),textarea:not(:disabled),select:not(:disabled),a[href]',
        ) || [],
      );
    (dialog?.querySelector<HTMLElement>('input,textarea') || focusables()[0])?.focus();
    const keydown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && !saving) {
        e.preventDefault();
        setModal(null);
      }
      if (e.key === 'Tab') {
        const nodes = focusables();
        const first = nodes[0],
          last = nodes.at(-1);
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last?.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first?.focus();
        }
      }
    };
    document.addEventListener('keydown', keydown);
    return () => {
      document.removeEventListener('keydown', keydown);
      previous?.focus();
    };
  }, [modal, saving]);
  const reload = useRef(0);
  const [recordRefresh, setRecordRefresh] = useState(0);
  useEffect(() => {
    if (!table) {
      setData(null);
      return;
    }
    const version = ++reload.current;
    setLoading(true);
    setData(null);
    setError('');
    api({ action: 'records', tableId: table, offset: String(offset) })
      .then((d) => {
        if (reload.current === version) setData(d);
      })
      .catch((e) => reload.current === version && setError(e.message))
      .finally(() => reload.current === version && setLoading(false));
    return () => {
      reload.current++;
    };
  }, [table, offset, recordRefresh]);
  const rows = useMemo(() => {
    const rows = (data?.rows || []).filter((row) =>
      Object.values(row).some((v) => display(v).toLowerCase().includes(query.toLowerCase())),
    );
    return sort
      ? [...rows].sort((a, b) => {
          const av = a[sort],
            bv = b[sort];
          const result =
            typeof av === 'number' && typeof bv === 'number'
              ? av - bv
              : display(av).localeCompare(display(bv), undefined, { numeric: true });
          return descending ? -result : result;
        })
      : rows;
  }, [data, query, sort, descending]);
  const active = tables.find((t) => t.id === table);
  const primary = data?.columns.filter((c) => c.primary) || [];
  const editable = data?.columns.filter((c) => c.editable) || [];
  function choose(id: string) {
    setTable(id);
    setOffset(0);
    setQuery('');
    setSort('');
    setNavOpen(false);
  }
  function openModal(
    kind: 'createBase' | 'createTable' | 'record',
    row: Record<string, unknown> | null = null,
  ) {
    setEdit(row);
    setModalError('');
    setModal(kind);
  }
  async function save(form: HTMLFormElement) {
    if (saving) return;
    setSaving(true);
    setModalError('');
    const formData = new FormData(form);
    try {
      if (modal === 'createBase' || modal === 'createTable') {
        const created = await api(
          {
            action: modal,
            title: formData.get('title'),
            ...(modal === 'createTable' ? { baseId: base } : {}),
          },
          true,
        );
        if (modal === 'createBase') {
          const list = await api({ action: 'bases' });
          setBases(list.bases);
          setBase(created.id);
        } else {
          const list = await api({ action: 'tables', baseId: base });
          setTables(list.tables);
          choose(created.id);
        }
      } else {
        const values: Record<string, unknown> = {};
        for (const col of editable) {
          const raw = formData.get(col.id);
          const original = edit?.[col.title];
          let value: unknown = col.type === 'Checkbox' ? raw === 'on' : raw === '' ? null : raw;
          if (
            value !== null &&
            ['Number', 'Decimal', 'Currency', 'Percent', 'Duration', 'Year'].includes(col.type)
          )
            value = Number(value);
          if (
            (!edit && value !== null && value !== false) ||
            (edit && display(value) !== display(original))
          )
            values[col.title] = value;
        }
        if (!Object.keys(values).length) throw new Error('No changed fields to save.');
        await api(
          {
            action: edit ? 'updateRecord' : 'createRecord',
            tableId: table,
            values,
            ...(edit ? { id: edit[primary[0].title] } : {}),
          },
          true,
        );
        setRecordRefresh((v) => v + 1);
      }
      setModal(null);
    } catch (e) {
      setModalError(e instanceof Error ? e.message : 'Unable to save.');
    } finally {
      setSaving(false);
    }
  }
  return (
    <div className={`workspace ${chatOpen ? 'with-chat' : ''}`}>
      <header className="workspace-header">
        <button
          className="icon-button mobile-menu"
          onClick={() => setNavOpen(!navOpen)}
          aria-label="Toggle navigation"
        >
          ☰
        </button>
        <Brand compact />
        <div className="header-center">
          <span className="status-dot" /> Your team’s little universe of data
        </div>
        <div className="header-user">
          <span className="avatar">{user.name.slice(0, 1).toUpperCase()}</span>
          <span title={user.email}>{user.name}</span>
          <button
            className="subtle-link"
            onClick={async () => {
              const res = await fetch('/api/auth/logout', {
                method: 'POST',
                headers: { 'content-type': 'application/json' },
                body: '{}',
              });
              if (res.ok) {
                router.replace('/signin');
                router.refresh();
              } else setError('Unable to sign out. Please try again.');
            }}
          >
            Sign out
          </button>
        </div>
      </header>
      <aside className={`workspace-nav ${navOpen ? 'open' : ''}`}>
        <label className="eyebrow" htmlFor="base">
          YOUR WORKSPACE
        </label>
        <select
          id="base"
          value={base}
          onChange={(e) => setBase(e.target.value)}
          aria-label="Workspace"
        >
          {!bases.length && <option value="">Choose a workspace</option>}
          {bases.map((b) => (
            <option key={b.id} value={b.id}>
              {b.title}
            </option>
          ))}
        </select>
        <button className="nav-item selected" onClick={() => setNavOpen(false)}>
          <span>▦</span> Tables <span className="count">{tables.length}</span>
        </button>
        <a className="nav-item" href={nocodbUrl} target="_blank" rel="noreferrer">
          <span>↗</span> Advanced spreadsheet
        </a>
        <a
          className="nav-item"
          href="https://app.sheethappensofficer.com"
          target="_blank"
          rel="noreferrer"
        >
          <span>☑</span> SheetHappensOfficer
        </a>
        <div className="nav-section">
          <span className="eyebrow">YOUR TABLES</span>
          <button
            aria-label="Create table"
            title="Create table"
            disabled={!base}
            onClick={() => openModal('createTable')}
          >
            ＋
          </button>
        </div>
        <div className="table-list">
          {tables.map((t) => (
            <button
              className={`table-link ${t.id === table ? 'active' : ''}`}
              key={t.id}
              onClick={() => choose(t.id)}
            >
              <span>▦</span>
              {t.title}
            </button>
          ))}
          {!tables.length && <p className="nav-empty">Your next good idea starts with a table.</p>}
        </div>
        <button className="new-workspace" onClick={() => openModal('createBase')}>
          ＋ New workspace
        </button>
        <div className="nav-bottom">
          <Mascot />
          <strong>
            Less hunting.
            <br />
            More knowing.
          </strong>
          <small>An Aplyd tool · Powered by NocoDB</small>
        </div>
      </aside>
      <main className="data-main">
        <div className="breadcrumb">
          Workspace <span>/</span> {bases.find((b) => b.id === base)?.title || 'Your data'}{' '}
          <span>/</span> Tables
        </div>
        <section className="table-heading">
          <div>
            <span className="eyebrow">GOOD DATA. GREAT POSSIBILITIES.</span>
            <h1>{active?.title || 'Make room for your data.'}</h1>
            <p>
              {active
                ? 'A little structure. A lot less spreadsheet chaos.'
                : 'Bring your team’s information into one happy place.'}
            </p>
          </div>
          <button
            className={chatOpen ? 'ai-toggle active' : 'ai-toggle'}
            onClick={() => setChatOpen(!chatOpen)}
          >
            ✦ Ask your data
          </button>
        </section>
        {error && (
          <div className="error banner" role="alert">
            {error}
            <button
              className="subtle-link"
              onClick={() => {
                setRefresh((v) => v + 1);
                setRecordRefresh((v) => v + 1);
              }}
            >
              Retry
            </button>
          </div>
        )}
        {active && (
          <>
            <div className="grid-toolbar">
              <span className="view-label">▦ Grid view</span>
              <label className="search-box">
                <span>⌕</span>
                <input
                  aria-label="Search this page"
                  placeholder="Search this page…"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                />
              </label>
              <select
                aria-label="Sort this page by"
                value={sort}
                onChange={(e) => setSort(e.target.value)}
              >
                <option value="">Sort this page</option>
                {data?.columns.map((c) => (
                  <option key={c.id} value={c.title}>
                    {c.title}
                  </option>
                ))}
              </select>
              {sort && (
                <button
                  className="icon-button"
                  onClick={() => setDescending(!descending)}
                  aria-label={descending ? 'Sort ascending' : 'Sort descending'}
                >
                  {descending ? '↓' : '↑'}
                </button>
              )}
              <button
                className="primary add-record"
                onClick={() => openModal('record')}
                disabled={loading || !editable.length}
              >
                ＋ Add record
              </button>
            </div>
            <div className="grid-scroll" aria-busy={loading}>
              <table className="data-grid">
                <thead>
                  <tr>
                    <th className="row-number">#</th>
                    {data?.columns.map((c) => (
                      <th key={c.id}>
                        <span className="field-icon">
                          {c.type === 'Checkbox'
                            ? '☑'
                            : c.type === 'Number' || c.primary
                              ? '#'
                              : 'T'}
                        </span>
                        {c.title}
                      </th>
                    ))}
                    <th className="edit-col">
                      <span className="sr-only">Actions</span>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {rows.map((row, i) => (
                    <tr key={primary.length === 1 ? display(row[primary[0].title]) : i}>
                      <td className="row-number">{offset + i + 1}</td>
                      {data?.columns.map((c) => (
                        <td key={c.id} title={display(row[c.title])}>
                          {c.type === 'Checkbox' ? (
                            <span className={row[c.title] ? 'checked' : 'unchecked'}>
                              {row[c.title] ? '✓' : '—'}
                            </span>
                          ) : (
                            <span className={c.type === 'SingleSelect' ? 'pill' : ''}>
                              {display(row[c.title]) || <span className="empty-cell">—</span>}
                            </span>
                          )}
                        </td>
                      ))}
                      <td>
                        <button
                          className="edit-button"
                          aria-label={`Edit record ${offset + i + 1}`}
                          disabled={primary.length !== 1 || !editable.length}
                          onClick={() => openModal('record', row)}
                        >
                          Edit
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {loading && (
                <div className="grid-state" role="status">
                  Gathering your data…
                </div>
              )}
              {!loading && !rows.length && (
                <div className="grid-state">
                  <strong>
                    {query ? 'No matches on this page.' : 'A clean sheet. A fresh start.'}
                  </strong>
                  <p>
                    {query
                      ? 'Try another search or move to another page.'
                      : 'Add your first record to get things rolling.'}
                  </p>
                </div>
              )}
            </div>
            <div className="grid-footer">
              <span>
                {data?.page.total !== null && data?.page.total !== undefined
                  ? `${data.page.total.toLocaleString()} total records · `
                  : ''}
                {rows.length} shown{query ? ' after page search' : ''}{' '}
                <span className="footer-dot">·</span> Changes save to your data engine
              </span>
              <div>
                <button
                  disabled={loading || offset === 0}
                  onClick={() => setOffset(Math.max(0, offset - 50))}
                >
                  ← Previous
                </button>
                <span>Page {Math.floor(offset / 50) + 1}</span>
                <button
                  disabled={loading || !data || data.page.isLast}
                  onClick={() => setOffset(offset + 50)}
                >
                  Next →
                </button>
              </div>
            </div>
            <p className="table-help">
              Need more field types, imports, relations or views?{' '}
              <a href={nocodbUrl} target="_blank" rel="noreferrer">
                Open the advanced spreadsheet ↗
              </a>
            </p>
          </>
        )}
        {!active && !loading && !error && (
          <section className="workspace-empty">
            <Mascot />
            <h2>
              {bases.length ? 'Holy sheet. It’s a blank canvas.' : 'Your data deserves a home.'}
            </h2>
            <p>
              {bases.length
                ? 'Create a table, then add your first few records.'
                : 'Create a workspace to keep related tables together.'}
            </p>
            <button
              className="primary"
              onClick={() => openModal(bases.length ? 'createTable' : 'createBase')}
            >
              ＋ {bases.length ? 'Create your first table' : 'Create your workspace'}
            </button>
          </section>
        )}
        {!active && loading && (
          <div className="grid-state" role="status">
            Opening your workspace…
          </div>
        )}
      </main>
      {chatOpen && (
        <Analyst key={table} table={active} ai={data?.ai} close={() => setChatOpen(false)} />
      )}
      {modal && (
        <div className="modal-shade" onClick={() => !saving && setModal(null)}>
          <section
            className="modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="modal-title"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              className="modal-close"
              aria-label="Close dialog"
              disabled={saving}
              onClick={() => setModal(null)}
            >
              ×
            </button>
            <span className="eyebrow">A LITTLE MORE ORGANISED ALREADY.</span>
            <h2 id="modal-title">
              {modal === 'record'
                ? edit
                  ? 'Edit this record'
                  : 'One more good entry.'
                : modal === 'createTable'
                  ? 'Meet your next table.'
                  : 'A home for your data.'}
            </h2>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                void save(e.currentTarget);
              }}
            >
              {modal === 'record' ? (
                <>
                  <p className="muted">
                    Simple fields are editable here. Relations, attachments and calculated fields
                    stay in the advanced spreadsheet.
                  </p>
                  {editable.map((col) => (
                    <label className="record-field" key={col.id}>
                      {col.title}
                      {col.required && ' *'}
                      {col.type === 'Checkbox' ? (
                        <input
                          name={col.id}
                          type="checkbox"
                          defaultChecked={Boolean(edit?.[col.title])}
                        />
                      ) : col.type === 'LongText' ? (
                        <textarea
                          name={col.id}
                          defaultValue={display(edit?.[col.title])}
                          maxLength={10000}
                          required={!edit && col.required}
                          rows={3}
                        />
                      ) : (
                        <input
                          name={col.id}
                          defaultValue={display(edit?.[col.title])}
                          maxLength={10000}
                          required={!edit && col.required}
                          type={
                            [
                              'Number',
                              'Decimal',
                              'Currency',
                              'Percent',
                              'Duration',
                              'Year',
                            ].includes(col.type)
                              ? 'number'
                              : col.type === 'Email'
                                ? 'email'
                                : 'text'
                          }
                          step="any"
                        />
                      )}
                    </label>
                  ))}
                </>
              ) : (
                <label className="record-field">
                  {modal === 'createTable' ? 'Table name' : 'Workspace name'}
                  <input
                    name="title"
                    placeholder={
                      modal === 'createTable' ? 'e.g. Customer accounts' : 'e.g. Team operations'
                    }
                    required
                    maxLength={80}
                    autoFocus
                  />
                </label>
              )}
              {modalError && (
                <p role="alert" className="error">
                  {modalError}
                </p>
              )}
              <div className="modal-actions">
                <button type="button" disabled={saving} onClick={() => setModal(null)}>
                  Cancel
                </button>
                <button className="primary" disabled={saving}>
                  {saving ? 'Saving…' : modal === 'record' ? 'Save record' : 'Create'}
                </button>
              </div>
            </form>
          </section>
        </div>
      )}
    </div>
  );
}
function Analyst({ table, ai, close }: { table?: Item; ai?: Data['ai']; close: () => void }) {
  const [input, setInput] = useState('');
  const messagesEnd = useRef<HTMLDivElement>(null);
  const transport = useMemo(
    () =>
      new DefaultChatTransport({
        api: '/api/chat',
        prepareSendMessagesRequest: ({ messages }) => ({
          body: chatPayload(messages, table?.id || ''),
        }),
      }),
    [table?.id],
  );
  const { messages, sendMessage, status, error, stop, setMessages, clearError } = useChat({
    transport,
  });
  const busy = status === 'submitted' || status === 'streaming';
  useEffect(() => {
    if (messages.length)
      messagesEnd.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }, [messages, status]);
  async function ask(text: string) {
    if (!text.trim() || busy || !ai?.ready) return;
    clearError();
    setInput('');
    await sendMessage({ text });
  }
  return (
    <aside className="analyst">
      <header>
        <span className="ai-spark">✦</span>
        <div>
          <h2>Ask your data</h2>
          <p>Same table. A fresh pair of eyes.</p>
        </div>
        <button className="icon-button" onClick={close} aria-label="Close AI panel">
          ×
        </button>
      </header>
      <div className="context-chip">
        <span className="status-dot" />
        <span>{table?.title || 'Choose a table'}</span>
        <small>TABLE CONTEXT</small>
      </div>
      <div className="ai-messages" aria-live="polite">
        {!messages.length && (
          <>
            <div className="analyst-intro">
              <Mascot />
              <h3>Aha moments, this way.</h3>
              <p>
                Ask a question about your table.
                <br />
                We’ll look for the story in the rows.
              </p>
            </div>
            {!ai?.ready ? (
              <div className="setup-note">
                <strong>{table ? 'A small setup step first.' : 'First, pick your data.'}</strong>
                <p>
                  {table
                    ? ai?.reason || 'Loading your table’s AI settings…'
                    : 'Open or create a table to give your analyst some context.'}
                </p>
                <p>Your table stays usable while AI is being connected.</p>
              </div>
            ) : (
              <div className="suggestions">
                {[
                  'Summarize this table',
                  'Which values are missing?',
                  'What patterns should I investigate?',
                ].map((text) => (
                  <button key={text} onClick={() => void ask(text)}>
                    {text}
                    <span>↗</span>
                  </button>
                ))}
              </div>
            )}
          </>
        )}
        {messages.map((m) => (
          <article key={m.id} className={`message ${m.role}`}>
            <span>{m.role === 'user' ? 'You' : '✦ DataDataEverywhere'}</span>
            <div>
              {m.parts.map((p, i) => (p.type === 'text' ? <span key={i}>{p.text}</span> : null))}
            </div>
          </article>
        ))}
        {status === 'submitted' && (
          <p className="muted" role="status">
            Finding the story in your rows…
          </p>
        )}
        {error && (
          <p role="alert" className="error">
            {error.message}
          </p>
        )}
        <div ref={messagesEnd} />
      </div>
      <form
        className="ai-compose"
        onSubmit={(e) => {
          e.preventDefault();
          void ask(input);
        }}
      >
        <label className="sr-only" htmlFor="question">
          Ask about your table
        </label>
        <textarea
          id="question"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={
            ai?.ready ? 'What’s hiding in these rows?' : 'Your analyst is waiting for setup…'
          }
          disabled={!ai?.ready || busy}
          maxLength={10000}
          rows={3}
        />
        <div>
          <button
            type="button"
            className="subtle-link"
            disabled={busy || !messages.length}
            onClick={() => {
              setMessages([]);
              clearError();
            }}
          >
            New chat
          </button>
          {busy ? (
            <button type="button" className="primary" onClick={() => stop()}>
              Stop
            </button>
          ) : (
            <button
              className="primary"
              disabled={!ai?.ready || !input.trim()}
              aria-label="Send question"
            >
              ↑
            </button>
          )}
        </div>
        <small>
          {ai?.ready
            ? `Up to 100 unfiltered rows · ${ai.fields.length} approved fields`
            : 'Read-only answers · approved fields only'}
          <br />
          AI can make mistakes. Check important answers.
        </small>
      </form>
    </aside>
  );
}
