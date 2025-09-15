import { ref, computed, type Ref } from 'vue'
import type { ComponentNode, ApplicationData } from '~/types/kycp'

/**
 * Composable for managing KYCP form state and rendering
 * This handles the dynamic rendering of KYCP components from schema
 */
export function useKycpForm(schema: Ref<any>) {
  // Form data state
  const formData = ref<ApplicationData>({})
  
  // Current application status (for status rights)
  const applicationStatus = ref('draft')
  
  // Track validation errors
  const errors = ref<Record<string, string>>({})
  
  // Track which fields are currently visible
  const visibleFields = computed(() => {
    const visible = new Set<string>()
    
    if (!schema.value?.fields) return visible
    
    for (const field of schema.value.fields) {
      // Skip internal fields
      if (field.internal) continue
      
      // Check status rights
      const statusRight = field.statusRights?.find((r: any) => r.status === applicationStatus.value)
      if (statusRight?.right === 'invisible') continue
      
      // Check visibility rules
      if (field.visibility?.length) {
        let isVisible = true
        
        for (const rule of field.visibility) {
          if (rule.allConditionsMustMatch) {
            // All conditions must match for AND logic
            const allMatch = rule.conditions.every((cond: any) => {
              const value = formData.value[cond.sourceKey]
              if (cond.operator === 'eq') {
                return value === cond.value
              } else if (cond.operator === 'neq') {
                return value !== cond.value
              }
              return true
            })
            
            if (!allMatch) {
              isVisible = false
              break
            }
          } else {
            // Any condition can match for OR logic
            const anyMatch = rule.conditions.some((cond: any) => {
              const value = formData.value[cond.sourceKey]
              if (cond.operator === 'eq') {
                return value === cond.value
              } else if (cond.operator === 'neq') {
                return value !== cond.value
              }
              return false
            })
            
            if (!anyMatch) {
              isVisible = false
              break
            }
          }
        }
        
        if (!isVisible) continue
      }
      
      visible.add(field.key)
    }
    
    return visible
  })
  
  // Get effective right for a field
  const getEffectiveRight = (field: any): 'hidden' | 'readOnly' | 'editable' => {
    // Check if field is visible
    if (!visibleFields.value.has(field.key)) {
      return 'hidden'
    }
    
    // Check status rights
    const statusRight = field.statusRights?.find((r: any) => r.status === applicationStatus.value)
    if (statusRight) {
      if (statusRight.right === 'read') return 'readOnly'
      if (statusRight.right === 'invisible') return 'hidden'
    }
    
    return 'editable'
  }
  
  // Update field value
  const updateField = (key: string, value: any) => {
    formData.value[key] = value
    
    // Clear error when field is updated
    if (errors.value[key]) {
      delete errors.value[key]
    }
  }
  
  // Validate a single field
  const validateField = (field: any): boolean => {
    const value = formData.value[field.key]
    const validation = field.validation || {}
    
    // Required validation
    if (validation.required && !value) {
      errors.value[field.key] = `${field.label} is required`
      return false
    }
    
    // String validations
    if (field.type === 'string' || field.type === 'freeText') {
      if (validation.minLength && value && value.length < validation.minLength) {
        errors.value[field.key] = `Minimum length is ${validation.minLength}`
        return false
      }
      
      if (validation.maxLength && value && value.length > validation.maxLength) {
        errors.value[field.key] = `Maximum length is ${validation.maxLength}`
        return false
      }
      
      if (validation.pattern && value) {
        const regex = new RegExp(validation.pattern)
        if (!regex.test(value)) {
          errors.value[field.key] = 'Invalid format'
          return false
        }
      }
    }
    
    // Number validations
    if (field.type === 'integer' || field.type === 'decimal') {
      const numValue = Number(value)
      
      if (validation.min !== undefined && numValue < validation.min) {
        errors.value[field.key] = `Minimum value is ${validation.min}`
        return false
      }
      
      if (validation.max !== undefined && numValue > validation.max) {
        errors.value[field.key] = `Maximum value is ${validation.max}`
        return false
      }
    }
    
    // Date validation
    if (field.type === 'date' && value) {
      // Check date format (DD/MM/YYYY)
      const dateRegex = /^(\d{2})\/(\d{2})\/(\d{4})$/
      if (!dateRegex.test(value)) {
        errors.value[field.key] = 'Date must be in DD/MM/YYYY format'
        return false
      }
    }
    
    return true
  }
  
  // Validate all visible fields
  const validateForm = (): boolean => {
    let isValid = true
    errors.value = {}
    
    if (!schema.value?.fields) return true
    
    for (const field of schema.value.fields) {
      // Only validate visible, editable fields
      if (getEffectiveRight(field) === 'editable') {
        if (!validateField(field)) {
          isValid = false
        }
      }
    }
    
    return isValid
  }
  
  // Get component name for field type
  const getComponentName = (field: any): string => {
    const typeMap: Record<string, string> = {
      'string': 'StringField',
      'freeText': 'FreeTextArea',
      'integer': 'IntegerField',
      'decimal': 'DecimalField',
      'date': 'DateField',
      'lookup': 'LookupField'
    }
    
    return typeMap[field.type] || 'StringField'
  }
  
  // Reset form
  const resetForm = () => {
    formData.value = {}
    errors.value = {}
  }
  
  // Set initial data
  const setFormData = (data: ApplicationData) => {
    formData.value = { ...data }
  }
  
  return {
    formData,
    applicationStatus,
    errors,
    visibleFields,
    getEffectiveRight,
    updateField,
    validateField,
    validateForm,
    getComponentName,
    resetForm,
    setFormData
  }
}