import { resolve } from 'node:path';
import type { NextConfig } from 'next';

const config: NextConfig = {
  output: 'standalone',
  poweredByHeader: false,
  // Keep the existing Docker/systemd artifact layout when root development tooling has its own lockfile.
  outputFileTracingRoot: resolve(process.cwd()),
};
export default config;
