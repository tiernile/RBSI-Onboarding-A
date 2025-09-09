/**
 * Schema validation using Zod
 * Ensures YAML schemas are well-formed before use
 */

import { z } from 'zod'

// Valid control types based on KYCP components
const ControlTypes = z.enum([
  'text',
  'email',
  'number',
  'date',
  'select',
  'radio',
  'checkbox',
  'textarea',
  'complex'
])

// Valid data types
const DataTypes = z.enum([
  'string',
  'number',
  'boolean',
  'date',
  'enum'
])

// Validation rules
const ValidationSchema = z.object({
  regex: z.string().nullable().optional(),
  max_length: z.number().positive().nullable().optional(),
  min_length: z.number().positive().nullable().optional(),
  min: z.number().nullable().optional(),
  max: z.number().nullable().optional()
})

// Visibility conditions
const VisibilitySchema = z.object({
  all: z.array(z.string()).default([]),
  any: z.array(z.string()).optional()
})

// Mappings to external systems
const MappingsSchema = z.object({
  crm_field: z.string().nullable().optional(),
  system_field: z.string().nullable().optional()
})

// Metadata for audit trail
const MetaSchema = z.object({
  source_row_ref: z.string().optional(),
  notes: z.string().optional(),
  html_index: z.number().optional(),
  spreadsheet_ref: z.string().optional(),
  match_score: z.number().optional(),
  match_confidence: z.string().optional(),
  source: z.string().optional(),
  extracted_date: z.string().optional()
})

// Individual schema item
const SchemaItemSchema = z.object({
  id: z.string().regex(/^[A-Za-z0-9_-]+$/, 'ID must be alphanumeric with underscores/hyphens'),
  label: z.string().min(1, 'Label is required'),
  help: z.string().nullable().optional(),
  entity_type: z.string().optional(),
  jurisdiction: z.string().optional(),
  stage: z.string().optional(),
  section: z.string().optional(),
  data_type: DataTypes,
  control: ControlTypes,
  options: z.array(z.string()).optional().default([]),
  mandatory: z.boolean().default(false),
  visibility: VisibilitySchema.default({ all: [] }),
  validation: ValidationSchema.optional().default({}),
  mappings: MappingsSchema.optional().default({}),
  meta: MetaSchema.optional()
})

// Complete schema structure
export const JourneySchemaValidator = z.object({
  key: z.string().regex(/^[a-z0-9-]+$/, 'Key must be lowercase alphanumeric with hyphens'),
  name: z.string().min(1, 'Name is required'),
  version: z.string().regex(/^\d+\.\d+\.\d+$/, 'Version must be semantic (x.y.z)'),
  description: z.string().optional(),
  metadata: z.record(z.any()).optional(),
  items: z.array(SchemaItemSchema).min(1, 'Schema must have at least one item')
})

// Type exports
export type SchemaItem = z.infer<typeof SchemaItemSchema>
export type JourneySchema = z.infer<typeof JourneySchemaValidator>

/**
 * Validate a schema and return errors if invalid
 */
export function validateSchema(schema: unknown): { 
  valid: boolean; 
  errors?: string[]; 
  data?: JourneySchema 
} {
  try {
    const validated = JourneySchemaValidator.parse(schema)
    return { valid: true, data: validated }
  } catch (error) {
    if (error instanceof z.ZodError) {
      const issues = (error as any).errors || (error as any).issues || []
      const errors = issues.map((e: any) => {
        const path = e.path.join('.')
        return `${path}: ${e.message}`
      })
      return { valid: false, errors }
    }
    return { valid: false, errors: ['Unknown validation error'] }
  }
}

/**
 * Validate a single schema item
 */
export function validateSchemaItem(item: unknown): {
  valid: boolean;
  errors?: string[];
  data?: SchemaItem
} {
  try {
    const validated = SchemaItemSchema.parse(item)
    
    // Additional business rule validations
    if (validated.control === 'select' || validated.control === 'radio') {
      if (!validated.options || validated.options.length === 0) {
        return { 
          valid: false, 
          errors: [`${validated.id}: ${validated.control} control requires options`] 
        }
      }
    }
    
    if (validated.data_type === 'enum' && (!validated.options || validated.options.length === 0)) {
      return { 
        valid: false, 
        errors: [`${validated.id}: enum data type requires options`] 
      }
    }
    
    return { valid: true, data: validated }
  } catch (error) {
    if (error instanceof z.ZodError) {
      const issues = (error as any).errors || (error as any).issues || []
      const errors = issues.map((e: any) => {
        const path = e.path.join('.')
        return `${path}: ${e.message}`
      })
      return { valid: false, errors }
    }
    return { valid: false, errors: ['Unknown validation error'] }
  }
}

/**
 * Safe parse with detailed error reporting
 */
export function safeParse<T>(
  validator: z.ZodSchema<T>,
  data: unknown
): { success: true; data: T } | { success: false; errors: string[] } {
  const result = validator.safeParse(data)
  
  if (result.success) {
    return { success: true, data: result.data }
  }
  
  const issues = (result as any).error?.errors || (result as any).error?.issues || []
  const errors = issues.map((e: any) => {
    const path = e.path.join('.')
    return path ? `${path}: ${e.message}` : e.message
  })
  
  return { success: false, errors }
}
