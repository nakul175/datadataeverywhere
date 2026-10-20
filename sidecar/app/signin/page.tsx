import { redirect } from 'next/navigation';
import { currentSession } from '@/lib/session';
import { HttpError } from '@/lib/errors';
import { Brand, Mascot } from '../brand';
import SignIn from './signin';
export const dynamic = 'force-dynamic';
export default async function SignInPage() {
  let authenticated = false;
  try {
    await currentSession();
    authenticated = true;
  } catch (e) {
    if (!(e instanceof HttpError && e.status === 401)) throw e;
  }
  if (authenticated) redirect('/');
  return (
    <main className="signin-page">
      <header>
        <Brand />
        <a
          className="subtle-link"
          href="https://app.sheethappensofficer.com"
          target="_blank"
          rel="noreferrer"
        >
          Meet the rest of Aplyd ↗
        </a>
      </header>
      <div className="signin-content">
        <section className="signin-story">
          <span className="eyebrow">A LITTLE ORDER. A LOT OF POSSIBILITIES.</span>
          <h1>
            Data, data everywhere.
            <br />
            <em>Finally, in one place.</em>
          </h1>
          <p>
            Bring your tables and questions together.
            <br />
            Less hunting. More knowing.
          </p>
          <Mascot className="signin-ghost" />
          <span className="ghost-caption">Holy sheet. That’s organised.</span>
        </section>
        <section className="signin-card">
          <span className="tiny-grid">▦</span>
          <h2>Good to have you back.</h2>
          <p>Your workspace is ready when you are.</p>
          <SignIn />
          <div className="login-note">
            One login. Your whole workspace.
            <small>Use your existing NocoDB account email and password.</small>
          </div>
        </section>
      </div>
      <footer>
        An Aplyd tool <span>·</span> Powered by NocoDB <span>·</span> Hosted on your team’s server
      </footer>
    </main>
  );
}
