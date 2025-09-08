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
      return { label: opt, value: opt }
    }
    return opt
  })
})
</script>

<style scoped>
.kycp-select {
  width: 100%;
  padding: var(--kycp-spacing-sm) var(--kycp-spacing-2xl) var(--kycp-spacing-sm) var(--kycp-spacing-md);
  font-family: var(--kycp-font-family);
  font-size: var(--kycp-font-size-base);
  color: var(--kycp-gray-900);
  background-color: var(--kycp-input-bg);
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3E%3Cpath stroke='%236B7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3E%3C/svg%3E");
  background-position: right var(--kycp-spacing-sm) center;
  background-repeat: no-repeat;
  background-size: 20px;
  border: 1px solid var(--kycp-input-border);
  border-radius: var(--kycp-radius-base);
  cursor: pointer;
  transition: all var(--kycp-transition-fast);
  -webkit-appearance: none;
  appearance: none;
}

.kycp-select:hover:not(:disabled) {
  border-color: var(--kycp-input-border-hover);
}

.kycp-select:focus {
  outline: none;
  border-color: var(--kycp-input-border-focus);
  box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.1);
}

.kycp-select--error {
  border-color: var(--kycp-error);
}

.kycp-select--error:focus {
  border-color: var(--kycp-error);
  box-shadow: 0 0 0 2px rgba(211, 47, 47, 0.1);
}

.kycp-select:disabled,
.kycp-select--disabled {
  background-color: var(--kycp-input-disabled-bg);
  color: var(--kycp-gray-400);
  cursor: not-allowed;
}
</style>