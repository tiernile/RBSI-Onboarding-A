<template>
  <div class="kycp-radio-group" :role="role" :aria-labelledby="ariaLabelledby">
    <label
      v-for="option in normalizedOptions"
      :key="option.value"
      class="kycp-radio-item"
      :class="{ 'kycp-radio-item--disabled': option.disabled || disabled }"
    >
      <input
        type="radio"
        :name="name"
        :value="option.value"
        :checked="modelValue === option.value"
        :disabled="option.disabled || disabled"
        :required="required"
        :aria-describedby="ariaDescribedby"
        class="kycp-radio-input"
        @change="handleChange(option.value)"
      />
      <span class="kycp-radio-label">{{ option.label }}</span>
    </label>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Option {
  label: string
  value: string | number
  disabled?: boolean
}

interface Props {
  modelValue?: string | number
  options: (string | Option)[]
  name?: string
  disabled?: boolean
  required?: boolean
  role?: string
  ariaLabelledby?: string
  ariaDescribedby?: string
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false,
  required: false,
  role: 'radiogroup'
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number]
}>()

const normalizedOptions = computed(() => {
  return props.options.map(opt => {
    if (typeof opt === 'string') {
      return { label: opt, value: opt }
    }
    return opt
  })
})

const handleChange = (value: string | number) => {
  emit('update:modelValue', value)
}
</script>

<style scoped>
.kycp-radio-group {
  display: flex;
  flex-direction: column;
  gap: var(--kycp-spacing-sm);
}

.kycp-radio-item {
  display: flex;
  align-items: center;
  cursor: pointer;
  position: relative;
}

.kycp-radio-input {
  width: 18px;
  height: 18px;
  margin: 0;
  margin-right: var(--kycp-spacing-sm);
  cursor: pointer;
  flex-shrink: 0;
}

.kycp-radio-label {
  font-size: var(--kycp-font-size-base);
  color: var(--kycp-gray-900);
  user-select: none;
  line-height: 1.5;
}

.kycp-radio-item--disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.kycp-radio-item--disabled .kycp-radio-input,
.kycp-radio-item--disabled .kycp-radio-label {
  cursor: not-allowed;
}

.kycp-radio-item:hover:not(.kycp-radio-item--disabled) .kycp-radio-label {
  color: var(--kycp-gray-700);
}
</style>