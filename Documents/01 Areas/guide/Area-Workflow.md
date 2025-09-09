# Area Workflow (PRD, ADR, Plan, Session Context)

Use this lightweight structure for every new phase of work so anyone can follow what we’re doing and why.

## Folder Structure
- `Documents/01 Areas/<area>/`
  - `PRD.md`: Problem, goals, scope, acceptance criteria (1–2 pages max).
  - `ADR-0001-<slug>.md` (and up): Decision records with context, options, rationale, consequences.
  - `Implementation-Plan.md`: Short checklist of tasks with owners/dates; keep status updated.
  - `README.md` (optional): Brief intro and links if the area spans many files.

## Session Context
- Log the work in `Documents/01 Areas/session-context/session-context-<nnn>.md` with front matter:
```
---
session_id: <nnn>
date: YYYY-MM-DD
facilitator: <name>
participants: [..]
related_journeys: [..]
related_files: [..]
---
```
- Include: summary, changes made, decisions, open questions, next actions, risks/mitigations, and links to artifacts.

## Naming & Conventions
- Area names: `importer-cli`, `visibility-engine`, `design-system`, etc.
- One ADR per material decision; small tweaks can append to the latest ADR under “Amendments”.
- Reference paths and schema keys in PRs (e.g., `data/schemas/<journey>/schema.yaml`, `GENFundSize`).

## PR Expectations
- Include: why, what changed, screenshots (or Loom), links to Diff/Export, and any affected spreadsheet refs.
- Keep changes small and scoped (schema vs. UI vs. server).

## Smart Defaults (Docs)
- Keep PRD concise; put details in linked notes or the Implementation Plan.
- Prefer tables/bullets over prose walls.
- Always link artifacts under `data/generated/` for audit.

Templates can be copied from existing areas (e.g., `poc-workflow/`).

