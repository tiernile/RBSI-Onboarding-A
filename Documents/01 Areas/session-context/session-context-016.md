---
session_id: 016
date: 2025-09-17
facilitator: Assistant
participants: [Assistant, Tiernan (Nile)]
related_journeys: [non-lux-1-1, non-lux-lp-2-0]
related_files: [
  "apps/prototype/data/schemas/non-lux-lp-2-0/schema-kycp.yaml",
  "apps/prototype/data/schemas/manifest.yaml",
  "apps/prototype/pages/preview-kycp/[journey].vue",
  "Documents/01 Areas/guide/Future-Prototype-Variant-Workflow.md",
  "apps/prototype/data/incoming/20250916-rewritten-draft.xlsx"
]
---

# Session Summary

- Goal: Stand up the v2.0 future journey shell and start cataloguing proposed copy changes without touching the AS-IS flow.
- Outcome: New journey registered with accordion layout, placeholder messaging, and Nile-sourced copy metadata recorded for every matched field; future workflow captured in docs.

## Changes Made

- File: apps/prototype/data/schemas/non-lux-lp-2-0/schema-kycp.yaml – Duplicated v1.1 schema, added accordion config, layered `original`/`future` metadata, and applied Nile draft wording (including option label updates via copy-map).
- File: apps/prototype/data/schemas/manifest.yaml – Added Mission Control card for `non-lux-lp-2-0` (variant KYCP).
- File: apps/prototype/pages/preview-kycp/[journey].vue – Enabled accordion rendering, fallback messaging, slug normalisation, display of future copy, and enhanced Explain Visibility to show AS-IS vs proposed text with provenance.
- File: Documents/01 Areas/guide/Future-Prototype-Variant-Workflow.md – Documented agreed workflow for future-state variants.
- File: apps/prototype/data/generated/non-lux-lp-2-0-copy-map.json – New mapping that links spreadsheet rows to field keys and option labels for traceability.
- File: Documents/01 Areas/guide/Future-Prototype-Outstanding-Copy.md – Logged unmatched rows/labels that still require schema aliases or new fields.

## Decisions

- Keep AS-IS schema untouched and treat `non-lux-lp-2-0` as the experimental copy container – allows side-by-side comparison.
- Use spreadsheet labels as primary keys; where multiple rows exist per label, log leftovers for manual aliasing – prevents accidental data loss.
- Show a calm “No questions to show yet” message when conditional accordions are empty – improves comprehension during exploration.

## Open Questions

- Map workbook rows with slight label drift (e.g., options, shortened prompts) to the right schema fields – owner: Assistant (needs alias list).
- Decide when future copy should replace AS-IS text in the UI (toggle vs default) – owner: Tiernan.

## Plan and Status

- [x] Duplicate v1.1 schema and register new journey.
- [x] Wire accordion layout with conditional placeholder messaging.
- [ ] Alias remaining workbook entries to field keys (see outstanding copy doc).
- [x] Surface `original`/`future` metadata in Explain Visibility panel.
- [ ] Apply option-level copy changes for unmapped rows (e.g., UK-specific variants, key principal repeaters).

## Next Actions

- Build alias map for unmatched workbook rows (options/key principals) – owner: Assistant – due: 2025-09-18.
- Apply remaining unmatched copy updates (fields/options) – owner: Assistant – due: 2025-09-18.

## Risks / Mitigations

- Risk: Workbook labels not matching schema keys could leave proposed copy unapplied – mitigation: derive alias table and review leftovers with Tiernan before rollout.

## Artefacts and Links

- /preview-kycp/non-lux-lp-2-0 – mission-control card now live.
- Documents/01 Areas/guide/Future-Prototype-Variant-Workflow.md – workflow reference.

## Notes

- Build checks (`pnpm build`) pass after accordion and metadata changes.
- Explain Visibility still shows AS-IS text; enhancement pending alias work.
