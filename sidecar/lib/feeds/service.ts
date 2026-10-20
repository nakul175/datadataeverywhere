import 'server-only';
import { randomBytes, randomUUID, createHmac, timingSafeEqual, createHash } from 'node:crypto';
import { HttpError } from '../errors';
import {
  canonical,
  hash,
  grantSchema,
  schemaFor,
  LIMITS,
  revocationNotice,
  type Grant,
  type Schema,
  type Source,
  type RecordRow,
} from './contracts';
import { FeedStore, feedStore } from './store';
import { sourceFor, authority, extract, verifyView, FeedSchemaError } from './source';
export type Actor = { id: string; token: string };
type Feed = {
  id: string;
  grant: Grant;
  policy: number;
  mapping: string;
  schema: Schema;
  generation: number;
  credential: string;
  seed: string;
  status: 'active' | 'paused' | 'revoked';
  reason?: string;
  schemaChange?: { version: string; fields: string[]; migration: string };
  createdAt: string;
};
type Manifest = {
  id: string;
  feedId: string;
  policyVersion: number;
  schemaVersion: string;
  extractedAt: string;
  expiresAt: string;
  rowCount: number;
  digest: string;
  digestAlgorithm: 'sha256';
  canonicalization: 'dde-json-sorted-v1-newline';
  ordering: 'source-key-text-C';
  consistency: 'repeatable-read';
  schema: Schema;
};
type Cursor = {
  feed: string;
  snapshot: string;
  generation: number;
  schema: string;
  position: number;
  expires: number;
  mode: 'rows' | 'changes';
  before?: string;
};
const hmac = (seed: string, value: string) =>
  createHmac('sha256', seed).update(value).digest('base64url');
