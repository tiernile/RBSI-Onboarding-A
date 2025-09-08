# API Contracts – Auth & Mission Control

## POST /api/auth/login

- Purpose: authenticate admin with a single password.
- Request: `Content-Type: application/json` body `{ password: string }`.
- Response (200): `{ ok: true }`, sets `admin=true` HTTP‑only cookie (SameSite=Strict, TTL ~1h).
- Response (200, error): `{ ok: false, error: string }`.
- Env: requires `NUXT_ADMIN_PASSWORD_HASH` (bcrypt). 5-try lockout per IP for ~15 minutes.

## GET /api/manifest

- Reads `data/schemas/manifest.yaml`, merges env overrides, returns journeys for Mission Control.
- Response: `{ isAdmin: boolean, active: Journey[] }`.
- Overrides: `MC_VISIBLE=key1,key2` (visible whitelist), `MC_STATUS={"key":"alpha|beta|live"}`.
- Sorting: by `display.group` then `display.order`.

## GET /api/schema/:journey

- Reads `/data/schemas/:journey/schema.yaml` and returns parsed JSON.
- Used by the preview route to render schema‑driven screens.

## (Planned) POST /api/admin/config

- Purpose: persist global overrides in dev to `/data/admin/config.json`.
- Guarded by admin cookie; not used in hosted environment.
