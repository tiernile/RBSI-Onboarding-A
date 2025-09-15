<template>
  <div class="preview-container">
    <header class="preview-header">
      <div class="preview-header-content">
        <NuxtLink to="/" class="back-link">← Mission Control</NuxtLink>
        <h1>{{ journeyName || journeyKey }}</h1>
        <p class="journey-meta">{{ journeyKey }} · Version {{ journeyVersion }}</p>
      </div>
    </header>

    <div v-if="error" class="error-message">
      <strong>Failed to load schema.</strong>
      <p>Please check that the journey exists in the manifest.</p>
    </div>
    
    <div v-else class="preview-content">
      <nav class="step-nav" aria-label="Form sections">
        <button 
          v-for="(g, i) in groups" 
          :key="g" 
          class="step-button" 
          :class="{ 'step-button--active': i === step, 'step-button--completed': i < step }" 
          @click="go(i)"
        >
          <span class="step-number">{{ i + 1 }}</span>
          <span class="step-label">{{ g }}</span>
        </button>
      </nav>

      <div class="form-container">
        <ErrorSummary :errors="errors" />
        
        <KycpFieldGroup 
          :title="currentGroup"
          :subtitle="`Section ${step + 1} of ${groups.length}`"
        >
          <div v-for="item in currentGroupItems" :key="item.id">
            <KycpFieldWrapper 
              :id="item.id" 
              :label="item.label" 
              :required="item.mandatory" 
              :error="errors[item.id] || null"
              :help="item.help"
            >
              <KycpInput
                v-if="item.control === 'text' || item.control === 'email' || item.control === 'number' || !item.control"
                :id="item.id"
                v-model="answers[item.id]"
                :type="item.control || 'text'"
                :placeholder="item.placeholder"
                :required="item.mandatory"
                :error="!!errors[item.id]"
                :aria-describedby="errors[item.id] ? `${item.id}-error` : undefined"
              />
              <KycpSelect
                v-else-if="item.control === 'select'"
                :id="item.id"
                v-model="answers[item.id]"
                :options="item.options || []"
                :placeholder="item.placeholder || 'Please select...'"
                :required="item.mandatory"
                :error="!!errors[item.id]"
                :aria-describedby="errors[item.id] ? `${item.id}-error` : undefined"
              />
              <KycpTextarea
                v-else-if="item.control === 'textarea'"
                :id="item.id"
                v-model="answers[item.id]"
                :placeholder="item.placeholder"
                :required="item.mandatory"
                :error="!!errors[item.id]"
                :aria-describedby="errors[item.id] ? `${item.id}-error` : undefined"
              />
            </KycpFieldWrapper>
          </div>
        </KycpFieldGroup>
        
        <div class="form-actions">
          <button 
            class="kycp-button kycp-button-secondary" 
            :disabled="step === 0" 
            @click="back"
          >
            Back
          </button>
          <button 
            v-if="step < groups.length - 1" 
            class="kycp-button kycp-button-primary"
            @click="next"
          >
            Next
          </button>
          <button 
            v-else 
            class="kycp-button kycp-button-primary"
            @click="onSubmit"
          >
            Submit
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import KycpInput from '~/components/kycp/base/KycpInput.vue'
import KycpSelect from '~/components/kycp/base/KycpSelect.vue'
import KycpTextarea from '~/components/kycp/base/KycpTextarea.vue'
import KycpFieldWrapper from '~/components/kycp/base/KycpFieldWrapper.vue'
import KycpFieldGroup from '~/components/kycp/base/KycpFieldGroup.vue'
import ErrorSummary from '~/components/nile/ErrorSummary.vue'
import { isVisible } from '~/composables/useConditions'
import { useValidation } from '~/composables/useValidation'

// Import KYCP design system
import '~/assets/kycp-design.css'

const route = useRoute()
const journeyKey = computed(() => route.params.journey as string)
const { data: schema, error } = await useSchema(journeyKey.value)

// Extract journey metadata
const journeyName = computed(() => schema.value?.name || '')
const journeyVersion = computed(() => schema.value?.version || '0.1.0')

const answers = reactive<Record<string, any>>({})
// Items not marked as internal_only
const publicItems = computed(() => {
  const items = (schema.value?.items || []) as any[]
  return items.filter(it => !it.internal_only)
})
// Visible, public items
const visibleItems = computed(() => {
  const items = publicItems.value
  return items.filter(it => isVisible(it.visibility, answers))
})

// Validate only public items
const { errors, validate } = useValidation(publicItems.value as any, answers)

function onSubmit() {
  if (validate()) {
    // For PoC, just alert success
    alert('Submitted')
  } else {
    // scroll to summary
    const el = document.querySelector('.error-summary') as HTMLElement
    if (el) el.scrollIntoView({ behavior: 'smooth' })
  }
}

