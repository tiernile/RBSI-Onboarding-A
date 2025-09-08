---
title: PoC Implementation Plan – Schema‑First Onboarding Slice (Vue/Nuxt)
version: 0.1.0
owner: @tiernan
status: draft
last_updated: 2025-08-28
---

# Overview

This plan breaks the PoC into concrete workstreams and tasks with owners, due dates, and dependencies. It should be kept up to date as work progresses.

## Workstreams

1) Schema & Data
- T1: Select demo slice (5–8 screens, 2+ branches). Owner: Tiernan. Due: TBC. STATUS: Done (Non‑Lux LP demo slice).
- T2: Draft `/data/schemas/non-lux-lp-demo/schema.yaml` with `meta.source_row_ref`. Owner: Assistant. Due: TBC. STATUS: Done.
- T3: Prepare minimal mapping JSON (if sheet available). Owner: Assistant. Due: TBC. STATUS: Done (`data/mappings/non-lux-lp-demo.json`).

2) Nuxt Scaffolding & Composables
- T4: Scaffold Nuxt app structure (pages, components, composables) per `.cursorrules`. Owner: Assistant. Due: TBC. STATUS: Done (scaffolded).
- T5: Implement `useManifest()` (merge env/file overrides). Owner: Assistant. Due: TBC. STATUS: Done (API + composable).
- T6: Implement `useSchema(journeyKey)`. Owner: Assistant. Due: TBC. STATUS: Done (server read YAML + composable).
- T7: Implement `useConditions()` (`==`, `!=`, `includes`, `&&`, `||`). Owner: Assistant. Due: TBC. STATUS: Done (basic evaluator).

3) Components & Accessibility
- T8: Build KYCP‑like inputs (text, textarea, number, date, radio, checkbox, select) with `v-model` conventions. Owner: Assistant. Due: TBC. STATUS: Partial (text, textarea, radio, select).
- T9: Field wrapper + error summary with anchors; focus management. Owner: Assistant. Due: TBC.
- T10: A11y tokens and CSS variables (contrast, spacing). Owner: Assistant. Due: TBC.

4) Rendering & Flow Logic
- T11: Render screens from schema (no hard‑coded copy/validation). Owner: Assistant. Due: TBC.
- T12: Wire validation per schema; page submit behaviour. Owner: Assistant. Due: TBC. STATUS: Partial (required/regex + group-level validate).

5) Mission Control (MVP)
- T13: Mission Control page: cards rendered from `manifest.yaml`. Owner: Assistant. Due: TBC. STATUS: Done (index.vue + /api/manifest).
- T14: Admin login API (bcrypt hash, HTTP‑only cookie) and basic lockout. Owner: Assistant. Due: TBC. STATUS: Partial (plain fallback, cookie set; hash TBD).
- T15: Visibility/status overrides (env in hosted; file in dev). Owner: Assistant. Due: TBC. STATUS: Done (env parsing in API).
  - T14a: Generate bcrypt hash for temporary password "Monday1" and set `NEXT_ADMIN_PASSWORD_HASH`; remove any plain fallback when ready. Owner: Assistant. Due: TBC.
  - T14b: Nuxt env guidance documented (use `.env.development`/`.env` in `apps/prototype/`). STATUS: Done.

6) Diff/Export & Audit
- T16: Generate human‑readable diff (HTML) mapped to `source_row_ref`. Owner: Assistant. Due: TBC. STATUS: Done (server endpoint writes and returns HTML).
- T17: Optional export (CSV) for slice. Owner: Assistant. Due: TBC. STATUS: Done (server endpoint writes CSV and serves download).
- T18: ADR(s) for platform gaps. Owner: Tiernan. Due: rolling.

7) Testing & Playback
- T19: Unit tests (composables/components). Owner: Assistant. Due: TBC.
- T20: E2E happy path + a11y checks (axe). Owner: Assistant. Due: TBC.
- T21: Evidence pack (screens/clip/diff link). Owner: Tiernan. Due: TBC.

## Milestones

- M1: Slice selected; schema drafted (T1–T2).
- M2: Nuxt scaffolding and composables ready (T4–T7).
- M3: Inputs + schema‑driven render + a11y (T8–T12, T10).
  - With step navigation by section and group-level validation.
- M4: Mission Control working; admin gating in dev; overrides wired (T13–T15).
- M5: Diff/export + tests + evidence pack (T16–T21).

## Acceptance Criteria

- Screens render entirely from schema; conditions and validations behave per spec.
- Axe checks pass on the slice; error summary anchors to fields; keyboard flows work.
- Diff HTML clearly maps changes to `source_row_ref`; export (if produced) is consumable.
- Mission Control lists the slice; visibility/status controllable globally (env/file).

## Dependencies & Inputs Needed

- Client spreadsheet rows for the selected slice (or confirmation to hand‑craft for v0).
- KYCP component catalogue (names, props, constraints, error patterns).
- Hosting approach for demos (affects env override flow).
- Admin password (we will store only the bcrypt hash) or approval to generate a temporary one.

## Status

- Completed: T1–T7, T13, T15, T16, T17; T8 partial; T12 partial.
- Pending: T9–T11 (a11y polish; wrappers complete), T14 (hashed auth + lockout), T18–T21 (ADRs, tests, evidence pack).

## Change Log

- 2025‑08‑28: Initial plan drafted.
