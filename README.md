# Nile RBSI Onboarding – Prototyping Repo

This repository turns client spreadsheets into clickable onboarding journeys using a schema‑driven Nuxt (Vue 3) prototype. It is not production code, but it is structured, auditable, and fast to iterate.

## Start Here
- System Overview (plain English): `Documents/01 Areas/guide/System-Overview.md`
- Area Workflow (PRD/ADR/Plan/Session): `Documents/01 Areas/guide/Area-Workflow.md`
- QuickStart (for demoing): `Documents/01 Areas/guide/QuickStart.md`
- Operations (how to update journeys): `Documents/01 Areas/guide/Operations.md`
- Spreadsheet to Prototype Workflow: `Documents/01 Areas/guide/Spreadsheet-to-Prototype-Workflow.md`
- Deployments (Vercel): `Documents/01 Areas/guide/Deployments.md`
- Tone of Voice Guidelines: `Documents/01 Areas/tone-of-voice/README.md`
- Contributor guide: `AGENTS.md`

## Run the Prototype
- App: `apps/prototype/`
  - Dev: `pnpm install && pnpm dev`
  - Build/Start: `pnpm build && pnpm start`
- Data lives under `apps/prototype/data/` (schemas, mappings, generated reports).

## Spreadsheet → Schema → UI
- Drop XLSX into `apps/prototype/data/incoming/`.
- Use mapping JSON in `apps/prototype/data/mappings/` to normalise columns/types.
- Generate/maintain `apps/prototype/data/schemas/<journey>/schema.yaml` with `meta.source_row_ref` for traceability.
- Mission Control reads `apps/prototype/data/schemas/manifest.yaml`; `/preview/<journey>` renders the UI.
- Admin can open Diff/Export for review artifacts under `apps/prototype/data/generated/`.

## Current Areas
- PoC Workflow: `Documents/01 Areas/poc-workflow/`
- Importer CLI (in progress): `Documents/01 Areas/importer-cli/`

Questions or issues: see the guide docs above or ask the Nile team.
