# KYCP Components – Developer Spec

This spec encodes the KYCP manuals into concrete interfaces, limits, and behaviours suitable for direct implementation. It is the single source of truth for component props and the in-memory data shape used by the prototype.

## Canonical Types

```ts
// Style-focused rendering vs type-focused validation
export type FieldStyle = 'field' | 'statement' | 'divider' | 'button'
export type DataType   = 'string' | 'integer' | 'decimal' | 'date' | 'lookup' | 'freeText'

// Rights model across statuses
export type StatusRight = 'invisible' | 'read' | 'write' | 'global'

export type Operator = 'eq' | 'neq'

export interface VisibilityCondition {
  sourceKey: string
  operator: Operator
  value: string
}

export interface VisibilityRule {
  entity: string
  targetKeys: string[]
  allConditionsMustMatch: boolean // AND semantics across conditions
  conditions: VisibilityCondition[]
}

export interface StatusRightRule {
  status: string
  right: StatusRight
}

export interface Validation {
  required?: boolean
  minLength?: number
  maxLength?: number
  min?: number
  max?: number
  precision?: number
  scale?: number
  pattern?: string
  dateFormat?: 'DD/MM/YYYY'
}

export interface LookupOption { value: string; label: string }

export interface BaseField {
  key: string
  label?: string
  description?: string
  style: FieldStyle
  type?: DataType // required when style === 'field'
  entity: string
  order?: number
  validation?: Validation
  options?: LookupOption[]
  statusRights?: StatusRightRule[]
  visibility?: VisibilityRule[]
  scriptId?: string // when style === 'button'
  internal?: boolean // do not surface on client UIs
}

export interface ComplexGroup {
  key: string
  label?: string
  entity: string
  repeatable: true
  fields: (BaseField | ComplexGroup)[]
  statusRights?: StatusRightRule[]
  visibility?: VisibilityRule[]
}

export type ComponentNode = BaseField | ComplexGroup

// Application data shape (flat fields + arrays for groups)
export type ApplicationData = Record<string, unknown | Record<string, unknown>[]> 
```

## Type Limits & Defaults

- string: maxLength 1024
- freeText: maxLength 8192
- integer: 32-bit signed max 2,147,483,647
- decimal: precision 18, scale 2, auto-round to 2dp
- date: format `DD/MM/YYYY`, invalid dates rejected, serialise as string
- lookup: single-select; values are stable codes from `LookupOption.value`
- statement/divider/button: non-data styles; `button.scriptId` links to predefined workflow action

## Status-aware Behaviour

```ts
export type EffectiveRight = 'hidden' | 'readOnly' | 'editable'

export function resolveRight(rules: StatusRightRule[] | undefined, status: string): EffectiveRight {
  const r = rules?.find(x => x.status === status)?.right
  if (!r || r === 'write' || r === 'global') return 'editable'
  if (r === 'read') return 'readOnly'
  return 'hidden' // invisible
}
```

Notes
- 'global' acts as module-level default; unless overridden per-field/group, treat as editable in prototypes.
- Honour `internal?: true` to suppress fields/groups in client UIs even if rights/visibility would allow them.

## Conditional Visibility

```ts
export function isVisible(node: ComponentNode, status: string, data: ApplicationData): boolean {
  if (resolveRight(node.statusRights, status) === 'hidden') return false
  const rules = node.visibility || []
  if (!rules.length) return true
  return rules.every(rule => rule.conditions.every(c => {
    const v = data[c.sourceKey]
    return c.operator === 'eq' ? v === c.value : v !== c.value
  }))
}
```

## Complex Groups

- Repeatable list of rows (objects). Data serialised as `groupKey: Array<Record<childKey, value>>`.
- Provide add/remove/change row handlers.
- Apply visibility and status rights at both group and child field levels.

## Mapping to Current Prototype

- Existing YAML schema items map to `BaseField` where `style === 'field'`.
- Current `control` values map to types:
  - text/email → `type: 'string'`
  - number → `type: 'integer' | 'decimal'` (infer by regex/precision when available)
  - select/radio → `type: 'lookup'`
  - textarea → `type: 'freeText'`
- Current visibility `{ all: string[] }` converts into `VisibilityRule` with AND semantics; initial adapter will focus on eq/neq.
- `internal_only` from importer maps to `internal: true`.

