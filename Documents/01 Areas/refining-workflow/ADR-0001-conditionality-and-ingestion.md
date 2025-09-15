# ADR-0001 — Conditionality, Ingestion, and Mapping Discipline

## Context

Spreadsheet inputs vary (empty cells, mixed casing, textual AND/OR). Prior imports suffered from positional drift, brittle value matching, and ambiguous visibility rules.

## Decision

1) Alignment — build rows using Excel column letters, not positional indices.

2) Conditionality — normalize to a constrained grammar and parse into a visibility AST:
- Normalize AND/OR → &&/||; = → ==; <> → !=.
- Case‑insensitive equals at runtime; prefer fixing source to remove overrides.

3) Internal/system — INTERNAL='a'|'Y' and SYSTEM='a'|'Y' are excluded from user‑facing schema (not rendered). Optionally retain as audit only.

4) Lookups — load from “Lookup Values” sheet via header discovery; add explicit fallbacks; final fallback option “Lookup items not provided”.

5) Non‑input rows — Title/Divider/Statement recognized from DATA TYPE or FIELD TYPE; KEYNAME may be synthesized; duplicates prevented.

6) Overrides — allowed but minimal: labels, visibility, options; prefer fixing source and removing overrides.

## Consequences

- Imports are more resilient; conditionality becomes deterministic.
- Case‑insensitive compares reduce false negatives; source corrections still encouraged.
- Internal/system data no longer leaks into the preview; schema can keep audit provenance.

## Alternatives Considered

- Strict case‑sensitive matching: higher precision but brittle; rejected for initial pass.
- Free‑form condition evaluation: risky and non‑portable; rejected.

## Status

Accepted and implemented for `non-lux-1-1`; to be extended across journeys.

