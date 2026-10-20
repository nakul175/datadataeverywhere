# Unified workspace release

The production DataDataEverywhere interface uses NocoDB accounts and a private server-side API client. The NocoDB session token is in a Secure, HttpOnly, SameSite=Lax, host-only cookie. Passwords are passed to the local NocoDB authentication API and are not persisted by this interface. Each request validates the session with NocoDB and uses that person's token for data access and writes. Native NocoDB roles continue to apply.

The interface supports bases (shown as workspaces), tables, paginated records (50 per page), search/sort within a page, simple record creation/editing, and a read-only AI panel using the active table. Advanced field types, imports, relations, team administration and views remain available in the native NocoDB interface. The native interface has its own cookie; it may ask you to sign in separately. Documents and Asana-style synchronization have not been implemented.

## Existing server installation

Run `scripts/deploy-unified-user.sh` as the existing `deploy` account after extracting a release into `/home/deploy/datadataeverywhere/releases/`. It installs a systemd user service and enables lingering so it starts at boot. It binds only to 127.0.0.1:3301. Existing root-owned engine containers, PostgreSQL data and SheetHappensOfficer remain in place. The older AI sidecar stays on 127.0.0.1:3300 for rollback.

Files owned by deploy:

- `/home/deploy/datadataeverywhere/current`: active release symlink.
- `/home/deploy/datadataeverywhere/shared/runtime.env`: provider settings; mode 0600.
- `/home/deploy/datadataeverywhere/shared/access.json`: approved AI table/field and email grants; mode 0600.
- `/home/deploy/datadataeverywhere/shared/data/budget.sqlite`: persistent atomic rate/budget accounting; mode 0600.
- `/home/deploy/.config/systemd/user/datadataeverywhere.service`: user service.

Commands:

```sh
systemctl --user status datadataeverywhere
journalctl --user -u datadataeverywhere -n 60 --no-pager
nano /home/deploy/datadataeverywhere/shared/runtime.env
systemctl --user restart datadataeverywhere
```

AI starts disabled. Add `OPENAI_API_KEY` with your actual key to runtime.env, or set `AI_PROVIDER=anthropic` and `ANTHROPIC_API_KEY` and the desired `ANTHROPIC_MODEL`. Do not paste keys into chat, source files, commits or shell command arguments. runtime.env is a systemd EnvironmentFile, not the root Docker .env. Changing the root Docker key does not configure this new service.

Use access.json to grant *specific account email addresses* approved table IDs and column titles. Its format is the same as the existing bundle config/access.json, except email keys are now supported. Empty arrays mean no AI data sharing. The operator must enter actual table IDs and exact field titles; the UI never silently approves an entire database. After editing the file, refresh the table. Both an approved table grant and that user's NocoDB permissions are necessary.

SQLite is used for this native service's budget gate: 6 admitted requests/minute/user, one in-flight/user, eight in-flight globally, 500,000 conservative daily token units/user and 5,000,000 globally. Reservations are not refunded after completion or failure. Requests time out after 90 seconds; leases expire after 180 seconds. Atomic transactions protect concurrent admission and accounting survives restarts. Token units conservatively include UTF-8 bytes for input/context plus output; these are a budget guard rather than a provider invoice calculation. The original Docker sidecar retains its Redis budget implementation.

## Validation and limits

Automated tests cover session rejection, per-user upstream tokens, cross-origin writes, forbidden table access, disallowed field writes, upstream projection, provider context bounds and persistent budget concurrency. Browser CRUD testing uses a disposable local API fixture, not production customer data. Live account sign-in was verified in the browser using the account owner’s already-entered credentials; no administrator password was reset, read or copied. Production record writes were not tested.

Changing a NocoDB password/account policy, signing out of other NocoDB sessions or changing roles is controlled by NocoDB. This app clears its local cookie on sign-out; it does not promise to revoke every existing NocoDB token. Sessions require a fresh sign-in when the upstream access token expires; refresh-token rotation is not implemented.

Back up the deploy-owned shared directory and user service along with the root-owned PostgreSQL/NocoDB data. For an online SQLite snapshot, use SQLite's backup API (or stop this service before copying budget.sqlite and its WAL); do not copy only a live main database file. Provider credentials and all access files require encrypted, access-controlled backups.

## Release verification

The unified interface is deployed at https://datadataeverywhere.aplyd.org. Caddy routes the interface to loopback 3301 and native NocoDB to loopback 8080. Application sessions replace the legacy dashboard Basic Auth prompt. Existing SheetHappensOfficer routes are preserved.

For rollback, restore the Caddy configuration backup created by scripts/switch-unified-proxy.py, validate it, then reload Caddy. The helper prints the actual backup path when run. Keep host-specific backup records in your private operations notes. To roll back a later interface release, atomically repoint the current symlink to the previous release and restart the user service.

Verified: live HTTPS, sign-in using the account owner’s existing NocoDB credentials, public branding assets, rejection of forged sessions and cross-origin login requests, and continued availability of native NocoDB and SheetHappensOfficer. No production test rows or accounts were created. Disposable local browser tests covered sign-in, record creation and editing.

The installed engine exposes account authentication under /api/v1/auth/user/; data/schema APIs use v2 endpoints. Authentication routes were verified against the live engine. AI provider credentials and approved-field grants remain operator configuration.
