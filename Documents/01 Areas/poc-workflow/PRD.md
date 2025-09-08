---
title: PoC PRD – Schema‑First Onboarding Slice (Vue/Nuxt)
version: 0.1.1
owner: @tiernan
status: draft
last_updated: 2025-08-29
---

# Background

RBSI needs an intuitive, digital‑first onboarding journey. We will validate a schema‑first, KYCP‑faithful prototype in Vue/Nuxt to de‑risk handover to FinOpz.

# Goals

- Validate spreadsheet → schema (YAML) → render → diff/export pipeline.
- Achieve credible interaction fidelity and WCAG 2.2 AA baseline.
- Establish audit trail mapping to source rows; produce evidence pack.
- Minimise platform gaps against KYCP by mirroring component props/behaviours.

# Non‑Goals

- Shipping production code; integrating with real backends; storing PII.

# Users & Roles

- Viewers: stakeholders accessing Mission Control.
- Testers: moderated participants; no login required.
- Admin: single password to control global visibility on Mission Control.

# Scope

- One journey slice (5–8 screens), 2+ conditional branches, validations.
- Controls: text, textarea, number, date, radio, checkbox, select.
- Mission Control card and visibility/status handling.

# Out of Scope (for PoC)

- File uploads, complex lookups, production auth, analytics.

# Functional Requirements

1. Mission Control lists journeys from `manifest.yaml`; applies overrides.
2. Admin login sets HTTP‑only cookie; basic rate‑limiting and lockout.
   - Hashed auth implemented: set `NUXT_ADMIN_PASSWORD_HASH` (bcrypt) in app env.
3. Preview route renders screens from schema; no hard‑coded copy/validation.
4. Condition engine supports `==`, `!=`, `includes`, `&&`, `||` and hides/shows fields live.
5. Validation shows field errors and an error summary with anchors (required, regex).
6. Diff/export produced for the slice, mapped to `meta.source_row_ref`.
   - Admin links on Mission Control cards: “View Diff” (HTML) and “Export CSV”.

# Non‑Functional Requirements

- Accessibility: WCAG 2.2 AA patterns; keyboard operable; visible focus.
- Performance: render a slice without noticeable lag on mid‑range laptops.
- Security: no PII; admin password hashed in env; HTTP‑only cookies. Dev fallback to plaintext env allowed only during PoC before hashing lands.
- Traceability: deterministic IDs; ADRs for platform gaps and key choices.

# Success Metrics

- Prototype RFT proxy ≥ baseline + agreed uplift in moderated tests.
- ≤ 2 a11y issues (axe critical/serious) on slice.
- Diff/export accepted by stakeholders as traceable and clear.

# Milestones

- M1: Schema + manifest entry.
- M2: Nuxt scaffolding + core inputs.
- M3: Schema‑driven render + a11y pass.
  - Includes step‑by‑step flow grouped by section (B2, B1, B11.1), with validation per step.
- M4: Diff/export + evidence pack.
- M5: Playback + decision gate.

# Risks & Mitigations

- Platform mismatch → build KYCP‑faithful facsimiles; log gaps (ADR).
- Scope creep → keep slice small; defer to backlog.
- Auth perception → simple, credible password auth with hash + lockout.

# Dependencies

- KYCP component catalogue (names/props/constraints) for parity.
- Client spreadsheet rows for the selected slice.

# Open Questions

- Exact slice fields and conditions; confirm with stakeholders.
- Hosting environment for shared demos (affects env override strategy).
- Do we accept PBKDF2 as an interim hash if bcrypt is unavailable in the environment during PoC? (Target remains bcrypt before hosting.)
