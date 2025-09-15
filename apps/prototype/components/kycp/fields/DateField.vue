<template>
  <KycpFieldWrapper :id="model.key" :label="model.label" :required="model.validation?.required" :help="model.description" :error="error">
    <KycpInput
      :id="model.key"
      v-model="text"
      type="text"
      :placeholder="'DD/MM/YYYY'"
      :readonly="isReadOnly"
      :disabled="isDisabled"
      :error="!!error"
      @blur="formatAndCommit"
    />
  </KycpFieldWrapper>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import KycpInput from '~/components/kycp/base/KycpInput.vue'
import KycpFieldWrapper from '~/components/kycp/base/KycpFieldWrapper.vue'
import type { BaseField, EffectiveRight } from '~/types/kycp'
import { resolveRight } from '~/types/kycp'

const props = defineProps<{ model: BaseField; modelValue: string | null; status?: string }>()
const emit = defineEmits<{ (e: 'update:modelValue', v: string | null): void }>()

const right = computed<EffectiveRight>(() => resolveRight(props.model.statusRights, props.status || ''))
const isReadOnly = computed(() => right.value === 'readOnly')
const isDisabled = computed(() => right.value === 'hidden')

const text = ref(props.modelValue || '')
watch(() => props.modelValue, v => { text.value = v || '' })

function isValidDate(d: string) {
  const m = d.match(/^(\d{2})\/(\d{2})\/(\d{4})$/)
  if (!m) return false
  const dd = Number(m[1]), mm = Number(m[2]), yyyy = Number(m[3])
  const date = new Date(yyyy, mm - 1, dd)
  return date.getFullYear() === yyyy && date.getMonth() === mm - 1 && date.getDate() === dd
}

function formatAndCommit() {
  if (!text.value) { emit('update:modelValue', null); return }
  // zero-pad if possible
  const parts = text.value.replace(/[^0-9/]/g, '').split('/')
  if (parts.length === 3) {
    const [d, m, y] = parts
    const dd = (d || '').padStart(2, '0').slice(0, 2)
    const mm = (m || '').padStart(2, '0').slice(0, 2)
    const yyyy = (y || '').slice(0, 4)
    const fmt = `${dd}/${mm}/${yyyy}`
    text.value = fmt
  }
  if (!isValidDate(text.value)) { emit('update:modelValue', null); return }
  emit('update:modelValue', text.value)
}

const error = computed(() => {
  if (props.model.validation?.required && (!props.modelValue || props.modelValue === '')) return `${props.model.label || props.model.key} is required`
  if (props.modelValue && !isValidDate(props.modelValue)) return 'Invalid date (DD/MM/YYYY)'
  return ''
})
</script>

