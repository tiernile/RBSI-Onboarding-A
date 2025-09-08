<template>
  <div class="kycp-field-group">
    <div class="kycp-field-group__header">
      <div class="kycp-field-group__header-icon" v-if="$slots.icon">
        <slot name="icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
            <line x1="3" y1="9" x2="21" y2="9"/>
            <line x1="9" y1="21" x2="9" y2="9"/>
          </svg>
        </slot>
      </div>
      <div class="kycp-field-group__header-content">
        <h3 class="kycp-field-group__title">{{ title }}</h3>
        <p v-if="subtitle" class="kycp-field-group__subtitle">{{ subtitle }}</p>
      </div>
    </div>
    <div class="kycp-field-group__content">
      <slot></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string
  subtitle?: string
}

defineProps<Props>()
</script>

<style scoped>
.kycp-field-group {
  border: 1px solid var(--kycp-gray-200);
  border-radius: var(--kycp-radius-base);
  overflow: hidden;
  margin-bottom: var(--kycp-spacing-xl);
  background: var(--kycp-white);
  box-shadow: var(--kycp-shadow-sm);
}

.kycp-field-group__header {
  background: var(--kycp-gray-500);
  color: var(--kycp-white);
  padding: var(--kycp-spacing-md) var(--kycp-spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--kycp-spacing-md);
}

.kycp-field-group__header-icon {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.kycp-field-group__header-content {
  flex: 1;
}

.kycp-field-group__title {
  margin: 0;
  font-size: var(--kycp-font-size-sm);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  line-height: 1.4;
}

.kycp-field-group__subtitle {
  margin: 2px 0 0 0;
  font-size: var(--kycp-font-size-xs);
  font-weight: 400;
  opacity: 0.9;
  line-height: 1.3;
}

.kycp-field-group__content {
  padding: var(--kycp-spacing-xl);
}
</style>