import { beforeEach, afterEach, expect, it, vi } from 'vitest';
import { mkdtempSync, writeFileSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
vi.mock('server-only', () => ({}));
const session = vi.hoisted(() => ({ engine: vi.fn() }));
vi.mock('../lib/engine', () => ({ engine: session.engine }));
import { authority, sources, FeedSchemaError } from '../lib/feeds/source';
import { schemaFor, type Source, type Grant } from '../lib/feeds/contracts';
const source: Source = {
  id: 'mapped',
  baseId: 'base',
  tableId: 'table',
  policyVersion: 'v1',
  schema: 'approved',
  view: 'safe',
  key: 'id',
  delegation: 'verified-full-base-admin-only',
  reviewRef: 'synthetic review',
  viewDefinitionHash: 'a'.repeat(64),
  fields: [{ id: 'name', column: 'name', title: 'Name', uidt: 'SingleLineText', pgType: 'text' }],
};
const grant: Grant = {
  source: 'mapped',
  fields: ['name'],
  scope: { kind: 'all', confirmed: true },
  consumer: 'app',
  owner: 'owner',
  expiresAt: '2027-01-01T00:00:00.000Z',
};
let folder: string, role: unknown, metadata: Record<string, unknown>;
beforeEach(() => {
  folder = mkdtempSync(join(tmpdir(), 'dde-source-'));
  role = 'owner';
  metadata = {
    id: 'table',
    base_id: 'base',
    columns: [{ id: 'name', column_name: 'name', title: 'Name', uidt: 'SingleLineText' }],
  };
  vi.stubEnv('FEEDS_ENABLED', 'true');
  vi.stubEnv('FEEDS_SOURCES_FILE', join(folder, 'source.json'));
  vi.stubEnv('FEEDS_NOCODB_TOKEN', 'synthetic-metadata-token');
  writeFileSync(join(folder, 'source.json'), JSON.stringify([source]));
  session.engine.mockResolvedValue(metadata);
  vi.stubGlobal(
    'fetch',
    vi.fn(async (input: URL) =>
      Response.json(
        input.pathname.endsWith('/users')
          ? { users: { list: [{ id: 'owner', roles: role }] } }
          : metadata,
      ),
    ),
  );
});
afterEach(() => {
  vi.unstubAllEnvs();
  vi.unstubAllGlobals();
  vi.clearAllMocks();
  rmSync(folder, { recursive: true, force: true });
});
it('refuses disabled, malformed, duplicate and unreviewed mappings', () => {
  expect(sources()).toHaveLength(1);
  vi.stubEnv('FEEDS_ENABLED', 'false');
  expect(() => sources()).toThrow();
  vi.stubEnv('FEEDS_ENABLED', 'true');
  writeFileSync(join(folder, 'source.json'), JSON.stringify([source, source]));
  expect(() => sources()).toThrow();
  writeFileSync(
    join(folder, 'source.json'),
    JSON.stringify([{ ...source, delegation: 'unverified' }]),
  );
  expect(() => sources()).toThrow();
});
it('checks native table access and current full-base owner identity', async () => {
  expect(await authority(source, 'owner', grant, { id: 'owner', token: 'actor-session' })).toEqual(
    schemaFor(source, grant),
  );
  expect(session.engine).toHaveBeenCalledWith('/api/v2/meta/tables/table', 'actor-session');
  expect(fetch).toHaveBeenCalledWith(
    expect.any(URL),
    expect.objectContaining({ headers: { 'xc-token': 'synthetic-metadata-token' } }),
  );
  role = 'viewer';
  await expect(authority(source, 'owner', grant)).rejects.toMatchObject({ status: 403 });
  role = 'creator';
  await expect(
    authority(source, 'owner', grant, { id: 'outsider', token: 'other' }),
  ).rejects.toMatchObject({ status: 403 });
});
it.each(['LinkToAnotherRecord', 'Lookup', 'Attachment', 'JSON', 'Formula'])(
  'rejects implicit %s projection and records a safe schema change',
  async (uidt) => {
    metadata.columns = [{ id: 'name', column_name: 'name', title: 'Name', uidt }];
    await expect(authority(source, 'owner', grant)).rejects.toBeInstanceOf(FeedSchemaError);
  },
);
it('detects rename/deletion/type drift without rebinding by display-name coincidence', async () => {
  metadata.columns = [
    { id: 'different', column_name: 'name', title: 'Name', uidt: 'SingleLineText' },
  ];
  try {
    await authority(source, 'owner', grant);
    throw new Error('Expected schema error');
  } catch (e) {
    expect(e).toBeInstanceOf(FeedSchemaError);
    expect((e as FeedSchemaError).change.fields).toEqual(['name']);
    expect((e as FeedSchemaError).change.version).toMatch(/^[a-f0-9]{64}$/);
  }
  metadata.base_id = 'other-base';
  await expect(authority(source, 'owner', grant)).rejects.toMatchObject({ status: 403 });
});
it('allows administrator lifecycle checks after schema drift without exposing any row values', async () => {
  metadata.columns = [];
  await expect(
    authority(source, 'owner', grant, { id: 'owner', token: 'actor' }, false),
  ).resolves.toEqual(schemaFor(source, grant));
});
