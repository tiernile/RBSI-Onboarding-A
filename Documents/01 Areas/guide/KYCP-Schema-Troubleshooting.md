# KYCP Schema Format Troubleshooting Guide

When journeys appear in the API but fields are invisible in the frontend UI, the issue is usually KYCP schema format compatibility.

## Quick Diagnosis

### 1. Check API Response Format
```bash
curl http://localhost:3002/api/schema/<journey-name> | jq 'keys'
```

**Expected Results**:
- ✅ **Working**: `["accordions", "entity", "fields", "key", "name", "version"]`
- ❌ **Not Working**: `["items", "key", "name", "version"]`
- ❌ **Error**: `["data", "stack", "statusCode", "statusMessage"]`

### 2. Check Schema Filename
- ✅ **KYCP Accordions**: `data/schemas/<journey>/schema-kycp.yaml`
- ❌ **Basic Items**: `data/schemas/<journey>/schema.yaml`

### 3. Check Server Logs
```bash
# Look for validation errors in dev server output
pnpm dev
# Watch for: "Invalid schema for journey <name>"
```

## Schema Format Requirements

### KYCP Accordions Format (Required for UI)
```yaml
key: journey-name
name: Journey Display Name
version: 0.1.0
entity: entity
accordions:
  - key: section-key
    title: "Section Title"
    fields: [field1, field2, field3]
fields:
  - key: field1  # NOT "id"
    entity: entity
    style: field
    label: "Question text"
    type: lookup  # NOT "data_type"
    options:  # Must be objects, not strings
      - value: "Option1"
        label: "Option1"
    validation: {}
    _metadata: {...}
```

### Basic Items Format (Limited UI Support)
```yaml
key: journey-name
name: Journey Display Name
version: 0.1.0
items:
  - id: field1  # NOT "key"
    label: "Question text"
    data_type: enum  # NOT "type"
    options: ["Option1", "Option2"]  # Simple strings
```

## Common Issues & Fixes

### Issue 1: Fields Invisible in Frontend
**Symptoms**: API returns data, but KYCP preview shows no fields
**Cause**: Using `items[]` format instead of `fields[]` + `accordions[]`
**Fix**:
1. Rename file to `schema-kycp.yaml`
2. Convert structure to KYCP format
3. Add accordions array

### Issue 2: Schema Validation Errors
**Symptoms**: Server logs show "Invalid schema" errors
**Causes & Fixes**:
- **Invalid field keys**: Must be `^[a-zA-Z][a-zA-Z0-9_-]*$`
- **Invalid data types**: Use `string|number|boolean|date|enum` (not `complex`)
- **Wrong options format**: Use `{value, label}` objects, not simple strings

### Issue 3: Accordion Structure Missing
**Symptoms**: Fields exist but no accordion organization
**Fix**: Add accordions array that groups fields by section
```yaml
accordions:
  - key: section-1
    title: "Section Title"
    fields: [field1, field2]
```

### Issue 4: File Naming Issues
**Symptoms**: API returns 404 or wrong format
**Fix**: Ensure correct filename:
- `schema-kycp.yaml` for KYCP accordion format
- `schema.yaml` for basic items format

## Debugging Workflow

1. **Check API Structure**: `curl <api-url> | jq 'keys'`
2. **Verify Filename**: Look in `data/schemas/<journey>/`
3. **Check Server Logs**: Look for validation errors
4. **Test Field Keys**: Ensure alphanumeric with underscores/hyphens
5. **Validate Options Format**: Ensure `{value, label}` structure
6. **Verify Accordions**: Ensure accordion structure exists

## Migration Steps: Items → KYCP Format

1. **Rename File**: `schema.yaml` → `schema-kycp.yaml`
2. **Convert Structure**:
   ```yaml
   # OLD (items format)
   items:
     - id: fieldKey
       data_type: enum
       options: ["A", "B"]

   # NEW (KYCP format)
   fields:
     - key: fieldKey
       type: lookup
       options:
         - {value: "A", label: "A"}
         - {value: "B", label: "B"}
   accordions:
     - key: section
       title: "Section"
       fields: [fieldKey]
   ```

## Prevention

- **Always use KYCP format** for new journeys with UI requirements
- **Test API structure** immediately after schema generation
- **Check server logs** during development for validation errors
- **Use consistent field naming** (alphanumeric + underscores/hyphens)
- **Follow working examples** from `non-lux-lp-2-2` schema structure

## Reference Examples

**Working KYCP Schema**: `data/schemas/non-lux-lp-2-2/schema-kycp.yaml`
**API Test URL**: `http://localhost:3002/api/schema/non-lux-lp-2-2`