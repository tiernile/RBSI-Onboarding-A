# PRD — Refining Workflow: Ingestion → Mapping → Schema → Preview

## Purpose

Establish a robust, auditable pipeline that produces KYCP‑compatible schemas with correct conditionality, consistent types/options, and deterministic visibility across journeys. Reduce rework by catching issues at import time and exposing clear reports.

## Goals

- High confidence in conditionality: normalized grammar, validated references, and scenario coverage.
- Deterministic schema generation: column alignment, type/lookup normalization, internal/system handling.
- Developer and reviewer ergonomics: clear reports (conditions, coverage, order), preview explainability, minimal overrides.

## Non‑Goals

- Building a general spreadsheet editor.
- Automating client rewording or content changes (we prefer fixing source).

## Users

- Designers/PMs: verify interaction logic and content fidelity.
- Engineers: rely on structured outputs and reports to implement/render reliably.
- Reviewers: trace schema fields back to spreadsheet provenance.

## Scope

- Ingestion from XLSX with column‑reference alignment.
- Mapping rules with explicit overrides (labels/visibility/options) and fallbacks.
- Conditionality parser/normalizer + linter.
- Reports and preview instrumentation.

## Requirements

- Column alignment uses Excel cell references; no positional drift when cells are empty.
- Internal/system handling: INTERNAL='a' (yes) or 'Y' → exclude from UI (and by default from schema); SYSTEM similarly.
- Value matching: equals is case‑insensitive at runtime to avoid brittle typos; long‑term fix is to correct source and remove overrides.
- Conditionality grammar: normalize (= → ==, <> → !=, AND/OR → &&/||); accept quoted multi‑word values.
- Linting: unresolved keys, option mismatch, suspicious numeric tokens; dependency order recommendations.
- Reports: conditions CSV/JSON, coverage matrix, dependency order; API endpoint to fetch them.
- Preview: single‑page; section dividers (excluding “General”); repeater rendering for groups; explain‑why mode for visibility (dev only).

## Acceptance Criteria

- Import produces a schema with 0 unresolved lookup options, 0 unresolved condition operands, and no YAML parse errors.
- Conditions report highlights 0 unresolved references and passes alias checks.
- Scenario tests pass for UK/non‑UK key paths.
- Internal/system rows never render in the preview.

