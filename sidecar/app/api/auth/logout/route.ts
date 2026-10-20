import { cookies } from 'next/headers';
import { SESSION_COOKIE, cookieOptions } from '@/lib/session';
import { sameOrigin } from '@/lib/engine';
import { errorResponse } from '@/lib/access';
export async function POST(req: Request) {
  try { sameOrigin(req); (await cookies()).set(SESSION_COOKIE, '', { ...cookieOptions, maxAge: 0 }); return Response.json({ ok: true }); }
  catch (e) { return errorResponse(e); }
}
