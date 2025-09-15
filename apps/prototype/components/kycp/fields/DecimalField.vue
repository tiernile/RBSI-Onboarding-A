<template>
  <KycpFieldWrapper :id="model.key" :label="model.label" :required="model.validation?.required" :help="model.description" :error="error">
    <KycpInput
      :id="model.key"
      v-model="text"
      type="text"
      :readonly="isReadOnly"
      :disabled="isDisabled"
      :error="!!error"
      @input="sanitize"
      @blur="roundToScale"
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

const precision = computed(() => props.model.validation?.precision ?? 18)
const scale = computed(() => props.model.validation?.scale ?? 2)
const text = ref(props.modelValue != null ? props.modelValue.toFixed(scale.value) : '')

watch(() => props.modelValue, v => { text.value = v != null ? v.toFixed(scale.value) : '' })

function sanitize() {
  // allow digits and a single dot; block exponent and extra dots
  let t = text.value
  t = t.replace(/[^0-9.]/g, '')
  const parts = t.split('.')
  if (parts.length > 2) t = parts[0] + '.' + parts.slice(1).join('')
  // enforce scale during input by trimming fractional part
  const [i, f] = t.split('.')
  if (f && f.length > scale.value) t = i + '.' + f.slice(0, scale.value)
  text.value = t
}

function roundToScale() {
  if (!text.value) { emit('update:modelValue', null); return }
  const num = Number(text.value)
  if (!Number.isFinite(num)) { emit('update:modelValue', null); text.value = ''; return }
  // enforce precision
  const [i, f = ''] = text.value.split('.')
  if ((i + f).length > precision.value) {
    // truncate integer part to fit precision
    const maxIntLen = precision.value - Math.min(scale.value, f.length)
    const truncated = i.slice(0, Math.max(0, maxIntLen))
    text.value = truncated + (f ? '.' + f : '')
  }
  const rounded = Math.round(num * Math.pow(10, scale.value)) / Math.pow(10, scale.value)
  emit('update:modelValue', rounded)
  text.value = rounded.toFixed(scale.value)
}

const error = computed(() => {
  if (props.model.validation?.required && (props.modelValue == null)) return `${props.model.label || props.model.key} is required`
  return ''
})
</script>