const credential = () => randomBytes(32).toString('base64url');
const compare = (a: string, b: string) => {
  const left = Buffer.from(a),
    right = Buffer.from(b);
  return left.length === right.length && timingSafeEqual(left, right);
};
export class FeedService {
  constructor(
    readonly store: FeedStore = feedStore(),
    readonly deps = { sourceFor, authority, extract, verifyView },
  ) {}
  readonly deadline = Date.now() + 45000;
  guard() {
    if (Date.now() > this.deadline)
      throw new HttpError(503, 'Feed operation timed out; retry without changing the grant.');
  }
  get(id: string): Feed {
    const row = this.store.db.prepare('SELECT body FROM feeds WHERE id=?').get(id);
    if (!row) throw new HttpError(404, 'Feed unavailable.');
    return JSON.parse(String(row.body));
  }
  save(feed: Feed) {
    this.store.db
      .prepare('INSERT INTO feeds VALUES (?,?) ON CONFLICT(id) DO UPDATE SET body=excluded.body')
      .run(feed.id, JSON.stringify(feed));
  }
  public(feed: Feed) {
    return {
      id: feed.id,
      grant: feed.grant,
      policyVersion: feed.policy,
      schema: feed.schema,
      status:
        Date.parse(feed.grant.expiresAt) <= Date.now() && feed.status !== 'revoked'
          ? 'expired'
          : feed.status,
      reason: feed.reason,
      schemaChange: feed.schemaChange,
      createdAt: feed.createdAt,
      revocationNotice,
    };
  }
  async verify(feed: Feed, actor?: Actor) {
    this.guard();
    const source = this.deps.sourceFor(feed.grant.source);
    try {
      if (hash(canonical(source)) !== feed.mapping)
        throw new HttpError(409, 'Reviewed source mapping changed; create a newly approved grant.');
      const schema = await this.deps.authority(source, feed.grant.owner, feed.grant, actor);
      this.guard();
      if (schema.version !== feed.schema.version)
        throw new HttpError(409, 'Export schema changed; reapproval required.');
      await this.deps.verifyView(source);
      this.guard();
      return source;
    } catch (e) {
      if (e instanceof HttpError && e.status === 409 && feed.status !== 'revoked')
        this.store.transaction(() => {
          const current = this.get(feed.id);
          if (current.status === 'revoked' || current.generation !== feed.generation) return;
          current.status = 'paused';
          current.reason = e.message;
          current.schemaChange =
            e instanceof FeedSchemaError
              ? e.change
              : {
                  version: hash(canonical({ mapping: source, reason: e.message })),
                  fields: current.grant.fields,
                  migration: 'Review the source mapping and create a new approved grant.',
                };
          this.save(current);
          this.store.audit(
            feed.id,
            'source-policy',
            'schema-pause',
            'denied',
            current.policy,
            undefined,
            feed.schema.version,
          );
        });
      throw e;
    }
  }
  async admin(id: string, actor: Actor) {
    const feed = this.get(id);
    try {
      await this.deps.authority(
        this.deps.sourceFor(feed.grant.source),
        feed.grant.owner,
        feed.grant,
        actor,
        false,
      );
    } catch (e) {
      this.store.audit(id, actor.id, 'admin-authorize', 'denied', feed.policy);
      throw e;
    }
    return feed;
  }
  async list(actor: Actor) {
    const items = [];
    for (const row of this.store.db.prepare('SELECT id FROM feeds LIMIT 64').all()) {
      this.guard();
      const feed = this.get(String(row.id));
      // Only the accountable owner sees an existing grant, including paused mapping failures.
      if (feed.grant.owner !== actor.id) continue;
      try {
        await this.deps.authority(
          this.deps.sourceFor(feed.grant.source),
          feed.grant.owner,
          feed.grant,
          actor,
          false,
        );
        items.push(this.public(feed));
      } catch {}
    }
    return items;
  }
  async create(input: unknown, actor: Actor) {
    const parsed = grantSchema.safeParse(input);
    if (!parsed.success)
      throw new HttpError(400, 'Select explicit fields, scope, consumer, owner and expiry.');
    const grant = parsed.data;
    const expiry = Date.parse(grant.expiresAt);
    if (grant.owner !== actor.id || expiry <= Date.now() || expiry > Date.now() + 30 * 86400000)
      throw new HttpError(400, 'Owner must be you; expiry must be within 30 days.');
    const source = this.deps.sourceFor(grant.source);
    if (
      grant.fields.some((id) => !source.fields.some((f) => f.id === id)) ||
      (grant.scope.kind === 'equals' && !grant.fields.includes(grant.scope.field))
    )
      throw new HttpError(403, 'Fields and scope must use approved projected columns.');
    const schema = await this.deps.authority(source, grant.owner, grant, actor);
    await this.deps.verifyView(source);
    const secret = credential();
    const feed: Feed = {
      id: randomUUID(),
      grant,
      policy: 1,
      mapping: hash(canonical(source)),
      schema,
      generation: 1,
      credential: hash(secret),
      seed: credential(),
      status: 'paused',
      reason: 'New grant; preview a complete snapshot before resuming.',
      createdAt: new Date().toISOString(),
    };
    this.store.transaction(() => {
      if (Number(this.store.db.prepare('SELECT count(*) AS n FROM feeds').get()?.n) >= LIMITS.feeds)
        throw new HttpError(429, 'Feed limit reached.');
      this.save(feed);
      this.store.audit(feed.id, actor.id, 'create', 'success', feed.policy);
    });
    return { feed: this.public(feed), credential: secret };
  }
  assertActive(feed: Feed) {
    if (feed.status !== 'active' || Date.parse(feed.grant.expiresAt) <= Date.now())
      throw new HttpError(403, 'Feed paused, expired or revoked.');
  }
  async consumer(id: string, secret: string) {
    const feed = this.get(id);
    try {
      if (!secret || secret.length > 200 || !compare(feed.credential, hash(secret)))
        throw new HttpError(403, 'Feed access refused.');
      this.assertActive(feed);
      await this.verify(feed);
      const current = this.get(id);
      this.assertActive(current);
      if (current.generation !== feed.generation)
        throw new HttpError(409, 'Grant changed; restart with the current credential.');
      return current;
    } catch (e) {
      this.store.audit(id, 'consumer', 'authorize', 'denied', feed.policy);
      throw e;
    }
  }
  async lifecycle(id: string, action: 'pause' | 'resume' | 'revoke' | 'rotate', actor: Actor) {
    const feed = await this.admin(id, actor);
    if (action === 'resume') await this.verify(feed, actor);
    let replacement: string | undefined;
    return this.store.transaction(() => {
      const current = this.get(feed.id);
      if (current.status === 'revoked')
        throw new HttpError(409, 'Revocation is permanent. Create a new approved grant.');
      if (action === 'resume') {
        if (Date.parse(current.grant.expiresAt) <= Date.now())
          throw new HttpError(409, 'Grant expired. Create a new approved grant.');
        if (
          !this.store.db
            .prepare(
              "SELECT id FROM snapshots WHERE feed=? AND generation=? AND expires>? AND manifest<>'{}'",
            )
            .get(id, current.generation, Date.now())
        )
          throw new HttpError(409, 'Build and preview a current snapshot first.');
        current.status = 'active';
        delete current.reason;
      } else if (action === 'pause') current.status = 'paused';
      else if (action === 'revoke') {
        current.status = 'revoked';
        current.generation++;
      } else {
        replacement = credential();
        current.credential = hash(replacement);
        current.generation++;
        current.status = 'paused';
        current.reason = 'Credential rotated. Build a new snapshot before resuming.';
      }
      this.save(current);
      this.store.audit(id, actor.id, action, 'success', current.policy);
      return { feed: this.public(current), ...(replacement ? { credential: replacement } : {}) };
    });
  }
  async build(id: string, actor: Actor, signal?: AbortSignal) {
    const feed = await this.admin(id, actor);
    const source = await this.verify(feed, actor);
    if (feed.status === 'revoked' || Date.parse(feed.grant.expiresAt) <= Date.now())
      throw new HttpError(403, 'Grant expired or revoked.');
    this.store.cleanup();
    const unlock = this.store.lock(id);
    const snapshot = randomUUID();
    let count = 0,
      bytes = 0;
    const digest = createHash('sha256');
    const extractedAt = new Date().toISOString();
    const manifest: Manifest = {
      id: snapshot,
      feedId: id,
      policyVersion: feed.policy,
      schemaVersion: feed.schema.version,
      extractedAt,
      expiresAt: new Date(
        Math.min(Date.now() + LIMITS.snapshotMs, Date.parse(feed.grant.expiresAt)),
      ).toISOString(),
      rowCount: 0,
      digest: '',
      digestAlgorithm: 'sha256',
      canonicalization: 'dde-json-sorted-v1-newline',
      ordering: 'source-key-text-C',
      consistency: 'repeatable-read',
      schema: feed.schema,
    };
    // Staging is private: no manifest marks it complete until extraction and fresh authority succeed.
    this.store.db
      .prepare('INSERT INTO snapshots VALUES (?,?,?,?,?)')
      .run(snapshot, id, feed.generation, Date.now() + 120000, '{}');
    try {
      await this.deps.extract(
        source,
        feed.grant,
        feed.schema,
        (key, values) => {
          const opaque = hmac(feed.seed, `record:${key}`);
          const row: RecordRow = { key: opaque, version: hash(canonical(values)), values };
          const payload = canonical(row);
          bytes += Buffer.byteLength(payload) + 1;
          if (++count > LIMITS.rows || bytes > LIMITS.bytes)
            throw new HttpError(
              413,
              'Snapshot exceeds the complete-export limit; narrow the approved row scope.',
            );
          digest.update(payload + '\n');
          this.store.db
            .prepare('INSERT INTO records VALUES (?,?,?,?,?)')
            .run(snapshot, count - 1, row.key, row.version, payload);
        },
        signal,
      );
      this.guard();
      await this.verify(feed, actor);
      manifest.rowCount = count;
      manifest.digest = digest.digest('hex');
      this.store.transaction(() => {
        const current = this.get(id);
        if (
          current.generation !== feed.generation ||
          current.status === 'revoked' ||
          Date.parse(current.grant.expiresAt) <= Date.now() ||
          signal?.aborted
        )
          throw new HttpError(409, 'Grant changed or extraction interrupted; restart.');
        this.store.db
          .prepare('UPDATE snapshots SET expires=?,manifest=? WHERE id=?')
          .run(Date.parse(manifest.expiresAt), JSON.stringify(manifest), snapshot);
        this.store.db
          .prepare(
            'DELETE FROM snapshots WHERE feed=? AND id NOT IN (SELECT id FROM snapshots WHERE feed=? AND expires>0 ORDER BY rowid DESC LIMIT 2)',
          )
          .run(id, id);
        this.store.audit(
          id,
          actor.id,
          'snapshot',
          'success',
          feed.policy,
          snapshot,
          feed.schema.version,
          { count: manifest.rowCount, digest: manifest.digest },
        );
      });
      return {
        manifest,
        preview: this.rows(snapshot, 0, 10),
        previewLimit: 10,
        completePreview: count <= 10,
      };
    } catch (e) {
      this.store.db.prepare('DELETE FROM snapshots WHERE id=?').run(snapshot);
      this.store.audit(
        id,
        actor.id,
        'snapshot',
        signal?.aborted ? 'interrupted' : 'failed',
        feed.policy,
      );
      throw e;
    } finally {
      unlock();
    }
  }
  snapshot(feed: Feed, id: string): Manifest {
    const row = this.store.db
      .prepare('SELECT * FROM snapshots WHERE id=? AND feed=?')
      .get(id, feed.id);
    if (
      !row ||
      String(row.manifest) === '{}' ||
      Number(row.expires) <= Date.now() ||
      Number(row.generation) !== feed.generation
    )
      throw new HttpError(
        409,
        'Snapshot/checkpoint unavailable or expired; restart with a fresh snapshot.',
      );
    const manifest = JSON.parse(String(row.manifest)) as Manifest;
    if (manifest.schemaVersion !== feed.schema.version)
      throw new HttpError(409, 'Schema changed; restart.');
    return manifest;
  }
  rows(snapshot: string, position: number, limit = LIMITS.page): RecordRow[] {
    return this.store.db
      .prepare(
        'SELECT payload FROM records WHERE snapshot=? AND position>=? ORDER BY position LIMIT ?',
      )
      .all(snapshot, position, limit)
      .map((r) => JSON.parse(String(r.payload)));
  }
  sign(feed: Feed, cursor: Cursor) {
    const payload = Buffer.from(canonical(cursor)).toString('base64url');
    return `${payload}.${hmac(feed.seed, payload)}`;
  }
  parse(feed: Feed, token: string): Cursor {
    if (token.length > 2000) throw new HttpError(400, 'Invalid cursor; restart.');
    const [payload, signature, ...rest] = token.split('.');
    if (!payload || !signature || rest.length || !compare(hmac(feed.seed, payload), signature))
      throw new HttpError(400, 'Invalid cursor; restart.');
    let c: Cursor;
    try {
      c = JSON.parse(Buffer.from(payload, 'base64url').toString('utf8'));
    } catch {
      throw new HttpError(400, 'Invalid cursor; restart.');
    }
    if (
      c.feed !== feed.id ||
      c.generation !== feed.generation ||
      c.schema !== feed.schema.version ||
      !Number.isSafeInteger(c.position) ||
      c.position < 0 ||
      c.expires <= Date.now() ||
      !['rows', 'changes'].includes(c.mode)
    )
      throw new HttpError(409, 'Cursor expired or grant changed; restart.');
    return c;
  }
  async page(
    id: string,
    secret: string,
    input: { snapshot?: string; cursor?: string; before?: string },
    signal?: AbortSignal,
  ) {
    const feed = await this.consumer(id, secret);
    try {
      if (signal?.aborted)
        throw new HttpError(499, 'Feed read interrupted; retry the same authorized cursor.');
      const manifest = input.cursor ? undefined : this.snapshot(feed, input.snapshot || '');
      const c = input.cursor
        ? this.parse(feed, input.cursor)
        : {
            feed: id,
            snapshot: manifest!.id,
            generation: feed.generation,
            schema: feed.schema.version,
            position: 0,
            expires: Date.parse(manifest!.expiresAt),
            mode: input.before ? ('changes' as const) : ('rows' as const),
            ...(input.before ? { before: input.before } : {}),
          };
      if (input.cursor && (input.snapshot || input.before))
        throw new HttpError(400, 'Use a cursor alone to resume.');
      const current = this.snapshot(feed, c.snapshot);
      let records: unknown[];
      if (c.mode === 'changes') {
        const before = this.snapshot(feed, c.before || '');
        if (before.extractedAt >= current.extractedAt)
          throw new HttpError(409, 'Checkpoint order is invalid; resnapshot.');
        // Immutable comparison: upserts contain only current approved fields, removals only an already-shared opaque key.
        records = this.store.db
          .prepare(`SELECT key, version, payload, kind FROM (
          SELECT n.key,n.version,n.payload,'upsert' AS kind FROM records n LEFT JOIN records o ON o.snapshot=? AND o.key=n.key WHERE n.snapshot=? AND (o.version IS NULL OR o.version<>n.version)
          UNION ALL SELECT o.key,o.version,NULL AS payload,'remove' AS kind FROM records o LEFT JOIN records n ON n.snapshot=? AND n.key=o.key WHERE o.snapshot=? AND n.key IS NULL
          ) ORDER BY key COLLATE BINARY LIMIT ? OFFSET ?`)
          .all(before.id, current.id, current.id, before.id, LIMITS.page + 1, c.position)
          .map((r) =>
            r.kind === 'remove'
              ? { kind: 'remove', key: r.key, version: hash(`${current.id}:${r.key}:remove`) }
              : { kind: 'upsert', ...JSON.parse(String(r.payload)) },
          );
      } else records = this.rows(c.snapshot, c.position, LIMITS.page + 1);
      const more = records.length > LIMITS.page;
      records = records.slice(0, LIMITS.page);
      const next = more ? this.sign(feed, { ...c, position: c.position + records.length }) : null;
      return this.store.transaction(() => {
        if (signal?.aborted)
          throw new HttpError(499, 'Feed read interrupted; retry the same authorized cursor.');
        const latest = this.get(id);
        this.assertActive(latest);
        if (latest.generation !== feed.generation)
          throw new HttpError(409, 'Grant changed; restart.');
        this.store.audit(
          id,
          feed.grant.consumer,
          c.mode,
          'success',
          feed.policy,
          c.snapshot,
          feed.schema.version,
          { count: records.length, digest: current.digest, position: c.position },
        );
        return {
          manifest: current,
          mode: c.mode,
          ...(c.before ? { before: c.before } : {}),
          records,
          next,
          pageComplete: !more,
          completion: more ? null : { ...current, complete: true },
        };
      });
    } catch (e) {
      this.store.audit(
        id,
        feed.grant.consumer,
        'page',
        e instanceof HttpError && e.status === 499 ? 'interrupted' : 'denied',
        feed.policy,
      );
      throw e;
    }
  }
  async history(id: string, actor: Actor, after: number) {
    const feed = await this.admin(id, actor);
    return this.store.transaction(() => {
      this.store.audit(id, actor.id, 'history', 'success', feed.policy);
      const oldest = Number(
        this.store.db.prepare('SELECT MIN(seq) AS n FROM audit WHERE feed=?').get(id)?.n || 0,
      );
      return {
        retention: 'Last 10000 events globally; older history is explicitly unavailable.',
        oldestRetainedSequence: oldest,
        gap: after > 0 && after < oldest,
        events: this.store.db
          .prepare(
            'SELECT seq,at,actor,action,outcome,policy,snapshot,schema,evidence FROM audit WHERE feed=? AND seq>? ORDER BY seq LIMIT 100',
          )
          .all(id, after),
      };
    });
  }
}
