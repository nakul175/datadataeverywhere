import { redirect } from 'next/navigation';
import { currentSession } from '@/lib/session';
import { HttpError } from '@/lib/errors';
import Feeds from './panel';
export const dynamic = 'force-dynamic';
export default async function Page() {
  try {
    await currentSession();
  } catch (e) {
    if (e instanceof HttpError && e.status === 401) redirect('/signin');
    throw e;
  }
  return <Feeds />;
}
