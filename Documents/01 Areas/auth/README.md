# Auth – Mission Control (MVP)

Purpose: provide a simple, credible admin gate for Mission Control to toggle global visibility/status of journeys. This is for prototype access control only (no PII; simple roles).

## Roles

- Viewer: default; sees only journeys with `display.visible == true`.
- Admin: after login, sees all journeys and gains controls to toggle visibility/status/variant.

## Flow

- Login button opens a modal on `/`.
- POST `/api/auth/login` with `{ password }`.
- On success, sets `admin=true` HTTP‑only cookie with short TTL; UI shows Admin badge and controls.

## Env Vars (Nuxt)

- Admin (required): `NUXT_ADMIN_PASSWORD_HASH=<bcrypt-hash>`.
- Data directory (optional): `NUXT_DATA_DIR=/absolute/path/to/repo/data`.

Place envs in `apps/prototype/.env.development` for dev, or `apps/prototype/.env` for build/start.
Generate a hash locally with: `pnpm install && pnpm hash "YourPassword"`.

## Endpoints

- `POST /api/auth/login`
  - Body: `{ password: string }`.
  - Returns: `{ ok: true }` and sets `admin=true` cookie; or `{ ok: false, error }`.
  - Errors: 400/401 for invalid, guidance when only plaintext fallback is active.

- `GET /api/manifest`
  - Returns `{ isAdmin: boolean, active: Journey[] }`.
  - Applies `MC_VISIBLE` and `MC_STATUS` overrides; sorts by `display.group` then `order`.

## Security Notes

- No PII; cookie is HTTP‑only, SameSite=Strict, short TTL.
- Bcrypt hash required before hosting; remove plaintext fallback.
- Add basic lockout/rate‑limiting (planned) to protect against brute force.

## Roadmap

- Replace plaintext fallback with bcrypt verification (`NUXT_ADMIN_PASSWORD_HASH`).
- Optional: add `POST /api/admin/config` to persist dev overrides into `/data/admin/config.json`.
- Optional: rate‑limit login and add lockout after 5 failures.
