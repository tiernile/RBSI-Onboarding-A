<template>
  <div class="preview-container">
    <header class="preview-header">
      <div class="preview-header-content">
        <NuxtLink to="/" class="back-link">← Mission Control</NuxtLink>
        <h1>{{ journeyName || journeyKey }}</h1>
        <p class="journey-meta">{{ journeyKey }} · Version {{ journeyVersion }} · KYCP Components</p>
      </div>
    </header>

    <div v-if="error" class="error-message">
      <strong>Failed to load schema.</strong>
      <p>{{ error }}</p>
    </div>
    
    <div v-else-if="!loading" class="preview-content">
      <div class="form-container">
        <!-- Error Summary -->
        <div v-if="Object.keys(errors).length > 0" class="error-summary">
          <h3>Please correct the following errors:</h3>
          <ul>
            <li v-for="(error, key) in errors" :key="key">
              {{ error }}
            </li>
          </ul>
        </div>
        
        <!-- All Sections on a single page -->
        <div v-for="section in sections" :key="section" class="form-section">
          <KycpDivider v-if="section !== 'General'" :title="section" />
          
          <div v-for="field in fieldsBySection(section)" :key="field.key" class="field-container">
            <!-- Statement fields -->
            <KycpStatement 
              v-if="field.style === 'statement'"
              :text="field.label"
            />
            
            <!-- Divider/Title fields -->
            <KycpDivider 
              v-else-if="field.style === 'divider'"
              :title="field.label"
            />
            
            <!-- Regular form fields -->
            <KycpFieldWrapper 
              v-else
              :id="field.key"
              :label="field.label"
              :required="field.validation?.required"
              :description="field.description"
              :error="errors[field.key]"
              :help="field.help"
            >
              <!-- String/Text input -->
              <KycpInput
                v-if="field.type === 'string' || field.type === 'text'"
                :id="field.key"
                v-model="formData[field.key]"
                :placeholder="field.placeholder"
                :required="field.validation?.required"
                :maxlength="field.validation?.maxLength || 1024"
                :error="!!errors[field.key]"
              />
              
              <!-- FreeText/Textarea -->
              <KycpTextarea
                v-else-if="field.type === 'freeText' || field.type === 'textarea'"
                :id="field.key"
                v-model="formData[field.key]"
                :placeholder="field.placeholder"
                :required="field.validation?.required"
                :maxlength="field.validation?.maxLength || 8192"
                :rows="4"
                :error="!!errors[field.key]"
              />
              
              <!-- Integer -->
              <KycpInput
                v-else-if="field.type === 'integer'"
                :id="field.key"
                v-model.number="formData[field.key]"
                type="number"
                :placeholder="field.placeholder"
                :required="field.validation?.required"
                :min="field.validation?.min || 0"
                :max="field.validation?.max || 2147483647"
                :step="1"
                :error="!!errors[field.key]"
              />
              
              <!-- Decimal -->
              <KycpInput
                v-else-if="field.type === 'decimal'"
                :id="field.key"
                v-model.number="formData[field.key]"
                type="number"
                :placeholder="field.placeholder"
                :required="field.validation?.required"
                :step="0.01"
                :error="!!errors[field.key]"
              />
              
              <!-- Date -->
              <KycpInput
                v-else-if="field.type === 'date'"
                :id="field.key"
                v-model="formData[field.key]"
                type="date"
                :placeholder="field.placeholder || 'DD/MM/YYYY'"
                :required="field.validation?.required"
                :error="!!errors[field.key]"
              />
              
              <!-- Lookup/Select -->
              <KycpSelect
                v-else-if="field.type === 'lookup' || field.type === 'enum'"
                :id="field.key"
                v-model="formData[field.key]"
                :options="field.options || []"
                :placeholder="field.placeholder || 'Please select...'"
                :required="field.validation?.required"
                :error="!!errors[field.key]"
              />
              
              <!-- Fallback for unknown types -->
              <KycpInput
                v-else
                :id="field.key"
                v-model="formData[field.key]"
                :placeholder="field.placeholder"
                :required="field.validation?.required"
                :error="!!errors[field.key]"
              />
            </KycpFieldWrapper>
          </div>

          <!-- Complex Groups (repeaters) for this section -->
          <div v-for="grp in groupsForSection(section)" :key="grp.key" class="group-container">
            <KycpDivider :title="grp.key" />
            <KycpRepeater v-model="formData[grp.key]" :item-label="grp.key" :title-field="grp.titleField">
              <template #item="{ item }">
                <div style="font-size: 13px; color: var(--kycp-gray-700);">
                  {{ grp.titleField && item[grp.titleField] ? item[grp.titleField] : 'Row' }}
                </div>
              </template>
              <template #form="{ item, save, cancel }">
                <div style="display: grid; gap: 16px;">
                  <div v-for="child in groupChildFields(grp)" :key="child.key" v-show="evaluateVisibilityForModel(child, item)">
                    <KycpFieldWrapper :id="child.key" :label="child.label" :required="child.validation?.required" :description="child.description">
                      <KycpInput
                        v-if="child.type === 'string' || child.type === 'text'"
                        :id="child.key"
                        v-model="item[child.key]"
                        :maxlength="child.validation?.maxLength || 1024"
                      />
                      <KycpTextarea
                        v-else-if="child.type === 'freeText' || child.type === 'textarea'"
                        :id="child.key"
                        v-model="item[child.key]"
                        :maxlength="child.validation?.maxLength || 8192"
                        :rows="4"
                      />
                      <KycpInput
                        v-else-if="child.type === 'integer'"
                        :id="child.key"
                        v-model.number="item[child.key]"
                        type="number"
                        :min="child.validation?.min || 0"
                        :max="child.validation?.max || 2147483647"
                        :step="1"
                      />
                      <KycpInput
                        v-else-if="child.type === 'decimal'"
                        :id="child.key"
                        v-model.number="item[child.key]"
                        type="number"
                        :step="0.01"
                      />
                      <KycpInput
                        v-else-if="child.type === 'date'"
                        :id="child.key"
                        v-model="item[child.key]"
                        type="date"
                        :placeholder="child.placeholder || 'DD/MM/YYYY'"
                      />
                      <KycpSelect
                        v-else-if="child.type === 'lookup' || child.type === 'enum'"
                        :id="child.key"
                        v-model="item[child.key]"
                        :options="child.options || []"
                        :placeholder="child.placeholder || 'Please select...'"
                      />
                      <KycpInput
                        v-else
                        :id="child.key"
                        v-model="item[child.key]"
                      />
                    </KycpFieldWrapper>
                  </div>
                  <div style="display: flex; gap: 12px; justify-content: flex-end;">
                    <KycpButton variant="secondary" label="Cancel" @trigger="cancel" />
                    <KycpButton variant="primary" label="Save" @trigger="save" />
                  </div>
                </div>
              </template>
            </KycpRepeater>
          </div>
        </div>
        
        <!-- Submit button only -->
        <div class="form-actions">
          <KycpButton 
            variant="primary"
            label="Submit"
            @trigger="submitForm"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'
