# RBSI Onboarding Prototype — Handover

Date: 2025-01-11  
Status: Complete prototype system with KYCP components, tone analysis, and full workflow documentation

## Overview

Purpose: Move from spreadsheets to clickable, schema‑driven journeys rapidly, with an audit trail suitable for client review. This is not production software and does not store personal data.

Current state
- Mission Control lists journeys; both standard and KYCP versions available.
- KYCP component library with exact visual parity to platform (Sessions 009-011).
- Components: String, FreeText, Integer, Decimal, Date, Lookup (no radio buttons).
- Two importers: standard and KYCP-aligned for different schema formats.
- Tone of voice analyzer with CSV reports for human review.
- Robust visibility engine (AND/OR, parentheses, includes, numeric compares).
- Complete workflow documented from spreadsheet to deployed prototype.
- Health endpoint `/api/health` confirms data availability.

## Architecture & Structure (key paths)

App (Nuxt 3): `apps/prototype/`
- Pages: `pages/index.vue` (Mission Control), `pages/preview/[journey].vue`, `pages/about.vue`
- Components: `components/kycp/base/*` (inputs), `components/nile/*` (layout)
- Composables: `useManifest.ts`, `useSchema.ts`, `useConditions.ts`, `useValidation.ts`
- Server: `server/api/*` (manifest, schema, diff, export, auth, health)
- Server utils: `server/utils/data.ts` (data loader), `server/utils/schema-validator.ts`
- Design tokens: `assets/kycp-design.css`

Data (bundled with app): `apps/prototype/data/`
- Schemas: `schemas/manifest.yaml`, `schemas/<journey>/schema.yaml`
- Mappings: `mappings/*.json`
- Incoming: `incoming/*.xlsx`
- Generated: `generated/importer-cli/<journey>/*`, `generated/exports/*`, `generated/diffs/*`

Docs: `Documents/01 Areas/guide/`
- System-Overview.md, Operations.md, Visibility-Rules.md, Deployments.md, Area-Workflow.md

Scripts (root):
- `scripts/import_xlsx.py` (Standard importer)
- `scripts/import_xlsx_kycp.py` (KYCP-aligned importer)
- `scripts/analyze_tone.py` (Tone of voice analyzer)
- `scripts/mapping_wizard.py` (interactive mapping)
- `scripts/preview_schema.py` (schema summary)

## Data & Import Pipeline

Inputs
- XLSX in `apps/prototype/data/incoming/`
- Mapping JSON in `apps/prototype/data/mappings/` (declares columns, normalization, ordering)

Command (example)
```
python scripts/import_xlsx.py \
  --mapping apps/prototype/data/mappings/non-lux-lp-demo.json \
  --input apps/prototype/data/incoming/20250828_draft-master-spreadsheet.xlsx \
  --sheet "LP Proposal" \
  --lookups-sheet "Lookup Values" \
  --journey-key non-lux-lp-demo
```

Outputs
- Schema: `apps/prototype/data/schemas/<journey>/schema.yaml`
- Reports: `apps/prototype/data/generated/importer-cli/<journey>/{summary.json, decisions.json}`

Defaults & rules
- Lookup = dropdown (select), including Yes/No when provided by lookup.
- Mandatory normalization accepts A/a/Required/Mandatory + Y/Yes/True/1.
- Visibility expressions normalized (AND/OR, operators, quoting RHS).
- If lookup type missing, control falls back to text (no invalid select).

## Deployment (Vercel)

Settings
- Framework: Nuxt.js; Root Directory: `apps/prototype`; leave Output Directory blank.

Data
- Bundled in `apps/prototype/data/`; no `NUXT_DATA_DIR` needed.

Env vars
- `NUXT_ADMIN_PASSWORD_HASH` (bcrypt from `pnpm hash "YourPassword"`).
- Optional: `MC_VISIBLE=non-lux-lp-demo`.

Health & checks
- `/api/health` → `{ dataDir, manifestExists, journeyCount }`.
- `/api/manifest` includes `non-lux-lp-demo` in active.
- Admin login shows the Admin badge; Diff/Export stream artifacts (writes may be skipped on serverless).

## Admin & Security

