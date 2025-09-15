---
session_id: 006
date: 2025-09-10
facilitator: Assistant
participants: [Assistant, Tiernan (Nile)]
related_journeys: [non-lux-lp-demo]
related_files: [
  "scripts/import_xlsx.py",
  "scripts/mapping_wizard.py",
  "apps/prototype/data/mappings/non-lux-lp-demo.json",
  "apps/prototype/data/schemas/non-lux-lp-demo/schema.yaml",
  "apps/prototype/data/generated/importer-cli/non-lux-lp-demo/summary.json",
  "apps/prototype/pages/preview/[journey].vue",
  "apps/prototype/server/utils/schema-validator.ts",
  "apps/prototype/server/utils/data.ts",
  "apps/prototype/server/api/manifest.get.ts",
  "apps/prototype/pages/index.vue"
]
---

# Session Summary

Goal: Capture “internal only” fields from the spreadsheet and exclude them from the prototype UI; improve provenance on Mission Control cards. Outcome: Importer now detects internal items (via dedicated column or the Action column heuristics), schemas annotate `internal_only: true`, journey preview filters them out, and Mission Control shows the source spreadsheet name and sheet used.

## Changes Made

- Importer (Python):
  - Added support for `internal_only` flags from either a mapped internal column or the Action column (case-insensitive match for the word “internal”).
  - Summary now records `input_file` in `generated/importer-cli/<journey>/summary.json`.
- Mapping:
  - Updated `apps/prototype/data/mappings/non-lux-lp-demo.json` to include `columns.action: "Action"`.
- Schema validator (server):
  - Allowed optional boolean `internal_only` on each item.
- UI – Journey preview:
  - Filters out items where `internal_only: true` before visibility and validation logic.
- Manifest API + Mission Control UI:
  - Server reads importer summary to attach `source.file` and `source.sheet` per journey.
  - Dashboard card shows “Source: <file> — <sheet>”.
- Re-imported `non-lux-lp-demo` to apply flags and provenance.

## Decisions

- Exclude internal-only fields from the prototype UI, but keep them in schema and reports for audit.
- Display spreadsheet provenance on Mission Control to improve traceability and handover quality.
- Keep Diff/Export including internal fields for now; consider an “Internal” column/flag in a later pass.

## Verification

- Importer run updated schema and reports:
  - `items_written`: 788
  - `internal_only: true` items: 311
  - `summary.json` has `input_file: 20250828_draft-master-spreadsheet.xlsx`, `sheet: LP Proposal`.
- UI: `/preview/non-lux-lp-demo` no longer shows internal-only fields; navigation and validation operate on public items only.
- Mission Control: card shows “Source: 20250828_draft-master-spreadsheet.xlsx — LP Proposal”.

## Next Actions

- Component fidelity: Move from PoC components to KYCP-faithful components based on docs to be provided.
- Components page: Keep all components prototyped and visible under `/showcase`, mirroring KYCP props/events/validation.
- Gaps log: Document any platform gaps or behaviour mismatches early (ADR/notes).
- Optional: Add “Internal” flag/column to Diff/Export; add a serverless mode flag for write skips; minimal tests for importer/visibility.

## Risks / Mitigations

- Heuristic “internal” detection in Action column may have false positives/negatives → refine with a stricter list or explicit mapping as needed.
- Divergence from KYCP behaviour as components get richer → validate against shared docs; add showcase examples per state.

## Artefacts

- Schema: `apps/prototype/data/schemas/non-lux-lp-demo/schema.yaml`
- Reports: `apps/prototype/data/generated/importer-cli/non-lux-lp-demo/{summary.json, decisions.json}`
- Mapping: `apps/prototype/data/mappings/non-lux-lp-demo.json`
- UI: `/preview/non-lux-lp-demo`, `/showcase`

