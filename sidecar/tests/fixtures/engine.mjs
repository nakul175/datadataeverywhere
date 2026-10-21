import { createServer } from 'node:http';

// Disposable test double. It is NOT an installed NocoDB compatibility/permission test.
export function fixtureEngine() {
  const bases = [
    { id: 'b-fixture', title: 'Disposable qualification fixture' },
    { id: 'b-private', title: 'Private fixture' },
  ];
  const columns = [
    { id: 'id', title: 'Id', uidt: 'ID', pk: true, ai: true },
    { id: 'title', title: 'Title', uidt: 'SingleLineText' },
    { id: 'notes', title: 'Notes', uidt: 'LongText' },
    { id: 'formula', title: 'Calculated', uidt: 'Formula' },
  ];
  const tables = [
    {
      id: 't-fixture',
      base: 'b-fixture',
      title: 'Synthetic records',
      columns,
      rows: Array.from({ length: 257 }, (_, i) => ({
        Id: i + 1,
        Title: i === 200 ? 'Needle beyond page one' : `Fixture ${String(i).padStart(3, '0')}`,
        Notes: 'Synthetic local data',
      })),
    },
    { id: 't-private', base: 'b-private', title: 'Private synthetic table', columns, rows: [] },
  ];
  let serial = 300;
  return createServer(async (req, res) => {
    function send(body, status = 200) {
      res.writeHead(status, { 'content-type': 'application/json' });
      res.end(JSON.stringify(body));
    }
    try {
      const url = new URL(req.url, 'http://127.0.0.1');
      let raw = '';
      for await (const part of req) {
        raw += part;
        if (raw.length > 64000) return send({}, 413);
      }
      const body = raw ? JSON.parse(raw) : {};
      if (url.pathname === '/api/v1/health') return send({ message: 'OK' });
      if (url.pathname === '/api/v1/auth/user/signin')
        return ['owner@example.test', 'reader@example.test'].includes(body.email) &&
          body.password === 'local-fixture-only'
          ? send({
              token:
                body.email === 'owner@example.test'
                  ? 'fixture-owner-token'
                  : 'fixture-reader-token',
            })
          : send({}, 401);
      const owner = req.headers['xc-auth'] === 'fixture-owner-token',
        reader = req.headers['xc-auth'] === 'fixture-reader-token';
      if (!owner && !reader) return send({}, 401);
      if (url.pathname === '/api/v1/auth/user/me')
        return send({
          id: owner ? 'owner' : 'reader',
          email: owner ? 'owner@example.test' : 'reader@example.test',
          display_name: owner ? 'Fixture owner' : 'Fixture reader',
          roles: { [owner ? 'org_level_creator' : 'org_level_viewer']: true },
        });
      if (req.method !== 'GET' && !owner) return send({}, 403);
      if (url.pathname.replace(/\/$/, '') === '/api/v2/meta/bases') {
        if (req.method === 'POST') {
          const b = { id: `b${++serial}`, title: body.title };
          bases.push(b);
          return send(b);
        }
        return send({
          list: bases
            .filter((b) => owner || b.id === 'b-fixture')
            .map((b) => ({ ...b, sources: [{ password: 'fixture-only-never-real' }] })),
        });
      }
      const baseMatch = url.pathname.match(/^\/api\/v2\/meta\/bases\/([^/]+)\/tables$/);
      if (baseMatch) {
        if (!owner && baseMatch[1] !== 'b-fixture') return send({}, 403);
        if (req.method === 'POST') {
          const t = {
            id: `t${++serial}`,
            base: baseMatch[1],
            title: body.title,
            columns: body.columns.map((c, i) => ({ ...c, id: `col${i}` })),
            rows: [],
          };
          tables.push(t);
          return send({ id: t.id, title: t.title });
        }
        return send({
          list: tables
            .filter((t) => t.base === baseMatch[1])
            .map((t) => ({ id: t.id, title: t.title })),
        });
      }
      const meta = url.pathname.match(/^\/api\/v2\/meta\/tables\/([^/]+)$/),
        records = url.pathname.match(/^\/api\/v2\/tables\/([^/]+)\/records$/);
      const table = tables.find((t) => t.id === (meta || records)?.[1]);
      if (!table) return send({}, 404);
      if (!owner && table.base !== 'b-fixture') return send({}, 403);
      if (meta) return send({ columns: table.columns });
      if (req.method === 'POST') {
        const row = { Id: ++serial, ...body };
        table.rows.push(row);
        return send(row);
      }
      if (req.method === 'PATCH') {
        const row = table.rows.find((r) => r.Id === body.Id);
        if (!row) return send({}, 404);
        Object.assign(row, body);
        return send(row);
      }
      let selected = [...table.rows];
      const where = url.searchParams.get('where');
      if (where) {
        const m = where.match(/^\(([^,]+),like,%(.*)%\)$/);
        if (!m) return send({}, 400);
        selected = selected.filter((r) =>
          String(r[m[1]] || '').includes(m[2].replace(/\\_/g, '_')),
        );
      }
      const sort = url.searchParams.get('sort');
      if (sort)
        selected.sort((a, b) => {
          for (const term of sort.split(',')) {
            const key = term.replace(/^-/, '');
            const x = a[key],
              y = b[key];
            const diff =
              typeof x === 'number' && typeof y === 'number'
                ? x - y
                : String(x || '').localeCompare(String(y || ''));
            if (diff) return term.startsWith('-') ? -diff : diff;
          }
          return 0;
        });
      const offset = Number(url.searchParams.get('offset') || 0),
        limit = Number(url.searchParams.get('limit') || 25);
      const fields = url.searchParams.get('fields')?.split(',');
      const page = selected
        .slice(offset, offset + limit)
        .map((r) => (fields ? Object.fromEntries(fields.map((f) => [f, r[f] ?? null])) : r));
      send({
        list: page,
        pageInfo: { isLastPage: offset + limit >= selected.length, totalRows: selected.length },
      });
    } catch {
      send({}, 500);
    }
  });
}
