<template>
  <KycpFieldWrapper :id="model.key" :label="model.label" :required="model.validation?.required" :help="model.description" :error="error">
    <KycpSelect
      :id="model.key"
      v-model="internal"
      :options="options"
      :disabled="isDisabled"
      :required="model.validation?.required"
      :error="!!error"
      :placeholder="placeholder || 'Please select...'"
    />
  </KycpFieldWrapper>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import KycpSelect from '~/components/kycp/base/KycpSelect.vue'
import KycpFieldWrapper from '~/components/kycp/base/KycpFieldWrapper.vue'
import type { BaseField, LookupOption, EffectiveRight } from '~/types/kycp'
import { resolveRight } from '~/types/kycp'

const props = defineProps<{ model: BaseField; modelValue: string | null; status?: string; placeholder?: string }>()
const emit = defineEmits<{ (e: 'update:modelValue', v: string | null): void }>()

const right = computed<EffectiveRight>(() => resolveRight(props.model.statusRights, props.status || ''))
const isDisabled = computed(() => right.value === 'hidden' || right.value === 'readOnly')
const placeholder = computed(() => props.placeholder || '')

const options = computed(() => (props.model.options || []).map(o => ({ label: o.label, value: o.value })) as LookupOption[])

const internal = computed({
  get: () => props.modelValue ?? '',
  set: (v: string | number) => emit('update:modelValue', v === '' ? null : String(v))
})

const error = computed(() => {
  if (props.model.validation?.required && (!props.modelValue || props.modelValue === '')) return `${props.model.label || props.model.key} is required`
  if (props.modelValue && !options.value.find(o => o.value === props.modelValue)) return 'Invalid option'
  return ''
})
</script>

