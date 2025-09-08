# Repository Guidelines

## Project Structure & Module Organization

- `apps/prototype/`: Nuxt 3 app (pages, components, composables, server API).
- `data/`: source data used by the app.
  - `schemas/`: YAML schemas (e.g., `manifest.yaml`, `<journey>/schema.yaml`).
  - `mappings/`, `generated/`: mappings and exported artifacts.
- `Documents/`: product/architecture notes and ADRs.

## Build, Test, and Development Commands

From `apps/prototype/`:

- `pnpm install`: install dependencies.
- `pnpm dev`: run local dev server with HMR.
- `pnpm build`: create production build.
- `pnpm start`: start built server.
- `pnpm hash "YourPassword"`: print bcrypt hash for admin login.

Env setup: copy `.env.example` to `.env.development`; set `NUXT_ADMIN_PASSWORD_HASH` and (if needed) `NUXT_DATA_DIR` to the absolute path of this repo’s `data/`.

## Coding Style & Naming Conventions

- Vue 3 SFC with `<script setup lang="ts">`; TypeScript preferred.
- Indentation: 2 spaces; single quotes in TS; minimal semicolons.
- Component files: PascalCase (e.g., `components/nile/ErrorSummary.vue`).
- Pages: use Nuxt conventions (e.g., `pages/preview/[journey].vue`).
- API routes: `server/api/<name>.(get|post).ts` (e.g., `server/api/schema/[journey].get.ts`).

## Testing Guidelines

- No formal test suite yet. Validate changes by:
  - Running `pnpm dev` and testing flows: `/`, `/showcase`, `/preview/:journey`.
  - Hitting APIs: `/api/manifest`, `/api/schema/:journey`, `/api/export/:journey`.
- If adding tests, prefer Vitest + Nuxt Test Utils; name files `*.spec.ts` alongside code.

## Commit & Pull Request Guidelines

- Commits: small, scoped, imperative. Prefer Conventional Commits (e.g., `feat(apps/prototype): add login dialog`).
- PRs: describe intent, list key changes, include screenshots for UI, link issues, and note any data/schema impacts.
- Keep changes atomic (UI, server API, or data) and reference affected paths (e.g., `data/schemas/...`).

## Security & Configuration Tips

- Never commit secrets; use `.env.development` locally. The admin cookie is HTTP-only.
- Generate password hashes via `pnpm hash` and set `NUXT_ADMIN_PASSWORD_HASH`.
- Avoid PII in `data/`; exports under `data/generated/` are for local inspection only.
