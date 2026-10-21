'use client';
import { useEffect, useState } from 'react';
type Source = {
  id: string;
  baseId: string;
  tableId: string;
  fields: { id: string; title: string }[];
};
type Feed = {
  id: string;
  status: string;
  reason?: string;
  grant: { consumer: string; owner: string; expiresAt: string };
  schema: { version: string };
};
const notice =
  'Stopping access prevents future reads. It cannot recall bytes already transmitted or guarantee erasure of exported copies. Requests admitted before the change may finish.';
export default function Feeds() {
  const [sources, setSources] = useState<Source[]>([]),
    [feeds, setFeeds] = useState<Feed[]>([]),
    [owner, setOwner] = useState('');
  const [source, setSource] = useState(''),
    [fields, setFields] = useState<string[]>([]),
    [all, setAll] = useState(false),
    [scopeField, setScopeField] = useState(''),
    [scopeValue, setScopeValue] = useState('');
  const [consumer, setConsumer] = useState(''),
    [expiry, setExpiry] = useState(''),
    [error, setError] = useState(''),
    [busy, setBusy] = useState(false),
    [result, setResult] = useState<unknown>(null),
    [secret, setSecret] = useState('');
  async function request(path: string, body?: unknown) {
    const r = await fetch(path, {
      method: body ? 'POST' : 'GET',
      headers: body ? { 'content-type': 'application/json' } : {},
      body: body ? JSON.stringify(body) : undefined,
      signal: AbortSignal.timeout(60000),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.error || 'Feed request failed.');
    return data;
  }
  async function load() {
    const data = await request('/api/feeds');
    setSources(data.sources);
    setFeeds(data.feeds);
    setOwner(data.owner);
  }
  useEffect(() => {
    let live = true;
    request('/api/feeds')
      .then((data) => {
        if (live) {
          setSources(data.sources);
          setFeeds(data.feeds);
          setOwner(data.owner);
        }
      })
      .catch((e) => {
        if (live) setError(e.message);
      });
    return () => {
      live = false;
    };
  }, []);
  async function run(body: unknown) {
    setBusy(true);
    setError('');
    setResult(null);
    setSecret('');
    try {
      const data = await request('/api/feeds', body);
      if (data.credential) setSecret(data.credential);
      setResult(data.credential ? { feed: data.feed } : data);
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Request failed.');
    } finally {
      setBusy(false);
    }
  }
  return (
    <main className="mx-auto max-w-5xl space-y-6 p-6">
      <a href="/" className="underline">
        ← Back to workspace
      </a>
      <h1 className="text-3xl font-bold">Governed data feeds</h1>
      <p>
        Share an explicitly approved dataset with one named application. Feed approval does not
        permit AI-provider sharing. Complex fields, linked records and attachments are excluded.
      </p>
      <p className="rounded-xl border p-4">{notice}</p>
      {error && (
        <p role="alert" className="text-red-700">
          {error}
        </p>
      )}
      <form
        className="space-y-4 rounded-xl border p-5"
        onSubmit={(e) => {
          e.preventDefault();
          if (!Number.isFinite(Date.parse(expiry))) {
            setError('Choose a valid expiry.');
            return;
          }
          void run({
            action: 'create',
            grant: {
              source,
              fields,
              owner,
              consumer,
              expiresAt: new Date(expiry).toISOString(),
              scope: all
                ? { kind: 'all', confirmed: true }
                : { kind: 'equals', field: scopeField, values: [scopeValue] },
            },
          });
        }}
      >
        <h2 className="text-xl font-semibold">Approve a new grant</h2>
        <label className="block">
          Reviewed workspace / table
          <select
            required
            value={source}
            disabled={busy}
            className="ml-3 border p-2"
            onChange={(e) => {
              setSource(e.target.value);
              setFields([]);
              setAll(false);
              setScopeField('');
            }}
          >
            <option value="">Select reviewed source</option>
            {sources.map((s) => (
              <option key={s.id} value={s.id}>
                {s.id} — {s.baseId} / {s.tableId}
              </option>
            ))}
          </select>
        </label>
        <fieldset disabled={busy}>
          <legend>Permitted fields (text/null; no hidden expansions)</legend>
          {sources
            .find((s) => s.id === source)
            ?.fields.map((f) => (
              <label key={f.id} className="mr-4 inline-block">
                <input
                  type="checkbox"
                  checked={fields.includes(f.id)}
                  onChange={(e) =>
                    setFields(
                      e.target.checked ? [...fields, f.id] : fields.filter((id) => id !== f.id),
                    )
                  }
                />
                {f.title}
              </label>
            ))}
        </fieldset>
        <label className="block">
          <input
            type="checkbox"
            checked={all}
            disabled={busy}
            onChange={(e) => setAll(e.target.checked)}
          />{' '}
          Explicitly approve every row in this reviewed view
        </label>
        {!all && (
          <div>
            <label>
              Row scope field{' '}
              <select
                required
                value={scopeField}
                disabled={busy}
                onChange={(e) => setScopeField(e.target.value)}
              >
                <option value="">Select field</option>
                {sources
                  .find((s) => s.id === source)
                  ?.fields.filter((f) => fields.includes(f.id))
                  .map((f) => (
                    <option key={f.id} value={f.id}>
                      {f.title}
                    </option>
                  ))}
              </select>
            </label>
            <label>
              {' '}
              equals{' '}
              <input
                required
                value={scopeValue}
                disabled={busy}
                className="border p-2"
                onChange={(e) => setScopeValue(e.target.value)}
              />
            </label>
          </div>
        )}
        <label className="block">
          Named consumer{' '}
          <input
            required
            maxLength={120}
            value={consumer}
            disabled={busy}
            className="border p-2"
            onChange={(e) => setConsumer(e.target.value)}
          />
        </label>
        <p>Accountable owner: {owner || 'Loading authenticated owner…'}</p>
        <label className="block">
          Expiry (within 30 days){' '}
          <input
            required
            type="datetime-local"
            value={expiry}
            disabled={busy}
            className="border p-2"
            onChange={(e) => setExpiry(e.target.value)}
          />
        </label>
        <button
          disabled={busy || !fields.length || !owner}
          className="rounded bg-purple-700 p-3 text-white"
        >
          Create paused grant
        </button>
      </form>
      {secret && (
        <section role="status" className="rounded-xl border p-4">
          <h2>Credential shown once</h2>
          <p>
            Copy privately into the consumer’s secret store. Rotation invalidates old credentials
            and cursors.
          </p>
          <code className="break-all">{secret}</code>
          <button className="ml-4 underline" onClick={() => setSecret('')}>
            Hide credential
          </button>
        </section>
      )}
      <section className="space-y-3">
        <h2 className="text-xl font-semibold">Your grants</h2>
        {feeds.map((f) => (
          <article className="rounded-xl border p-4" key={f.id}>
            <h3 className="font-bold">
              {f.grant.consumer} · {f.status}
            </h3>
            <p>
              Feed {f.id} · owner {f.grant.owner} · expires {f.grant.expiresAt}
            </p>
            {f.reason && <p>{f.reason}</p>}
            <p>Schema {f.schema.version}</p>
            <div className="flex flex-wrap gap-3">
              {(['snapshot', 'resume', 'pause', 'rotate', 'revoke'] as const).map((action) => (
                <button
                  disabled={busy || f.status === 'revoked'}
                  className="rounded border p-2"
                  key={action}
                  onClick={() => {
                    if (
                      (action === 'revoke' || action === 'rotate') &&
                      !window.confirm(
                        `${action === 'revoke' ? 'Permanently revoke this grant?' : 'Replace the credential and invalidate cursors?'} ${notice}`,
                      )
                    )
                      return;
                    void run({ action, id: f.id });
                  }}
                >
                  {action === 'snapshot' ? 'Build snapshot & preview' : action}
                </button>
              ))}
              <button
                disabled={busy}
                className="underline"
                onClick={() => {
                  setBusy(true);
                  setError('');
                  request(`/api/feeds?action=history&id=${encodeURIComponent(f.id)}`)
                    .then(setResult)
                    .catch((e) => setError(e.message))
                    .finally(() => setBusy(false));
                }}
              >
                Access history (first 100 events)
              </button>
            </div>
          </article>
        ))}
      </section>
      {result !== null && (
        <section>
          <h2 className="text-xl font-semibold">Result / preview</h2>
          <p>
            Preview contains at most 10 rows of this immutable snapshot. The manifest reports the
            full count. Consumer pages use the same snapshot ID; later snapshots may reflect source
            changes.
          </p>
          <pre className="max-h-96 overflow-auto rounded border p-4">
            {JSON.stringify(result, null, 2)}
          </pre>
        </section>
      )}
    </main>
  );
}
