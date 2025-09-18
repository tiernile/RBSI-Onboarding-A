# Session Context 017: Wicked Problem Areas CSV Implementation

**Date**: 2025-09-17
**Session Goal**: Create working prototype from wicked problem areas CSV data
**Status**: ✅ COMPLETED - Full working prototype with accordion organization

## Context & Request

User provided CSV file with 48 questions organized by 5 wicked problem areas:
- **Turnover** (2 questions)
- **Purpose of Business** (12 questions)
- **Source of Funds** (9 questions)
- **Account Activity** (7 questions)
- **Tax** (18 questions)

**Key Requirements**:
- Wicked problem area → accordion title
- Question → new Nile question text
- Helper → new Nile helper text
- Current Section → AS-IS section for auditability
- Field Type → links to appropriate KYCP components
- Merge with existing AS-IS field definitions for complete functionality

## Implementation Approach

### 1. CSV Data Processing
- **Source**: `P2140 - RBSI Onboarding wicked-problem-area-questions-sprint-2-testing-flow.csv`
- **Mapping**: Created `data/mappings/wicked-problem-areas.json`
- **Import Script**: `scripts/import_csv_wicked_problem_areas.py`

### 2. Field Enhancement Strategy
- **AS-IS Integration**: Loaded existing field definitions from previous schemas
- **Data Merging**: Combined CSV enhancements with AS-IS functionality (types, options, validation, visibility rules)
- **Audit Trail**: Preserved source row references and metadata

### 3. Schema Format Challenge & Solution

**❌ Initial Problem**: Generated schema in wrong format
- Used `items[]` array (old format)
- Missing `accordions[]` structure
- Frontend KYCP components couldn't render fields

**✅ Solution Discovery**: KYCP components require specific schema format
- **Working Format**: `fields[]` + `accordions[]` structure
- **Filename**: Must use `schema-kycp.yaml` (not `schema.yaml`)
- **Field Structure**: `key`, `type`, `options` as `{value, label}` objects
- **Accordion Organization**: Groups fields by wicked problem area

## Technical Implementation Details

### Schema Structure (Working Format)
```yaml
key: wicked-problem-areas
name: Wicked Problem Areas Sprint 2
version: 0.1.0
entity: entity
accordions:
  - key: turnover
    title: Turnover
    fields: [GENCashMngtAccPurpose, GENCashMngtAccTurnover]
  - key: purpose-of-business
    title: Purpose of Business
    fields: [field_Application_type_1_, GENIndicativeAppetiteCountryRegistration, ...]
fields:
  - key: GENCashMngtAccPurpose
    entity: entity
    style: field
    label: "What will you use this account for?" # New Nile text
    help: "This could include payments..." # New Nile helper
    type: freeText
    original:
      label: "Please advise what the account..." # AS-IS label
    _metadata:
      source_row_ref: "ROW:2|KEY:GENCashMngtAccPurpose"
      wicked_area: "Turnover"
      as_is_section: "Banking Requirements"
```

### Key Lessons Learned

**KYCP Schema Format Requirements**:
1. **Filename**: Use `schema-kycp.yaml` for accordion-based schemas
2. **Structure**: Must have both `fields[]` and `accordions[]` arrays
3. **Field Format**: `key` (not `id`), `type` (not `data_type`)
4. **Options**: Must be `{value, label}` objects, not simple strings
5. **Accordion Grouping**: Required for proper UI rendering

**Validation Pitfalls**:
- Server expects different formats for different schema types
- `items[]` format for basic schemas, `fields[]` + `accordions[]` for KYCP
- Field keys must be alphanumeric with underscores/hyphens only
- Invalid characters cause schema validation failures

## Results Achieved

### ✅ Working Prototype Available
- **Dashboard**: `http://localhost:3002/` (Testing group, alpha status)
- **Live Form**: `http://localhost:3002/preview-kycp/wicked-problem-areas`
- **Debug Mode**: `http://localhost:3002/preview-kycp/wicked-problem-areas?explain=1`

### ✅ Complete Functionality
- **5 Accordions** organized by wicked problem areas
- **48 Fields** with enhanced Nile questions/helpers
- **AS-IS Integration** with complete field definitions, validation, visibility
- **Audit Trail** with source references and metadata
- **Debug Tools** compatible (Explain Visibility, Conditions Report)

### ✅ Data Quality
- **Field Types**: Properly mapped (lookup, freeText, number, complex)
- **Options**: Converted to working `{value, label}` format
- **Validation**: All schema validation errors resolved
- **Enhancement Flags**: Clear distinction between Nile improvements and AS-IS data

## Files Created/Modified

**New Files**:
- `data/incoming/P2140 - RBSI Onboarding wicked-problem-area-questions-sprint-2-testing-flow.csv`
- `data/mappings/wicked-problem-areas.json`
- `data/schemas/wicked-problem-areas/schema-kycp.yaml`
- `scripts/import_csv_wicked_problem_areas.py`

**Modified Files**:
- `data/schemas/manifest.yaml` (added wicked-problem-areas journey)

## Next Steps & Recommendations

1. **Documentation Updates**: Update guide docs with KYCP schema format requirements
2. **Template Creation**: Create CSV import template for future problem area work
3. **Field Optimization**: Review complex fields for proper implementation
4. **Stakeholder Testing**: Use debug tools for validation with business users

## Critical Knowledge for Future Sessions

**Schema Format Debugging**:
1. Check filename: `schema-kycp.yaml` vs `schema.yaml`
2. Verify structure: `fields[]` + `accordions[]` vs `items[]`
3. API test: `curl http://localhost:3002/api/schema/journey-name | jq 'keys'`
4. Server logs: Check for "Invalid schema" errors in dev server output

**CSV Import Best Practices**:
1. Always merge with AS-IS field definitions for complete functionality
2. Use explicit column mapping - cannot be automated
3. Preserve audit trail with source row references
4. Organize by accordion structure for better UX

This session successfully demonstrated the complete CSV-to-prototype workflow with proper KYCP integration and wicked problem area organization.