import 'server-only';
import type { Column } from './workspace';
import { HttpError } from './errors';

const textTypes = new Set(['SingleLineText', 'LongText', 'Email', 'PhoneNumber', 'URL']);
const safeName = /^[\p{L}\p{N}_][\p{L}\p{N} _-]{0,79}$/u;

// A deliberately small typed contract. Never accept raw NocoDB where/sort syntax.
export function recordQuery(params: URLSearchParams, columns: Column[]) {
  const allowed = new Set([
    'action',
    'tableId',
    'offset',
    'scope',
    'query',
    'fieldId',
    'sortId',
    'direction',
  ]);
  for (const key of params.keys())
    if (!allowed.has(key) || params.getAll(key).length !== 1)
      throw new HttpError(400, 'Unsupported or repeated query parameter.');
  const offset = Number(params.get('offset') || 0);
  if (!Number.isSafeInteger(offset) || offset < 0 || offset > 10000000)
    throw new HttpError(400, 'Invalid page.');
  const scope = params.get('scope') || 'page';
  if (!['page', 'table'].includes(scope)) throw new HttpError(400, 'Invalid query scope.');
  const query = new URLSearchParams({ limit: '50', offset: String(offset) });
  if (scope === 'page') {
    for (const key of ['query', 'fieldId', 'sortId', 'direction'])
      if (params.has(key)) throw new HttpError(400, 'Table query requires explicit table scope.');
    return { query, scope, offset };
  }
  const primary = columns.filter((c) => c.primary);
  if (primary.length !== 1 || !safeName.test(primary[0].title))
    throw new HttpError(400, 'Full-table queries need a single supported primary key.');
  const value = params.get('query') || '';
  if (value.length > 200 || !/^[\p{L}\p{N} .@_+-]*$/u.test(value))
    throw new HttpError(
      400,
      'Search supports up to 200 letters, numbers, spaces, dots, @, +, - and _.',
    );
  function column(id: string | null) {
    const c = columns.find((c) => c.id === id);
    if (!c || !safeName.test(c.title)) throw new HttpError(400, 'Unsupported query field.');
    return c;
  }
  if (value) {
    const c = column(params.get('fieldId'));
    if (!textTypes.has(c.type)) throw new HttpError(400, 'Search needs a supported text field.');
    // Escape SQL LIKE wildcard characters; grammar delimiters are refused above.
    query.set('where', `(${c.title},like,%${value.replace(/_/g, '\\_')}%)`);
  }
  const sort = params.get('sortId') ? column(params.get('sortId')) : primary[0];
  const direction = params.get('direction') || 'asc';
  if (!['asc', 'desc'].includes(direction)) throw new HttpError(400, 'Invalid sort direction.');
  if (!sort.primary && !sort.editable)
    throw new HttpError(400, 'Sort needs a supported simple field.');
  query.set(
    'sort',
    `${direction === 'desc' ? '-' : ''}${sort.title}${sort.primary ? '' : ',' + primary[0].title}`,
  );
  return { query, scope, offset };
}
