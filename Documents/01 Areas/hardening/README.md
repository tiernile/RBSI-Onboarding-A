# Security & Robustness Hardening Plan

Based on security review feedback, this document outlines critical fixes and improvements for the RBSI onboarding prototype.

## Priority 1: Critical Security Fixes (Immediate)

### 1. Path Traversal Vulnerability
**Risk**: Journey parameter allows `../` directory traversal in server routes
**Impact**: High - Could access arbitrary files on server

**Fix**:
```typescript
// Add to all server routes using journey parameter
function validateJourneySlug(journey: string): boolean {
  return /^[a-z0-9-]+$/i.test(journey);
}

// In route handler
if (!validateJourneySlug(journey)) {
  return createError({ statusCode: 400, statusMessage: 'Invalid journey identifier' });
}
```

### 2. CSV Injection
**Risk**: Unescaped cell values can trigger formulas in Excel
**Impact**: High - Code execution in Excel

**Fix**:
```typescript
function escapeCSVCell(value: string): string {
  // Prefix formula triggers with single quote
  if (/^[=+@-]/.test(value)) {
    value = "'" + value;
  }
  // Quote if contains comma, newline, or quote
  if (/[,\n"]/.test(value)) {
    value = '"' + value.replace(/"/g, '""') + '"';
  }
  return value;
}
```

### 3. Cookie Security
**Risk**: Cookies not marked secure in production
**Impact**: Medium - Session hijacking potential

**Fix**:
```typescript
// In auth handler
const isProduction = process.env.NODE_ENV === 'production';
setCookie(event, 'admin-auth', token, {
  httpOnly: true,
  secure: isProduction,
  sameSite: 'strict',
  maxAge: 3600
});
```

## Priority 2: Data Pipeline Hardening

### 1. Schema Validation
**Approach**: Use Zod for runtime validation

```typescript
import { z } from 'zod';

const SchemaItemSchema = z.object({
  id: z.string().regex(/^[A-Za-z0-9_-]+$/),
  label: z.string(),
  control: z.enum(['text', 'select', 'radio', 'textarea', 'checkbox', 'complex']),
  data_type: z.enum(['string', 'number', 'boolean', 'date', 'enum']),
  mandatory: z.boolean(),
  options: z.array(z.string()).optional(),
  visibility: z.object({
    all: z.array(z.string())
  }),
  validation: z.object({
    regex: z.string().nullable(),
    max_length: z.number().nullable()
  })
});

const SchemaSchema = z.object({
  key: z.string(),
  name: z.string(),
  version: z.string(),
  items: z.array(SchemaItemSchema)
});
```

### 2. Robust Importer CLI
**New structure** for `scripts/import-spreadsheet.py`:

```python
#!/usr/bin/env python3
"""
Robust spreadsheet importer with CLI interface
"""

import argparse
import logging
import json
import sys
from pathlib import Path

def setup_logging(verbose=False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def validate_headers(df, required_columns, mapping):
    """Case-insensitive header validation"""
    normalized = {col.upper().strip(): col for col in df.columns}
    missing = []
    
    for required in required_columns:
        mapped = mapping.get(required, required).upper()
        if mapped not in normalized:
            missing.append(required)
    
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    return normalized

def main():
    parser = argparse.ArgumentParser(description='Import spreadsheet to schema')
    parser.add_argument('--input', required=True, help='Input spreadsheet path')
    parser.add_argument('--mapping', required=True, help='Column mapping JSON')
    parser.add_argument('--sheet', default='LP Proposal', help='Sheet name')
    parser.add_argument('--lookups-sheet', default='Lookup Values', help='Lookups sheet')
    parser.add_argument('--out', required=True, help='Output schema path')
    parser.add_argument('--journey-key', required=True, help='Journey identifier')
    parser.add_argument('--verbose', action='store_true', help='Verbose logging')
    parser.add_argument('--validate-only', action='store_true', help='Validate without writing')
    
    args = parser.parse_args()
    setup_logging(args.verbose)
    
    try:
        # Load mapping
        with open(args.mapping) as f:
            mapping = json.load(f)
        
        # Process spreadsheet
        result = process_spreadsheet(
            args.input, 
            mapping, 
            args.sheet,
            args.lookups_sheet,
            args.journey_key
        )
        
        # Validate schema
        validation_errors = validate_schema(result['schema'])
        if validation_errors:
            logging.error(f"Schema validation failed: {validation_errors}")
            sys.exit(1)
        
        # Write output
        if not args.validate_only:
            write_schema(result['schema'], args.out)
            write_report(result['report'], args.out + '.report.json')
        
        logging.info(f"Successfully processed {result['report']['total_fields']} fields")
        
    except Exception as e:
        logging.error(f"Import failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## Priority 3: Frontend Hardening

### 1. Component Renderer Map
Create `apps/prototype/utils/component-map.ts`:

```typescript
export const CONTROL_COMPONENT_MAP = {
  text: 'KycpInput',
  email: 'KycpInput',
  number: 'KycpInput',
  date: 'KycpDatePicker',
  select: 'KycpSelect',
  radio: 'KycpRadio',
  checkbox: 'KycpCheckbox',
  textarea: 'KycpTextarea',
  complex: 'KycpComplexField'
} as const;

