# Importer CLI – PRD

## Problem
We need a repeatable way to turn client spreadsheets into our schema, with smart defaults and an audit trail. Current scripts work but lack a simple CLI, robust error messages, and predictable outputs.

## Goals
- One command converts an XLSX + mapping JSON into `data/schemas/<journey>/schema.yaml`.
- Generate audit artifacts (summary, decisions) under `data/generated/importer-cli/`.
- Enforce schema validity; fail fast with actionable errors.
- Keep smart defaults (operator/type normalisation, yes/no fallbacks) and traceability (`meta.source_row_ref`).

## Non‑Goals
- Full ETL for production; only what’s needed for rapid prototyping with auditability.

## Success Criteria
- CLI runs with 1–2 required flags; helpful `--help`.
- Schema validates with Zod and renders in `/preview/<journey>` without manual edits.
- Reports list unmapped/assumed fields and missing lookups.
- Wizard supports interactive header detection, column mapping, optional filters, lookups sheet selection, and field ordering; saves mapping JSON and can run importer.

## Users
- Designers/analysts importing spreadsheets; engineers reviewing diffs/exports.

## Risks & Mitigations
- Sheet format variance → flags for `--sheet`/`--lookups-sheet`; tolerant header matching.
- Missing lookups → default sensible options and log for client follow‑up.
- Ambiguous conditions → accept simple expressions; flag complex ones for manual review.
