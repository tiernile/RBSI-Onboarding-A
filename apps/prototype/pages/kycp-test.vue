<template>
  <div class="kycp-test">
    <header class="header">
      <NuxtLink to="/" class="back-link">← Back to Mission Control</NuxtLink>
      <h1>KYCP Components Test</h1>
      <p class="subtitle">Testing dynamic form rendering with KYCP-aligned schema</p>
    </header>

    <div class="controls">
      <label>
        Application Status:
        <select v-model="applicationStatus">
          <option value="draft">Draft</option>
          <option value="submitted">Submitted</option>
          <option value="approved">Approved</option>
        </select>
      </label>
      <button @click="validateForm" class="validate-btn">Validate Form</button>
      <button @click="resetForm" class="reset-btn">Reset</button>
    </div>

    <main class="form-container" v-if="schema">
      <div class="form-info">
        <p>Total fields: {{ schema.fields?.length || 0 }}</p>
        <p>Visible fields: {{ visibleFields.size }}</p>
        <p>Fields with errors: {{ Object.keys(errors).length }}</p>
      </div>

      <form @submit.prevent="handleSubmit">
        <div v-for="field in visibleFieldsList" :key="field.key" class="field-wrapper">
          <!-- String Field -->
          <StringField
            v-if="field.type === 'string'"
            :id="field.key"
            :label="field.label"
            :modelValue="formData[field.key]"
            @update:modelValue="updateField(field.key, $event)"
            :required="field.validation?.required"
            :maxLength="field.validation?.maxLength"
            :pattern="field.validation?.pattern"
            :helpText="field.description"
            :error="errors[field.key]"
            :statusRights="field.statusRights"
            :applicationStatus="applicationStatus"
          />

          <!-- FreeText Field -->
          <FreeTextArea
            v-else-if="field.type === 'freeText'"
            :id="field.key"
            :label="field.label"
            :modelValue="formData[field.key]"
            @update:modelValue="updateField(field.key, $event)"
            :required="field.validation?.required"
            :maxLength="field.validation?.maxLength"
            :helpText="field.description"
            :error="errors[field.key]"
            :statusRights="field.statusRights"
            :applicationStatus="applicationStatus"
          />

          <!-- Integer Field -->
          <IntegerField
            v-else-if="field.type === 'integer'"
            :id="field.key"
            :label="field.label"
            :modelValue="formData[field.key]"
            @update:modelValue="updateField(field.key, $event)"
            :required="field.validation?.required"
            :min="field.validation?.min"
            :max="field.validation?.max"
            :helpText="field.description"
            :error="errors[field.key]"
            :statusRights="field.statusRights"
            :applicationStatus="applicationStatus"
          />

          <!-- Decimal Field -->
          <DecimalField
            v-else-if="field.type === 'decimal'"
            :id="field.key"
            :label="field.label"
            :modelValue="formData[field.key]"
            @update:modelValue="updateField(field.key, $event)"
            :required="field.validation?.required"
            :precision="field.validation?.precision"
            :scale="field.validation?.scale"
            :helpText="field.description"
            :error="errors[field.key]"
            :statusRights="field.statusRights"
            :applicationStatus="applicationStatus"
          />

          <!-- Date Field -->
          <DateField
            v-else-if="field.type === 'date'"
            :id="field.key"
            :label="field.label"
            :modelValue="formData[field.key]"
            @update:modelValue="updateField(field.key, $event)"
            :required="field.validation?.required"
            :format="field.validation?.dateFormat || 'DD/MM/YYYY'"
            :helpText="field.description"
            :error="errors[field.key]"
            :statusRights="field.statusRights"
            :applicationStatus="applicationStatus"
          />

          <!-- Lookup Field -->
          <LookupField
            v-else-if="field.type === 'lookup'"
            :id="field.key"
            :label="field.label"
            :modelValue="formData[field.key]"
            @update:modelValue="updateField(field.key, $event)"
            :required="field.validation?.required"
            :options="field.options || []"
            :helpText="field.description"
            :error="errors[field.key]"
            :statusRights="field.statusRights"
            :applicationStatus="applicationStatus"
          />

          <!-- Debug info -->
          <div v-else class="debug-field">
            <strong>Unknown field type: {{ field.type }}</strong>
            <pre>{{ field }}</pre>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="submit-btn">Submit Form</button>
        </div>
      </form>

      <!-- Debug Panel -->
      <details class="debug-panel">
        <summary>Debug: Form Data</summary>
        <pre>{{ JSON.stringify(formData, null, 2) }}</pre>
      </details>
    </main>

    <div v-else class="loading">
      Loading schema...
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useKycpForm } from '~/composables/useKycpForm'
import StringField from '~/components/kycp/fields/StringField.vue'
import FreeTextArea from '~/components/kycp/fields/FreeTextArea.vue'
import IntegerField from '~/components/kycp/fields/IntegerField.vue'
import DecimalField from '~/components/kycp/fields/DecimalField.vue'
import DateField from '~/components/kycp/fields/DateField.vue'
import LookupField from '~/components/kycp/fields/LookupField.vue'