export function getComponentForControl(control: string): string {
  const component = CONTROL_COMPONENT_MAP[control as keyof typeof CONTROL_COMPONENT_MAP];
  if (!component) {
    console.error(`Unknown control type: ${control}`);
    return 'KycpUnknownField'; // Fallback component that shows error
  }
  return component;
}
```

### 2. Enhanced Visibility Engine
Extend `composables/useConditions.ts`:

```typescript
type Operator = '==' | '!=' | '>' | '<' | '>=' | '<=' | 'includes' | 'not_includes';

interface Condition {
  field: string;
  operator: Operator;
  value: any;
}

function parseCondition(expr: string): Condition {
  // Parse expressions like "field >= 10" or "field includes 'text'"
  const patterns = [
    /^(\w+)\s*(==|!=|>=|<=|>|<)\s*(.+)$/,
    /^(\w+)\s+(includes|not_includes)\s+(.+)$/
  ];
  
  for (const pattern of patterns) {
    const match = expr.match(pattern);
    if (match) {
      return {
        field: match[1],
        operator: match[2] as Operator,
        value: parseValue(match[3])
      };
    }
  }
  
  throw new Error(`Invalid condition: ${expr}`);
}

function evaluateCondition(condition: Condition, values: Record<string, any>): boolean {
  const fieldValue = values[condition.field];
  
  switch (condition.operator) {
    case '==': return fieldValue == condition.value;
    case '!=': return fieldValue != condition.value;
    case '>': return Number(fieldValue) > Number(condition.value);
    case '<': return Number(fieldValue) < Number(condition.value);
    case '>=': return Number(fieldValue) >= Number(condition.value);
    case '<=': return Number(fieldValue) <= Number(condition.value);
    case 'includes': 
      return Array.isArray(fieldValue) 
        ? fieldValue.includes(condition.value)
        : String(fieldValue).includes(condition.value);
    case 'not_includes':
      return Array.isArray(fieldValue)
        ? !fieldValue.includes(condition.value)
        : !String(fieldValue).includes(condition.value);
    default:
      return false;
  }
}
```

## Priority 4: Testing Infrastructure

### 1. Unit Tests Setup
Create `apps/prototype/tests/conditions.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import { evaluateVisibility } from '~/composables/useConditions';

describe('Visibility Conditions', () => {
  it('evaluates simple equality', () => {
    const result = evaluateVisibility(
      { all: ['field1 == Yes'] },
      { field1: 'Yes' }
    );
    expect(result).toBe(true);
  });
  
  it('evaluates numeric comparison', () => {
    const result = evaluateVisibility(
      { all: ['amount >= 1000'] },
      { amount: 1500 }
    );
    expect(result).toBe(true);
  });
  
  it('evaluates includes operator', () => {
    const result = evaluateVisibility(
      { all: ['countries includes UK'] },
      { countries: ['UK', 'US', 'FR'] }
    );
    expect(result).toBe(true);
  });
});
```

### 2. Server Route Tests
Create `apps/prototype/tests/server-routes.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import { validateJourneySlug } from '~/server/utils/validation';

describe('Server Security', () => {
  it('rejects path traversal attempts', () => {
    expect(validateJourneySlug('../etc/passwd')).toBe(false);
    expect(validateJourneySlug('../../secret')).toBe(false);
    expect(validateJourneySlug('valid-journey-name')).toBe(true);
  });
  
  it('escapes CSV injection vectors', () => {
    expect(escapeCSVCell('=1+1')).toBe("'=1+1");
    expect(escapeCSVCell('+44123')).toBe("'+44123");
    expect(escapeCSVCell('@SUM(A1:A10)')).toBe("'@SUM(A1:A10)");
  });
});
```

### 3. Python Importer Tests
Create `scripts/tests/test_importer.py`:

```python
import pytest
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from import_spreadsheet import validate_headers, normalize_value

def test_header_validation():
    """Test case-insensitive header matching"""
    df = pd.DataFrame(columns=['KEYNAME', 'Field Name', 'DATA TYPE'])
    mapping = {'field_name': 'Field Name'}
    
    normalized = validate_headers(df, ['KEYNAME', 'field_name'], mapping)
    assert 'KEYNAME' in normalized
    assert 'FIELD NAME' in normalized
    
def test_normalize_value():
    """Test value normalization"""
    assert normalize_value('YES') == 'Yes'
    assert normalize_value('NO') == 'No'
    assert normalize_value('  trimmed  ') == 'trimmed'
```

## Implementation Timeline

### Week 1 (Immediate)
- [ ] Fix path traversal vulnerability
- [ ] Implement CSV injection protection
- [ ] Add secure cookie configuration
- [ ] Basic input sanitization

### Week 2
- [ ] Schema validation with Zod
- [ ] Robust importer CLI
- [ ] Component renderer map
- [ ] Enhanced visibility engine

### Week 3
- [ ] Complete test suite
- [ ] CI/CD setup
- [ ] Security audit
- [ ] Documentation update

## Success Metrics

- Zero security vulnerabilities in OWASP top 10
- 100% of user inputs validated
- Schema validation catches 100% of malformed data
- Test coverage > 80% for critical paths
- All CSV exports safe for Excel/Google Sheets