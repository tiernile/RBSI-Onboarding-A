# Implementation Plan — Refining Workflow

## Phase 1 — Hardening (now)

- Column alignment by cell reference (done).
- DATA TYPE/FIELD TYPE normalization; non‑input detection (done).
- INTERNAL/SYSTEM handling: exclude from UI/schema (done).
- Lookup Values header detection + fallbacks + final placeholder (done).
- Case‑insensitive value matching in preview; AND/OR normalization (done).
- Complex groups: render with repeater; exclude internal children (done).

## Phase 2 — Conditionality Linter + Reports

- Parser: export normalized condition strings and AST.
- Lints:
  - Unresolved left‑hand keys.
  - Option value not found in controller’s options (with alias map pass).
  - Suspicious numeric tokens (e.g., 81.0) flagged.
  - Dependency cycle detection.
- Reports:
  - `conditions.json/csv`: key → normalized expressions + lint results.
  - Coverage: controller → option → affected fields.
  - Order: suggested controller‑before‑dependent listing.
- API: `/api/conditions-report/:journey` returns JSON; add `?format=html` for a quick HTML table.

## Handover — Relevant Files & Entry Points

- Importer: `apps/prototype/scripts/import_non_lux_1_1.py`
- Mapping: `apps/prototype/data/mappings/non-lux-1.1.json`
- Schema out: `apps/prototype/data/schemas/<journey>/schema-kycp.yaml`
- Preview (KYCP): `apps/prototype/pages/preview-kycp/[journey].vue`
- Conditions report API: `apps/prototype/server/api/conditions-report/[journey].get.ts`
- Diff/export APIs: `apps/prototype/server/api/diff/[journey].get.ts`, `.../export/[journey].get.ts`
- Utilities: `apps/prototype/server/utils/{data,validation,schema-validator}.ts`
- Docs: `Documents/01 Areas/refining-workflow/{PRD.md,ADR-0001-conditionality-and-ingestion.md,Implementation-Plan.md}`
- Session context: `Documents/01 Areas/session-context/session-context-013.md`

## Phase 3 — Scenario Tests + CI

- Seed fixtures: UK path, non‑UK+Yes, non‑UK+No.
- Assertions: field visibility and options presence.
- CI step: run importer + lints + scenarios; fail on red lints or scenario diffs.

## Phase 4 — UX Instrumentation

- Preview dev mode: toggle to show “why visible/hidden” inline (controller/value pairs).
- Group titles: friendly names for groups; pull from nearest Title row if available.

## Operating Model

- Mapping as code; minimal overrides with rationale in session notes.
- Prefer fixing source (labels/options/conditions) then removing overrides.
- Strict mode import option for sign‑off builds.
