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
  type?: 'text' | 'email' | 'tel' | 'number' | 'password' | 'url'
  placeholder?: string
  disabled?: boolean
  readonly?: boolean
  required?: boolean
  maxlength?: number
  error?: boolean
  ariaDescribedby?: string
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  disabled: false,
  readonly: false,
  required: false,
  error: false
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
  padding: var(--kycp-spacing-sm) var(--kycp-spacing-md);
  font-family: var(--kycp-font-family);
  font-size: var(--kycp-font-size-base);
  color: var(--kycp-gray-900);
  background-color: var(--kycp-input-bg);
  border: 1px solid var(--kycp-input-border);
  border-radius: var(--kycp-radius-base);
  transition: all var(--kycp-transition-fast);
  -webkit-appearance: none;
  appearance: none;
}

.kycp-input:hover:not(:disabled) {
  border-color: var(--kycp-input-border-hover);
}

.kycp-input:focus {
  outline: none;
  border-color: var(--kycp-input-border-focus);
  box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.1);
}

.kycp-input::placeholder {
  color: var(--kycp-placeholder-color);
}

.kycp-input--error {
  border-color: var(--kycp-error);
}

.kycp-input--error:focus {
  border-color: var(--kycp-error);
  box-shadow: 0 0 0 2px rgba(211, 47, 47, 0.1);
}

.kycp-input:disabled,
.kycp-input--disabled {
  background-color: var(--kycp-input-disabled-bg);
  color: var(--kycp-gray-400);
  cursor: not-allowed;
}
</style>