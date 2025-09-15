<template>
  <KycpFieldWrapper :id="model.key" :label="model.label" :required="model.validation?.required" :help="model.description" :error="error">
    <KycpInput
      :id="model.key"
      v-model="text"
      type="text"
      :readonly="isReadOnly"
      :disabled="isDisabled"
      :error="!!error"
      @blur="commit"
    />
  </KycpFieldWrapper>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import KycpInput from '~/components/kycp/base/KycpInput.vue'
import KycpFieldWrapper from '~/components/kycp/base/KycpFieldWrapper.vue'
import type { BaseField, EffectiveRight } from '~/types/kycp'
import { resolveRight } from '~/types/kycp'

const props = defineProps<{ model: BaseField; modelValue: number | null; status?: string }>()
const emit = defineEmits<{ (e: 'update:modelValue', v: number | null): void }>()

const right = computed<EffectiveRight>(() => resolveRight(props.model.statusRights, props.status || ''))
const isReadOnly = computed(() => right.value === 'readOnly')
const isDisabled = computed(() => right.value === 'hidden')

const maxDefault = 2147483647
const minDefault = 0
const text = ref(props.modelValue != null ? String(props.modelValue) : '')

watch(() => props.modelValue, v => { text.value = v != null ? String(v) : '' })

function commit() {
  // strip non-digits
  const digits = (text.value || '').replace(/[^0-9-]/g, '')
  let num = digits === '' || digits === '-' ? null : Number(digits)
  if (num != null) {
    const min = props.model.validation?.min ?? minDefault
    const max = props.model.validation?.max ?? maxDefault
    if (!Number.isFinite(num)) num = null
    else num = Math.max(min, Math.min(max, Math.trunc(num)))
  }
  emit('update:modelValue', num)
  text.value = num == null ? '' : String(num)
}

const error = computed(() => {
  if (props.model.validation?.required && (props.modelValue == null)) return `${props.model.label || props.model.key} is required`
  if (props.modelValue != null) {
    const min = props.model.validation?.min ?? minDefault
    const max = props.model.validation?.max ?? maxDefault
    if (props.modelValue < min) return `Minimum is ${min}`
    if (props.modelValue > max) return `Maximum is ${max}`
  }
  return ''
})
</script>

