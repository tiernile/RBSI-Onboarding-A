---
adr: 0001
title: Use Vue/Nuxt and Schema‑First Workflow for PoC
status: accepted
date: 2025-08-29
deciders: [@tiernan]
---

## Context

KYCP (target platform) uses Vue. Our goal is to validate a schema‑first prototype with high interaction fidelity and a clean handover path. Team familiarity is higher with Next.js, but parity with KYCP reduces handover risk.

## Decision

Adopt Vue 3 with Nuxt 3 for the PoC UI layer. Keep data model, condition engine, and diff/export framework‑agnostic so a pivot to Next.js remains straightforward if parity issues arise.

## Consequences

- Closer alignment with KYCP components/props; fewer surprises at handover.
- Slightly slower initial velocity vs React, mitigated by focused scope and clear conventions (`.cursorrules`).
- Shared schema/tools enable reuse if we migrate UI later.

## Alternatives Considered

- Next.js/React for PoC: fastest for team, but introduces translation risk to Vue.
- Dual‑track build (React + Vue): high effort; unnecessary for PoC scope.

## Implementation Notes

- Use Nuxt 3 with TypeScript, Composition API, `<script setup>`.
- Mission Control: admin gating via HTTP‑only cookie.
  - Dev PoC fallback: allow plaintext env `NEXT_ADMIN_PASSWORD_PLAIN` until bcrypt verification is added.
  - Target before hosting: use `NEXT_ADMIN_PASSWORD_HASH` (bcrypt) and remove plaintext fallback.
- Inputs: build KYCP‑like facsimiles (text, textarea, number, date, radio, checkbox, select) with `v-model` conventions.
- Accessibility: WCAG 2.2 AA baseline; error summary with anchors.
- Diff/export: generate human‑readable HTML and optional XLSX mapped to `meta.source_row_ref`.
