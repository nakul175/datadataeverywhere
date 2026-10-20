import 'server-only';
import { engine, engineId } from './engine';
import { HttpError } from './errors';
export type Column = { id: string; title: string; type: string; primary: boolean; editable: boolean; required: boolean };
const editable = new Set(['SingleLineText', 'LongText', 'Email', 'PhoneNumber', 'URL', 'Number', 'Decimal', 'Currency', 'Percent', 'Checkbox', 'Date', 'DateTime', 'Duration', 'Year']);
export async function tableSchemaFor(id: string, token: string): Promise<Column[]> {
  const table = await engine(`/api/v2/meta/tables/${engineId(id)}`, token);
  if (!Array.isArray(table.columns)) throw new HttpError(502, 'Unexpected table schema.');
  return table.columns.filter((c: Record<string, unknown>) => typeof c.title === 'string' && !c.system).map((c: Record<string, unknown>) => ({
    id: String(c.id), title: String(c.title), type: String(c.uidt || c.dt || 'Text'), primary: Boolean(c.pk),
    editable: editable.has(String(c.uidt)) && !c.pk && !c.ai && !c.au && !c.system,
    required: Boolean(c.rqd && !c.cdf),
  }));
}
export function checkedValues(columns: Column[], input: unknown) {
  if (!input || typeof input !== 'object' || Array.isArray(input)) throw new HttpError(400, 'Invalid record.');
  const entries = Object.entries(input);
  if (entries.length > 100 || !entries.length) throw new HttpError(400, 'Enter at least one field.');
  const result: Record<string, string | number | boolean | null> = Object.create(null);
  for (const [key, value] of entries) {
    const column = columns.find(c => c.title === key && c.editable);
    if (!column) throw new HttpError(400, 'This field must be edited using the advanced spreadsheet.');
    if (value !== null && typeof value !== 'string' && typeof value !== 'number' && typeof value !== 'boolean') throw new HttpError(400, 'Only simple field values are supported here.');
    if (typeof value === 'string' && value.length > 10000 || typeof value === 'number' && !Number.isFinite(value)) throw new HttpError(400, 'Invalid field value.');
    result[key] = value;
  }
  return result;
}