import KycpInput from '~/components/kycp/base/KycpInput.vue'
import KycpTextarea from '~/components/kycp/base/KycpTextarea.vue'
import KycpSelect from '~/components/kycp/base/KycpSelect.vue'
import KycpFieldWrapper from '~/components/kycp/base/KycpFieldWrapper.vue'
import KycpStatement from '~/components/kycp/base/KycpStatement.vue'
import KycpDivider from '~/components/kycp/base/KycpDivider.vue'
import KycpButton from '~/components/kycp/base/KycpButton.vue'
import KycpRepeater from '~/components/kycp/base/KycpRepeater.vue'

const route = useRoute()
const journeyKey = computed(() => route.params.journey as string)

// Load schema
const { data: schema, error: schemaError, pending: loading } = await useFetch(`/api/schema/${journeyKey.value}`)

const error = computed(() => {
  if (schemaError.value) return 'Failed to load journey schema'
  if (!schema.value) return 'No schema found'
  return null
})

// Extract journey metadata
const journeyName = computed(() => schema.value?.name || '')
const journeyVersion = computed(() => schema.value?.version || '1.0.0')

// Form data
const formData = reactive<Record<string, any>>({})
const errors = reactive<Record<string, string>>({})

// Fields processing
const allFields = computed(() => {
  if (!schema.value?.fields) return []
  // Filter out internal fields
  return schema.value.fields.filter((f: any) => !f.internal && !f.internal_only)
})

