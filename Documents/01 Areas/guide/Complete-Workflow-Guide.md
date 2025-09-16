# Complete Workflow Guide - RBSI Onboarding Prototype

## Overview

This guide consolidates all workflows for the RBSI onboarding prototype system. It covers the complete journey from receiving a client spreadsheet to deploying a working KYCP-compliant prototype with tone-of-voice analysis.

## System Architecture

```
RBSI-onboarding/
├── apps/prototype/          # Nuxt 3 application
│   ├── components/kycp/     # KYCP-compliant components
│   ├── pages/              # Application pages
│   ├── server/             # API endpoints (includes Conditions Report)
│   └── data/               # All data files
│       ├── incoming/       # Source spreadsheets
│       ├── mappings/       # Column mappings
│       ├── schemas/        # Generated schemas
│       └── generated/      # Reports and analysis
├── scripts/                # Processing tools
│   ├── import_xlsx.py      # Standard importer
│   ├── import_non_lux_1_1.py # KYCP-aligned importer for Non‑Lux v1.1
│   └── analyze_tone.py     # Tone analysis tool
└── Documents/01 Areas/     # Documentation
    ├── guide/              # User guides
    ├── tone-of-voice/      # Content guidelines
    └── session-context/    # Work logs

```

## Complete Workflow

### Phase 1: Data Preparation

#### 1.1 Receive Spreadsheet
```bash
# Place in incoming directory with date prefix
cp client_spreadsheet.xlsx apps/prototype/data/incoming/YYYYMMDD_descriptive_name.xlsx
```

#### 1.2 Verify Structure
Check the spreadsheet has:
- Main data sheet (e.g., "LP Proposal")
- Lookup values sheet
- Required columns: KEYNAME, FIELD NAME, DATA TYPE, MANDATORY, VISIBILITY

#### 1.3 Create/Update Mapping
If no mapping exists, create `apps/prototype/data/mappings/journey-key.json`:
```json
{
  "sheet": "Main Sheet Name",
  "filters": {
    "PROGRAMME": "Filter Value",
    "ENTITY": "Filter Value"
  },
  "columns": {
    "id": "KEYNAME",
    "label": "FIELD NAME",
    "data_type": "DATA TYPE",
    "mandatory": "MANDATORY",
    "visibility": "VISIBILITY CONDITION/GROUP NAME",
    "action": "Action"
  },
  "lookups_sheet": "Lookup Values",
  "lookups": {}
}
```

### Phase 2: Import and Generation

#### 2.1 Run Importer (KYCP)
```bash
cd apps/prototype
python3 scripts/import_non_lux_1_1.py
```

#### 2.2 Verify Output
Check generated files:
- Schema: `apps/prototype/data/schemas/non-lux-1-1/schema-kycp.yaml`
- Console output: include/exclude summary and unresolved lookups

### Phase 3: Tone Analysis

#### 3.1 Run Analysis
```bash
python3 scripts/analyze_tone.py \
  --schema apps/prototype/data/schemas/journey-key-kycp/schema-kycp.yaml \
  --output analysis/journey_tone_analysis.csv \
  --summary
```

#### 3.2 Review Results
1. Open CSV in spreadsheet application
2. Review each suggestion
3. Mark decisions: Accept/Reject/Modified
4. Add notes for rationale
5. Save for audit trail

#### 3.3 Apply Improvements
Based on accepted changes:
- Update source spreadsheet for next import
- Or manually edit schema YAML
- Document significant changes

### Phase 4: Configure Prototype

#### 4.1 Add to Manifest
Edit `apps/prototype/data/schemas/manifest.yaml`:
```yaml
active:
  - key: journey-key-kycp
    name: Journey Display Name
    version: 1.0.0
    variant: KYCP
    owner: "@yourname"
    display:
      group: Funds
      order: 10
      visible: true
      status: beta
```

#### 4.2 Test Locally
```bash
cd apps/prototype
pnpm install  # if first time
pnpm dev
```

Navigate to http://localhost:3000:
- Check journey appears on Mission Control
- Click "Open" to test the form
- Verify KYCP components render correctly
- Test visibility conditions; use Explain visibility (checkbox or `?explain=1`)
- Check validation works

### Phase 5: Quality Assurance

#### 5.1 Component Compliance
Verify all fields use correct KYCP components:
- String → KycpInput (max 1,024 chars)
- FreeText → KycpTextarea (max 8,192 chars)
- Integer → KycpInput type="number"
- Decimal → KycpInput type="number" step="0.01"
- Date → KycpInput type="date"
- Lookup → KycpSelect (NO radio buttons)

