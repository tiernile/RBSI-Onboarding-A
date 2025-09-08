# KYCP Component Analysis

Based on HTML analysis of the as-is form implementation, here are the KYCP component patterns identified and their specifications for faithful recreation.

## Component Types Identified

### 1. v-select Dropdown (`KycpSelect`)
**HTML Pattern**: `<div class="v-select vs--single vs--searchable dropdownSelect">`

**Key Features**:
- Searchable dropdown with typeahead
- "None Selected" default state
- Clear button when value selected
- Dropdown arrow indicator
- Loading spinner capability

**Props**:
```typescript
interface KycpSelectProps {
  options: string[] | { label: string; value: any }[]
  placeholder?: string // Default: "None Selected"
  searchable?: boolean // Default: true
  clearable?: boolean // Default: true
  disabled?: boolean
  mandatory?: boolean
  modelValue?: any
}
```

### 2. Text Input (`KycpInput`)
**HTML Pattern**: `<input type="text" class="form-control col-12 mb-2">`

**Variants**:
- Standard text: `txtInput-*`
- Decimal input: `txtDecimalInput-*`

**Props**:
```typescript
interface KycpInputProps {
  type?: 'text' | 'decimal' | 'email'
  mandatory?: boolean
  disabled?: boolean
  maxLength?: number
  pattern?: string // For validation
  placeholder?: string
  modelValue?: string
}
```

### 3. Textarea (`KycpTextarea`)
**HTML Pattern**: `<textarea class="form-control col-12 mb-2" rows="6">`

**Props**:
```typescript
interface KycpTextareaProps {
  rows?: number // Default: 6
  cols?: number // Default: 20
  mandatory?: boolean
  disabled?: boolean
  maxLength?: number
  placeholder?: string
  modelValue?: string
}
```

### 4. Complex Field Container (`KycpComplexField`)
**HTML Pattern**: `<ul class="fieldContainer effisComplex effUl">`

**Description**: Container for grouped/repeatable field sets

**Props**:
```typescript
interface KycpComplexFieldProps {
  title: string
  fields: FieldDefinition[]
  repeatable?: boolean
  addButtonText?: string
}
```

### 5. Toggle Switch (`KycpToggle`)
**HTML Pattern**: `<input class="form-check-input" type="checkbox" role="switch">`

**Props**:
```typescript
interface KycpToggleProps {
  label: string
  size?: 'small' | 'large'
  modelValue?: boolean
}
```

## Common Patterns

### Field Wrapper Structure
All fields follow this pattern:
```html
<li class="mt-3">
  <div>
    <!-- Label with mandatory indicator -->
    <div class="d-flex justify-content-between">
      <span class="col-12 text-break">Question Text*</span>
      <span style="display: none"><!-- Warning icon --></span>
    </div>
    <!-- Help text (optional) -->
    <label class="col-12 text-break">Help text</label>
    <!-- Input component -->
    <span><!-- Component here --></span>
  </div>
</li>
```

### Mandatory Field Indicator
- Asterisk (*) appended to question text
- Warning icon capability (hidden by default)

### Visibility Conditions
- Applied via `style="display: none"` on container
- Conditional rendering based on other field values

## Component Behaviors

### 1. Validation
- On blur for individual fields
- On submit for form-level validation
- Error state with warning icon display

### 2. Save State
- "SAVE FIELDS" button in top toolbar
- Saves current form state without submission

### 3. Field Dependencies
- Fields can be shown/hidden based on other field values
- Complex visibility conditions support

### 4. Add New Option
- Some dropdowns have "ADD NEW..." capability
- Displayed as `<div class="btnAddItem">`

## Style Classes

### Bootstrap Integration
- `form-control`: Standard form input styling
- `col-12`: Full width
- `mb-2`: Bottom margin
- `mt-3`: Top margin for field containers
- `text-break`: Text wrapping for long labels

### Custom Classes
- `dropdownSelect`: Custom dropdown styling
- `fieldContainer`: Complex field container
- `effisComplex`: Complex field marker
- `warningColor`: Error/warning state

## Implementation Requirements

### 1. Accessibility
- Proper ARIA labels (`aria-labelledby`, `aria-label`)
- Role attributes for custom components
- Keyboard navigation support

### 2. State Management
- v-model compatible for Vue integration
- Emit events: `update:modelValue`, `blur`, `focus`
- Validation state tracking

### 3. Error Handling
- Display warning icon on validation error
- Error message placement below field
- Highlight field border in error state

## Component File Structure

```
apps/prototype/components/kycp/
├── KycpSelect.vue
├── KycpInput.vue
├── KycpTextarea.vue
├── KycpComplexField.vue
├── KycpToggle.vue
├── KycpFieldWrapper.vue    # Common wrapper for all fields
└── index.ts                 # Export all components
```

## Next Steps

1. Create base component implementations
2. Add validation logic and error states
3. Implement visibility condition engine
4. Add save state functionality
5. Create component showcase page for testing