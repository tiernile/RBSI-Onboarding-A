<template>
  <div class="kycp-field" :class="{ 'kycp-field--error': !!error }">
    <label v-if="label" :for="id" class="kycp-field__label" :class="{ 'kycp-field__label--required': required }">
      {{ label }}
    </label>
    <div v-if="description" class="kycp-field__description" v-html="sanitizedDescription"></div>
    <div class="kycp-field__input">
      <slot></slot>
    </div>
    <p v-if="help && !error" :id="`${id}-help`" class="kycp-field__help">
      {{ help }}
    </p>
    <p v-if="error" :id="`${id}-error`" class="kycp-field__error" role="alert">
      {{ error }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  id?: string
  label?: string
  description?: string
  required?: boolean
  help?: string
  error?: string
}

const props = defineProps<Props>()

const sanitizedDescription = computed(() => {
  if (!props.description) return ''
  return props.description
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
    .replace(/on\w+="[^"]*"/gi, '')
    .replace(/on\w+='[^']*'/gi, '')
})
</script>

<style scoped>
.kycp-field {
  margin-bottom: 20px;
}

.kycp-field__label {
  display: block;
  margin-bottom: 4px;
  font-size: var(--kycp-font-size-base);
  font-weight: 500;
  color: var(--kycp-label-color);
  line-height: 1.4;
}

.kycp-field__label--required::after {
  content: "*";
  color: #ef4444;
  margin-left: 2px;
  font-weight: normal;
}

.kycp-field__description {
  margin: 6px 0 10px;
  font-size: var(--kycp-font-size-sm);
  line-height: 1.5;
  color: var(--kycp-label-color);
}

.kycp-field__description :deep(br) {
  display: block;
  margin: 2px 0;
}

.kycp-field__description :deep(ul) {
  margin: 6px 0;
  padding-left: 16px;
}

.kycp-field__description :deep(li) {
  margin: 2px 0;
  list-style-type: disc;
  font-size: 12px;
  line-height: 1.5;
}

.kycp-field__description :deep(strong) {
  font-weight: 600;
  color: #374151;
}

.kycp-field__input {
  position: relative;
}

.kycp-field__help {
  margin-top: 6px;
  font-size: var(--kycp-font-size-sm);
  color: var(--kycp-label-color);
  line-height: 1.4;
}

.kycp-field__error {
  margin-top: 6px;
  font-size: 12px;
  color: #ef4444;
  line-height: 1.4;
}

.kycp-field--error .kycp-field__label {
  color: #ef4444;
}
</style>