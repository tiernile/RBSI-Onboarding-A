# E2E Implementation Plan — Spreadsheet → Prototype

Objective: achieve authentic, repeatable end‑to‑end generation of a working prototype from a spreadsheet — including importer, schema evolution, adapter mapping to KYCP‑aligned models, component rendering, and automated checks.

## Outcomes
- One component library renders any journey from a canonical schema (no per‑journey code).
- Importer v2 produces all data the components need (style, type, validation, lookups with codes, structured visibility, internal flags, optional groups/rights).
- Automated E2E verifies: import → app boots → journey renders → visibility/validation behave → repeaters work → data serialises in KYCP‑compatible shapes.

## Scope
- Sources: XLSX main sheet (+ optional Lookup Values), mapping JSON (+ optional groups/status_rights overrides).
- Targets: YAML schema, importer reports, in‑app preview `/preview/:journey`, showcase `/showcase`.
- Journeys: start with `non-lux-lp-demo`; include example complex groups (ID docs, shareholders).

## Milestones (Week‑level)
1) Importer v2 and Schema Extensions
2) Adapter + Validators + Rights/Visibility composables
3) Component Library (leafs, structure, repeater) + Showcase
4) E2E Harness + Reference Data + CI script

## Work Breakdown

1) Importer v2 (scripts/import_xlsx.py, mapping_wizard)
- Style & Type: emit `style` ('field' | 'statement' | 'divider' | 'button') and `type` ('string' | 'integer' | 'decimal' | 'date' | 'lookup' | 'freeText'). Infer or map explicitly.
- Lookups with codes: if lookup sheet has Code/Label columns, emit `{ value, label }`; else slugify label to a stable `value`.
- Validation envelope: emit `validation` with defaults per type (string 1024; freeText 8192; integer max 2147483647; decimal precision 18/scale 2; dateFormat 'DD/MM/YYYY'). Allow overrides via mapping.
- Visibility compiler: parse ANDed eq/neq expressions into `visibility: [{ entity, targetKeys, allConditionsMustMatch, conditions[] }]`. Keep original string for fallback.
- Internal flags: keep `internal_only: true` detection (incl. Action column heuristic).
- Groups: accept optional `groups` in mapping (e.g., IDDocs/shareholders) listing child field keys; emit `ComplexGroup` stubs.
- Status rights: if `status_rights.json` present, apply per field/group; record decisions.

2) Schema Validator & Adapter (apps/prototype/server/utils/schema-validator.ts, new adapter util)
- Extend validator to accept optional: `style`, `type`, `validation`, `statusRights`, `visibility` (structured), `options: {value,label}[]`, `internal_only`.
- Adapter: YAML → `ComponentNode[]` (apps/prototype/types/kycp.ts). Map controls/types, convert options, visibility, internal flags, and assemble declared groups.
- Composables: `resolveRight`, `isVisible`, `useValidation` (type‑aware limits and messages).

3) Component Library & Showcase (apps/prototype/components/*, pages/showcase.vue)
- Leafs: StringField, FreeTextArea, IntegerField, DecimalField, DateField, LookupField — Vue 3 `<script setup>` with `modelValue` and validators; emit canonical values (codes/dates/numbers); respect rights.
- Structure: StatementBlock, DividerLine, ActionButton (emit `trigger` with `scriptId`).
- ComplexGroupRepeater: add/remove rows, nested children, rights/visibility at group+child levels.
- Showcase: examples for each component — editable/readOnly/hidden, invalid values, max lengths, decimal rounding, date format; complex groups for ID Docs and Shareholders.

4) E2E Harness & Scripts
- Test data: curate a minimal XLSX with:
  - PEP example (conditional freeText)
  - Lookup with codes (e.g., Country)
  - Decimal and Integer fields (limits)
  - Date field (DD/MM/YYYY)
  - Complex groups: `IDDocs`, `Shareholders`
- Scripts:
  - `pnpm import:demo` → run importer for the demo mapping
  - `pnpm e2e:dev` → start app and run headless checks (Nuxt Test Utils + Playwright or minimal fetch + DOM assertions)
- E2E checks:
  - Health endpoints up; manifest lists journey with `source.file/sheet`
  - Journey renders; internal fields suppressed
  - Visibility: changing PEP to YES reveals details field; to NO hides it and clears error state
  - Validation: integer rejects non‑digits and > 2147483647; decimal clamps to 2 dp; date enforces DD/MM/YYYY with leap‑year validation
  - Lookup stores codes; restoring a code reselects the option
  - Complex groups: add/remove ID Doc rows; data serialises as array under `IDDocs`

## Acceptance Criteria
- Importer emits enriched schema with style/type/validation/options(codes)/visibility(structured)/internal/groups; decisions log explains derivations.
- Adapter renders journeys solely from schema; no per‑journey code paths required.
- Components enforce KYCP limits; rights/visibility respected; complex groups functional.
- Showcase demonstrates all behaviours; `/preview/:journey` passes interactive checks.
- E2E script runs locally to completion and provides a concise report.

## Risks & Mitigations
- Spreadsheet variance → mapping wizard + tolerant headers + decisions log; fallback to labels→codes slugification.
- Partial visibility strings → retain original and fall back to current parser where compiler cannot translate.
- Decimal/Date edge cases → centralised validators with unit tests; shared helpers in composables.

## Next Actions
1) Implement Importer v2 (lookups with codes, structured visibility, style/type, validation defaults)
2) Extend schema validator and build YAML → ComponentNode adapter
3) Implement leaf components + validators; add ComplexGroupRepeater
4) Expand showcase; create E2E demo XLSX + mapping; add pnpm scripts and E2E harness

