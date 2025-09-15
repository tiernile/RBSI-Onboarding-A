<template>
  <div class="kycp-section">
    <div class="kycp-section__header">
      <h2 class="kycp-section__title">{{ title }}</h2>
      <p v-if="description" class="kycp-section__description">{{ description }}</p>
      <p v-if="instructions" class="kycp-section__instructions">{{ instructions }}</p>
    </div>
    <div class="kycp-section__content">
      <slot></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string
  description?: string
  instructions?: string
}

defineProps<Props>()
</script>

<style scoped>
.kycp-section {
  margin-bottom: 32px;
}

.kycp-section__header {
  padding-bottom: 16px;
  border-bottom: 1px solid var(--kycp-section-border);
  margin-bottom: 24px;
}

.kycp-section__title {
  margin: 0 0 12px;
  font-size: 20px;
  font-weight: 600;
  color: var(--kycp-gray-900);
  line-height: 1.3;
}

.kycp-section__description {
  margin: 0 0 12px;
  font-size: 14px;
  color: var(--kycp-gray-700);
  line-height: 1.5;
}

.kycp-section__instructions {
  margin: 0;
  font-size: 13px;
  color: var(--kycp-gray-600);
  line-height: 1.5;
  font-style: italic;
}

.kycp-section__content {
  /* Content area for form fields */
}
</style>