// Simple grouping by section (first occurrence order)
const groups = computed(() => {
  const items = (publicItems.value || []) as any[]
  const seen = new Set<string>()
  const order: string[] = []
  for (const it of items) {
    const section = it.section || 'General'
    if (!seen.has(section)) { seen.add(section); order.push(section) }
  }
  return order
})

const step = ref(0)
const currentGroup = computed(() => groups.value[step.value])
const currentGroupItems = computed(() => visibleItems.value.filter((it: any) => (it.section || 'General') === currentGroup.value))

function go(i: number) { step.value = i }
function back() { if (step.value>0) step.value-- }
function next() {
  // validate current group only
  const allItems = (publicItems.value || []) as any[]
  const current = allItems.filter(it => (it.section || 'General') === currentGroup.value)
  const { errors: errs, validate } = useValidation(current as any, answers)
  const ok = validate()
  // merge current errors into main errors bag
  Object.keys(errors).forEach(k => delete (errors as any)[k])
  Object.assign(errors, errs)
  if (ok && step.value < groups.value.length-1) step.value++
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
  max-width: 900px;
  margin: 0 auto;
  padding: 0 24px;
}

.back-link {
  color: var(--kycp-primary);
  text-decoration: none;
  font-size: 14px;
  display: inline-block;
  margin-bottom: 12px;
}

.back-link:hover {
  text-decoration: underline;
}

.preview-header h1 {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 600;
  color: var(--kycp-gray-900);
}

.journey-meta {
  margin: 0;
  color: var(--kycp-gray-600);
  font-size: 14px;
}

.error-message {
  max-width: 900px;
  margin: 32px auto;
  padding: 24px;
  background: var(--kycp-error-bg);
  border: 1px solid var(--kycp-error);
  border-radius: var(--kycp-radius-base);
  color: var(--kycp-error);
}

.error-message strong {
  display: block;
  margin-bottom: 8px;
}

.preview-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 24px 48px;
}

.step-nav {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
  padding: 16px;
  background: white;
  border: 1px solid var(--kycp-gray-200);
  border-radius: var(--kycp-radius-lg);
  overflow-x: auto;
}

.step-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--kycp-gray-50);
  border: 1px solid var(--kycp-gray-300);
  border-radius: var(--kycp-radius-full);
  font-size: 14px;
  color: var(--kycp-gray-600);
  cursor: pointer;
  transition: all var(--kycp-transition-fast);
  white-space: nowrap;
}

.step-button:hover {
  background: var(--kycp-gray-100);
  border-color: var(--kycp-gray-400);
}

.step-button--active {
  background: var(--kycp-primary);
  border-color: var(--kycp-primary);
  color: white;
}

.step-button--completed {
  background: var(--kycp-success-bg);
  border-color: var(--kycp-success);
  color: var(--kycp-success);
}

.step-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  font-size: 12px;
  font-weight: 600;
  color: inherit;
}

.step-button--active .step-number {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.step-label {
  font-weight: 500;
}

.form-container {
  background: white;
  border-radius: var(--kycp-radius-lg);
  padding: 0;
  box-shadow: var(--kycp-shadow-sm);
}

.form-actions {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  padding: 24px;
  border-top: 1px solid var(--kycp-gray-200);
  background: var(--kycp-gray-50);
  border-radius: 0 0 var(--kycp-radius-lg) var(--kycp-radius-lg);
}

/* Button styles from design system */
.kycp-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--kycp-spacing-sm) var(--kycp-spacing-xl);
  font-family: var(--kycp-font-family);
  font-size: var(--kycp-font-size-base);
  font-weight: 500;
  border-radius: var(--kycp-radius-base);
  border: 1px solid transparent;
  cursor: pointer;
  transition: all var(--kycp-transition-fast);
  text-decoration: none;
}

.kycp-button-primary {
  background: var(--kycp-primary);
  color: white;
  border-color: var(--kycp-primary);
}

.kycp-button-primary:hover:not(:disabled) {
  background: var(--kycp-primary-hover);
  border-color: var(--kycp-primary-hover);
}

.kycp-button-secondary {
  background: white;
  color: var(--kycp-gray-700);
  border-color: var(--kycp-gray-300);
}

.kycp-button-secondary:hover:not(:disabled) {
  background: var(--kycp-gray-50);
  border-color: var(--kycp-gray-400);
}

.kycp-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 640px) {
  .step-nav {
    padding: 12px;
  }
  
  .step-button {
    padding: 6px 12px;
    font-size: 13px;
  }
  
  .form-actions {
    flex-direction: column-reverse;
  }
  
  .kycp-button {
    width: 100%;
  }
}
</style>
