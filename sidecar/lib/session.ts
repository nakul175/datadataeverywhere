import 'server-only';
import { cookies } from 'next/headers';
import { engine } from './engine';
import { HttpError } from './errors';
export const SESSION_COOKIE = 'dde_session';
export const cookieOptions = {
  httpOnly: true,
  secure: process.env.NODE_ENV === 'production',
  sameSite: 'lax' as const,
  path: '/',
};
export async function currentSession() {
  const token = (await cookies()).get(SESSION_COOKIE)?.value;
  if (!token || token.length > 8192) throw new HttpError(401, 'Please sign in.');
  const user = await engine('/api/v1/auth/user/me', token);
  if (typeof user.id !== 'string' || typeof user.email !== 'string' || user.roles?.guest)
    throw new HttpError(401, 'Please sign in again.');
  return {
    token,
    id: user.id as string,
    email: (user.email as string).toLowerCase(),
    name: typeof user.display_name === 'string' ? user.display_name : user.email.split('@')[0],
  };
}
