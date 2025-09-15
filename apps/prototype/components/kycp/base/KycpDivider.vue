<template>
  <div class="kycp-divider">
    <h3 v-if="title" class="kycp-divider__title">
      <span class="kycp-divider__dash">—</span>
      {{ title }}
    </h3>
    <hr v-else class="kycp-divider__line" />
  </div>
</template>

<script setup lang="ts">
interface Props {
  title?: string
}

defineProps<Props>()
</script>

<style scoped>
.kycp-divider {
  margin: 20px 0;
}

.kycp-divider__title {
  position: relative;
  margin: 0;
  padding: 12px 0;
  font-size: 15px;
  font-weight: 500;
  color: #4a5568;
  border-bottom: 1px solid #d1d5db;
  display: flex;
  align-items: center;
}

.kycp-divider__dash {
  margin-right: 8px;
  color: #9ca3af;
}

.kycp-divider__line {
  margin: 0;
  border: none;
  border-top: 1px solid #d1d5db;
}
</style>