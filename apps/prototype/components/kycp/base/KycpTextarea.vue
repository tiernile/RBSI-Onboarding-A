<template>
  <textarea
    :id="id"
    v-model="internalValue"
    :placeholder="placeholder"
    :disabled="disabled"
    :readonly="readonly"
    :required="required"
    :maxlength="maxlength"
    :rows="rows"
    :aria-invalid="error ? 'true' : undefined"
    :aria-describedby="ariaDescribedby"
    class="kycp-textarea"
    :class="{
      'kycp-textarea--error': error,
      'kycp-textarea--disabled': disabled
    }"
    @blur="$emit('blur', $event)"
    @focus="$emit('focus', $event)"
  />
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  id?: string
  modelValue?: string
  placeholder?: string
  disabled?: boolean
  readonly?: boolean
  required?: boolean
  maxlength?: number
  rows?: number
  error?: boolean
  ariaDescribedby?: string
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false,
  readonly: false,
  required: false,
  error: false,
  rows: 4
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  'blur': [event: FocusEvent]
  'focus': [event: FocusEvent]
}>()

const internalValue = computed({
  get: () => props.modelValue ?? '',
  set: (value) => emit('update:modelValue', value)
})
</script>

<style scoped>
.kycp-textarea {
  width: 100%;
  padding: var(--kycp-spacing-sm) var(--kycp-spacing-md);
  font-family: var(--kycp-font-family);
  font-size: var(--kycp-font-size-base);
  color: var(--kycp-gray-900);
  background-color: var(--kycp-input-bg);
  border: 1px solid var(--kycp-input-border);
  border-radius: var(--kycp-radius-base);
  transition: all var(--kycp-transition-fast);
  resize: vertical;
  min-height: 80px;
}

.kycp-textarea:hover:not(:disabled) {
  border-color: var(--kycp-input-border-hover);
}

.kycp-textarea:focus {
  outline: none;
  border-color: var(--kycp-input-border-focus);
  box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.1);
}

.kycp-textarea::placeholder {
  color: var(--kycp-placeholder-color);
}

.kycp-textarea--error {
  border-color: var(--kycp-error);
}

.kycp-textarea--error:focus {
  border-color: var(--kycp-error);
  box-shadow: 0 0 0 2px rgba(211, 47, 47, 0.1);
}

.kycp-textarea:disabled,
.kycp-textarea--disabled {
  background-color: var(--kycp-input-disabled-bg);
  color: var(--kycp-gray-400);
  cursor: not-allowed;
  resize: none;
}
</style>