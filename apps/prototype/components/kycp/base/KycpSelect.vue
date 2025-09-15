<template>
  <select
    :id="id"
    v-model="internalValue"
    :disabled="disabled"
    :required="required"
    :aria-invalid="error ? 'true' : undefined"
    :aria-describedby="ariaDescribedby"
    class="kycp-select"
    :class="{
      'kycp-select--error': error,
      'kycp-select--disabled': disabled
    }"
    @change="$emit('change', $event)"
  >
    <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
    <option
      v-for="option in normalizedOptions"
      :key="option.value"
      :value="option.value"
      :disabled="option.disabled"
    >
      {{ option.label }}
    </option>
  </select>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Option {
  label: string
  value: string | number
  disabled?: boolean
}

interface Props {
  id?: string
  modelValue?: string | number
  options: (string | Option)[]
  placeholder?: string
  disabled?: boolean
  required?: boolean
  error?: boolean
  ariaDescribedby?: string
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false,
  required: false,
  error: false
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number]
  'change': [event: Event]
}>()

const internalValue = computed({
  get: () => props.modelValue ?? '',
  set: (value) => emit('update:modelValue', value)
})

const normalizedOptions = computed(() => {
  return props.options.map(opt => {
    if (typeof opt === 'string') {
      // For string options, use the string as both code and label
      return { label: opt, value: opt }
    }
    // Ensure we have value (code) and label
    return {
      value: opt.value || opt.code || '', // Support both 'value' and 'code' properties
      label: opt.label || opt.value || '',
      disabled: opt.disabled
    }
  })
})
</script>

<style scoped>
.kycp-select {
  width: 100%;
  padding: 8px 32px 8px 10px;
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 13px;
  line-height: 1.5;
  color: #111827;
  background-color: #ffffff;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'%3E%3Cpath fill='%236b7280' d='M5 6L0 0h10z'/%3E%3C/svg%3E");
  background-position: right 10px center;
  background-repeat: no-repeat;
  background-size: 10px 6px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.15s ease;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

.kycp-select:hover:not(:disabled) {
  border-color: #9ca3af;
}

.kycp-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.kycp-select--error {
  border-color: #ef4444;
}

.kycp-select--error:focus {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.kycp-select:disabled,
.kycp-select--disabled {
  background-color: #f9fafb;
  color: #9ca3af;
  cursor: not-allowed;
}
</style>