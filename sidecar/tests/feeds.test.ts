import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
vi.mock('server-only', () => ({}));
import { FeedStore } from '../lib/feeds/store';
import { FeedService } from '../lib/feeds/service';
import { hash, canonical, schemaFor, type Source, type Grant } from '../lib/feeds/contracts';
import { HttpError } from '../lib/errors';
const actor = { id: 'owner', token: 'fixture-session' };
const source: Source = {
  id: 'source',
  baseId: 'base',
  tableId: 'table',
  policyVersion: 'v1',
  schema: 'public',
  view: 'approved',
  key: 'id',
  delegation: 'verified-full-base-admin-only',
  reviewRef: 'synthetic-fixture-review',
  viewDefinitionHash: 'a'.repeat(64),
  fields: [
    { id: 'title', column: 'title', title: 'Title', uidt: 'SingleLineText', pgType: 'text' },
    { id: 'group', column: 'group_name', title: 'Group', uidt: 'SingleLineText', pgType: 'text' },
  ],
};
let folder: string, store: FeedStore, svc: FeedService;
let rows: { key: string; values: Record<string, string | null> }[];
let allowed: boolean;
const grant = (): Grant => ({
  source: 'source',
  fields: ['title', 'group'],
  scope: { kind: 'equals', field: 'group', values: ['approved'] },
  consumer: 'app-one',
  owner: 'owner',
  expiresAt: new Date(Date.now() + 3600000).toISOString(),
});
beforeEach(() => {
  folder = mkdtempSync(join(tmpdir(), 'dde-feed-test-'));
  store = new FeedStore(join(folder, 'state.sqlite'));
  allowed = true;
  rows = Array.from({ length: 257 }, (_, i) => ({
    key: String(i),
    values: { title: `Fixture ${i}`, group: 'approved' },
  }));
  svc = new FeedService(store, {
    sourceFor: () => structuredClone(source),
    verifyView: async () => {},
    authority: async (s, gOwner, g, a) => {
      if (!allowed || gOwner !== 'owner' || (a && a.id !== 'owner'))
        throw new HttpError(403, 'Source denied.');
      return schemaFor(s, g);
    },
    extract: async (_s, _g, _schema, accept, signal) => {
      for (const r of rows) {
        if (signal?.aborted) throw new HttpError(499, 'Interrupted');
        accept(r.key, r.values);
      }
    },
  });
});
afterEach(() => {
  store.db.close();
  rmSync(folder, { recursive: true, force: true });
  vi.restoreAllMocks();
});
async function ready() {
  const created = await svc.create(grant(), actor);
  const snapshot = await svc.build(created.feed.id, actor);
  await svc.lifecycle(created.feed.id, 'resume', actor);
  return { ...created, ...snapshot };
}
describe('Governed feed boundaries and snapshot lifecycle', () => {
  it('requires explicit scope/fields/consumer/owner/expiry and refuses hidden fields', async () => {
    for (const patch of [
      { scope: undefined },
      { scope: { kind: 'all' } },
      { consumer: '' },
      { owner: 'another' },
      { expiresAt: new Date(0).toISOString() },
      { fields: ['secret'] },
      { fields: ['title', 'title'] },
    ])
      await expect(svc.create({ ...grant(), ...patch }, actor)).rejects.toBeInstanceOf(HttpError);
    await expect(
      svc.create(
        {
          ...grant(),
          scope: { kind: 'equals', field: 'group', values: ['approved'] },
          fields: ['title'],
        },
        actor,
      ),
    ).rejects.toMatchObject({ status: 403 });
  });
  it('exports 257 rows exactly, replays cursors and matches preview and independently calculated digest', async () => {
    const f = await ready();
    const first = await svc.page(f.feed.id, f.credential, { snapshot: f.manifest.id });
    expect(first.records).toEqual(expect.arrayContaining(f.preview));
    expect(first.completion).toBeNull();
    const second = await svc.page(f.feed.id, f.credential, { cursor: first.next! });
    expect(await svc.page(f.feed.id, f.credential, { cursor: first.next! })).toEqual(second);
    const third = await svc.page(f.feed.id, f.credential, { cursor: second.next! });
    const all = [...first.records, ...second.records, ...third.records];
    expect(all).toHaveLength(257);
    expect(new Set(all.map((r) => (r as { key: string }).key)).size).toBe(257);
    expect(third.completion?.digest).toBe(hash(all.map((r) => canonical(r) + '\n').join('')));
    expect(third.completion?.complete).toBe(true);
    expect(JSON.stringify(all)).not.toContain('source_key');
    expect(JSON.stringify(svc.public(svc.get(f.feed.id)))).not.toContain(f.credential);
  });
  it.each([0, 1, 100, 200])('completes a %i row boundary without false truncation', async (n) => {
    rows = rows.slice(0, n);
    const f = await ready();
    let p = await svc.page(f.feed.id, f.credential, { snapshot: f.manifest.id });
    let count = p.records.length;
    while (p.next) {
      p = await svc.page(f.feed.id, f.credential, { cursor: p.next });
      count += p.records.length;
    }
    expect(count).toBe(n);
    expect(p.completion?.rowCount).toBe(n);
  });
  it('does not activate an incomplete staging snapshot during extraction', async () => {
    const f = await svc.create(grant(), actor);
    let release!: () => void;
    let started!: () => void;
    const start = new Promise<void>((r) => {
      started = r;
    });
    const waiting = new Promise<void>((r) => {
      release = r;
    });
    svc.deps.extract = async () => {
      started();
      await waiting;
      throw new HttpError(503, 'Synthetic failure');
    };
    const building = svc.build(f.feed.id, actor);
    await start;
    try {
      await expect(svc.lifecycle(f.feed.id, 'resume', actor)).rejects.toMatchObject({
        status: 409,
      });
    } finally {
      release();
    }
    await expect(building).rejects.toMatchObject({ status: 503 });
    expect(svc.get(f.feed.id).status).toBe('paused');
    expect(store.db.prepare('SELECT count(*) AS n FROM snapshots').get()?.n).toBe(0);
  });
  it('keeps an immutable snapshot after source rows change', async () => {
    const f = await ready();
    rows[0].values.title = 'Changed';
    rows.pop();
    expect(
      (await svc.page(f.feed.id, f.credential, { snapshot: f.manifest.id })).manifest.rowCount,
    ).toBe(257);
  });
  it('denies cross-feed credentials, forged cursors and normal session strings', async () => {
    const a = await ready(),
      b = await ready();
    const p = await svc.page(a.feed.id, a.credential, { snapshot: a.manifest.id });
    for (const secret of [b.credential, 'fixture-session', ''])
      await expect(svc.page(a.feed.id, secret, { snapshot: a.manifest.id })).rejects.toMatchObject({
        status: 403,
      });
    await expect(
      svc.page(a.feed.id, a.credential, { cursor: p.next! + 'x' }),
    ).rejects.toMatchObject({ status: 400 });
    await expect(svc.page(b.feed.id, b.credential, { cursor: p.next! })).rejects.toBeInstanceOf(
      HttpError,
    );
  });
  it('rechecks pause, source access, expiry and permanent revocation between pages', async () => {
    const f = await ready();
    const p = await svc.page(f.feed.id, f.credential, { snapshot: f.manifest.id });
    await svc.lifecycle(f.feed.id, 'pause', actor);
    await expect(svc.page(f.feed.id, f.credential, { cursor: p.next! })).rejects.toMatchObject({
      status: 403,
    });
    await svc.lifecycle(f.feed.id, 'resume', actor);
    allowed = false;
    await expect(svc.page(f.feed.id, f.credential, { cursor: p.next! })).rejects.toMatchObject({
      status: 403,
    });
    allowed = true;
    const saved = svc.get(f.feed.id);
    saved.grant.expiresAt = new Date(0).toISOString();
    svc.save(saved);
    await expect(svc.page(f.feed.id, f.credential, { cursor: p.next! })).rejects.toMatchObject({
      status: 403,
    });
    saved.grant.expiresAt = grant().expiresAt;
    svc.save(saved);
    await svc.lifecycle(f.feed.id, 'revoke', actor);
    await expect(svc.lifecycle(f.feed.id, 'resume', actor)).rejects.toMatchObject({ status: 409 });
    await expect(svc.page(f.feed.id, f.credential, { cursor: p.next! })).rejects.toMatchObject({
      status: 403,
    });
  });
  it('rotation invalidates old credentials, snapshots and continuation state', async () => {
    const f = await ready();
    const p = await svc.page(f.feed.id, f.credential, { snapshot: f.manifest.id });
    const rotated = await svc.lifecycle(f.feed.id, 'rotate', actor);
    expect(rotated.credential).toBeTruthy();
    await expect(svc.page(f.feed.id, f.credential, { cursor: p.next! })).rejects.toMatchObject({
      status: 403,
    });
    await expect(svc.lifecycle(f.feed.id, 'resume', actor)).rejects.toMatchObject({ status: 409 });
    await svc.build(f.feed.id, actor);
    await svc.lifecycle(f.feed.id, 'resume', actor);
    await expect(
      svc.page(f.feed.id, rotated.credential!, { cursor: p.next! }),
    ).rejects.toMatchObject({ status: 409 });
  });
  it('produces repeatable upserts and payload-free removals; gaps require restart', async () => {
    rows = rows.slice(0, 3);
    const f = await ready();
    await new Promise((r) => setTimeout(r, 2));
    rows = [
      { key: '0', values: { title: 'Updated', group: 'approved' } },
      rows[2],
      { key: '3', values: { title: 'New', group: 'approved' } },
    ];
    const newer = await svc.build(f.feed.id, actor);
    const p = await svc.page(f.feed.id, f.credential, {
      snapshot: newer.manifest.id,
      before: f.manifest.id,
    });
    expect(p.records).toHaveLength(3);
    expect(
      await svc.page(f.feed.id, f.credential, {
        snapshot: newer.manifest.id,
        before: f.manifest.id,
      }),
    ).toEqual(p);
    const removed = p.records.find((r) => (r as { kind: string }).kind === 'remove');
    expect(Object.keys(removed as object).sort()).toEqual(['key', 'kind', 'version']);
    await new Promise((r) => setTimeout(r, 2));
    await svc.build(f.feed.id, actor);
    await expect(
      svc.page(f.feed.id, f.credential, { snapshot: newer.manifest.id, before: f.manifest.id }),
    ).rejects.toMatchObject({ status: 409 });
  });
  it('pauses changed mappings and does not disclose old payload through history', async () => {
    const f = await ready();
    svc.deps.sourceFor = () => ({ ...source, policyVersion: 'v2' });
    await expect(
      svc.page(f.feed.id, f.credential, { snapshot: f.manifest.id }),
    ).rejects.toMatchObject({ status: 409 });
    expect(svc.get(f.feed.id).status).toBe('paused');
    const history = await svc.history(f.feed.id, actor, 0);
    expect(JSON.stringify(history)).not.toContain(f.credential);
    expect(JSON.stringify(history)).not.toContain('Fixture');
    await expect(
      svc.history(f.feed.id, { id: 'outsider', token: 'other' }, 0),
    ).rejects.toMatchObject({ status: 403 });
  });
  it('fails closed on audit failure and rolls back a lifecycle change', async () => {
    const f = await ready();
    const fail = vi.spyOn(store, 'audit').mockImplementation(() => {
      throw new HttpError(503, 'Audit unavailable');
    });
    await expect(
      svc.page(f.feed.id, f.credential, { snapshot: f.manifest.id }),
    ).rejects.toMatchObject({ status: 503 });
    await expect(svc.lifecycle(f.feed.id, 'revoke', actor)).rejects.toMatchObject({ status: 503 });
    expect(svc.get(f.feed.id).status).toBe('active');
    fail.mockRestore();
  });
  it('rejects an expired snapshot and removes interrupted builds without completion', async () => {
    const f = await ready();
    store.db.prepare('UPDATE snapshots SET expires=0').run();
    await expect(
      svc.page(f.feed.id, f.credential, { snapshot: f.manifest.id }),
    ).rejects.toMatchObject({ status: 409 });
    const abort = new AbortController();
    abort.abort();
    await expect(svc.build(f.feed.id, actor, abort.signal)).rejects.toBeInstanceOf(HttpError);
    expect(
      store.db.prepare('SELECT count(*) AS n FROM snapshots WHERE manifest=?').get('{}')?.n,
    ).toBe(0);
  });
});
