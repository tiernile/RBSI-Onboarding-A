# Handover – Non-Lux LP v2.0 Prototype

_Last updated: 2025-09-17_

## Summary
- **Journey clone:** `non-lux-lp-2-0/schema-kycp.yaml` mirrors the v1.1 KYCP schema (357 public fields) with a new `accordions` config and `future` metadata to carry Nile copy proposals.
- **Mission Control:** `manifest.yaml` exposes the new journey as “Non‑Lux LP — v2.0 (Future Draft)” pointing to `/preview-kycp/non-lux-lp-2-0`.
- **Copy mapping:** `apps/prototype/data/generated/non-lux-lp-2-0-copy-map.json` links every row in `20250916-rewritten-draft.xlsx` to the schema field/option, noting whether it was a direct match, alias, or still outstanding.
- **UI:** `/preview-kycp/[journey].vue` renders the proposed copy (labels + helpers) while Explain Visibility shows AS‑IS vs proposed wording, lookup updates, and change provenance. Accordions render conditionally with a placeholder message when empty.

## Progress Snapshot
- 357 fields available in the prototype (no AS‑IS content removed).
- 99 workbook rows mapped + applied to fields/options (`future` metadata or option labels).
- 25 workbook rows remain unmatched (see “Outstanding Copy” table below); schema still renders them with AS‑IS text.
- Select component now respects placeholders, so conditional sections only appear after the user picks an option.

## Key Files
- `apps/prototype/data/schemas/non-lux-lp-2-0/schema-kycp.yaml`
- `apps/prototype/data/generated/non-lux-lp-2-0-copy-map.json`
- `apps/prototype/pages/preview-kycp/[journey].vue`
- `Documents/01 Areas/guide/Future-Prototype-Variant-Workflow.md`
- `Documents/01 Areas/guide/Future-Prototype-Outstanding-Copy.md`

## Decisions
- Keep AS‑IS journey untouched; all future copy lives in the duplicated `non-lux-lp-2-0` schema.
- Record every copy proposal (even if the field is unchanged) in the JSON copy map for traceability.
- Proposed copy is rendered directly in the UI; explain-mode highlights the AS‑IS wording for comparison.
- Option label updates are flagged in explain-mode so reviewers can validate lookup rewrites.

## Outstanding Copy (needs alias or schema update)
See `Documents/01 Areas/guide/Future-Prototype-Outstanding-Copy.md` for the full list. Highlights:
- 3rd-party captive option (application type) and Money Service/Crypto prompts (journey + key principals).
- Key-principal repeater fields: role, new/existing, name, entity type, controller status, address, contact details, tax info.
- High-risk jurisdiction prompt and industry/SIC descriptor.
- Annual transaction question in Banking Requirements.

## Recommended Next Steps
1. **Alias the outstanding rows** – map workbook labels to repeater child keys/options or introduce new schema entries where required.
2. **Re-run copy application** – update the copy map → rerun the metadata script so all fields/options carry their proposed text.
3. **QA conditionality** – once aliases are in place, retest accordion visibility (esp. key principals + intermediary paths) with `/preview-kycp/non-lux-lp-2-0?explain=1`.
4. **Importer alignment (optional)** – if long-term plan is to re-run the importer, bake alias mappings into the import script to regenerate `schema-kycp.yaml` automatically.

## Verification Checklist
- `pnpm --dir apps/prototype build` succeeds (tested 2025-09-17).
- `/preview-kycp/non-lux-1-1` (AS‑IS) unaffected.
- `/preview-kycp/non-lux-lp-2-0?explain=1` shows proposed copy + lookup updates + change provenance.

## Contacts
- Prototype tooling: Assistant
- Product / copy decisions: Tiernan (Nile)

