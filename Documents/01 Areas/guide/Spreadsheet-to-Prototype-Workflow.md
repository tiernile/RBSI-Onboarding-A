# Spreadsheet to Prototype Workflow Guide

This guide provides step-by-step instructions for converting a client spreadsheet into a working KYCP-compliant prototype. Follow these steps to create a new journey from an Excel file.

## Prerequisites

- Python 3 installed
- Node.js and pnpm installed
- Access to the RBSI-onboarding repository
- The client spreadsheet in .xlsx format

## Complete Workflow

### Step 1: Prepare the Spreadsheet

1. **Place the spreadsheet** in the incoming directory:
   ```bash
   cp your-spreadsheet.xlsx apps/prototype/data/incoming/YYYYMMDD_descriptive_name.xlsx
   ```
   Example: `20250911_master_non-lux.xlsx`

2. **Verify the spreadsheet structure**:
   - Main data should be in a sheet like "LP Proposal" or similar
   - Lookup values should be in a sheet like "Lookup Values"
   - Should have columns for: KEYNAME, FIELD NAME, DATA TYPE, MANDATORY, VISIBILITY, etc.

### Step 2: Create or Update Mapping Configuration

1. **Check if a mapping exists** for your journey type:
   ```bash
   ls apps/prototype/data/mappings/
   ```

2. **Create a new mapping** if needed:
   ```json
   {
     "sheet": "LP Proposal",
     "filters": {
       "PROGRAMME": "Account is for - a Fund (CIS) - Non Luxembourg",
       "ENTITY": "Limited Partnership"
     },
     "columns": {
       "id": "KEYNAME",
       "label": "FIELD NAME",
       "data_type": "DATA TYPE",
       "field_type": "FIELD TYPE",
       "lookup_type": "LOOKUP",
       "mandatory": "MANDATORY",
       "visibility": "VISIBILITY CONDITION/GROUP NAME",
       "regex": "REGEX",
       "ref": "REF",
       "action": "Action"
     },
     "normalization": {
       "data_type": {
         "Lookup": "enum",
         "Free Text": "string",
         "Number": "number",
         "Date": "date"
       },
       "operators": {
         "=": "==",
         "<>": "!="
       }
     },
     "lookups_sheet": "Lookup Values",
     "lookups": {
       "Yes/No": ["Yes", "No"],
       "Fund Size": ["< 50m", "50m - 250m", "250m - 500m", ...]
     }
   }
   ```
   Save as: `apps/prototype/data/mappings/your-journey-key.json`

### Step 3: Run the Importer (KYCP)

For Non‑Lux v1.1, run the built‑in KYCP importer:

```bash
cd apps/prototype
python3 scripts/import_non_lux_1_1.py
```

Output:
- Schema: `apps/prototype/data/schemas/non-lux-1-1/schema-kycp.yaml`
- Console summary with include/exclude counts and unresolved lookups

### Step 4: Add Journey to Manifest

1. **Edit the manifest file**:
   ```bash
   vi apps/prototype/data/schemas/manifest.yaml
   ```

2. **Add your journey entries**:
   ```yaml
   active:
     # ... existing entries ...
     
     # Standard version (optional, for comparison)
     - key: your-journey-key
       name: Your Journey Name - Standard
       version: 0.1.0
       variant: A
       owner: "@yourname"
       display:
         group: Funds
         order: 50
         visible: true
         status: alpha
     
     # KYCP version (recommended)
     - key: your-journey-key-kycp
       name: Your Journey Name - KYCP
       version: 0.1.0
       variant: KYCP
       owner: "@yourname"
       display:
         group: Funds
         order: 51
         visible: true
         status: beta
   ```

### Step 5: Test the Prototype

1. **Start the development server**:
   ```bash
   cd apps/prototype
   pnpm install  # if needed
   pnpm dev
   ```

2. **Open Mission Control**:
   - Navigate to: http://localhost:3000
   - You should see your new journey(s) listed

3. **Test the journey**:
   - Click "Open" on your KYCP journey
   - It routes to `/preview-kycp/non-lux-1-1`
   - Verify KYCP components render correctly
   - Check visibility conditions work
   - Use Explain visibility (checkbox or `?explain=1`) to debug rules

### Step 6: Validate Components and Styling

1. **Check component rendering**:
   - Text inputs (string type) → KycpInput
   - Textareas (freeText type) → KycpTextarea
   - Dropdowns (lookup type) → KycpSelect
   - Numbers (integer/decimal) → KycpInput with type="number"
   - Dates → KycpInput with type="date"
   - Statements → KycpStatement (plain text)
   - Dividers → KycpDivider with title

