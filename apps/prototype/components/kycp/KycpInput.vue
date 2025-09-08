<template>
  <input
    :id="id"
    v-model="model"
    type="text"
    :required="required"
    :aria-invalid="ariaInvalid ? 'true' : 'false'"
    :aria-describedby="ariaDescribedby || undefined"
  />
</template>

<script setup lang="ts">
const props = defineProps<{ id: string; required?: boolean; ariaDescribedby?: string; ariaInvalid?: boolean }>()
const model = defineModel<string>({ default: '' })
</script>
