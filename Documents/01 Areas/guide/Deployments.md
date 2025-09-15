# Deployments (Vercel)

This prototype ships its data with the app for reliable serverless deploys. Follow these steps for Vercel.

## Settings
- Framework: Nuxt.js
- Root Directory: `apps/prototype`
- Build Command: default (Nuxt) or `pnpm install && pnpm build`
- Output Directory: leave blank

## Data
- Data is bundled under `apps/prototype/data/` (schemas, mappings, incoming, generated).
- No `NUXT_DATA_DIR` required. The server auto‑detects this folder and, if needed, reads from Nitro server assets.

## Env Vars
- `NUXT_ADMIN_PASSWORD_HASH`: bcrypt hash (generate with `pnpm hash "YourPassword"`).
- `MC_VISIBLE` (optional): comma list of journey keys to show (e.g., `non-lux-lp-demo`).

## Health & Verification
- `GET /api/health` → `{ dataDir, manifestExists, journeyCount }`
- `GET /api/manifest` → returns journeys; `non-lux-lp-demo` is visible by default.
- Mission Control shows the visible journeys; Admin login reveals Diff/Export.

## Notes (Serverless)
- Diff/Export stream artifacts in the response; writes to disk may not persist on Vercel (read‑only FS). This is expected.
- To show only a specific journey temporarily, use `MC_VISIBLE` instead of editing the manifest.

