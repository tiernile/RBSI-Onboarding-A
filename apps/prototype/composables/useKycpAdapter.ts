import type { ComponentNode, BaseField, ComplexGroup, LookupOption, VisibilityRule, VisibilityCondition, Validation } from '~/types/kycp'

/**
 * Transform YAML schema format to KYCP component format
 * This is the critical missing layer between our data ingestion and component rendering
 */

interface YamlSchemaItem {
  id: string
  label: string
  help?: string | null
  data_type: string
  control: string
  options?: string[]
  mandatory: boolean
  visibility?: { all: string[] }
  validation?: { regex?: string | null; max_length?: number | null }
  internal_only?: boolean
  section?: string
  stage?: string
}

interface YamlSchema {
  key: string
  name: string
  version: string
  items: YamlSchemaItem[]
}

/**
 * Map YAML data_type to KYCP type
 */
function mapDataType(dataType: string, control: string): string {
  const dt = dataType.toLowerCase()
  const ctrl = control.toLowerCase()
  
  // Handle enums/lookups
  if (dt === 'enum' || ctrl === 'select' || ctrl === 'radio') {
    return 'lookup'
  }
  
  // Handle text areas
  if (ctrl === 'textarea') {
    return 'freeText'
  }
  
  // Handle numbers
  if (dt === 'number') {
    // Could differentiate integer vs decimal based on validation or field name
    return 'integer'
  }
  
  // Handle dates
  if (dt === 'date') {
    return 'date'
  }
  
  // Default to string
  return 'string'
}

/**
 * Parse visibility expression into structured conditions
 * Handles simple expressions like: 'Field1 == "value"' or 'Field2 != "other"'
 * And compound expressions: 'Field1 == "A" && Field2 != "B"'
 */
function parseVisibilityExpression(expr: string): VisibilityCondition[] {
  if (!expr || !expr.trim()) return []
  
  const conditions: VisibilityCondition[] = []
  
  // Split by && (we'll handle || separately if needed)
  const parts = expr.split('&&').map(p => p.trim())
  
  for (const part of parts) {
    // Match patterns like: Field == "value" or Field != "value"
    const eqMatch = part.match(/^([A-Za-z0-9_]+)\s*(==|!=)\s*"([^"]*)"/)
    if (eqMatch) {
      conditions.push({
        sourceKey: eqMatch[1],
        operator: eqMatch[2] === '==' ? 'eq' : 'neq',
        value: eqMatch[3]
      })
      continue
    }
    
    // Also handle unquoted values for backwards compatibility
    const simpleMatch = part.match(/^([A-Za-z0-9_]+)\s*(==|!=)\s*([A-Za-z0-9_]+)/)
    if (simpleMatch) {
      conditions.push({
        sourceKey: simpleMatch[1],
        operator: simpleMatch[2] === '==' ? 'eq' : 'neq',
        value: simpleMatch[3]
      })
    }
  }
  
  return conditions
}

/**
 * Transform visibility rules from YAML format to KYCP format
 */
function transformVisibility(visibility?: { all: string[] }): VisibilityRule[] {
  if (!visibility?.all?.length) return []
  
  const rules: VisibilityRule[] = []
  
  for (const expr of visibility.all) {
    const conditions = parseVisibilityExpression(expr)
    if (conditions.length > 0) {
      rules.push({
        entity: 'entity', // Default entity context
        targetKeys: [], // Not used in current implementation
        allConditionsMustMatch: true, // AND logic
        conditions
      })
    }
  }
  
  return rules
}

/**
 * Transform validation rules from YAML to KYCP format
 */
function transformValidation(yamlItem: YamlSchemaItem): Validation {
  const validation: Validation = {}
  
  if (yamlItem.mandatory) {
    validation.required = true
  }
  
  if (yamlItem.validation?.regex) {
    validation.pattern = yamlItem.validation.regex
  }
  
  if (yamlItem.validation?.max_length) {
    validation.maxLength = yamlItem.validation.max_length
  }
  
  // Add type-specific validation based on data_type
  const dt = yamlItem.data_type.toLowerCase()
  if (dt === 'date') {
    validation.dateFormat = 'DD/MM/YYYY'
  }
  
  return validation
}

/**
 * Transform options from string array to LookupOption array
 */
function transformOptions(options?: string[]): LookupOption[] {
  if (!options?.length) return []
  
  return options.map(opt => ({
    value: opt,
    label: opt
  }))
}

/**
 * Transform a single YAML schema item to KYCP BaseField
 */
function transformField(item: YamlSchemaItem): BaseField {
  const dataType = mapDataType(item.data_type, item.control)
  
  const field: BaseField = {
    key: item.id,
    label: item.label,
    description: item.help || undefined,
    style: 'field', // All regular fields use 'field' style
    type: dataType as any,
    entity: 'entity', // Default entity
    validation: transformValidation(item),
    visibility: transformVisibility(item.visibility),
    internal: item.internal_only
  }
  
  // Add options for lookup types
  if (dataType === 'lookup' && item.options) {
    field.options = transformOptions(item.options)
  }
  
  // Add order if we want to preserve schema ordering
  // This could be enhanced to use section/stage grouping
  
  return field
}

/**
 * Group fields by section into ComplexGroups (optional enhancement)
 * For now, we'll return flat fields, but this shows how we could group them
 */
function groupFieldsBySection(fields: BaseField[]): ComponentNode[] {
  // For MVP, return flat list
  // Later we can group by section/stage for better organization
  return fields
}

/**
 * Main adapter function: Transform YAML schema to KYCP ComponentNode array
 */
export function adaptYamlToKycp(schema: YamlSchema): ComponentNode[] {
  if (!schema?.items?.length) return []
  
  // Filter out internal-only fields
  const visibleItems = schema.items.filter(item => !item.internal_only)
  
  // Transform each item to KYCP format
  const fields = visibleItems.map(item => transformField(item))
  
  // Optionally group by section (for now returning flat)
  return groupFieldsBySection(fields)
}

/**
 * Composable for using the adapter in components
 */
export function useKycpAdapter() {
  /**
   * Transform a schema loaded from YAML to KYCP component format
   */
  const transformSchema = (schema: any): ComponentNode[] => {
    try {
      return adaptYamlToKycp(schema)
    } catch (error) {
      console.error('Error transforming schema:', error)
      return []
    }
  }
  
  /**
   * Check if a field should be visible based on current data
   * This could be enhanced to use the isVisible helper from types/kycp.ts
   */
  const checkVisibility = (field: ComponentNode, data: Record<string, any>): boolean => {
    if (!field.visibility?.length) return true
    
    // Use the visibility rules to determine if field should show
    for (const rule of field.visibility) {
      const allMatch = rule.conditions.every(cond => {
        const value = data[cond.sourceKey]
        if (cond.operator === 'eq') {
          return value === cond.value
        } else {
          return value !== cond.value
        }
      })
      
      if (!allMatch && rule.allConditionsMustMatch) {
        return false
      }
    }
    
    return true
  }
  
  return {
    transformSchema,
    checkVisibility
  }
}