// Load KYCP schema
const schema = ref<any>(null)

// Use KYCP form composable
const {
  formData,
  applicationStatus,
  errors,
  visibleFields,
  getEffectiveRight,
  updateField,
  validateForm: validate,
  resetForm: reset
} = useKycpForm(schema)

// Get list of visible fields
const visibleFieldsList = computed(() => {
  if (!schema.value?.fields) return []
  
  return schema.value.fields.filter((field: any) => {
    const right = getEffectiveRight(field)
    return right !== 'hidden'
  })
})

// Load schema on mount
onMounted(async () => {
  try {
    // Load the KYCP-format schema we just generated
    const response = await fetch('/api/schema/non-lux-lp-demo-kycp')
    if (response.ok) {
      schema.value = await response.json()
    } else {
      console.error('Failed to load schema')
    }
  } catch (error) {
    console.error('Error loading schema:', error)
  }
})

// Handle form submission
const handleSubmit = () => {
  if (validate()) {
    console.log('Form is valid!', formData.value)
    alert('Form submitted successfully! Check console for data.')
  } else {
    console.log('Form has errors:', errors.value)
    alert('Please fix validation errors')
  }
}

// Wrapper functions for template
const validateForm = () => {
  const isValid = validate()
  if (isValid) {
    alert('Form is valid!')
  } else {
    alert(`Form has ${Object.keys(errors.value).length} error(s)`)
  }
}

const resetForm = () => {
  reset()
  alert('Form reset')
}
</script>

<style scoped>
.kycp-test {
  min-height: 100vh;
  background: var(--color-bg);
  padding: 24px;
}

.header {
  max-width: 1200px;
  margin: 0 auto 32px;
}

.back-link {
  display: inline-block;
  margin-bottom: 16px;
  color: var(--color-link);
  text-decoration: none;
}

.back-link:hover {
  text-decoration: underline;
}

h1 {
  margin: 0 0 8px;
  font-size: 32px;
  color: var(--color-text-primary);
}

.subtitle {
  margin: 0;
  color: var(--color-text-secondary);
}

.controls {
  max-width: 1200px;
  margin: 0 auto 24px;
  padding: 16px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  display: flex;
  gap: 16px;
  align-items: center;
}

.controls label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.controls select {
  padding: 4px 8px;
  border: 1px solid var(--color-border);
  border-radius: 4px;
}

.validate-btn,
.reset-btn {
  padding: 8px 16px;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  background: var(--color-surface);
  cursor: pointer;
}

.validate-btn:hover,
.reset-btn:hover {
  background: var(--color-bg);
}

.form-container {
  max-width: 1200px;
  margin: 0 auto;
}

.form-info {
  padding: 16px;
  margin-bottom: 24px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  display: flex;
  gap: 32px;
}

.form-info p {
  margin: 0;
  color: var(--color-text-secondary);
}

form {
  background: var(--color-surface);
  padding: 32px;
  border-radius: 8px;
  border: 1px solid var(--color-border);
}

.field-wrapper {
  margin-bottom: 24px;
}

.debug-field {
  padding: 16px;
  background: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: 4px;
}

.debug-field pre {
  margin: 8px 0 0;
  font-size: 12px;
  overflow-x: auto;
}

.form-actions {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--color-border);
}

.submit-btn {
  padding: 12px 24px;
  background: var(--color-link);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.submit-btn:hover {
  background: var(--color-link-hover);
}

.debug-panel {
  margin-top: 24px;
  padding: 16px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
}

.debug-panel summary {
  cursor: pointer;
  font-weight: 500;
  color: var(--color-text-primary);
}

.debug-panel pre {
  margin-top: 16px;
  padding: 16px;
  background: var(--color-bg);
  border-radius: 4px;
  overflow-x: auto;
  font-size: 12px;
}

.loading {
  max-width: 1200px;
  margin: 0 auto;
  padding: 48px;
  text-align: center;
  color: var(--color-text-secondary);
}
</style>