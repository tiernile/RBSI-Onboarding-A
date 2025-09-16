# Operations Guide (Plain English)

This guide explains how the team updates the prototype with new/changed questions from a spreadsheet, and how to generate the audit trail.

## 1) Place the Spreadsheet

- Save the latest file to `data/incoming/` using `YYYYMMDD_<name>.xlsx`.
- No personal data in the spreadsheet — catalogue of questions only.

## 2) Create/Update a Mapping (columns → schema)

- Create `data/mappings/<shortname>.json` with:
  - `sheet`: the tab name (e.g., `LP Proposal`).
  - `filters`: column filters (e.g., Programme = Non‑Lux, Entity = Limited Partnership).
  - `columns`: which spreadsheet columns map to which schema fields (e.g., KEYNAME → id, FIELD NAME → label).
  - `normalization`: how to standardise types and operators (e.g., `Lookup` → `enum`, `=` → `==`, `<>` → `!=`).
  - `lookups`: code lists (e.g., Yes/No; Fund Size ranges).

Tip: See `data/mappings/non-lux-lp-demo.json` as a starter.

## 3) Run Importer (KYCP)

For Non‑Lux v1.1:

```
cd apps/prototype
python3 scripts/import_non_lux_1_1.py
```

Outputs:
- Schema: `apps/prototype/data/schemas/non-lux-1-1/schema-kycp.yaml`
- Console: include/exclude summary and unresolved lookups

## 4) Draft or Update the Schema

- Add or edit `data/schemas/<journey-key>/schema.yaml`.
- Keep it human‑readable: quote labels with `:` and any values with spaces.
- Include `meta.source_row_ref` so we can trace each field back to the spreadsheet row (e.g., `ROW:123|KEY:GENFundSize`).
- Group fields using `section` (e.g., `B2 - Bank Relationship`) and set `visibility` rules using simple expressions (e.g., `GENFundClosed == "Yes"`).

Tip: See `data/schemas/non-lux-lp-demo/schema.yaml` for examples.

## 5) Register the Journey

- Add an entry in `data/schemas/manifest.yaml` with:
  - `key`, `name`, `version`, `variant`, `owner` (quoted), and `display { group, order, visible, status }`.
- This makes it appear on Mission Control.

## 6) Run & Review

- From `apps/prototype`:
  - Dev: `pnpm install && pnpm dev` (use `.env.development` or `.env`).
  - Build/Start: `pnpm build && pnpm start` (use `.env`).
- Open the journey from Mission Control and review the screens.

## 7) Generate the Audit Trail & Reports

- As admin on Mission Control, use the links on the card:
  - View Diff → creates/opens `/data/generated/diffs/<journey>/<timestamp>.html`.
  - Export CSV → creates/downloads `/data/generated/exports/<journey>/<timestamp>.csv`.
  - Conditions Report → opens `/api/conditions-report/<journey>?format=html` with lints for conditionality.
- Include these links in PRs and playbacks.

## 8) Keep the Docs Updated

- Record material decisions as ADRs in `Documents/01 Areas/poc-workflow/`.
- Update the session context log with progress and next actions.
- Avoid PII in repo; keep references to source spreadsheet rows only.

## Troubleshooting

- Manifest/schema errors on load:
  - Quote labels with `:` and owners with `@` in YAML.
  - Ensure env files live in `apps/prototype/` and restart.
- Admin login not working:
  - Use `.env.development` (dev) or `.env` (start) with `NUXT_ADMIN_PASSWORD_PLAIN`.
  - For hosting, switch to `NUXT_ADMIN_PASSWORD_HASH` (bcrypt) and remove the plain fallback.

## Extras

- Explain visibility: use the checkbox in KYCP preview or append `?explain=1` to the URL.
- Scenario checks: from `apps/prototype`, run `pnpm scenarios` to assert critical visibility paths.
