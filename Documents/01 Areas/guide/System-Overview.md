# System Overview (Plain English)

This prototype turns client spreadsheets into clickable journeys using smart defaults and an auditable workflow. It is not production code, but it is structured, repeatable, and explainable.

## What It Does
- Renders journeys from a schema (a readable list of questions, rules, and options).
- Applies visibility and validation rules so screens adapt as you answer.
- Generates review artifacts (HTML diff and CSV export) with references back to the source spreadsheet.

## How It Works (End‑to‑End)
1) Input: Drop the latest XLSX into `data/incoming/` and/or edit a schema in `data/schemas/<journey>/schema.yaml`.
2) Mapping: `data/mappings/*.json` defines how spreadsheet columns map to schema fields and normalises types/operators.
3) Schema: The canonical definition lives under `data/schemas/<journey>/schema.yaml` and includes `meta.source_row_ref` for traceability.
4) App: The Nuxt app (`apps/prototype/`) reads the schema and renders components (text, select, radio, textarea) with grouping by `section`.
5) Review: Mission Control lists journeys from `data/schemas/manifest.yaml`; admin can open Diff/Export to produce audit artifacts.

## Smart Defaults
- Sheet names, lookups, and operators follow the mapping JSON; missing lookups fall back to simple options (e.g., Yes/No) and are flagged for review.
- Controls are inferred from type/lookup (e.g., enum → select/radio); unknown controls render as text with a visible warning.
- Visibility rules accept simple expressions like `KEY == "Yes"` and `A && (B != "UK")`; unsupported patterns fail safe (field remains hidden).

## Day‑to‑Day Workflow
- Place XLSX in `data/incoming/YYYYMMDD_<name>.xlsx`.
- Update/add `data/mappings/<journey>.json` as needed.
- Generate or edit `data/schemas/<journey>/schema.yaml` (ensure `meta.source_row_ref`).
- Add journey entry to `data/schemas/manifest.yaml` (key, name, version, display).
- Run from `apps/prototype/`: `pnpm dev`; open `/preview/<journey>`.
- As admin, open Diff/Export from Mission Control for review packs.

## Auditability (What We Keep)
- Source references: `meta.source_row_ref` (e.g., `ROW:123|KEY:GENFundSize`).
- Diff HTML: `data/generated/diffs/<journey>/<timestamp>.html`.
- CSV export: `data/generated/exports/<journey>/<timestamp>.csv`.
- (Optional) Snapshots per version for before/after comparisons.

## Where Things Live
- App: `apps/prototype/`
- Schemas: `data/schemas/<journey>/schema.yaml`
- Manifest: `data/schemas/manifest.yaml`
- Mappings: `data/mappings/*.json`
- Incoming files: `data/incoming/`
- Generated artifacts: `data/generated/*`

See also: QuickStart, Operations, Visibility Rules, and FAQ in this folder for step‑by‑step usage.
