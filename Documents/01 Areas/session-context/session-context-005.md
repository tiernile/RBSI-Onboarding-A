---
session_id: 005
date: 2025-09-09
facilitator: Assistant
participants: [Assistant, Tiernan (Nile)]
related_journeys: [non-lux-lp-demo]
related_files: [
  "apps/prototype/server/utils/data.ts",
  "apps/prototype/server/api/manifest.get.ts",
  "apps/prototype/server/api/schema/[journey].get.ts",
  "apps/prototype/server/api/export/[journey].get.ts",
  "apps/prototype/server/api/diff/[journey].get.ts",
  "apps/prototype/server/api/health.get.ts",
  "apps/prototype/nuxt.config.ts",
  "apps/prototype/data/schemas/manifest.yaml",
  "apps/prototype/data/schemas/non-lux-lp-demo/schema.yaml"
]
---

# Session Summary

Goal: Make deploys reliable on Vercel and expose only the latest journey. Outcome: Data is bundled with the app; server reads schemas via server assets fallback; health endpoint added; only `non-lux-lp-demo` is visible by default; admin auth configured.

## Changes Made

- Moved `data/` → `apps/prototype/data/` and bundled via Nitro server assets.
- Added safe data loader (`server/utils/data.ts`) with filesystem + server-assets fallback.
- Patched API routes to use the loader (manifest/schema/diff/export) and to no-op writes on read-only FS.
- Added `/api/health` for quick diagnostics (dataDir, manifestExists, journeyCount).
- Updated manifest: `non-lux-lp-demo` visible, `zelda` hidden.

## Decisions

- Simplest deploy path: ship data within the app; avoid runtime absolute paths.
- Use `MC_VISIBLE` only if an env override is needed; otherwise rely on manifest.
- Keep admin behind `NUXT_ADMIN_PASSWORD_HASH` only (no plain fallback in prod).

## Verification

- Deployed app: `/api/manifest` returns active with `non-lux-lp-demo`.
- `/api/health` shows `manifestExists: true` and journeyCount > 0.
- Admin login works with bcrypt hash; badge shown on Mission Control.

## Next Actions

- Add a serverless flag to skip disk writes for Diff/Export and always stream artifacts.
- Create a concise Vercel deployment guide and link it from README.
- Optional: pnpm scripts for importer/wizard; light tests for visibility/parser.

## Risks / Mitigations

- Serverless FS writes may fail → stream responses; document behavior.
- Future sheet variations → mapping wizard + importer reports.

