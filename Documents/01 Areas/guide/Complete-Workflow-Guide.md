# Complete Workflow Guide - RBSI Onboarding Prototype

## Overview

This guide consolidates all workflows for the RBSI onboarding prototype system. It covers the complete journey from receiving a client spreadsheet to deploying a working KYCP-compliant prototype with advanced features including field grouping, complex fields, and debugging tools.

**Critical Success Factor**: Column mapping is the most important step and requires explicit user decisions based on domain knowledge. This cannot be automated.

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

#### 1.3 Create/Update Mapping (CRITICAL USER INPUT REQUIRED)
**This is the most critical step and requires explicit user decisions**

Column mapping cannot be automated and requires domain knowledge including:
- Understanding field meanings and relationships
- Deciding field types and validation rules
- Defining section organization and flow
- Setting up conditional logic and dependencies
- Configuring lookup values and options

Create `apps/prototype/data/mappings/journey-key.json`:
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
    "action": "Action",
    "complex": "COMPLEX",
    "complex_identifier": "COMPLEX IDENTIFIER"
  },
  "lookups_sheet": "Lookup Values",
  "lookups": {},
  "value_aliases": {
    "USA": "United States",
    "UK": "United Kingdom"
  }
}
```

### Phase 2: Import and Generation

#### 2.1 Run Importer
For current journeys, use the appropriate import script:
```bash
cd apps/prototype
# For Non-Lux v1.1
python3 scripts/import_non_lux_1_1.py

# For general KYCP imports
python3 scripts/import_xlsx_kycp.py --mapping [mapping] --input [xlsx] --sheet [sheet] --lookups-sheet [lookups] --journey-key [key]
```

#### 2.2 Verify Output
Check generated files:
- Schema: `apps/prototype/data/schemas/[journey-key]/schema-kycp.yaml`
- Console output: include/exclude summary and unresolved lookups
- Field organization and grouping applied
- Complex fields identified for implementation

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

### Phase 4: Field Organization & Advanced Features

#### 4.1 Field Grouping Implementation
The system supports field grouping to reduce cognitive load:
- Related fields are visually organized into logical groups
- Dependency chains (parent→child→grandchild) are preserved
- Groups appear with clear visual separation and hierarchy
- Results in up to 85% cognitive load reduction in complex sections

#### 4.2 Complex Fields Implementation
For repeatable field groups:
- Parent fields marked as `type: complex` in schema
- Child fields defined in `children[]` array
- UI renders with add/remove functionality
- Data stored as array items under parent key

#### 4.3 Flow Optimization
Apply backwards dependency elimination:
- Ensure questions only depend on earlier answers
- Move critical branching decisions early in flow
- Place unconditional fields before conditional ones within sections
- Use dependency chain analysis to optimize field ordering

### Phase 5: Configure Prototype

#### 5.1 Add to Manifest
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

#### 5.2 Test Locally
```bash
cd apps/prototype
pnpm install  # if first time
pnpm dev
```

Navigate to http://localhost:3000:
- Check journey appears on Mission Control
- Click "Open" to test the form
- Verify KYCP components render correctly
- Test visibility conditions; use **Explain Visibility** toggle or append `?explain=1`
- Verify field grouping displays correctly
- Test complex field add/remove functionality
- Check validation works and error messages are clear

### Phase 6: Quality Assurance & Debugging

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

#### 6.3 Conditions Report & Debugging
**Essential admin tool for validating conditional logic**:
- From Mission Control (Admin), click "Conditions Report" on journey card
- HTML format: `/api/conditions-report/[journey-key]?format=html`
- JSON format: `/api/conditions-report/[journey-key]`
- Flags: unresolved keys, option mismatches, parse errors, dependency cycles
- Use with **Explain Visibility** mode for comprehensive debugging

#### 6.4 Field Organization Validation
- Verify field grouping reduces cognitive load
- Check dependency chains are preserved
- Ensure complex fields render with proper add/remove functionality
- Validate flow optimization eliminates backwards dependencies

#### 5.4 Accessibility
Ensure:
- All fields have labels
- Required fields marked with *
- Error messages are clear
- Tab order is logical
- Screen reader compatible

### Phase 7: Documentation

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

### Phase 8: Deployment (Optional)

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

## Quality Improvement Rules

### Flow Design Principles
1. **Backwards Dependency Elimination**: Questions should only depend on earlier answers
2. **Decision Points First**: Critical branching decisions come as early as possible
3. **Natural Information Flow**: Follow logical business conversation order
4. **Cognitive Load Management**: Simple decisions before complex ones

### Field Organization Best Practices
1. **Field Grouping**: Cluster related fields for visual organization
2. **Dependency Preservation**: Maintain parent→child→grandchild relationships
3. **Unconditional First**: Place unconditional fields before conditional ones within sections
4. **Complex Field Implementation**: Use repeatable components for multi-entry fields

### Mapping Quality Guidelines
1. **User Input Required**: Never assume mapping can be automated
2. **Domain Knowledge Critical**: Understanding field relationships is essential
3. **Section Organization Impact**: Mapping decisions affect entire user experience
4. **Validation Setup**: Proper mapping prevents downstream issues

## Quick Reference

### Common Commands

```bash
# Import Non-Lux v1.1 (current)
cd apps/prototype && python3 scripts/import_non_lux_1_1.py

# Import general KYCP format
python3 scripts/import_xlsx_kycp.py --mapping [mapping] --input [xlsx] --sheet [sheet] --lookups-sheet [lookups] --journey-key [key]

# Start dev server
cd apps/prototype && pnpm dev

# Run scenario validation
cd apps/prototype && pnpm scenarios

# Field analysis
cd apps/prototype && pnpm fields

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
- KYCP Journey with Debug: http://localhost:3000/preview-kycp/[journey-key]?explain=1
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

### Critical Success Factors
1. **Column Mapping First** - Most critical step requiring explicit user decisions
2. **Domain Knowledge Essential** - Cannot automate field relationships and meanings
3. **Test with Explain Visibility** - Essential debugging tool for conditional logic
4. **Use Conditions Report** - Validate all conditional dependencies before deployment

### Quality & Process
5. **Field Grouping Implementation** - Reduces cognitive load significantly
6. **Flow Optimization** - Eliminate backwards dependencies for better UX
7. **Complex Fields Setup** - Implement repeatable components where needed
8. **Incremental Testing** - Import, test, fix, repeat
9. **Document Decisions** - Session contexts provide valuable audit trail
10. **Stakeholder Review** - Validate mapping decisions and flow changes

## Support Resources

- Tone of Voice Guidelines: `Documents/01 Areas/tone-of-voice/README.md`
- Component Documentation: `/kycp-components` page
- Session Contexts: `Documents/01 Areas/session-context/`
- This Guide: `Documents/01 Areas/guide/Complete-Workflow-Guide.md`

---

*Last Updated: 2025-09-17*
