import { redirect } from 'next/navigation';
import { identity, allowedTables, HttpError } from '@/lib/access';
import { currentSession } from '@/lib/session';
import Chat from './chat';
import Workspace from './workspace';
import { publicUrls } from '@/lib/public-urls';
export const dynamic = 'force-dynamic';
export default async function Page() {
  if (process.env.AUTH_MODE === 'nocodb') {
    let session;
    try {
      session = await currentSession();
    } catch (e) {
      if (e instanceof HttpError && e.status === 401) redirect('/signin');
      throw e;
    }
    return (
      <Workspace
        user={{ email: session.email, name: session.name }}
        nocodbUrl={publicUrls().nocodb}
        tasksUrl={publicUrls().tasks}
      />
    );
  }
  const user = await identity();
  const tables = await allowedTables(user);
  return <Chat user={user} tables={tables.map(({ id, name }) => ({ id, name }))} />;
}
