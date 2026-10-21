import { identity, allowedTables, errorResponse } from '@/lib/access';
import { localStoreHealth } from '@/lib/local-limits';
import { redis } from '@/lib/redis';
import { aiReadiness } from '@/lib/provider-config';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

// Authenticated dependency check. Does not call an AI provider or return configuration/secrets.
export async function GET() {
  try {
    const user = await identity();
    const results = await Promise.allSettled([
      fetch(new URL('/api/v1/health', process.env.NOCODB_URL || 'http://127.0.0.1:8080'), {
        cache: 'no-store',
        redirect: 'error',
        signal: AbortSignal.timeout(3000),
      }).then((r) => {
        if (!r.ok) throw new Error('EngineUnavailable');
      }),
      process.env.SQLITE_BUDGET_FILE
        ? localStoreHealth()
        : redis().then((r) => r.withAbortSignal(AbortSignal.timeout(3000)).ping()),
      allowedTables(user),
    ]);
    const checks = Object.fromEntries(
      ['engine', 'budget', 'accessPolicy'].map((key, i) => [
        key,
        results[i].status === 'fulfilled',
      ]),
    );
    const ready = Object.values(checks).every(Boolean);
    const configured = aiReadiness().ready;
    return Response.json(
      {
        status: ready ? 'ready' : 'degraded',
        checks,
        ai: { configured, providerConnectionVerified: false },
      },
      { status: ready ? 200 : 503, headers: { 'Cache-Control': 'no-store' } },
    );
  } catch (e) {
    return errorResponse(e);
  }
}
