<template>
  <div role="radiogroup" :aria-labelledby="id" :aria-describedby="ariaDescribedby || undefined">
    <div v-for="opt in options" :key="opt" class="radio">
      <input :id="`${id}-${opt}`" type="radio" :name="id" :value="opt" v-model="model" :required="required" />
      <label :for="`${id}-${opt}`">{{ opt }}</label>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ id: string; options: string[]; required?: boolean; ariaDescribedby?: string; ariaInvalid?: boolean }>()
const model = defineModel<string>({ default: '' })
</script>

<style scoped>
.radio{display:flex;align-items:center;gap:6px;margin:4px 0}
</style>
