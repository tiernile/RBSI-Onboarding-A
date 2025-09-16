# Future Prototype Variant Workflow (2.0 Journeys)

This guide records the agreed workflow for shaping future-state journeys while keeping the AS-IS (v1.1) schema intact. Use it when creating `non-lux-lp-2-0` and any later variants.

## Goals
- Preserve the cleaned `non-lux-1-1` KYCP schema as the authoritative AS-IS snapshot.
- Stand up a separate 2.0 journey (`non-lux-lp-2-0`) that experiments with revised wording, grouping, and UX.
- Maintain an explicit audit trail: every proposed change carries provenance, original text, and rationale.

## 1) Duplicate the Baseline Schema
1. Copy `apps/prototype/data/schemas/non-lux-1-1/schema-kycp.yaml` to `apps/prototype/data/schemas/non-lux-lp-2-0/schema-kycp.yaml`.
2. Update the header:
   - `key: non-lux-lp-2-0`
   - `name: Non-Lux LP — v2.0 (Future Draft)` (adjust as needed)
   - Increment the `version` (e.g., `0.2.0`).
3. Confirm every field remains in the copy; we do **not** drop questions for the prototype stage.

## 2) Register the Journey in Mission Control
1. Add a card in `apps/prototype/data/schemas/manifest.yaml`:
   ```yaml
   - key: non-lux-lp-2-0
     name: Non‑Lux LP — v2.0 (Future Draft)
     version: 0.2.0
     variant: KYCP
     owner: "@tiernan"
     display:
       group: Funds
       order: 8
       visible: true
       status: draft
   ```
2. The card should open `/preview-kycp/non-lux-lp-2-0`.
3. Leave the v1.1 card untouched so stakeholders can compare AS-IS vs future.

## 3) Catalogue Proposed Changes
1. Source of truth for copy and grouping updates: `apps/prototype/data/incoming/20250916-rewritten-draft.xlsx` (sheet: `P2140 RBSi Onboarding - Phase 2`).
2. For each row:
   - Column A → proposed accordion group label.
   - Column B → current AS-IS label (matches v1.1 schema).
   - Column C → proposed label.
   - Column D → helper/microcopy.
3. Build a lookup keyed by the existing label so we can overlay proposed text without losing unmatched fields.
4. When we receive “bulk” suggestions, pause and record the origin (e.g., Nile team, client SME) so the rationale is explicit.

## 4) Extend Schema Metadata for Audit Trail
Add the following structure to each field in the 2.0 schema:
```yaml
original:
  label: <v1.1 label>
  help: <v1.1 help or null>
future:
  proposedLabel: <column C>
  proposedHelp: <column D>
  changeSource: <e.g., "Nile team"> # confirm per batch
  rationale: <free-form notes>       # capture when provided
```
Notes:
- Keep empty strings as `null` to avoid noise.
- If there is no proposed change for a field, still populate `original.*` so the audit trail is consistent and leave `future` empty or `null`.
- Continue to retain existing `scriptId`, `_section`, `_stage`, and visibility rules.

## 5) Model Accordion Grouping
1. Wrap each Column-A group inside a `KycpAccordion` section in the KYCP preview.
2. Represent grouping in the schema:
   ```yaml
accordions:
  - key: start-a-new-application
    title: Start a New Application
    order: 1
  - key: business-appetite
    title: Business Appetite
    order: 2
   ```
   and add `accordionKey: start-a-new-application` to each field.
3. Fields that are not listed in the draft spreadsheet should sit inside a catch-all accordion (e.g., `legacy-content`) so nothing disappears.

## 6) Update the Preview Experience
1. `/pages/preview-kycp/[journey].vue` should:
   - Detect the new `accordions` structure and render fields inside `KycpAccordion` sections.
   - Respect complex group repeaters inside each accordion.
2. Enhance the “Explain visibility” toggle so that when enabled, each field panel shows:
   - Original label/help (AS-IS).
   - Proposed label/help.
   - Change source (e.g., “Nile team”) and any rationale text.
   - Visibility rule breakdown (existing behaviour).

## 7) Tracking Change Provenance
- For every batch or individual change, confirm the source with the requester. Example prompt: “These proposed rewrites for Start a New Application – should the changeSource read ‘Nile team’?”
- Record the answer in the schema metadata.
- If rationale comes from a workshop or document, capture a short summary and reference (e.g., “Workshop 2025-09-17” or Confluence link).

## 8) Verification Checklist
- `/preview-kycp/non-lux-1-1` still renders the AS-IS journey untouched.
- `/preview-kycp/non-lux-lp-2-0` renders with accordion sections and Explain Visibility shows change details.
- Admin reports (Diff, CSV, Conditions Report) load with the new journey key.
- No fields missing: cross-check count between v1.1 and v2.0 schemas.

## 9) Documentation & Session Logs
- Update `Documents/01 Areas/session-context` after each working session describing applied change sets, sources, and outstanding clarifications.
- Reference this guide in handover notes when sharing future-state progress with stakeholders.

## Open Questions
- Do we surface future-state copy in the default experience or keep it behind a toggle? (Decision pending product sign-off.)
- How should we ingest rationale text when supplied outside the spreadsheet (e.g., via email)? Consider adding a lightweight registry in `data/mappings/`.

Keep refining this document as the prototype evolves.