2. **Verify KYCP compliance**:
   - NO radio buttons (all single-select uses dropdowns)
   - Field limits enforced:
     - string: max 1,024 chars
     - freeText: max 8,192 chars
     - integer: 0 to 2,147,483,647
     - decimal: precision 18, scale 2
   - Statements are plain text without borders/backgrounds
   - Field descriptions support HTML and bullet lists

### Step 7: Quality Checks

1) Conditions Report (Admin)
- From Mission Control (Admin), click “Conditions Report” on the journey card, or visit:
  - `/api/conditions-report/non-lux-1-1?format=html` (HTML table)
  - `/api/conditions-report/non-lux-1-1` (JSON)
- Flags unresolved keys, option mismatches (with aliasing), parse issues, and cycles.

2) Scenario Checks (CLI)
- From `apps/prototype`, run:
  ```bash
  pnpm scenarios
  ```
- Asserts key visibility paths (UK/non‑UK, USA forks) stay correct.

### Step 8: Document the Update

1. **Create a session context file**:
   ```bash
   vi Documents/01\ Areas/session-context/session-context-XXX.md
   ```

2. **Include key information**:
   ```markdown
   ---
   session_id: XXX
   date: YYYY-MM-DD
   facilitator: Your Name
   participants: [Your Name, Others]
   related_journeys: [your-journey-key-kycp]
   related_files: [
     "apps/prototype/data/incoming/YYYYMMDD_your_spreadsheet.xlsx",
     "apps/prototype/data/schemas/your-journey-key-kycp/schema-kycp.yaml"
   ]
   ---
   
   # Session Summary
   Goal: Import and create prototype for [Journey Name]
   
   ## Results
   - Fields imported: XXX
   - Internal fields: XXX
   - Conditional fields: XXX
   ```

## Troubleshooting

### Common Issues and Solutions

1. **Build errors with components**:
   - Check for deleted components (e.g., KycpRadio no longer exists)
   - Verify all imports in preview pages
   - Run `pnpm build` to catch syntax errors

2. **Schema not loading**:
   - Verify journey key in manifest matches exactly
   - Check file exists at correct path
   - Look for YAML syntax errors

3. **Fields not visible**:
   - Check `internal_only` flag isn't set
   - Verify visibility conditions
   - Check section grouping (`_section` field)

4. **Validation errors**:
   - Review regex patterns (some may be invalid)
   - Check required field settings
   - Verify data type mappings

5. **Component styling issues**:
   - Ensure CSS variables are defined in app.vue (not scoped)
   - Check component uses correct KYCP classes
   - Verify design tokens match KYCP platform

## Advanced Features

### Visibility Rules
- Grammar: equality only (`==`, `!=`) with AND/OR logic (no parentheses).
- OR is modeled as multiple rules; AND as multiple conditions in one rule.
- Case‑insensitive comparisons; values are canonicalized to controller options using a mapping `value_aliases` (e.g., `USA` → `United States`).

### Internal Fields
- Detected by "Action" column containing "internal"
- Or by dedicated internal column in mapping
- These fields are hidden from client view automatically

### Internal Fields
- Per-status visibility: invisible/read/write
- Global defaults with per-field overrides
- Buttons respect read-only states

## Best Practices

1. **Always run both importers** - Compare outputs to ensure consistency
2. **Test incrementally** - Import, test, fix, repeat
3. **Document changes** - Create session context files
4. **Preserve source references** - Keep ROW:XXX references for traceability
5. **Validate before deploy** - Run `pnpm build` to catch errors

### Complex Groups (Repeaters)
- Parent row has `DATA TYPE = Complex` → becomes a `type: complex` container in schema.
- Child rows reference the parent via the `COMPLEX` column (value = parent KEYNAME).
- UI renders a KycpRepeater; rows are stored as array items under the parent key.

## Quick Reference Commands

```bash
# Import Non‑Lux v1.1 (KYCP)
cd apps/prototype && python3 scripts/import_non_lux_1_1.py

# Start dev server
cd apps/prototype && pnpm dev

# Run scenario checks
cd apps/prototype && pnpm scenarios

# Build for production
cd apps/prototype && pnpm build

# Generate password hash for admin
cd apps/prototype && pnpm hash "YourPassword"
```

## Support

- Check existing journeys for examples: `non-lux-lp-demo-kycp`
- Review session contexts for patterns: `Documents/01 Areas/session-context/`
- Component documentation: `/kycp-components` page in running app
