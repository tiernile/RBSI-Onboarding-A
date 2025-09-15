# Handover — KYCP Components Phase

Date: 2025-01-11
Status: Components visually matched to KYCP platform; build errors resolved; showcase demonstrates accurate styling.

## Overview

We've achieved visual parity with the KYCP platform. Components now exactly match KYCP's appearance based on screenshots. All build errors from deleted radio components have been resolved. The showcase page at `/kycp-components` demonstrates realistic KYCP forms with proper styling. Components are pure UI with no business logic, ready for schema-driven rendering.

## What's Done

- Visual Updates (Session 009)
  - KycpDivider: Added em dash prefix, matched KYCP colors and spacing
  - KycpStatement: Removed all styling, now plain text only
  - KycpFieldWrapper: Added description prop with HTML/bullet list support
  - Form inputs: Updated padding, fonts, borders to match KYCP exactly
  - Design tokens: Comprehensive KYCP variables in app.vue
- Build Fixes
  - Removed all KycpRadio references (component deleted per KYCP spec)
  - Fixed template syntax errors in showcase
  - Updated component mappings in useSchemaForm.ts
- Previous Work (Sessions 006-008)
  - Importer detects internal‑only fields
  - Schema validator and preview handle internal flags
  - KYCP-aligned component library created
  - Strict platform limits enforced

## Where Things Live

- Components: `apps/prototype/components/kycp/{fields,structure,complex}/`
- Showcase: `apps/prototype/pages/showcase.vue`
- Types: `apps/prototype/types/kycp.ts`
- Importer: `scripts/import_xlsx.py`, mapping `apps/prototype/data/mappings/*.json`
- Schema/data: `apps/prototype/data/schemas/*`, `.../generated/importer-cli/*`
- Docs: `Documents/01 Areas/kycp-components/*`, session logs `Documents/01 Areas/session-context/session-context-00{6,7}.md`

## How to Run

- Dev server: `cd apps/prototype && pnpm install && pnpm dev` → `/`, `/about`, `/showcase`, `/preview/non-lux-lp-demo`.
- Re‑import (with Action→internal detection):
  - `python3 scripts/import_xlsx.py --mapping apps/prototype/data/mappings/non-lux-lp-demo.json --input apps/prototype/data/incoming/20250828_draft-master-spreadsheet.xlsx --sheet "LP Proposal" --lookups-sheet "Lookup Values" --journey-key non-lux-lp-demo`
- Admin (optional): set `NUXT_ADMIN_PASSWORD_HASH` via `pnpm hash "YourPassword"`.

## Verified

- Build completes successfully with no errors
- Components visually match KYCP platform screenshots exactly
- `/kycp-components` page shows realistic KYCP form example
- All KycpRadio references removed (radio buttons don't exist in KYCP)
- Statement component renders as plain text without decoration
- Field descriptions support HTML and bullet lists

## Next Actions (Proposed Order)

1) Importer v2
- Emit `style` and `type`; enrich `validation`; generate lookup codes (`{ value,label }`); compile simple AND eq/neq visibility into structured rules; optional `groups` in mapping.

2) Adapter & Validator Composables
- Build YAML → `ComponentNode[]` adapter using `apps/prototype/types/kycp.ts`.
- Centralise validators for integer/decimal/date; reuse in components.

3) Preview Wiring
- Render `/preview/:journey` via adapter and new components (flagged rollout; keep current path as fallback initially).

4) Showcase + E2E
- Add PEP conditional example; expand states.
- Create small demo XLSX + mapping; add pnpm scripts; set up headless checks for visibility/validation/groups.

## Open Questions / Inputs

- Lookup codes: do we have Code/Label columns in lookups sheet consistently? If not, OK to slugify labels into codes?
- Status rights: any initial per‑status rules to include now (e.g., read‑only after Onboarded)?
- Complex groups: confirm initial groups beyond ID Docs, Shareholders (e.g., Directors, Addresses?).

## Risks / Notes

- Spreadsheet variance → Wizard + tolerant headers + decisions log.
- Visibility strings may exceed eq/neq AND → retain original parser as fallback.
- Decimal/date edge cases → centralised helpers; unit tests.

## References

- Session context: `Documents/01 Areas/session-context/session-context-006.md`, `.../session-context-007.md`
- Spec & plans: `Documents/01 Areas/kycp-components/{Spec.md,Implementation-Plan.md,E2E-Implementation-Plan.md}`
- Current manifest: `apps/prototype/data/schemas/manifest.yaml`
- Key APIs: `/api/health`, `/api/manifest`, `/api/schema/:journey`, `/api/diff/:journey`, `/api/export/:journey`

