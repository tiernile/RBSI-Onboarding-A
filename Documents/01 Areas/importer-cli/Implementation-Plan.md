# Importer CLI – Implementation Plan

## Milestones
- M1: CLI scaffold with argparse, `--mapping`, `--input`, `--sheet`, `--lookups-sheet`, `--out`, `--journey-key`.
- M2: Mapping validation + header resolution; smart defaults for operators/types; `meta.source_row_ref`.
- M3: Reports: `summary.json` and `decisions.json` under `data/generated/importer-cli/<journey>/`.
- M4: Schema validation (Zod on server path) and preview smoke test instructions.
- M5: Docs + examples; add small pytest suite.

## Tasks
- [x] Scaffold CLI entry `scripts/import_xlsx.py` with argparse + logging
- [x] Implement header normalisation and required column checks
- [x] Apply mapping JSON (operators, types, lookups) with fallbacks
- [x] Emit `schema.yaml` and write reports (summary/decisions)
- [ ] Verify schema via app (`/preview/<journey>`); fix gaps
- [ ] Add minimal tests and update guide docs

## Owners
- Engineering: Assistant (implementation)
- Product/Design: Tiernan (mapping defaults, lookup confirmations)

## Dependencies
- Python: `pandas`, `pyyaml` (prefer stdlib/installed stack; add `openpyxl` if needed)
