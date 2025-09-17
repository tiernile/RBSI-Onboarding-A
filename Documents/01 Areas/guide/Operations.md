# Operations Guide (Plain English)

This guide explains how the team updates the prototype with new/changed questions from a spreadsheet, generates audit trails, and uses advanced debugging tools for quality assurance.

**Critical**: Column mapping (step 2) requires explicit user decisions and cannot be automated.

## 1) Place the Spreadsheet

- Save the latest file to `data/incoming/` using `YYYYMMDD_<name>.xlsx`.
- No personal data in the spreadsheet — catalogue of questions only.

## 2) Create/Update a Mapping (columns → schema) - CRITICAL USER INPUT

**This is the most important step and requires explicit user decisions based on domain knowledge.**

Mapping decisions impact:
- Field types and validation rules
- Section organization and user experience
- Conditional logic and dependencies
- Field grouping and cognitive load reduction
- Complex field implementation

Create `data/mappings/<shortname>.json` with:
- `sheet`: the tab name (e.g., `LP Proposal`)
- `filters`: column filters (e.g., Programme = Non‑Lux, Entity = Limited Partnership)
- `columns`: which spreadsheet columns map to schema fields (KEYNAME → id, FIELD NAME → label)
- `normalization`: standardise types and operators (`Lookup` → `enum`, `=` → `==`)
- `value_aliases`: canonicalize option values (`USA` → `United States`)
- `field_grouping`: enable visual organization for sections >10 fields
- `lookups`: code lists (Yes/No; Fund Size ranges)

Tip: See `data/mappings/non-lux-1-1.json` for current implementation.

## 3) Run Importer

For current journeys:

```
cd apps/prototype
# For Non‑Lux v1.1 (current)
python3 scripts/import_non_lux_1_1.py

# For general KYCP imports
python3 scripts/import_xlsx_kycp.py --mapping [mapping] --input [xlsx] --journey-key [key]
```

Outputs:
- Schema: `apps/prototype/data/schemas/[journey-key]/schema-kycp.yaml`
- Field organization and grouping implementation
- Complex field identification and setup
- Console: include/exclude summary and unresolved lookups

## 4) Draft or Update the Schema

- Add or edit `data/schemas/<journey-key>/schema.yaml`.
- Keep it human‑readable: quote labels with `:` and any values with spaces.
- Include `meta.source_row_ref` so we can trace each field back to the spreadsheet row (e.g., `ROW:123|KEY:GENFundSize`).
- Group fields using `section` (e.g., `B2 - Bank Relationship`) and set `visibility` rules using simple expressions (e.g., `GENFundClosed == "Yes"`).

Tip: See `data/schemas/non-lux-lp-demo/schema.yaml` for examples.

## 5) Register the Journey

- Add an entry in `data/schemas/manifest.yaml` with:
  - `key`, `name`, `version`, `variant`, `owner` (quoted), and `display { group, order, visible, status }`.
- This makes it appear on Mission Control.

## 6) Run & Quality Check

- From `apps/prototype`:
  - Dev: `pnpm install && pnpm dev`
  - Build/Start: `pnpm build && pnpm start`
- **Essential Quality Checks**:
  - Use **Explain Visibility** toggle or append `?explain=1` to debug conditional logic
  - Run **Conditions Report** (admin) to validate all dependencies
  - Verify field grouping displays correctly and reduces cognitive load
  - Test complex field add/remove functionality if applicable
  - Check for backwards dependencies in flow (later questions affecting earlier ones)

## 7) Admin Tools & Debugging

**Essential admin tools for quality assurance:**

- **Conditions Report**: **Critical debugging tool**
  - Access: Click "Conditions Report" on journey card (admin)
  - Purpose: Validates all conditional logic
  - Detects: Unresolved keys, option mismatches, parse errors, dependency cycles
  - Formats: HTML (`/api/conditions-report/<journey>?format=html`) or JSON

- **Explain Visibility**: **Primary debugging feature**
  - Access: Toggle in KYCP preview or append `?explain=1`
  - Purpose: Shows which fields are visible/hidden and why
  - Displays: Field keys, visibility conditions, dependency chains
  - Use: Essential for troubleshooting conditional logic

- **Audit Trail Generation**:
  - View Diff → `/data/generated/diffs/<journey>/<timestamp>.html`
  - Export CSV → `/data/generated/exports/<journey>/<timestamp>.csv`
  - Include these in PRs and stakeholder reviews

## 8) Keep the Docs Updated

- Record material decisions as ADRs in `Documents/01 Areas/poc-workflow/`.
- Update the session context log with progress and next actions.
- Avoid PII in repo; keep references to source spreadsheet rows only.

## Quality Assurance Workflows

### Pre-Deployment Checklist
- [ ] Column mapping decisions documented and reviewed
- [ ] Conditions Report shows no errors (unresolved keys, parse errors, cycles)
- [ ] Explain Visibility tested for all conditional logic
- [ ] Field grouping implemented for sections >10 fields
- [ ] Complex fields working (add/remove functionality)
- [ ] No backwards dependencies in flow
- [ ] Journey completion tested end-to-end

### Troubleshooting Common Issues

**Conditional Logic Problems:**
1. **Run Conditions Report** (primary diagnostic)
2. **Use Explain Visibility** to see exact visibility calculations
3. **Check value aliases** in mapping (e.g., USA → United States)
4. **Verify dependency direction** (no later questions affecting earlier ones)

**Field Organization Issues:**
- **Missing fields**: Check visibility conditions and `internal_only` flags
- **Poor UX**: Implement field grouping for cognitive load reduction
- **Complex fields**: Verify parent-child setup and component functionality
- **Flow problems**: Apply backwards dependency elimination principles

**System Issues:**
- **Schema errors**: Quote labels with `:` and owners with `@` in YAML
- **Admin access**: Verify `NUXT_ADMIN_PASSWORD_HASH` environment variable
- **Environment**: Ensure env files in `apps/prototype/` directory

## Advanced Features & Commands

### Field Organization
- **Field Grouping**: Reduces cognitive load by up to 85% in complex sections
- **Complex Fields**: Repeatable components with add/remove functionality
- **Flow Optimization**: Backwards dependency elimination for better UX

### Debugging Commands
```bash
# Essential quality checks
cd apps/prototype
pnpm scenarios    # Validate critical visibility paths
pnpm fields       # Analyze field organization

# Debug URLs
# Explain Visibility: http://localhost:3000/preview-kycp/[journey]?explain=1
# Conditions Report: http://localhost:3000/api/conditions-report/[journey]?format=html
```

### Universal Principles
- **Column mapping requires user input** - cannot be automated
- **Debug early and often** - use Conditions Report and Explain Visibility
- **Implement field grouping** for sections with many fields
- **Eliminate backwards dependencies** for optimal user experience
- **Test complex fields thoroughly** - ensure add/remove functionality works
