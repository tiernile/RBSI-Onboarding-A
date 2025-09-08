# Proof‑of‑Concept Workflow

Objective: validate the spreadsheet → schema → render → diff pipeline and interaction fidelity while KYCP component facsimiles mature. Keep data/logic UI‑agnostic so we can render in Vue (primary) or pivot to React if required.

## Goals

- Validate schema‑first pipeline: spreadsheet → schema (YAML) → screens → diff/export.
- Achieve credible interaction fidelity using Vue/Nuxt with KYCP‑faithful component facsimiles.
- Establish baseline accessibility patterns (labels, error summary, focus, contrast) that pass axe checks.
- Prove auditability with a human‑readable diff and export aligned to source row references.
- De‑risk handover to KYCP by matching component props/behaviours and logging platform gaps early.
- Produce a small, testable slice and evidence pack for stakeholder playback.

## Scope

- Controls: text, textarea, number, date, radio, checkbox, select (exclude uploads/complex lookups initially).
- Styling: simple tokens approximating KYCP (spacing, radius, colours). No theming overrides.
- Journey slice: 5–8 screens, at least two conditional branches and validation.

## Implementation Plan

Phase 1 — Define slice and schema
- Pick a representative slice (5–8 screens, 2+ condition branches, validations).
- Draft `/data/schemas/demo-lp-cdd/schema.yaml` with `meta.source_row_ref` placeholders.
- Add entry to `data/schemas/manifest.yaml` with `display` (group, order, visible, status) and `version: 0.1.0`.

Phase 2 — Nuxt scaffolding and composables
- Set up Nuxt 3 app structure (pages, components, composables) per `.cursorrules`.
- Implement `useManifest()` to read manifest.yaml and apply overrides.
- Implement `useSchema(journeyKey)` to load the demo schema.
- Implement `useConditions()` supporting `==`, `!=`, `includes`, `&&`, `||`.

Phase 3 — Components and rendering
- Create accessible inputs: text, textarea, number, date, radio, checkbox, select under `components/kycp/*` with Vue `v-model` conventions.
- Build field wrappers (label, hint, error, help) and error summary linking.
- Render screens entirely from schema; no hard‑coded copy/validation.

Phase 4 — Diff/export (audit trail)
- Generate a human‑readable diff (HTML) mapping `source_row_ref` to schema deltas.
- Optionally produce a cleaned export (XLSX) for the slice.

Phase 5 — Mission Control (MVP)
- Show a card for the demo journey based on `manifest.yaml`.
- Optional: env‑driven visibility/status overrides (`MC_VISIBLE`, `MC_STATUS`), admin login (bcrypt hash) for dev.

Phase 6 — QA, a11y, and playback
- Run axe checks; verify keyboard flows and focus management.
- Happy‑path submit across the slice; verify error summary anchors.
- Capture proxy metrics in memory only during a short moderated test.
- Compile evidence pack (screenshots, short clip, diff link) for playback.

## Acceptance Criteria

- End‑to‑end pipeline works; schema drives render; diffs map to source rows.
- Basic accessibility and error patterns in place; no hard‑coded content.
- At least one platform gap identified and logged as an ADR.

## Roles & Ownership

- Design lead: owns slice selection, copy, and a11y sign‑off.
- Prototyper: implements Nuxt app, components, composables, and diff/export.
- Reviewer: verifies schema alignment, testing, and evidence pack.

## Timeline & Milestones (indicative)

- Day 1: Slice selection, schema draft, manifest entry.
- Day 2: Nuxt scaffolding, composables, initial inputs.
- Day 3: Schema‑driven render, diff/export stub, a11y pass.
- Day 4: Moderated test, evidence pack, decision gate (continue in Vue or pivot).

## Status Tracker

- [x] Example `manifest.yaml` added with `display` fields.
- [x] PoC workflow doc created; goals and plan documented.
- [x] Demo slice agreed and schema drafted at `/data/schemas/non-lux-lp-demo/schema.yaml`.
- [x] Nuxt scaffolding in place; `useManifest`/`useSchema`/`useConditions` implemented.
- [x] KYCP‑like inputs built (Input, Textarea, Radio, Select, FieldGroup, FieldWrapper, Tag components)
- [x] Component showcase created at `/showcase` with interactive demos and code examples
- [x] Schema‑driven screens render; no hard‑coded copy
- [x] Preview pages now use KYCP components with professional styling
- [x] Diff HTML generated (via `/api/diff/:journey`); optional export CSV produced (via `/api/export/:journey`).
- [ ] A11y checks pass; error summary anchors verified. (Components built with ARIA support)
- [ ] Evidence pack prepared; ADR for any platform gaps.
- [x] Design system documented with PRD and ADR
- [x] Mission Control redesigned with flat, professional aesthetic

## Tech Choice

- Start in Vue/Nuxt to align with KYCP and reduce handover risk.
- Keep schema, condition engine, and diff/export framework‑agnostic to preserve the option to pivot to Next.js if needed.

## Update Protocol

- Update the Status Tracker as items complete; include commit hashes where useful.
- Record material deviations or platform gaps as ADRs in `/docs/decisions/` and link them here.
- Keep this document as the single source of truth for PoC scope, plan, and status.
