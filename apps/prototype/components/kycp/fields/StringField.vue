<template>
  <KycpFieldWrapper :id="model.key" :label="model.label" :required="model.validation?.required" :help="model.description" :error="error">
    <KycpInput
      :id="model.key"
      v-model="internal"
      :placeholder="placeholder"
      :readonly="isReadOnly"
      :disabled="isDisabled"
      :maxlength="model.validation?.maxLength ?? 1024"
      :error="!!error"
    />
  </KycpFieldWrapper>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import KycpInput from '~/components/kycp/base/KycpInput.vue'
import KycpFieldWrapper from '~/components/kycp/base/KycpFieldWrapper.vue'
import type { BaseField, EffectiveRight } from '~/types/kycp'
import { resolveRight } from '~/types/kycp'

const props = defineProps<{ model: BaseField; modelValue: string; status?: string; placeholder?: string }>()
const emit = defineEmits<{ (e: 'update:modelValue', v: string): void }>()

const right = computed<EffectiveRight>(() => resolveRight(props.model.statusRights, props.status || ''))
const isReadOnly = computed(() => right.value === 'readOnly')
const isDisabled = computed(() => right.value === 'hidden')
const placeholder = computed(() => props.placeholder || '')

const error = computed(() => {
  if (props.model.validation?.required && (!props.modelValue || props.modelValue === '')) return `${props.model.label || props.model.key} is required`
  const max = props.model.validation?.maxLength ?? 1024
  if (props.modelValue && String(props.modelValue).length > max) return `Maximum length is ${max}`
  return ''
})

const internal = computed({
  get: () => props.modelValue || '',
  set: (v: string) => emit('update:modelValue', v)
})
</script>

