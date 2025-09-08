<template>
  <span class="kycp-tag" :class="{ 'kycp-tag--removable': removable }">
    <span class="kycp-tag__label">{{ label }}</span>
    <button
      v-if="removable"
      type="button"
      class="kycp-tag__remove"
      :aria-label="`Remove ${label}`"
      @click="$emit('remove')"
    >
      <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
        <path d="M9 3L3 9M3 3L9 9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
    </button>
  </span>
</template>

<script setup lang="ts">
interface Props {
  label: string
  removable?: boolean
}

withDefaults(defineProps<Props>(), {
  removable: false
})

defineEmits<{
  remove: []
}>()
</script>

<style scoped>
.kycp-tag {
  display: inline-flex;
  align-items: center;
  padding: var(--kycp-spacing-xs) var(--kycp-spacing-md);
  background: var(--kycp-gray-100);
  border: 1px solid var(--kycp-gray-300);
  border-radius: var(--kycp-radius-full);
  font-size: var(--kycp-font-size-sm);
  color: var(--kycp-gray-700);
  margin-right: var(--kycp-spacing-sm);
  margin-bottom: var(--kycp-spacing-sm);
  line-height: 1.5;
}

.kycp-tag--removable {
  padding-right: var(--kycp-spacing-xs);
}

.kycp-tag__label {
  white-space: nowrap;
}

.kycp-tag__remove {
  margin-left: var(--kycp-spacing-sm);
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--kycp-gray-400);
  color: var(--kycp-white);
  border: none;
  cursor: pointer;
  transition: background var(--kycp-transition-fast);
  padding: 0;
  flex-shrink: 0;
}

.kycp-tag__remove:hover {
  background: var(--kycp-error);
}

.kycp-tag__remove:focus {
  outline: 2px solid var(--kycp-primary);
  outline-offset: 1px;
}
</style>