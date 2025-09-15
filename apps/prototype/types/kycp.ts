// KYCP-aligned component and data model types
export type FieldStyle = 'field' | 'statement' | 'divider' | 'button'
export type DataType = 'string' | 'integer' | 'decimal' | 'date' | 'lookup' | 'freeText'

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
  allConditionsMustMatch: boolean
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
  type?: DataType
  entity: string
  order?: number
  validation?: Validation
  options?: LookupOption[]
  statusRights?: StatusRightRule[]
  visibility?: VisibilityRule[]
  scriptId?: string
  internal?: boolean
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
export type ApplicationData = Record<string, unknown | Record<string, unknown>[]>

export type EffectiveRight = 'hidden' | 'readOnly' | 'editable'

export function resolveRight(rules: StatusRightRule[] | undefined, status: string): EffectiveRight {
  const r = rules?.find(x => x.status === status)?.right
  if (!r || r === 'write' || r === 'global') return 'editable'
  if (r === 'read') return 'readOnly'
  return 'hidden'
}

export function isVisible(node: ComponentNode, status: string, data: ApplicationData): boolean {
  if (resolveRight(node.statusRights, status) === 'hidden') return false
  const rules = node.visibility || []
  if (!rules.length) return true
  return rules.every(rule => rule.conditions.every(c => {
    const v = (data as any)[c.sourceKey]
    return c.operator === 'eq' ? v === c.value : v !== c.value
  }))
}

