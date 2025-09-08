<template>
  <div class="kycp-field" :class="{ 'kycp-field--error': !!error }">
    <label v-if="label" :for="id" class="kycp-field__label" :class="{ 'kycp-field__label--required': required }">
      {{ label }}
    </label>
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
interface Props {
  id?: string
  label?: string
  required?: boolean
  help?: string
  error?: string
}

defineProps<Props>()
</script>

<style scoped>
.kycp-field {
  margin-bottom: var(--kycp-spacing-lg);
}

.kycp-field__label {
  display: block;
  margin-bottom: var(--kycp-spacing-sm);
  font-size: var(--kycp-font-size-sm);
  font-weight: 500;
  color: var(--kycp-label-color);
}

.kycp-field__label--required::after {
  content: " *";
  color: var(--kycp-error);
}

.kycp-field__input {
  position: relative;
}

.kycp-field__help {
  margin-top: var(--kycp-spacing-xs);
  font-size: var(--kycp-font-size-sm);
  color: var(--kycp-gray-600);
  line-height: 1.4;
}

.kycp-field__error {
  margin-top: var(--kycp-spacing-xs);
  font-size: var(--kycp-font-size-sm);
  color: var(--kycp-error);
  line-height: 1.4;
}

.kycp-field--error .kycp-field__label {
  color: var(--kycp-error);
}
</style>