- Password-only admin with HTTP‑only cookie.
- Zod schema validation on server.
- CSV export escaping (formula injection safe).
- Slug validation on journey params (path traversal safe).

## Known Constraints

- Vercel FS is read‑only: Diff/Export write attempts are best‑effort; responses still stream back CSV/HTML.
- About page provides a stable overview; session-context files track detailed progress.

## Next Steps

- Serverless flag to skip disk writes for Diff/Export.
- pnpm convenience scripts for importer/wizard.
- Minimal tests for visibility grammar and importer normalization.
- Optional: CSRF on POST `/api/auth/login`.

## Quick Start

Local
```
cd apps/prototype
pnpm install
pnpm dev
# http://localhost:3000
```

Deploy (Vercel)
- Set `NUXT_ADMIN_PASSWORD_HASH`, deploy from `apps/prototype` (Nuxt preset).
- Verify `/api/health` and `/api/manifest`.

## References

- Guides: `Documents/01 Areas/guide/*`
- Sessions: `Documents/01 Areas/session-context/session-context-00*.md`
- This handover will be updated at the end of each working session.
   - Success metrics (80% RFT)
   - Stakeholder requirements

2. **Project Structure**: `/Documents/01 Areas/project-structure.md`
   - Development workflow
   - Branching strategy
   - PR requirements

3. **POC Workflow**: `/Documents/01 Areas/poc-workflow/README.md`
   - Implementation phases
   - Status tracker
   - Acceptance criteria

4. **Design System**: `/Documents/01 Areas/design-system/`
   - PRD for component showcase
   - ADR for architecture decisions
   - Component specifications

5. **Session Contexts**: `/Documents/01 Areas/session-context/`
   - session-context-001.md: Initial setup
   - session-context-002.md: Component library creation
   - session-context-003.md: Importer CLI scaffolding and analysis
   - session-context-004.md: Importer/visibility hardening; deploy path
   - session-context-005.md: Data bundling; admin/health; visibility
   - session-context-006.md: Internal-only flags; provenance on cards
   - session-context-007.md: KYCP component fidelity phase
   - session-context-008.md: Strict KYCP parity achieved
   - session-context-009.md: Visual matching to KYCP platform
   - session-context-010.md: Process new spreadsheet with both importers
   - session-context-011.md: Complete workflow with tone analysis

## 🔑 Key Decisions Made

1. **Vue/Nuxt over React/Next**
   - Aligns with KYCP (client's platform)
   - Better handover compatibility

2. **Custom components over libraries**
   - Exact KYCP match required
   - No unnecessary dependencies
   - Full control over behavior

3. **Schema-first approach**
   - Single source of truth
   - Auditable changes
   - Clean separation of data/UI

4. **Flat design for Mission Control**
   - Journey-agnostic
   - Professional without branding
   - Clear information hierarchy

## 💡 Tips for Next Developer

1. **Always check CSS scoping** - Global variables must be in app.vue
2. **Use v-if for component switching** - More reliable than dynamic components
3. **Test in multiple browsers** - Especially Safari for form controls
4. **Keep schemas clean** - They drive everything
5. **Document decisions** - Future you will thank you
6. **Run pnpm dev from /apps/prototype** - Not from root
7. **Check CLAUDE.md** - Has specific gotchas for this project

## 🚀 Quick Start for New Session

```bash
# 1. Navigate to project
cd /Users/tiernaugh/Documents/PARA/Areas/Nile/01 Projects/RBSI-onboarding/apps/prototype

# 2. Start dev server
pnpm dev

# 3. Open browser
open http://localhost:3000

# 4. Check latest session context
cat ../../../Documents/01\ Areas/session-context/session-context-002.md

# 5. Review this handover
cat ../../../Documents/01\ Areas/HANDOVER.md
```

## 📞 Support & Resources

- **Component Issues**: Check `/apps/prototype/CLAUDE.md`
- **Schema Questions**: See `/data/schemas/README.md`
- **Design Decisions**: Review ADRs in `/Documents/01 Areas/design-system/`
- **Git History**: Detailed commit messages explain changes

---

**Remember**: This is a prototype for demonstration and testing. It's not production code, but it should feel production-ready to users testing it.

**Last Updated**: 2025-01-11 by Assistant in Session 009