// Groups metadata and helpers
const groups = computed(() => (schema.value?.groups || []) as any[])
const fieldMap = computed(() => {
  const m: Record<string, any> = {}
  for (const f of allFields.value) m[f.key] = f
  return m
})
const groupedChildKeys = computed(() => new Set((groups.value || []).flatMap((g: any) => g.children || [])))
// Exclude grouped children from main listing
const displayFields = computed(() => allFields.value.filter((f: any) => !groupedChildKeys.value.has(f.key)))

// Visibility evaluation
function evaluateVisibility(field: any): boolean {
  if (!field.visibility || field.visibility.length === 0) return true
  
  for (const rule of field.visibility) {
    const conditions = rule.conditions || []
    const allMatch = rule.allConditionsMustMatch !== false // default true
    
    if (allMatch) {
      // All conditions must match (AND)
      const allPass = conditions.every((cond: any) => {
        const sourceValue = formData[cond.sourceKey]
        const targetValue = cond.value
        
        if (cond.operator === 'eq' || cond.operator === '==') {
          return sourceValue == targetValue
        } else if (cond.operator === 'neq' || cond.operator === '!=') {
          return sourceValue != targetValue
        }
        return true
      })
      if (allPass) return true
    } else {
      // Any condition can match (OR)
      const anyPass = conditions.some((cond: any) => {
        const sourceValue = formData[cond.sourceKey]
        const targetValue = cond.value
        
        if (cond.operator === 'eq' || cond.operator === '==') {
          return sourceValue == targetValue
        } else if (cond.operator === 'neq' || cond.operator === '!=') {
          return sourceValue != targetValue
        }
        return false
      })
      if (anyPass) return true
    }
  }
  
  return false
}

const visibleFields = computed(() => displayFields.value.filter(field => evaluateVisibility(field)))

function groupSection(g: any): string {
  const firstChild = (g.children || []).map((k: string) => fieldMap.value[k]).find(Boolean)
  return firstChild?._section || 'General'
}
function groupsForSection(section: string) {
  return (groups.value || [])
    .filter((g: any) => groupSection(g) === section)
    .filter((g: any) => groupChildFields(g).length > 0)
}
function groupChildFields(g: any) {
  return (g.children || [])
    .map((k: string) => fieldMap.value[k])
    .filter((f: any) => !!f && !f.internal && !f.internal_only)
}
function evaluateVisibilityForModel(field: any, model: Record<string, any>) {
  if (!field.visibility || field.visibility.length === 0) return true
  for (const rule of field.visibility) {
    const conditions = rule.conditions || []
    const allMatch = rule.allConditionsMustMatch !== false
    const test = (cond: any) => {
      const sourceValue = (cond.sourceKey in model) ? model[cond.sourceKey] : formData[cond.sourceKey]
      const targetValue = cond.value
      if (cond.operator === 'eq' || cond.operator === '==') return sourceValue == targetValue
      if (cond.operator === 'neq' || cond.operator === '!=') return sourceValue != targetValue
      return true
    }
    if (allMatch) { if (!conditions.every(test)) return false } else { if (!conditions.some(test)) return false }
  }
  return true
}

