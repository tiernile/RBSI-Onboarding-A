import { ref, computed, type Ref } from 'vue'

/**
 * Pure schema-driven form composable
 * All logic comes from the schema, components are just UI
 */

interface SchemaField {
  key: string
  label: string
  type: string
  style?: string
  description?: string
  placeholder?: string
  required?: boolean
  readonly?: boolean
  disabled?: boolean
  maxLength?: number
  minLength?: number
  pattern?: string
  min?: number
  max?: number
  options?: Array<{ value: string; label: string }>
  visibility?: any[]
  validation?: any
}

interface FormSchema {
  key: string
  name: string
  fields: SchemaField[]
}

export function useSchemaForm(schema: Ref<FormSchema | null>) {
  // Form data
  const formData = ref<Record<string, any>>({})
  
  // Track errors
  const errors = ref<Record<string, string>>({})
  
  // Track touched fields
  const touched = ref<Set<string>>(new Set())
  
  // Get visible fields based on conditions
  const visibleFields = computed(() => {
    if (!schema.value?.fields) return []
    
    return schema.value.fields.filter(field => {
      // If no visibility rules, always show
      if (!field.visibility?.length) return true
      
      // Check visibility conditions from schema
      // This is where the schema would define visibility logic
      // For now, just return true (you'd implement the actual logic here)
      return true
    })
  })
  
  // Get component type for a field
  const getComponentType = (field: SchemaField): string => {
    // Map schema type to component name
    const typeMap: Record<string, string> = {
      'string': 'KycpInput',
      'text': 'KycpInput',
      'email': 'KycpInput',
      'number': 'KycpInput',
      'integer': 'KycpInput',
      'decimal': 'KycpInput',
      'freeText': 'KycpTextarea',
      'textarea': 'KycpTextarea',
      'lookup': 'KycpSelect',
      'select': 'KycpSelect',
      'radio': 'KycpSelect',
      'boolean': 'KycpSelect',
      'date': 'KycpInput'  // Would use date picker component
    }
    
    return typeMap[field.type] || 'KycpInput'
  }
  
  // Get props for a component based on field schema
  const getComponentProps = (field: SchemaField): Record<string, any> => {
    const props: Record<string, any> = {
      modelValue: formData.value[field.key],
      placeholder: field.placeholder,
      disabled: field.disabled,
      readonly: field.readonly,
      error: !!errors.value[field.key]
    }
    
    // Add type-specific props
    if (field.type === 'email') {
      props.type = 'email'
    } else if (field.type === 'number' || field.type === 'integer' || field.type === 'decimal') {
      props.type = 'number'
      if (field.min !== undefined) props.min = field.min
      if (field.max !== undefined) props.max = field.max
    } else if (field.type === 'date') {
      props.type = 'date'
    }
    
    // Add textarea-specific props
    if (field.type === 'freeText' || field.type === 'textarea') {
      props.rows = 4
      if (field.maxLength) props.maxlength = field.maxLength
    }
    
    // Add select/radio options
    if (field.type === 'lookup' || field.type === 'select' || field.type === 'radio') {
      props.options = field.options || []
    }
    
    return props
  }
  
  // Update field value
  const updateField = (key: string, value: any) => {
    formData.value[key] = value
    touched.value.add(key)
    
    // Clear error when field is updated
    if (errors.value[key]) {
      delete errors.value[key]
    }
  }
  
  // Validate a single field based on schema rules
  const validateField = (field: SchemaField): boolean => {
    const value = formData.value[field.key]
    
    // Required validation
    if (field.required && !value) {
      errors.value[field.key] = `${field.label} is required`
      return false
    }
    
    // Length validation
    if (value && typeof value === 'string') {
      if (field.minLength && value.length < field.minLength) {
        errors.value[field.key] = `Minimum length is ${field.minLength}`
        return false
      }
      if (field.maxLength && value.length > field.maxLength) {
        errors.value[field.key] = `Maximum length is ${field.maxLength}`
        return false
      }
    }
    
    // Pattern validation
    if (field.pattern && value) {
      const regex = new RegExp(field.pattern)
      if (!regex.test(value)) {
        errors.value[field.key] = 'Invalid format'
        return false
      }
    }
    
    // Number validation
    if ((field.type === 'number' || field.type === 'integer' || field.type === 'decimal') && value) {
      const num = Number(value)
      if (field.min !== undefined && num < field.min) {
        errors.value[field.key] = `Minimum value is ${field.min}`
        return false
      }
      if (field.max !== undefined && num > field.max) {
        errors.value[field.key] = `Maximum value is ${field.max}`
        return false
      }
    }
    
    return true
  }
  
  // Validate all visible fields
  const validateForm = (): boolean => {
    errors.value = {}
    let isValid = true
    
    for (const field of visibleFields.value) {
      if (!validateField(field)) {
        isValid = false
      }
    }
    
    return isValid
  }
  
  // Reset form
  const resetForm = () => {
    formData.value = {}
    errors.value = {}
    touched.value.clear()
  }
  
  // Get form data for submission
  const getFormData = () => {
    // Only return data for visible fields
    const data: Record<string, any> = {}
    for (const field of visibleFields.value) {
      if (formData.value[field.key] !== undefined) {
        data[field.key] = formData.value[field.key]
      }
    }
    return data
  }
  
  return {
    formData,
    errors,
    touched,
    visibleFields,
    getComponentType,
    getComponentProps,
    updateField,
    validateField,
    validateForm,
    resetForm,
    getFormData
  }
}