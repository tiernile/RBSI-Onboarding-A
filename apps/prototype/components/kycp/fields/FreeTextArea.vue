<template>
  <KycpFieldWrapper :id="model.key" :label="model.label" :required="model.validation?.required" :help="model.description" :error="error">
    <KycpTextarea
      :id="model.key"
      v-model="internal"
      :rows="rows"
      :readonly="isReadOnly"
      :disabled="isDisabled"
      :maxlength="model.validation?.maxLength ?? 8192"
      :error="!!error"
    />
  </KycpFieldWrapper>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import KycpTextarea from '~/components/kycp/base/KycpTextarea.vue'
import KycpFieldWrapper from '~/components/kycp/base/KycpFieldWrapper.vue'
import type { BaseField, EffectiveRight } from '~/types/kycp'
import { resolveRight } from '~/types/kycp'

const props = defineProps<{ model: BaseField; modelValue: string; status?: string; rows?: number }>()
const emit = defineEmits<{ (e: 'update:modelValue', v: string): void }>()

const right = computed<EffectiveRight>(() => resolveRight(props.model.statusRights, props.status || ''))
const isReadOnly = computed(() => right.value === 'readOnly')
const isDisabled = computed(() => right.value === 'hidden')
const rows = computed(() => props.rows ?? 6)

const error = computed(() => {
  if (props.model.validation?.required && (!props.modelValue || props.modelValue === '')) return `${props.model.label || props.model.key} is required`
  const max = props.model.validation?.maxLength ?? 8192
  if (props.modelValue && String(props.modelValue).length > max) return `Maximum length is ${max}`
  return ''
})

const internal = computed({
  get: () => props.modelValue || '',
  set: (v: string) => emit('update:modelValue', v)
})
</script>

