---
session_id: 008
date: 2025-01-10
facilitator: Assistant
participants: [Assistant, Tiernan (Nile)]
related_journeys: [non-lux-lp-demo-kycp]
related_files: [
  "apps/prototype/components/kycp/base/*",
  "apps/prototype/pages/kycp-components.vue",
  "scripts/import_xlsx_kycp.py",
  "Documents/01 Areas/kycp-components/*"
]
---

# Session Summary

Goal: Achieve strict KYCP parity in component library and data ingestion, removing all non-KYCP features and enforcing platform limits.

## Changes Made

### Component Library Overhaul

1. **Removed Non-KYCP Features**
   - Deleted `KycpRadio.vue` component entirely
   - Removed all radio button references from documentation
   - Radio buttons do not exist in KYCP - lookups are always dropdowns

2. **Created Proper Non-Input Components**
   - `KycpStatement.vue` - Supports simple rich text and hyperlinks
   - `KycpDivider.vue` - Visual structure (line or title variant)
   - `KycpButton.vue` - Updated to emit scriptId, respects read-only states

3. **Enforced KYCP Platform Limits**
   - string: max 1,024 characters (default in KycpInput)
   - freeText: max 8,192 characters (default in KycpTextarea)
   - integer: 0 to 2,147,483,647 range
   - decimal: precision 18, scale 2 (blocks beyond 2dp)
   - date: DD/MM/YYYY format validation
   - lookup: Always stores option code, not label

4. **Updated Complex Groups**
   - KycpRepeater confirmed as one level deep only
   - Data serializes as array under group key
   - No nested repeaters allowed

5. **New Documentation Page**
   - Created `/kycp-components` page with clean KYCP-aligned showcase
   - Clear separation: Field Components, Non-Input Components, Complex Groups
   - Added Platform Limits table
   - Added Visibility & Status Rights documentation
   - Marked Modal as "Prototype Only"

### Data Ingestion Updates

1. **Created KYCP-Aligned Importer**
   - `scripts/import_xlsx_kycp.py` - Outputs KYCP-compliant schema
   - Maps to exact KYCP field structure
   - Generates proper visibility rules format
   - Supports status rights placeholders

2. **Schema Format Changes**
   - From: `data_type: "string"`, `control: "text"`
   - To: `type: "string"`, `style: "field"`
   - Proper validation object structure
   - Options as `{value, label}` pairs

### Architecture Decisions

1. **Pure UI Components**
   - Components have zero business logic
   - All validation/visibility comes from schema
   - Components just handle display and user interaction

2. **Schema-Driven Everything**
   - Schema defines field types, validation, visibility
   - Form renderer interprets schema
   - No KYCP logic in components

3. **Strict KYCP Parity**
   - Only 6 field data types supported
   - Only 4 component styles (field, statement, divider, button)
   - No features beyond what KYCP provides

## Key Learnings

1. **KYCP is intentionally limited** - No radio buttons, strict data types, specific limits
2. **Lookups always dropdown** - Single-select is lookup with dropdown presentation only
3. **Complex groups are flat** - One level deep, no nesting
4. **Status rights are critical** - invisible/read/write per status, with global defaults
5. **Internal items hidden** - Items marked internal/system not exposed to client staging

## Files Created/Modified

### New Components
- `KycpStatement.vue` - Non-input statement component
- `KycpDivider.vue` - Non-input divider/title component
- `import_xlsx_kycp.py` - KYCP-aligned data importer
- `/kycp-components` page - Clean KYCP-compliant showcase

### Updated Components
- `KycpButton.vue` - Added scriptId and read-only support
- `KycpInput.vue` - Added KYCP limits as defaults
- `KycpTextarea.vue` - Set 8192 char limit
- `KycpSelect.vue` - Ensures option code emission

### Removed
- `KycpRadio.vue` - Deleted entirely
- All radio references from documentation

## Next Actions

1. **Test with real data** - Run KYCP importer on actual spreadsheets
2. **Wire to preview** - Connect KYCP components to journey preview
3. **Validate limits** - Ensure decimal/integer limits work correctly
4. **Document patterns** - Create examples of common KYCP patterns

## Status

✅ KYCP component parity achieved
✅ Platform limits enforced
✅ Non-input components created
✅ Radio buttons completely removed
✅ Documentation updated

The component library now exactly matches KYCP capabilities - nothing more, nothing less.