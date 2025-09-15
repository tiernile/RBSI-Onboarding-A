---
session_id: 013
date: 2025-09-15
facilitator: Assistant
participants: [Assistant, Tiernan (Nile)]
related_journeys: [non-lux-1-1]
related_files: [
  "apps/prototype/data/incoming/20250911_master_non-lux.xlsx",
  "apps/prototype/data/mappings/non-lux-1.1.json",
  "apps/prototype/data/schemas/non-lux-1-1/schema-kycp.yaml",
  "apps/prototype/scripts/import_non_lux_1_1.py"
]
---

# Session Summary

Goal: Create an AS-IS KYCP-format schema from the 20250911 master Non-Lux LP workbook, including complex group markings, smart defaults, and initial section groupings provided by the client. Add a new Mission Control card for `non-lux-1-1` and prepare for later analysis/rewording.

## Decisions (Smart Defaults)

- Filters: include only `PROGRAMME = "Account is for - a Fund (CIS) - Non Luxembourg"` and `ENTITY = "Limited Partnership"`.
- Exclusions: any row where `Action` contains "(internal)" (case-insensitive), or `INTERNAL = Y`, or `SYSTEM = Y`, or `FIELD NAME` contains "Internal Analysis".
- Identity: `id = KEYNAME` (hard-fail on duplicates). `label = FIELD NAME`. `help = DESCRIPTION` (optional).
- KYCP types/controls:
  - Lookup → dropdown only (Yes/No also dropdown), options sourced from "Lookup Values" by `LOOKUP TYPE`. If type exists but has no values, keep dropdown with placeholder (no seeded demo values).
  - Free Text → `freeText` (textarea).
  - Number → `integer` by default; treat as `decimal` if `FIELD LENGTH` suggests decimals (e.g., contains a dot). Decimal default scale = 2.
  - Date → `date` (DD/MM/YYYY).
- Required: from `MANDATORY = Y`.
- Visibility: parse `VISIBILITY CONDITION/GROUP NAME` for simple AND conditions with `==`/`!=` (normalize `=`→`==`, `<>`→`!=`). Non-expression tokens ignored.
- Complex: rows with non-empty `COMPLEX` are marked as members of that group. We record `groups` metadata at the root (group key, title field from `COMPLEX IDENTIFIER`, children keys). For now, fields are emitted flat in `fields[]` (no UI repeater yet) to keep `/preview-kycp` stable.
- Sections: apply the provided grouping list where labels match; otherwise `_section = "General"`. `_stage` preserved from `STAGE` for reference.
- Audit trail: `scriptId = ROW:<REF>|KEY:<KEYNAME>` on fields.

## Open Items

- Complex repeater UI in `/preview-kycp`: next step is to render `groups` with `KycpRepeater` using child field schemas.
- External lists (Country, Industry) referenced but not enumerated → placeholders only for now.
- Decimal inference may be refined if a column explicitly encodes precision/scale.

## Output Targets

- Mapping: `apps/prototype/data/mappings/non-lux-1.1.json`.
- Importer: `apps/prototype/scripts/import_non_lux_1_1.py` (no external deps).
- Schema: `apps/prototype/data/schemas/non-lux-1-1/schema-kycp.yaml`.
- Manifest: add Mission Control card for `non-lux-1.1` (variant KYCP).

---

## Progress Update (2025-09-15)

### Implemented

- Journey slug fixed: changed from `non-lux-1.1` → `non-lux-1-1` (server enforces slug rules). Updated manifest and file paths accordingly.
- Importer hardened:
  - YAML writer now uses block scalars for multi-line text to avoid parsing errors (previous 404 was due to a multiline quoted string).
  - Closed-zip usage bug removed; all reads happen inside the zipfile context.
  - Fallback lookups supported via mapping (`fallback_lookups`).
  - Lookup Values header detection fixed (uses LOOKUP TYPE/LOOKUP VALUE positions).
  - Robust Yes/No detection (handles variants like "Yes/ No", "Yes-No", spaces/hyphens).
  - LP Proposal table alignment fixed: rows built using Excel cell references (column letters) to keep values aligned when cells are empty.
  - Misaligned lookup rescue: if LOOKUP is blank but DATA TYPE equals a known lookup type (present in Lookup Values or fallbacks), treat as lookup and load options; if still no items, add fallback option "Lookup items not provided".
  - Non-input detection expanded: Title/Divider in either DATA TYPE or FIELD TYPE → `style: divider`; Statement/Note/Information in either → `style: statement`.
  - Non-input rows with blank KEYNAME included by synthesising stable keys (e.g., `title_<slug>`); duplicate checking moved after synthesis.
  - Internal marking by label: rows with `FIELD NAME` containing "OBT TO COMPLETE" are marked `internal: true` (hidden from the user experience but retained in schema for audit).
