<template>
  <input
    :id="id"
    v-model="internalValue"
    :type="type"
    :placeholder="placeholder"
    :disabled="disabled"
    :readonly="readonly"
    :required="required"
    :maxlength="maxlength"
    :aria-invalid="error ? 'true' : undefined"
    :aria-describedby="ariaDescribedby"
    class="kycp-input"
    :class="{
      'kycp-input--error': error,
      'kycp-input--disabled': disabled
    }"
    @blur="$emit('blur', $event)"
    @focus="$emit('focus', $event)"
  />
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  id?: string
  modelValue?: string | number
  type?: 'text' | 'email' | 'tel' | 'number' | 'password' | 'url' | 'date'
  dataType?: 'string' | 'integer' | 'decimal' | 'date'
  placeholder?: string
  disabled?: boolean
  readonly?: boolean
  required?: boolean
  maxlength?: number
  min?: number
  max?: number
  step?: number | string
  error?: boolean
  ariaDescribedby?: string
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  dataType: 'string',
  disabled: false,
  readonly: false,
  required: false,
  error: false,
  // KYCP platform limits
  maxlength: 1024, // string default
  min: 0, // integer minimum
  max: 2147483647, // integer maximum  
  step: 1 // integer step
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number]
  'blur': [event: FocusEvent]
  'focus': [event: FocusEvent]
}>()

const internalValue = computed({
  get: () => props.modelValue ?? '',
  set: (value) => emit('update:modelValue', value)
})
</script>

<style scoped>
.kycp-input {
  width: 100%;
  padding: 8px 10px;
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 13px;
  line-height: 1.5;
  color: #111827;
  background-color: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  transition: all 0.15s ease;
  -webkit-appearance: none;
  appearance: none;
}

.kycp-input:hover:not(:disabled) {
  border-color: #9ca3af;
}

.kycp-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.kycp-input::placeholder {
  color: #9ca3af;
}

.kycp-input--error {
  border-color: #ef4444;
}

.kycp-input--error:focus {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.kycp-input:disabled,
.kycp-input--disabled {
  background-color: #f9fafb;
  color: #9ca3af;
  cursor: not-allowed;
}
</style>