---
session_id: 001
date: 2025-08-28
facilitator: Tiernan (Nile)
participants: [Tiernan (Nile), Assistant]
related_journeys: [non-lux-lp-demo]
related_files: [
  "Documents/01 Areas/project-structure.md",
  "Documents/01 Areas/project-context.md",
  "Documents/01 Areas/poc-workflow/README.md",
  "Documents/01 Areas/poc-workflow/PRD.md",
  "Documents/01 Areas/poc-workflow/ADR-0001-tech-and-workflow.md"
]
---

# Session Summary

- Goal: Establish canonical project structure and define workflows (PoC and Mission Control MVP) while aligning on tech direction.
- Outcome: Canonical structure updated; PoC area created with PRD and ADR; Mission Control (MVP) approach added; protection model updated to reflect admin gating and global visibility; example manifest added; Cursor rules set for Vue/Nuxt; demo mapping + schema drafted and registered in manifest.

## Changes Made

- File: Documents/01 Areas/project-structure.md – Completed “Adding a new user flow” steps; added Mission Control (MVP) section; noted `/data/admin/` overrides; added env notes for `NUXT_ADMIN_PASSWORD_HASH`, `MC_VISIBLE`, `MC_STATUS`.
- File: Documents/01 Areas/project-context.md – Clarified protection to include admin‑gated Mission Control with global visibility controls; no analytics on gate pages.
- File: Documents/01 Areas/poc-workflow/README.md – Canonical PoC plan with goals, phased implementation, acceptance criteria, status tracker.
- File: Documents/01 Areas/poc-workflow/PRD.md – Product requirements for the PoC slice.
- File: Documents/01 Areas/poc-workflow/ADR-0001-tech-and-workflow.md – Decision to use Vue/Nuxt with schema‑first workflow.
- File: Documents/01 Areas/poc-workflow/Implementation-Plan.md – Workstreams, tasks, milestones, acceptance criteria.
- File: data/schemas/manifest.yaml – Added `non-lux-lp-demo` entry.
- File: data/mappings/non-lux-lp-demo.json – Mapping stub for demo slice.
- File: data/schemas/non-lux-lp-demo/schema.yaml – Demo schema (7 fields) with conditions/options.
- File: Documents/README.md – Documents entry point updated to link the PoC area.
- File: .cursorrules – Vue/Nuxt build rules to guide implementation.
- File: Documents/01 Areas/guide/* – Plain English guides for non‑technical readers (Using, Quick Start, Glossary, FAQ).
- File: Documents/01 Areas/guide/Operations.md – Plain-English operations guide for importing data and generating audit trail.

## Decisions

- Keep project-structure canonical; PoC workflow resides in a separate doc – improves clarity and governance.
- Tech direction (prototype): Start in Vue/Nuxt to align with KYCP and reduce handover risk; keep schema/logic UI‑agnostic; pivot only if parity issues arise.
- Proceed on best‑guess assumptions (e.g., SDD vs CDD filter deferred; `MANDATORY` "a" = required; normalize operators in visibility conditions). Revisit with client as needed.
- Admin auth: switched to bcrypt hash required in app env; plain fallback removed. Use `pnpm hash "Password"` to generate and set `NUXT_ADMIN_PASSWORD_HASH`.
- Mission Control admin changes are global. Persistence via env vars on hosted deploys; file‑backed overrides in dev. Presents as professional without heavy infra.
- Auth model: single admin password (bcrypt hash in env), short‑TTL HTTP‑only cookie, light rate‑limit/lockout.

## Open Questions

- KYCP component catalogue: final names/props/error patterns to lock facsimiles.
- Validation and condition limits supported by KYCP (regex, nesting, cross‑section rules).
- Navigation constraints (save‑as‑you‑go, back behaviour, timeouts) and theming tokens for close visual parity.
- Mission Control grouping (by programme/jurisdiction) – required now or later?
- Hosted global persistence: stick with env approach or introduce a lightweight KV later if needed.

## Plan and Status

- [x] Add example `manifest.yaml` entry with `display` fields (group, order, visible, status).
- [x] Create PoC area with PRD and ADR.
- [x] Prepare demo schema and mapping for PoC slice (non‑lux‑lp‑demo).
- [x] Create PoC Implementation Plan with workstreams, tasks, owners, dates.
- [x] Nuxt scaffolding; implement `useManifest`, `useSchema`, `useConditions`.
- [x] Mission Control page and admin login (plain fallback) scaffolded.
- [x] KYCP‑like base inputs (text, textarea, radio, select) scaffolded.
- [x] Grouped step flow by section with per-step validation.
- [x] YAML fixes (quoted owners/labels) and stable `dataDir` resolution.
- [x] Nuxt env guidance: use `.env.development`/`.env` in `apps/prototype/`; `.env.local` is not read in Nuxt.
- [x] Define Mission Control API contracts (auth login, admin config update; env/file modes).
- [ ] Draft acceptance tests for visibility and admin gating (spec‑level only for now).
- [x] Add field wrapper and error summary.
- [ ] A11y review pass.
- [x] Diff HTML and export CSV endpoints implemented; files are written under `/data/generated/`.
- [x] Plain English guide area created (Using, Quick Start, Glossary, FAQ) and linked from Documents README.
- [x] About page added to the app with FAQs and links to guides; About link added to Mission Control.
- [x] Admin-only links added to Mission Control cards for Diff and Export CSV.
 - [x] Hashed admin auth implemented with in‑memory lockout; docs and env templates updated.

## Next Actions

- Draft acceptance tests for visibility and admin gating – owner: Assistant.
- Run an a11y review pass on the demo slice – owner: Assistant.
- Confirm with FinOpz initial component list and constraints – owner: Tiernan – due: when available.
- Decide on dev admin config writer endpoint (persist overrides) – owner: Tiernan/Assistant.

## Risks / Mitigations

- Over‑engineering prototype admin: keep to single password and env/file persistence; defer user management.
- Divergence from KYCP behaviour: log platform gaps early; avoid patterns FinOpz cannot build.
- Spreadsheet drift: maintain round‑trip diff/export and clear ownership of updates.

## Artefacts and Links

- Documents/01 Areas/project-structure.md
- Documents/01 Areas/project-context.md
- Documents/01 Areas/poc-workflow/README.md
- Documents/01 Areas/poc-workflow/PRD.md
- Documents/01 Areas/poc-workflow/ADR-0001-tech-and-workflow.md
- Documents/01 Areas/poc-workflow/Implementation-Plan.md
- .cursorrules
- data/schemas/manifest.yaml
- data/mappings/non-lux-lp-demo.json
- data/schemas/non-lux-lp-demo/schema.yaml
 - apps/prototype/README.md
 - apps/prototype/.env.example
 - Documents/01 Areas/auth/README.md
 - Documents/01 Areas/auth/API-Contracts.md

## Notes

- No PII in repo or Mission Control. Preview gates remain password‑protected per prototype.