- Mapping updates (`non-lux-1.1.json`):
  - Added fallbacks for: Yes/No, Bank Account Jurisdiction, Fund Size, Country, "Application Options- Funds/ FRE", jurisdiction-specific brands (Brands Jersey/Guernsey/Gibraltar/Isle of Man/United Kingdom), Currencycrm (GBP/USD/EUR/CHF/JPY), Industry description incl SIC code (starter list), and Risk Score (Low/Medium/High).
  - Added section mapping based on client-provided groupings; default `_section` remains "General" where no match.
  - Exclusions applied: `Action` contains “(internal)”, `INTERNAL=Y`, `SYSTEM=Y`, and labels containing “Internal Analysis”.
- Schema generated: `apps/prototype/data/schemas/non-lux-1-1/schema-kycp.yaml` (KYCP format). Includes `_section` and `_stage` and `groups` metadata for complex sets.
- Mission Control: added card for `non-lux-1-1` (variant KYCP) → `/preview-kycp/non-lux-1-1`.
- Preview UX: updated KYCP preview to single-page layout (no stepper). Sections render as dividers only; validation checks all visible fields on submit.

### Verified fixes

- `/api/health` confirms `dataDir` is live filesystem under `apps/prototype/data`.
- `/api/schema/non-lux-1-1` returns schema (YAML parses cleanly).
- "Account jurisdiction" shows seeded options (Jersey, Guernsey, IOM, Gibraltar, UK).
- "Which option best describes your application?" now shows the two application options (fallback list).
- "Where is the 3rd party administrator domiciled?" shows a seeded country list.
- "Under which brand would you like to open this account?" now shows jurisdiction-specific brand choices when visible.
- "Intermediary Details" (Title) now respects conditionality (visibility set to match 3rd party administrator path).
- "Does the business involve:" (GENBusinessType) correctly renders as a dropdown from Lookup Values (Undertake Business), not a free text input.
 - Fields labelled with "OBT TO COMPLETE" no longer render in the UI (marked internal), but remain in the schema artifacts.

### Complex groups wiring (preview)

- Implemented generic repeater rendering in `/preview-kycp/[journey].vue`:
  - Uses `schema.groups` to render `KycpRepeater` blocks per section.
  - Child fields render inside the repeater form with the same input components and visibility logic (row-level values can satisfy conditions; falls back to global form data when needed).
  - Grouped child fields are removed from the main (non-group) listing to avoid duplication.

### Import run summary (latest)

- Included: 690 items
- Excluded: 98 items (`action internal`: 96; `missing id/label`: 2)
- Unresolved lookups: 1 (GENStatutoryProvision) — add to Lookup Values or provide fallback to resolve.

### Current Decisions (reconfirmed)

- AS-IS content: use `FIELD NAME` verbatim; ignore rewordings.
- KYCP-only components; Lookup = dropdown (including Yes/No).
- Numbers: default integer; decimal if field length suggests decimals (scale 2).
- Grouping: all content on one page; sections used as visual dividers only.
- Complex groups: detected via `COMPLEX`; recorded in schema `groups` metadata (key, `titleField`, child keys). Rendering as flat fields for now; UI repeater wiring to follow.

### Root-cause summaries

- 400 invalid journey: dot in slug (`non-lux-1.1`) → fixed to hyphens (`non-lux-1-1`).
- 404 schema not found: YAML parse failure due to multiline quoted string → switched to block scalars in importer.

### Open Items / Next Steps

- Seed additional fallback lookups (prioritise: Status, Applicant Role, Industry, extended Country list) or provide complete lists in "Lookup Values".
- Wire `KycpRepeater` to render complex groups using `groups` metadata.
- Optional: enhance section mapping/ordering once reviewed.
- Hold content analysis/rewording until design guidance is provided.
