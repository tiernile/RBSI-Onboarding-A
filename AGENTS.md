# Repository Guidelines

## Project Structure & Module Organization

- `apps/prototype/`: Nuxt 3 app (pages, components, composables, server API).
- `apps/prototype/data/`: source data used by the app (bundled for deploy).
  - `schemas/`: YAML schemas (e.g., `manifest.yaml`, `<journey>/schema.yaml`).
  - `mappings/`, `generated/`, `incoming/`: mappings, generated reports, input files.
- `Documents/`: product/architecture notes and ADRs.

## Build, Test, and Development Commands

From `apps/prototype/`:

- `pnpm install`: install dependencies
- `pnpm dev`: run local dev server with HMR
- `pnpm build`: create production build
- `pnpm start`: start built server
- `pnpm hash "YourPassword"`: print bcrypt hash for admin login
- `pnpm scenarios`: run scenario validation for critical paths
- `pnpm fields`: analyze field organization and grouping

### Import and Analysis Commands

- `python3 scripts/import_non_lux_1_1.py`: Import current v1.1 journey (AS-IS)
- `python3 scripts/import_non_lux_2_2.py`: Import v2.2 with Paul's structure
- `python3 scripts/analyze_fields.mjs non-lux-1-1`: Field analysis

### Debug URLs (Development)

- Mission Control: `http://localhost:3000`
- Journey with Debug: `http://localhost:3000/preview-kycp/[journey]?explain=1`
- Conditions Report: `http://localhost:3000/api/conditions-report/[journey]?format=html`

Env setup: copy `.env.example` to `.env.development`; set `NUXT_ADMIN_PASSWORD_HASH` (use `pnpm hash "password"` to generate). In Vercel, data is bundled under `apps/prototype/data/` and auto-detected; set `NUXT_DATA_DIR` only if hosting data elsewhere.

**Current Journeys**:
- `non-lux-1-1`: AS-IS implementation with current features
- `non-lux-lp-2-2`: Paul's structural optimizations with field grouping

**For Complete System Understanding**: See `/Documents/01 Areas/guide/System-Overview.md`

## Coding Style & Naming Conventions

- Vue 3 SFC with `<script setup lang="ts">`; TypeScript preferred.
- Indentation: 2 spaces; single quotes in TS; minimal semicolons.
- Component files: PascalCase (e.g., `components/nile/ErrorSummary.vue`).
- Pages: use Nuxt conventions (e.g., `pages/preview/[journey].vue`).
- API routes: `server/api/<name>.(get|post).ts` (e.g., `server/api/schema/[journey].get.ts`).

## Testing Guidelines

- **Manual Testing with Debug Tools**: Validate changes by:
  - Running `pnpm dev` and testing flows: `/`, `/preview-kycp/:journey`
  - **Essential**: Use Explain Visibility (`?explain=1`) for conditional logic debugging
  - **Critical**: Run Conditions Report for comprehensive validation
  - Testing APIs: `/api/manifest`, `/api/schema/:journey`, `/api/conditions-report/:journey`
- **Scenario Validation**: Run `pnpm scenarios` for critical path testing
- **Field Analysis**: Run `pnpm fields` for field organization review
- If adding tests, prefer Vitest + Nuxt Test Utils; name files `*.spec.ts` alongside code

## Commit & Pull Request Guidelines

- Commits: small, scoped, imperative. Prefer Conventional Commits (e.g., `feat(apps/prototype): add login dialog`).
- PRs: describe intent, list key changes, include screenshots for UI, link issues, and note any data/schema impacts.
- Keep changes atomic (UI, server API, or data) and reference affected paths (e.g., `data/schemas/...`).

## Security & Configuration Tips

- Never commit secrets; use `.env.development` locally. The admin cookie is HTTP-only.
- Generate password hashes via `pnpm hash` and set `NUXT_ADMIN_PASSWORD_HASH`.
- Avoid PII in `data/`; exports under `data/generated/` are for local inspection only.
