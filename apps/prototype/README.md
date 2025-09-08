# RBSI Prototype App (Nuxt 3)

## Run Locally

1. Copy `.env.example` to `.env.development` and adjust values as needed.
2. From this folder:
   - Dev: `pnpm install && pnpm dev`
   - Build: `pnpm build` and `pnpm start`

## Env Vars (Nuxt)

- `NUXT_ADMIN_PASSWORD_HASH` – bcrypt hash for admin password (required for admin login).
- `NUXT_DATA_DIR` – absolute path to the repo `data/` folder if auto-detect fails.
- `MC_VISIBLE`, `MC_STATUS` – Mission Control visibility/status overrides.

### Generate a hash

- From this folder: `pnpm install` then `pnpm hash "YourPassword"`
- Copy the printed hash into `.env.development` as `NUXT_ADMIN_PASSWORD_HASH=...`

## API

- `GET /api/manifest` – reads `data/schemas/manifest.yaml`, applies overrides, returns cards; includes `isAdmin`.
- `GET /api/schema/:journey` – reads `data/schemas/:journey/schema.yaml` and returns JSON.
- `POST /api/auth/login` – accepts `{ password }`, sets `admin=true` cookie on success.

## Notes

- No PII in prototype or telemetry; admin cookie is HTTP-only.
- Schema-driven screens under `/preview/:journey`; Mission Control at `/`.
