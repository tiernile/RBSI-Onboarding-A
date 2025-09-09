# Importer CLI (Area Overview)

Plain-English: one command takes a client spreadsheet and a small mapping JSON and generates a journey schema we can render immediately. It applies smart defaults, logs assumptions, and writes an audit trail.

## Inputs
- XLSX: `data/incoming/YYYYMMDD_<name>.xlsx`
- Mapping JSON: `data/mappings/<journey>.json` (columns, filters, normalisation, lookups)

## Outputs
- Schema: `data/schemas/<journey>/schema.yaml`
- Reports: `data/generated/importer-cli/<journey>/{summary.json, decisions.json}`
 - Alignment: `Documents/01 Areas/as-is-analysis/alignment-report.md` (for as‑is slice)

## Usage (proposed)
```
python scripts/import_xlsx.py \
  --mapping data/mappings/non-lux-lp-demo.json \
  --input data/incoming/20250828_client.xlsx \
  --sheet "LP Proposal" \
  --lookups-sheet "Lookup Values" \
  --out data/schemas/non-lux-lp-demo/schema.yaml \
  --journey-key non-lux-lp-demo
```

See PRD and ADR for scope and decisions. Implementation Plan tracks tasks.

## Example Run (non-lux-lp-demo)

- Command:
  - `python scripts/import_xlsx.py --mapping data/mappings/non-lux-lp-demo.json --input data/incoming/20250828_draft-master-spreadsheet.xlsx --sheet "LP Proposal" --lookups-sheet "Lookup Values" --out data/schemas/non-lux-lp-demo/schema.yaml --journey-key non-lux-lp-demo`
- Outputs:
  - `data/schemas/non-lux-lp-demo/schema.yaml` (788 items)
  - `data/generated/importer-cli/non-lux-lp-demo/summary.json` (header_row_used=1, conditions_transformed=377, lookup_defaults_used=282)
  - `data/generated/importer-cli/non-lux-lp-demo/decisions.json` (per-field inferences)

Notes:
- Filters were applied after resolving the correct header row automatically.
- Two invalid regex patterns were dropped and noted in the summary.
- Data types were normalised to supported set: enum (399), string (352), number (20), date (17).
 - Mandatory normalization treats `A/a/Required/Mandatory` as true in addition to `Y/Yes/1/True`.
