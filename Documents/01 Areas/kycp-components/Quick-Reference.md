# KYCP Components Quick Reference

## Component Usage

### String Field (max 1,024 chars)
```vue
<KycpFieldWrapper label="Company Name" :required="true">
  <KycpInput v-model="data.name" :maxlength="1024" />
</KycpFieldWrapper>
```

### FreeText Field (max 8,192 chars)
```vue
<KycpFieldWrapper label="Description" help="Detailed description">
  <KycpTextarea v-model="data.description" :maxlength="8192" :rows="4" />
</KycpFieldWrapper>
```

### Integer Field (0 to 2,147,483,647)
```vue
<KycpFieldWrapper label="Employee Count">
  <KycpInput 
    v-model="data.employees" 
    type="number"
    :min="0"
    :max="2147483647"
    :step="1"
  />
</KycpFieldWrapper>
```

### Decimal Field (precision 18, scale 2)
```vue
<KycpFieldWrapper label="Annual Revenue">
  <KycpInput 
    v-model="data.revenue" 
    type="number"
    :step="0.01"
    @input="enforceDecimalScale"
  />
</KycpFieldWrapper>
```

### Date Field (DD/MM/YYYY)
```vue
<KycpFieldWrapper label="Date of Birth" :required="true">
  <KycpInput 
    v-model="data.dob" 
    type="date"
    placeholder="DD/MM/YYYY"
  />
</KycpFieldWrapper>
```

### Lookup Field (Dropdown only - NO radio buttons)
```vue
<KycpFieldWrapper label="Country" :required="true">
  <KycpSelect 
    v-model="data.country"
    :options="countryOptions"
    placeholder="Select..."
  />
</KycpFieldWrapper>

<script>
// Options must have value (code) and label
const countryOptions = [
  { value: 'GB', label: 'United Kingdom' },
  { value: 'US', label: 'United States' }
]
// Stores 'GB' not 'United Kingdom'
</script>
```

### Statement (Non-input)
```vue
<KycpStatement 
  html="<strong>Note:</strong> All fields are required. 
        See <a href='#'>guidelines</a> for details."
/>
```

### Divider/Title (Non-input)
```vue
<!-- With title -->
<KycpDivider title="Section 2: Financial Information" />

<!-- Simple line -->
<KycpDivider />
```

### Button (Non-input, triggers scripts)
```vue
<KycpButton 
  variant="primary"
  label="Submit"
  scriptId="submit_application"
  @trigger="handleScriptTrigger"
/>
```

### Complex Group (Repeater)
```vue
<KycpRepeater
  v-model="data.documents"
  item-label="Document"
  title-field="type"
>
  <template #form="{ item, save, cancel }">
    <KycpFieldWrapper label="Type">
      <KycpSelect v-model="item.type" :options="docTypes" />
    </KycpFieldWrapper>
    <KycpFieldWrapper label="Number">
      <KycpInput v-model="item.number" />
    </KycpFieldWrapper>
    <KycpButton @click="save">Save</KycpButton>
    <KycpButton @click="cancel">Cancel</KycpButton>
  </template>
</KycpRepeater>
```

## Data Structures

### Simple Fields
```json
{
  "companyName": "Acme Corp",
  "employees": 150,
  "revenue": 1000000.50,
  "incorporationDate": "15/03/2020",
  "country": "GB"
}
```

### Complex Groups
```json
{
  "documents": [
    {
      "type": "PASS",
      "number": "123456789",
      "expiry": "31/12/2030"
    },
    {
      "type": "DRVL",
      "number": "987654321",
      "expiry": "15/06/2028"
    }
  ]
}
```

## Visibility Rules

```javascript
// Schema defines visibility
{
  visibility: [
    {
      entity: "entity",
      conditions: [
        { sourceKey: "country", operator: "eq", value: "GB" },
        { sourceKey: "amount", operator: "neq", value: "0" }
      ],
      allConditionsMustMatch: true // AND logic
    }
  ]
}
```

## Status Rights

```javascript
// Per-field status rights
{
  statusRights: [
    { status: "draft", right: "write" },
    { status: "submitted", right: "read" },
    { status: "approved", right: "invisible" }
  ]
}
```

## Important Reminders

⛔ **NO RADIO BUTTONS** - They don't exist in KYCP. Use KycpSelect.

📏 **ENFORCE LIMITS** - Components have defaults but be explicit.

💾 **STORE CODES** - Lookups store option code, not label.

📅 **DATE FORMAT** - Always DD/MM/YYYY as string.

🔒 **READ-ONLY** - Buttons do nothing in read-only states.

🏗️ **MODAL** - Prototype-only, not a KYCP component.