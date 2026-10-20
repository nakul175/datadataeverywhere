import { describe, expect, it, vi } from 'vitest';
vi.mock('server-only', () => ({}));
import { recordQuery } from '../lib/table-query';
const columns = [
  { id: 'id', title: 'Id', type: 'ID', primary: true, editable: false, required: true },
  {
    id: 'name',
    title: 'Name',
    type: 'SingleLineText',
    primary: false,
    editable: true,
    required: false,
  },
  {
    id: 'secret',
    title: 'Nested',
    type: 'Links',
    primary: false,
    editable: false,
    required: false,
  },
];
describe('Typed full-table query contract', () => {
  it('preserves the original default page request', () => {
    const result = recordQuery(new URLSearchParams('action=records&tableId=t1&offset=50'), columns);
    expect(result.query.toString()).toBe('limit=50&offset=50');
    expect(result.scope).toBe('page');
  });
  it('builds a bounded remote filter and stable sort across pages', () => {
    const p = new URLSearchParams({
      scope: 'table',
      query: 'outside page one',
      fieldId: 'name',
      sortId: 'name',
      direction: 'desc',
      offset: '100',
    });
    const result = recordQuery(p, columns);
    expect(result.query.get('where')).toBe('(Name,like,%outside page one%)');
    expect(result.query.get('sort')).toBe('-Name,Id');
    expect(result.query.get('offset')).toBe('100');
    expect(result.query.get('limit')).toBe('50');
  });
  it.each(['(Name,neq,x)', 'x~or', 'x%y', 'x,y', 'x\\y', 'x\ny'])(
    'refuses grammar/wildcard injection %s',
    (query) => {
      expect(() =>
        recordQuery(new URLSearchParams({ scope: 'table', fieldId: 'name', query }), columns),
      ).toThrow();
    },
  );
  it('does not treat an underscore as a search wildcard', () => {
    expect(
      recordQuery(
        new URLSearchParams({ scope: 'table', fieldId: 'name', query: 'a_b' }),
        columns,
      ).query.get('where'),
    ).toBe('(Name,like,%a\\_b%)');
  });
  it.each([
    'where=(Name,eq,x)',
    'scope=page&query=x',
    'scope=table&sortId=secret',
    'scope=table&query=x&fieldId=secret',
    'offset=-1',
    'offset=1.5',
    'scope=table&direction=sideways',
    'scope=table&scope=page',
  ])('rejects unsupported or ambiguous input %s', (input) =>
    expect(() => recordQuery(new URLSearchParams(input), columns)).toThrow(),
  );
  it('refuses a global query without an unambiguous stable key', () => {
    expect(() => recordQuery(new URLSearchParams('scope=table'), columns.slice(1))).toThrow();
  });
});