#### 5.2 Tone of Voice
Check questions follow guidelines:
- ✅ Under 20 words
- ✅ Use "you/your" not "the entity"
- ✅ Active voice
- ✅ No unexplained jargon
- ✅ One idea per sentence

#### 5.3 Conditions and Lints
Use the Conditions Report to review conditionality:
- HTML: `/api/conditions-report/non-lux-1-1?format=html`
- JSON: `/api/conditions-report/non-lux-1-1`
- Flags unresolved keys, option mismatches (with aliasing), parse errors (e.g., operator tokens inside values), and cycles.

#### 5.4 Accessibility
Ensure:
- All fields have labels
- Required fields marked with *
- Error messages are clear
- Tab order is logical
- Screen reader compatible

### Phase 6: Documentation

#### 6.1 Create Session Context
Document the work in `Documents/01 Areas/session-context/session-context-XXX.md`:
```markdown
---
session_id: XXX
date: YYYY-MM-DD
facilitator: Your Name
participants: [Names]
related_journeys: [journey-key-kycp]
related_files: [
  "apps/prototype/data/incoming/YYYYMMDD_file.xlsx",
  "apps/prototype/data/schemas/journey-key-kycp/schema-kycp.yaml"
]
---

# Session Summary
Goal: Import and create prototype for [Journey Name]

## Results
- Fields imported: XXX
- Internal fields: XXX  
- Tone issues found: XXX
- Issues resolved: XXX
```

#### 6.2 Update Handover Docs
If significant changes, update relevant handover documents

### Phase 7: Deployment (Optional)

#### 7.1 Build for Production
```bash
cd apps/prototype
pnpm build
```

#### 7.2 Deploy to Vercel
```bash
vercel --prod
```

Set environment variables:
- `NUXT_ADMIN_PASSWORD_HASH` - For admin features

## Quick Reference

### Common Commands

```bash
# Import KYCP format
python3 scripts/import_xlsx_kycp.py --mapping [mapping] --input [xlsx] --sheet [sheet] --lookups-sheet [lookups] --journey-key [key]

# Analyze tone
python3 scripts/analyze_tone.py --schema [schema] --output [csv] --summary

# Start dev server
cd apps/prototype && pnpm dev

# Build for production
cd apps/prototype && pnpm build
```

### File Locations

| Type | Location |
|------|----------|
| Incoming spreadsheets | `apps/prototype/data/incoming/` |
| Mappings | `apps/prototype/data/mappings/` |
| Schemas | `apps/prototype/data/schemas/` |
| Reports | `apps/prototype/data/generated/` |
| Components | `apps/prototype/components/kycp/` |
| Pages | `apps/prototype/pages/` |

### Key URLs (Development)

- Mission Control: http://localhost:3000
- KYCP Journey: http://localhost:3000/preview-kycp/[journey-key]
- Conditions Report: http://localhost:3000/api/conditions-report/[journey-key]?format=html
- Component Showcase: http://localhost:3000/kycp-components
- Admin Login: http://localhost:3000 (click Admin)

## Troubleshooting

### Import Issues
- **Missing columns**: Check mapping JSON matches spreadsheet headers
- **Invalid regex**: Will be logged and removed automatically
- **Missing lookups**: Check lookups sheet name and content

### Build Errors
- **Component not found**: Check for deleted components (e.g., KycpRadio)
- **Template syntax**: Watch for nested quotes in attributes
- **CSS variables**: Must be defined in app.vue (not scoped)

### Tone Analysis
- **No issues found**: Rare but possible for simple schemas
- **Too many issues**: Focus on High severity first
- **Suggestions unclear**: Review and create custom rewrite

## Best Practices

1. **Always run both importers** - Compare outputs
2. **Run tone analysis immediately** - Catch issues early
3. **Keep CSV reports** - Audit trail for decisions
4. **Test incrementally** - Import, test, fix, repeat
5. **Document everything** - Session contexts are valuable
6. **Review with stakeholders** - Get buy-in on tone changes
7. **Version control schemas** - Track changes over time

## Support Resources

- Tone of Voice Guidelines: `Documents/01 Areas/tone-of-voice/README.md`
- Component Documentation: `/kycp-components` page
- Session Contexts: `Documents/01 Areas/session-context/`
- This Guide: `Documents/01 Areas/guide/Complete-Workflow-Guide.md`

---

*Last Updated: 2025-01-11*
