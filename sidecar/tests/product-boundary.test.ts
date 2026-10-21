import { readFile } from 'node:fs/promises';
import { describe, expect, it } from 'vitest';

const memberSurfaces = [
  'app/page.tsx',
  'app/workspace.tsx',
  'app/chat.tsx',
  'app/signin/page.tsx',
  'app/signin/signin.tsx',
];

describe('DataDataEverywhere product boundary', () => {
  it('does not expose engine branding, admin links or licensed workspace creation', async () => {
    const source = (
      await Promise.all(
        memberSurfaces.map((path) => readFile(new URL(`../${path}`, import.meta.url), 'utf8')),
      )
    ).join('\n');
    expect(source).not.toMatch(/NocoDB|Powered by|Advanced spreadsheet|New workspace|\/nocodb/);
  });
});