// Sections (order of first appearance); used as dividers only
const sections = computed(() => {
  const sectionSet = new Set<string>()
  const sectionOrder: string[] = []
  for (const field of visibleFields.value) {
    const section = field._section || 'General'
    if (!sectionSet.has(section)) {
      sectionSet.add(section)
      sectionOrder.push(section)
    }
  }
  return sectionOrder.length > 0 ? sectionOrder : ['General']
})

function fieldsBySection(section: string) {
  return visibleFields.value.filter((field: any) => (field._section || 'General') === section)
}

// Validation
function validateAll(): boolean {
  // Clear all errors
  for (const key of Object.keys(errors)) delete errors[key]
  let isValid = true
  for (const field of visibleFields.value) {
    if (field.validation?.required && !formData[field.key]) {
      errors[field.key] = `${field.label} is required`
      isValid = false
    }
    
    // Add more validation rules as needed
    if (field.type === 'integer' && formData[field.key]) {
      const value = Number(formData[field.key])
      if (isNaN(value) || !Number.isInteger(value)) {
        errors[field.key] = `${field.label} must be a whole number`
        isValid = false
      }
    }
    
    if (field.type === 'decimal' && formData[field.key]) {
      const value = Number(formData[field.key])
      if (isNaN(value)) {
        errors[field.key] = `${field.label} must be a number`
        isValid = false
      }
    }
  }
  return isValid
}

function submitForm() {
  if (validateAll()) {
    // For now, just show success
    alert('Form submitted successfully!')
    console.log('Form data:', formData)
  } else {
    const errorEl = document.querySelector('.error-summary')
    if (errorEl) {
      errorEl.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }
}
</script>

<style scoped>
.preview-container {
  min-height: 100vh;
  background: #f8f9fa;
}

.preview-header {
  background: white;
  border-bottom: 1px solid #e1e4e8;
  padding: 24px 0;
  margin-bottom: 32px;
}

.preview-header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.back-link {
  display: inline-block;
  margin-bottom: 12px;
  color: #0969da;
  text-decoration: none;
  font-size: 14px;
}

.back-link:hover {
  text-decoration: underline;
}

h1 {
  margin: 0 0 8px;
  font-size: 32px;
  font-weight: 600;
  color: #0d1117;
}

.journey-meta {
  margin: 0;
  color: #57606a;
  font-size: 14px;
}

.error-message {
  max-width: 800px;
  margin: 32px auto;
  padding: 24px;
  background: #ffebe9;
  border: 1px solid #ff8182;
  border-radius: 6px;
}

.error-message strong {
  color: #cf222e;
}

.preview-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px 48px;
}

.step-nav {
  display: flex;
  gap: 24px;
  margin-bottom: 32px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  overflow-x: auto;
}

.step-button {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: #57606a;
  white-space: nowrap;
  transition: all 0.2s;
}

.step-button:hover {
  color: #0d1117;
}

.step-button--active {
  color: #0969da;
  font-weight: 600;
}

.step-button--completed {
  color: #1a7f37;
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #f0f3f6;
  font-weight: 600;
  font-size: 12px;
}

.step-button--active .step-number {
  background: #0969da;
  color: white;
}

.step-button--completed .step-number {
  background: #1a7f37;
  color: white;
}

.form-container {
  background: white;
  border-radius: 8px;
  padding: 32px;
}

.error-summary {
  margin-bottom: 24px;
  padding: 16px;
  background: #ffebe9;
  border: 1px solid #ff8182;
  border-radius: 6px;
}

.error-summary h3 {
  margin: 0 0 12px;
  font-size: 16px;
  font-weight: 600;
  color: #cf222e;
}

.error-summary ul {
  margin: 0;
  padding-left: 20px;
}

.error-summary li {
  margin: 4px 0;
  color: #cf222e;
  font-size: 14px;
}

.form-section {
  margin-bottom: 32px;
}

.field-container {
  margin-bottom: 24px;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  padding-top: 24px;
  border-top: 1px solid #e1e4e8;
}
</style>
