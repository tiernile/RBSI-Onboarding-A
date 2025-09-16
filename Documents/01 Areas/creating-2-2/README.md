# Creating Version 2.2 - Paul's Structure Suggestions

## Overview
This area tracks the development of **Non-Lux LP v2.2** prototype focusing on Paul's structural reorganization suggestions from the spreadsheet.

## Key Distinctions from v2.1
- **v2.1**: Nile team's content suggestions (improved labels, help text)
- **v2.2**: Paul's structural suggestions (field ordering, section organization)
- **Content**: Keep original v1.1 labels/help as primary (AS-IS approach)
- **Structure**: Apply Paul's B-section hierarchy and question ordering

## Paul's Structural Columns
- **PAUL Question Order**: Field ordering suggestions within sections
- **PAUL Section Suggestion**: New section organization (B1, B2, B4, B5, B7, etc.)

## Paul's Section Structure Observed
- **B1**: Pre-App Qs
- **B2**: Bank Relationship  
- **B4**: Introduction of Applicant
- **B4.1**: Introduction of Applicant - Introducer / Contact Details
- **B5**: Applicant Details
- **B7**: Controlling Parties
- **B12**: Your Requirements

## Testing Focus
Test Paul's suggested information architecture and flow to evaluate:
1. **Logical grouping**: Do Paul's sections make sense to users?
2. **Field ordering**: Is the suggested sequence intuitive?
3. **Section hierarchy**: Does the B-prefix structure work effectively?
4. **Comparison**: How does Paul's structure compare to current v1.1 flow?

## Files in This Area
- `README.md` - This overview document
- `paul-analysis.md` - Analysis of Paul's structural suggestions
- `section-mapping.md` - Mapping of fields to Paul's B-sections
- `progress-tracking.md` - Development progress log

## Related System Files
- Schema: `apps/prototype/data/schemas/non-lux-lp-2-2/schema-kycp.yaml`
- Mapping: `apps/prototype/data/mappings/non-lux-lp-2-2.json` 
- Import Script: `apps/prototype/scripts/import_non_lux_2_2.py`

## Status
- **Started**: 2025-09-16
- **Phase**: 1 - Analysis & Setup
- **Focus**: Paul's structural reorganization vs content changes
- **Baseline**: v1.1 content with Paul's structural suggestions applied

## Note on Naming
The existing `Documents/01 Areas/creating-2-2` contains v2.1 work (should have been `creating-2-1`). This new `creating-2-2` directory is correctly named for v2.2 work.