<template>
  <textarea
    :id="id"
    v-model="model"
    rows="4"
    :required="required"
    :aria-invalid="ariaInvalid ? 'true' : 'false'"
    :aria-describedby="ariaDescribedby || undefined"
  ></textarea>
</template>

<script setup lang="ts">
const props = defineProps<{ id: string; required?: boolean; ariaDescribedby?: string; ariaInvalid?: boolean }>()
const model = defineModel<string>({ default: '' })
</script>
