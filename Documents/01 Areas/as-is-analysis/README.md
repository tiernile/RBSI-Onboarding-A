# As-Is Journey Analysis

This directory contains the analysis, mapping, and documentation for recreating the current KYCP as-is journey.

## Purpose

Create a fully auditable process to:
1. Analyze the existing KYCP form implementation
2. Map form fields to master spreadsheet questions
3. Build a cleaned schema with all known metadata
4. Enable recreation of the current journey with KYCP-faithful components

## Directory Structure

```
as-is-analysis/
├── README.md                     # This file
├── field-mapping.md              # HTML ↔ Spreadsheet field mapping
├── component-analysis.md         # KYCP component patterns and behaviors
├── discrepancy-report.md        # Fields that don't match or are missing
├── implementation-notes.md      # Technical decisions and platform gaps
└── audit-trail.md              # Complete transformation documentation
```

## Key Files

### Field Mapping (`field-mapping.md`)
- Maps HTML form questions to spreadsheet KEYNAMEs
- Documents field types, validation rules, and dependencies
- Provides bidirectional lookup capability

### Component Analysis (`component-analysis.md`)
- Documents KYCP component patterns found in HTML
- Specifications for faithful component recreation
- Props, events, and behavioral requirements

### Discrepancy Report (`discrepancy-report.md`)
- Fields present in HTML but not in spreadsheet
- Fields in spreadsheet but not implemented in HTML
- Mismatched field types or validation rules

## Process Overview

1. **Extract**: Parse HTML to identify all form fields and components
2. **Analyze**: Map spreadsheet data model to form implementation
3. **Document**: Create comprehensive mapping with full metadata
4. **Validate**: Identify and document any discrepancies
5. **Implement**: Build schema and components for recreation

## Source References

- HTML Form: `/Documents/01 Areas/As-is/Project Stealth Code Questions (1).html`
- Master Spreadsheet: `/data/incoming/20250828_draft-master-spreadsheet.xlsx`
- Generated Schema: `/data/schemas/as-is-journey/schema.yaml`

## Audit Trail

All transformations are documented with:
- Source reference (HTML element, spreadsheet row)
- Transformation logic applied
- Validation of output against source
- Sign-off checkpoints

## Success Metrics

- ✅ 100% of HTML fields identified and documented
- ✅ All spreadsheet questions mapped or flagged
- ✅ Component behaviors accurately specified
- ✅ Full traceability from source to implementation