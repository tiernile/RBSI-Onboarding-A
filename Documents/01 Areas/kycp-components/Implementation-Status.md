# KYCP Components Implementation Status

Last Updated: 2025-01-10

## ✅ Completed Components

### Field Components (Data Types)
All 6 KYCP data types are implemented with correct limits:

| Component | KYCP Type | Status | Limits Enforced |
|-----------|-----------|--------|-----------------|
| KycpInput (text) | string | ✅ Complete | Max 1,024 chars |
| KycpTextarea | freeText | ✅ Complete | Max 8,192 chars |
| KycpInput (number) | integer | ✅ Complete | 0 to 2,147,483,647 |
| KycpInput (decimal) | decimal | ✅ Complete | Precision 18, scale 2 |
| KycpInput (date) | date | ✅ Complete | DD/MM/YYYY format |
| KycpSelect | lookup | ✅ Complete | Stores option code |

### Non-Input Components
All KYCP non-input styles implemented:

| Component | KYCP Style | Status | Notes |
|-----------|------------|--------|-------|
| KycpStatement | statement | ✅ Complete | Supports rich text & links |
| KycpDivider | divider/title | ✅ Complete | Line or title variant |
| KycpButton | button | ✅ Complete | Emits scriptId, respects read-only |

### Complex Components

| Component | Purpose | Status | Notes |
|-----------|---------|--------|-------|
| KycpRepeater | Complex groups | ✅ Complete | One level deep, array storage |
| KycpFieldWrapper | Field container | ✅ Complete | Label, help, error, required indicator |
| KycpSection | Section grouping | ✅ Complete | For demo purposes |
| KycpModal | Upload dialogs | ⚠️ Prototype Only | Not a KYCP feature |

## ❌ Removed Components

| Component | Reason for Removal |
|-----------|--------------------|
| KycpRadio | Radio buttons do not exist in KYCP |
| Field wrapper components | Unnecessary abstraction layer |

## 📋 Implementation Details

### Strict KYCP Rules Enforced

1. **No Radio Buttons**
   - All single-select fields use Lookup with dropdown presentation
   - Radio component completely removed from codebase

2. **Platform Limits**
   ```typescript
   // Default limits in components
   string: maxlength = 1024
   freeText: maxlength = 8192  
   integer: min = 0, max = 2147483647
   decimal: precision = 18, scale = 2
   date: format = "DD/MM/YYYY"
   ```

3. **Data Storage**
   - Simple fields: Flat map keyed by fieldname
   - Complex groups: Array of objects under group key
   - Lookups: Always store option code, not label
   - Dates: Stored as DD/MM/YYYY strings

4. **Visibility Rules**
   - Simple equals/not-equals comparisons
   - Multiple conditions use AND logic
   - Target single fields or whole groups
   - Hidden required fields don't block submission

5. **Status Rights**
   - Per status: invisible, read, write
   - Global mode can blanket-apply
   - Read-only states make buttons no-op

## 🔄 Data Flow

```
Spreadsheet (XLSX)
    ↓
import_xlsx_kycp.py
    ↓
KYCP-format schema.yaml
    ↓
Schema-driven form renderer
    ↓
Pure UI Components (no logic)
```

## 📁 File Structure

```
/apps/prototype/
  /components/kycp/base/
    KycpInput.vue         # string, integer, decimal, date
    KycpTextarea.vue      # freeText
    KycpSelect.vue        # lookup (dropdown only)
    KycpStatement.vue     # statement (non-input)
    KycpDivider.vue       # divider/title (non-input)
    KycpButton.vue        # button (triggers scripts)
    KycpRepeater.vue      # complex groups
    KycpFieldWrapper.vue  # field container
    KycpModal.vue         # prototype-only
  /pages/
    kycp-components.vue   # Component showcase

/scripts/
  import_xlsx_kycp.py     # KYCP-aligned importer

/Documents/01 Areas/kycp-components/
  README.md               # Overview
  Spec.md                 # KYCP specification
  Implementation-Status.md # This file
```

## 🚀 Usage

### Component Library
Visit `/kycp-components` to see all components with:
- Live examples
- Platform limits
- Code samples
- Data structures

### Import Data
```bash
python3 scripts/import_xlsx_kycp.py \
  --mapping apps/prototype/data/mappings/journey.json \
  --input apps/prototype/data/incoming/spreadsheet.xlsx \
  --sheet "Sheet Name" \
  --journey-key journey-name
```

## ⚠️ Important Notes

1. **Components are pure UI** - No business logic
2. **Schema drives everything** - Validation, visibility, rights
3. **KYCP parity is strict** - No extra features
4. **Modal is prototype-only** - Not a KYCP component
5. **Radio buttons don't exist** - Use lookup/dropdown

## ✅ Acceptance Criteria Met

- [x] Radio removed completely, lookups are dropdown only
- [x] Platform limits enforced by default
- [x] Repeater serialization matches complex-type array model
- [x] Non-input components documented (statement, divider, button)
- [x] Visibility and status rights documented
- [x] Modal marked as prototype-only
- [x] All components emit proper data format
- [x] Read-only states respected