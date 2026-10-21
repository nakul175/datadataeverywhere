import { z } from 'zod';
import { createHash } from 'node:crypto';
export const id = z.string().regex(/^[a-zA-Z0-9_-]{1,100}$/);
const text = z.string().trim().min(1).max(120);
export const scopeSchema = z.discriminatedUnion('kind', [
  z.object({ kind: z.literal('all'), confirmed: z.literal(true) }).strict(),
  z
    .object({
      kind: z.literal('equals'),
      field: id,
      values: z.array(z.string().max(500).nullable()).min(1).max(100),
    })
    .strict(),
]);
export const grantSchema = z
  .object({
    source: id,
    fields: z.array(id).min(1).max(30),
    scope: scopeSchema,
    consumer: text,
    owner: id,
    expiresAt: z.string().datetime(),
  })
  .strict()
  .refine((v) => new Set(v.fields).size === v.fields.length, 'Duplicate fields');
export type Grant = z.infer<typeof grantSchema>;
export const sourceSchema = z
  .object({
    id,
    baseId: id,
    tableId: id,
    policyVersion: id,
    schema: id,
    view: id,
    key: id,
    delegation: z.literal('verified-full-base-admin-only'),
    viewDefinitionHash: z.string().regex(/^[a-f0-9]{64}$/),
    reviewRef: z.string().min(1).max(500),
    fields: z
      .array(z.object({ id, column: id, title: text, uidt: text, pgType: text }).strict())
      .min(1)
      .max(30),
  })
  .strict();
export type Source = z.infer<typeof sourceSchema>;
export type Field = Source['fields'][number];
export type Schema = { version: string; fields: Field[] };
export type RecordRow = { key: string; version: string; values: Record<string, string | null> };
export const hash = (v: string) => createHash('sha256').update(v).digest('hex');
export const canonical = (v: unknown): string => {
  if (Array.isArray(v)) return `[${v.map(canonical).join(',')}]`;
  if (v !== null && typeof v === 'object')
    return `{${Object.entries(v)
      .sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0))
      .map(([k, val]) => `${JSON.stringify(k)}:${canonical(val)}`)
      .join(',')}}`;
  return JSON.stringify(v);
};
export const schemaFor = (s: Source, g: Grant): Schema => {
  const fields = s.fields
    .filter((f) => g.fields.includes(f.id))
    .sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
  return { version: hash(canonical(fields)), fields };
};
export const LIMITS = {
  rows: 25000,
  bytes: 16_000_000,
  page: 100,
  snapshotMs: 86400000,
  feeds: 64,
  audit: 10000,
};
export const revocationNotice =
  'Stopping access prevents future reads. It cannot recall bytes already transmitted or guarantee erasure of exported copies. Requests admitted before the change may finish.';
