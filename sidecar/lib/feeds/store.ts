import 'server-only';
import { DatabaseSync } from 'node:sqlite';
import { mkdirSync, chmodSync } from 'node:fs';
import { dirname, isAbsolute } from 'node:path';
import { randomUUID } from 'node:crypto';
import { HttpError } from '../errors';
import { LIMITS } from './contracts';
export class FeedStore {
  readonly db: DatabaseSync;
  constructor(path: string) {
    if (!isAbsolute(path))
      throw new HttpError(503, 'Feed storage requires an absolute private path.');
    mkdirSync(dirname(path), { recursive: true, mode: 0o700 });
    this.db = new DatabaseSync(path);
    chmodSync(path, 0o600);
    this.db.exec(`PRAGMA journal_mode=WAL; PRAGMA busy_timeout=3000; PRAGMA foreign_keys=ON;
      PRAGMA max_page_count=65536;
      CREATE TABLE IF NOT EXISTS feeds (id TEXT PRIMARY KEY, body TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS snapshots (id TEXT PRIMARY KEY, feed TEXT NOT NULL, generation INTEGER NOT NULL, expires INTEGER NOT NULL, manifest TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS records (snapshot TEXT NOT NULL REFERENCES snapshots(id) ON DELETE CASCADE, position INTEGER NOT NULL, key TEXT NOT NULL, version TEXT NOT NULL, payload TEXT NOT NULL, PRIMARY KEY(snapshot, position), UNIQUE(snapshot,key));
      CREATE INDEX IF NOT EXISTS snapshots_feed ON snapshots(feed);
      CREATE TABLE IF NOT EXISTS audit (seq INTEGER PRIMARY KEY AUTOINCREMENT, feed TEXT NOT NULL, at TEXT NOT NULL, actor TEXT NOT NULL, action TEXT NOT NULL, outcome TEXT NOT NULL, policy INTEGER, snapshot TEXT, schema TEXT, evidence TEXT);
      CREATE TABLE IF NOT EXISTS requests (id TEXT PRIMARY KEY, expires INTEGER NOT NULL);
      CREATE TABLE IF NOT EXISTS locks (feed TEXT PRIMARY KEY, id TEXT NOT NULL, expires INTEGER NOT NULL);`);
  }
  transaction<T>(fn: () => T): T {
    this.db.exec('BEGIN IMMEDIATE');
    try {
      const result = fn();
      this.db.exec('COMMIT');
      return result;
    } catch (e) {
      this.db.exec('ROLLBACK');
      throw e;
    }
  }
  audit(
    feed: string,
    actor: string,
    action: string,
    outcome: string,
    policy?: number,
    snapshot?: string,
    schema?: string,
    evidence?: { count: number; digest: string; position?: number },
  ) {
    try {
      this.db
        .prepare(
          'INSERT INTO audit(feed,at,actor,action,outcome,policy,snapshot,schema,evidence) VALUES (?,?,?,?,?,?,?,?,?)',
        )
        .run(
          feed,
          new Date().toISOString(),
          actor,
          action,
          outcome,
          policy ?? null,
          snapshot ?? null,
          schema ?? null,
          evidence ? JSON.stringify(evidence) : null,
        );
      this.db
        .prepare('DELETE FROM audit WHERE seq <= (SELECT COALESCE(MAX(seq),0)-? FROM audit)')
        .run(LIMITS.audit);
    } catch {
      throw new HttpError(503, 'Audit storage unavailable; access refused.');
    }
  }
  lock(feed: string) {
    const token = randomUUID();
    this.transaction(() => {
      this.db.prepare('DELETE FROM locks WHERE expires<?').run(Date.now());
      if (Number(this.db.prepare('SELECT count(*) AS n FROM locks').get()?.n) >= 2)
        throw new HttpError(429, 'Two snapshot builds are already running.');
      try {
        this.db.prepare('INSERT INTO locks VALUES (?,?,?)').run(feed, token, Date.now() + 120000);
      } catch {
        throw new HttpError(429, 'This feed already has an active operation.');
      }
    });
    return () => {
      this.db.prepare('DELETE FROM locks WHERE feed=? AND id=?').run(feed, token);
    };
  }
  admit() {
    const token = randomUUID();
    this.transaction(() => {
      this.db.prepare('DELETE FROM requests WHERE expires<?').run(Date.now());
      if (Number(this.db.prepare('SELECT count(*) AS n FROM requests').get()?.n) >= 4)
        throw new HttpError(429, 'Feed request concurrency limit reached.');
      this.db.prepare('INSERT INTO requests VALUES (?,?)').run(token, Date.now() + 90000);
    });
    return () => {
      this.db.prepare('DELETE FROM requests WHERE id=?').run(token);
    };
  }
  cleanup() {
    this.db.prepare('DELETE FROM snapshots WHERE expires<?').run(Date.now());
    // Completed snapshots have a bounded lifetime; at most two retained per feed/generation.
  }
}
let instance: FeedStore | undefined;
export function feedStore() {
  if (!process.env.FEEDS_STATE_FILE)
    throw new HttpError(503, 'Private feed storage is not configured.');
  return (instance ??= new FeedStore(process.env.FEEDS_STATE_FILE));
}
