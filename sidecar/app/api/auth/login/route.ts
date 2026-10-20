import { cookies } from 'next/headers';
import { z } from 'zod';
import { engine, boundedBody, sameOrigin } from '@/lib/engine';
import { SESSION_COOKIE, cookieOptions } from '@/lib/session';
import { loginAdmission } from '@/lib/local-limits';
import { HttpError, errorResponse } from '@/lib/access';
export const runtime = 'nodejs';
export async function POST(req: Request) {
  try {
    sameOrigin(req);
    if (process.env.AUTH_MODE !== 'nocodb')
      throw new HttpError(404, 'Account sign-in is not enabled.');
    const parsed = z
      .object({ email: z.email().max(254), password: z.string().min(1).max(256) })
      .strict()
      .safeParse(await boundedBody(req));
    if (!parsed.success) throw new HttpError(400, 'Enter your email and password.');
    await loginAdmission(parsed.data.email);
    let result;
    try {
      result = await engine('/api/v1/auth/user/signin', undefined, 'POST', parsed.data);
    } catch (e) {
      if (e instanceof HttpError && [400, 401, 403].includes(e.status))
        throw new HttpError(401, 'Email or password was not accepted.');
      throw e;
    }
    if (typeof result.token !== 'string' || !result.token || result.token.length > 8192)
      throw new HttpError(502, 'Unexpected sign-in response.');
    // Validate the token with NocoDB; never trust a decoded token for identity or permissions.
    const user = await engine('/api/v1/auth/user/me', result.token);
    if (!user.id || !user.email || user.roles?.guest) throw new HttpError(401, 'Sign-in failed.');
    let maxAge = 28800;
    try {
      const exp = JSON.parse(Buffer.from(result.token.split('.')[1], 'base64url').toString()).exp;
      if (Number.isFinite(exp))
        maxAge = Math.max(1, Math.min(maxAge, Math.floor(exp - Date.now() / 1000)));
    } catch {
      /* Cookie expiry alone grants no authority. */
    }
    (await cookies()).set(SESSION_COOKIE, result.token, { ...cookieOptions, maxAge });
    return Response.json({ ok: true }, { headers: { 'Cache-Control': 'no-store' } });
  } catch (e) {
    return errorResponse(e);
  }
}
