# RBSI Institutional Onboarding – Prototyping README

This README is the single starting point for anyone joining the team. It covers how we turn client spreadsheets into working, testable prototypes, how we collaborate, and how we keep an audit trail that maps back to the client’s source material.

## Purpose

Design and deliver intuitive onboarding journeys for institutional customers, using an AI‑first but human‑judged workflow. Interaction fidelity is the priority. Prototypes must only use components the client can actually build with FinOpz (KYCP).

---

## Repo structure

```
/README.md                         – this file
/apps/prototype/                   – Nuxt (Vue 3) app we deploy
  /components/kycp/                – client component facsimiles + wrappers
  /components/nile/                – glue components, layout, utilities
  /features/                       – feature‑flagged journeys and experiments
  /lib/                            – schema parser, condition engine, validators
  /pages/                          – routes, previews, review packs
  /styles/                         – tokens that mimic KYCP theming
  /test/                           – interaction tests and lints
/data/                             – canonical schemas and imports
  /incoming/                       – raw client CSV/XLSX drops (read‑only)
  /mappings/                       – column → schema field maps per sheet flavour
  /schemas/                        – normalised JSON/YAML schemas per journey
  /generated/                      – TS types, scaffolds, diff reports
  /admin/                          – optional overrides (dev‑only) for Mission Control visibility/status
/docs/                             – Obsidian‑friendly documentation vault
  /decisions/                      – ADRs, one per decision (YAML front matter)
  /notes/                          – meeting notes + Fireflies links/summary
  /playbacks/                      – stakeholder packs and sign‑off artefacts
  /style/                          – content style guide and microcopy patterns
.github/                           – PR templates, issue templates, CI config
/scripts/                          – import, normalise, generate, diff, export
```

---

## Local setup

