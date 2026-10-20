'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
export default function SignIn() {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();
  return (
    <form
      onSubmit={async (e) => {
        e.preventDefault();
        if (busy) return;
        setBusy(true);
        setError('');
        const data = new FormData(e.currentTarget);
        try {
          const res = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify({ email: data.get('email'), password: data.get('password') }),
          });
          const json = await res.json();
          if (!res.ok) throw new Error(json.error || 'Unable to sign in.');
          router.replace('/');
          router.refresh();
        } catch (err) {
          setError(err instanceof Error ? err.message : 'Unable to sign in.');
        } finally {
          setBusy(false);
        }
      }}
    >
      <label htmlFor="email">Email address</label>
      <input
        id="email"
        name="email"
        type="email"
        autoComplete="username"
        placeholder="Your NocoDB account email"
        maxLength={254}
        required
      />
      <label htmlFor="password">Password</label>
      <input
        id="password"
        name="password"
        type="password"
        autoComplete="current-password"
        placeholder="Your password"
        maxLength={256}
        required
      />
      {error && (
        <p role="alert" className="error">
          {error}
        </p>
      )}
      <button className="primary login-button" disabled={busy}>
        {busy ? 'Opening your workspace…' : 'Let’s make sense of it'} <span>↗</span>
      </button>
      <a className="account-help" href="/nocodb" target="_blank" rel="noreferrer">
        Need account help? Open NocoDB ↗
      </a>
    </form>
  );
}
