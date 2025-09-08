# Documents

Central working docs for the RBSI Institutional Onboarding prototype. These files are canonical and describe how we work and what we’re building.

## Start Here

- Documents/01 Areas/project-context.md – Why the project exists, outcomes, scope, and ways of working.
- Documents/01 Areas/project-structure.md – Canonical repo structure, workflows, Mission Control (MVP), and conventions.
- Documents/01 Areas/guide/README.md – Using the Prototype (plain English overview and how‑to).

## Workflows and Specs

- Documents/01 Areas/poc-workflow/ – PoC area (README plan, PRD, ADRs).
- Documents/01 Areas/session-context/ – Session logs to maintain continuity across working sessions.
 - Documents/01 Areas/auth/ – Auth docs (README, API contracts).
 - Documents/01 Areas/guide/ – Plain English guides (Using, Quick Start, Operations, Glossary, FAQ).
  - template.md – Template for new session logs.
  - session-context-001.md – Current progress summary and next actions.

## Notes

- These docs are source‑controlled. Avoid PII. Link to artefacts in `/data` and code in `/apps/prototype` as they are created.
- Mission Control visibility and status default to `data/schemas/manifest.yaml` and can be overridden globally via env or (in dev) `/data/admin/config.json`.