1. Install Node LTS and pnpm.
2. `pnpm install` at repo root.
3. `pnpm dev` to run the prototype at [http://localhost:3000](http://localhost:3000).
4. Optional: set `ANALYTICS_DISABLED=true` in `.env` for local runs.
5. Env file location and naming (Nuxt): place `.env.development` (dev) or `.env` (build/start) inside `apps/prototype/` (not repo root). Restart `pnpm dev`/`pnpm start` after changes.
6. Admin auth envs: `NUXT_ADMIN_PASSWORD_HASH` (bcrypt) is required for admin login.
7. Data path: by default the app reads `data/` from repo root. To override, set `NUXT_DATA_DIR=/absolute/path/to/repo/data`.
8. Global visibility overrides: `MC_VISIBLE` / `MC_STATUS` env vars (or `/data/admin/config.json` in dev when writer is added).

---

## Branching and releases

- Trunk‑based with short‑lived branches. Naming: `journey/<jurisdiction>-<entity>-<due-diligence>-<topic>` or `fix/<slug>`.
- PRs required for merge to `main`. At least one reviewer from the design team. For sign‑off artefacts, tag `@stephen` in the client review issue.
- We deploy from `apps/prototype` on every merge to `main`.

**PR template (auto‑applied):**

- Scope: journey and variant
- Why: problem and desired outcome
- Changes: high‑level summary
- Schema delta: link to `/data/generated/diffs/<journey>/<ts>.html`
- Spreadsheet refs: list of spreadsheet row IDs (REF/KEYNAME) touched
- Accessibility checks run and passed
- Screenshots or short Loom of interaction

---

## How we define journeys and variants

A “journey” is the combination of entity type, jurisdiction, and due‑diligence level (SDD, CDD, EDD), plus optional sub‑variants. We keep a manifest.

`/data/schemas/manifest.yaml`

```yaml
active:
  - key: lux-limited-partnership-cdd
    name: Luxembourg Limited Partnership – CDD
    version: 0.3.0
    variant: A    # A/B or multivariant where relevant
    owner: @tiernan
    display:
      group: Funds
      order: 10
      visible: true
      status: beta
  - key: non-uk-fund-cis-sdd
    name: Non‑UK Fund (CIS) – SDD
    version: 0.2.1
    owner: @designer2
    display:
      group: Funds
      order: 20
      visible: true
      status: alpha
```

Each journey has:

- `/data/schemas/<journey>/schema.yaml` – the canonical schema
- `/apps/prototype/features/<journey>/` – screens that render that schema
- `/docs/decisions/<journey>-*.md` – decision records

---

## Spreadsheet → schema → prototype pipeline

We treat the **schema** as the source of truth inside the repo. The spreadsheet remains the client’s canonical artefact, and we maintain a round‑trip mapping and diff so we can always trace changes.

### 1) Import

- Drop the client spreadsheet into `/data/incoming/<date>_<client-version>.xlsx`.
- Run `pnpm scripts:ingest --sheet <file> --map <mapping>` where mapping is a small JSON that declares which spreadsheet columns map to which schema fields. Store mappings in `/data/mappings/` by flavour.

### 2) Normalise

- Scripts normalise rows to our schema entity:

```yaml
id: GENIndicativeAppetiteInvesthighrisk            # from KEYNAME or FIELD NAME
label: "Does or will the fund make investments in high risk countries or activities?"
help: null
entity_type: limited_partnership
jurisdiction: non-luxembourg
stage: purpose_of_entity
data_type: boolean                                 # from DATA TYPE + FIELD TYPE
control: radio                                     # Lookup Yes/No → radio
options: [Yes, No]
mandatory: true                                    # from MANDATORY = Y
visibility:
  all: [GENIndicativeAppetiteQuestions == YES]     # from VISIBILITY CONDITION
validation:
  regex: null
  max_length: null
mappings:
  crm_field: null                                  # from CRM Mapping Info
  system_field: null                               # SYSTEM / INTERNAL columns
meta:
  source_row_ref: "REF:2|KEY:GENIndicativeAppetiteInvesthighrisk"
  notes: "Visibility conditions based on country/activities list"
```

- The script writes to `/data/schemas/<journey>/schema.yaml` and generates typed interfaces in `/data/generated/types/<journey>.d.ts`.

### 3) Scaffolding

- `pnpm scripts:scaffold --journey <key>` creates screens for the journey under `/apps/prototype/features/<journey>/`, wiring the condition engine and placeholders for content.

### 4) Prototype build

- Components render from schema definitions. We never hard‑code question text or validation in the React screens.
- We mirror KYCP component names and props in `/components/kycp`. If a real component does not exist, we stub a facsimile that matches likely behaviour and accessibility.

### 5) Diff and round‑trip

- For the PoC, hit the endpoints to generate artefacts:
  - `GET /api/diff/<journey>` → writes `/data/generated/diffs/<journey>/<timestamp>.html` and returns the HTML.
  - `GET /api/export/<journey>` → writes `/data/generated/exports/<journey>/<timestamp>.csv` and streams a CSV download.
- Include the diff/export links in PRs and playbacks. This is our audit trail.

---

## Screen structure and flow logic

- Screens are defined by grouping rules derived from spreadsheet columns `PAUL Section Suggestion`, `STAGE`, and our own usability groupings. We keep groups small to reduce cognitive load.
- Condition engine reads simple expressions such as `GENFundClosed == Yes`. We support `==`, `!=`, `includes`, and basic boolean logic.
- Cross‑screen dependencies are resolved before render. If a dependency is unresolved, the control is disabled with helper text.

---

## Component facsimiles

- All inputs are wrappers that respect KYCP constraints: required marks, error placement, label conventions, focus management.
- If KYCP has a pattern for dynamic lookups or complex identifiers, we model it faithfully. Missing patterns are raised as “platform gaps” in `/docs/decisions/` and the FinOpz request list.

---

## Content style guide (starter)

- Plain English, front‑load the action, avoid double negatives.
- Write for reading age 9‑11 where practical for public content; expert terms may remain but must be defined in context.
- Use task‑oriented labels: “Tell us about the fund’s investment activities” rather than “Fund description”.
- Error messages tell the user how to fix the problem.
- Help text is optional, collapsible, and never repeats the label.
- Follow GOV.UK patterns where they apply to forms, without copying UI that KYCP does not support.

`/docs/style/microcopy.md` holds worked examples and banned terms.

---

## Accessibility

- Aim for WCAG 2.2 AA. Keyboard first, visible focus, sufficient target sizes.
- Associate every input with a label. Use `aria-describedby` for errors and help.
- Do not rely on colour alone. Ensure contrast and state cues.
- Validate on submit and on blur. Keep error summaries at top of the page and link them to fields.
- Timeouts and long sessions are flagged early.

We run axe in CI for basic checks and add manual checks in the PR checklist.

---

## Notes, transcripts and decisions

- Meeting notes live in `/docs/notes/` as Markdown with YAML front matter:

```yaml
---
date: 2025-08-28
attendees: [client: Stephen, Nile: Tiernan]
related_journeys: [lux-limited-partnership-cdd]
related_keys: [GENFundClosed, GENFundSize]
decisions: ["Use targeted size when closed = No"]
actions: ["FinOpz to confirm max radio options per group"]
fireflies_url: "..."
---
```

- Each material decision becomes an ADR in `/docs/decisions/ADR-XXXX-<slug>.md` with context, options considered, consequences, and links to schema IDs and commits.
- We include a short, AI‑assisted summary at the top of each note, but keep sources and quotes linked for traceability.

---

## Testing cadence and evidence

- Fortnightly customer tests. Capture tasks, success criteria, time on task, errors, and subjective ease.
- Store protocols and results in `/docs/playbacks/<yyyy-mm-dd>-round-N/` with prototype commit hash and journey keys.
- Export a test evidence pack after each round for stakeholder playback and include links to diffs.

---

## Success measures in prototype

- Proxy RFT: proportion of flows completed without validation errors on submission plus no blockers observed in moderated sessions.
- Capture basic interaction telemetry in memory only during moderated tests (no PII). Log events: `field_error`, `backtrack`, `abandon`, `time_to_complete`. Do not ship telemetry to third parties.

---

## GitHub usage quick guide

- **Clone** and create a branch from `main`.
- **Commit** early with messages that reference spreadsheet row IDs: `feat(lux-lp-cdd): group B11 objectives – refs REF:2|KEY:GENFundClosed`.
- **PR** to `main` with the template auto‑filled. Attach the diff report and a short Loom of the interaction.
- **Review** at least one peer. If schema changes affect others, mention `@channel` in the design team.

---

## Adding a new user flow

1. Create a journey entry in `manifest.yaml` with a semantic version starting at `0.1.0`.
2. Import and normalise the relevant spreadsheet rows.
3. Scaffold screens and commit.
4. Prepare baseline variant A. If testing alternatives, branch `variant/b` and keep screens under `features/<journey>-b` with the same schema keys but different copy/grouping as needed. Track each active variant in `manifest.yaml`.
5. Run smoke tests: render all screens, happy‑path submit, error summary links, and axe checks on key templates.
6. Generate diff and export: `pnpm scripts:diff --journey <key> --sheet <file>` and attach links in the PR.
7. Create or update ADRs for material decisions and any platform gaps discovered; tag FinOpz for confirmation where needed.
8. Prepare playback pack under `/docs/playbacks/<yyyy-mm-dd>-round-N/` with commit hash, journey keys, screenshots, and the diff link.
9. After sign‑off, merge to `main` and bump the journey `version` in `manifest.yaml`. Record the change in the ADR and link the commit.
10. For merging variants, raise an ADR that states the winning variant, rationale, and any schema/content changes; deprecate the losing variant in the manifest.

---

## Mission Control (MVP)

Landing page listing journeys as cards, with a simple admin mode to globally control what’s visible to non‑admins.

- Source of truth: `data/schemas/manifest.yaml` with per‑journey `display` fields: `{ group, order, visible, status }`.
- Global overrides:
  - Hosted: env vars `MC_VISIBLE=key1,key2` and `MC_STATUS={"<key>":"alpha|beta|live"}` resolve at runtime/build.
  - Dev: optional `/data/admin/config.json` with `{ visible: { <key>: bool }, status: { <key>: "alpha|beta|live" }, variant: { <key>: "A|B" } }`.
- Auth: single admin password, verified server‑side against `NEXT_ADMIN_PASSWORD_HASH` (bcrypt). On success, set a short‑TTL, HTTP‑only cookie; apply basic rate‑limit/lockout.
- Viewer vs Admin:
  - Viewer sees cards where `effective.visible == true` (manifest merged with overrides). Hidden journeys show a clear gate if accessed directly.
  - Admin sees all journeys plus inline controls (Show/Hide, Status, Variant) and a banner indicating config source (env vs file) with copyable snippets.
- Acceptance:
  - Admin changes are global (file in dev for immediate effect; env in hosted with ops/redeploy).
  - No PII on the landing; only metadata. Preview routes respect visibility for non‑admins.
  - Admin convenience: links on each card to “View Diff” (HTML) and “Export CSV” for audit artefacts.
