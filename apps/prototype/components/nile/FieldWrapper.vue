<template>
  <div class="field" :class="{ invalid: !!error }">
    <label :for="id">
      <span>{{ label }}</span>
      <span v-if="required" class="req" aria-hidden="true">*</span>
    </label>
    <slot />
    <p v-if="hint" class="hint" :id="`${id}-hint`">{{ hint }}</p>
    <p v-if="error" class="error" :id="`${id}-error`">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{ id: string; label: string; required?: boolean; hint?: string|null; error?: string|null }>()
</script>

<style scoped>
.field{margin-bottom:16px}
label{display:flex;gap:6px;margin-bottom:6px}
.req{color:#b00020}
.hint{color:#555;font-size:0.9rem;margin-top:4px}
.error{color:#b00020;margin-top:4px}
.invalid input,.invalid select,.invalid textarea{border-color:#b00020}
</style>

