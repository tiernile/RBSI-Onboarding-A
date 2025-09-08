<template>
  <select :id="id" v-model="model" :required="required" :aria-invalid="ariaInvalid ? 'true' : 'false'" :aria-describedby="ariaDescribedby || undefined">
    <option value="" disabled>Select an option</option>
    <option v-for="opt in options" :key="opt" :value="opt">{{ opt }}</option>
  </select>
</template>

<script setup lang="ts">
const props = defineProps<{ id: string; options: string[]; required?: boolean; ariaDescribedby?: string; ariaInvalid?: boolean }>()
const model = defineModel<string>({ default: '' })
</script>
