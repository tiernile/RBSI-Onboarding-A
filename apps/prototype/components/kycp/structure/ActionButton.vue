<template>
  <div class="kycp-action">
    <button class="kycp-button" type="button" @click="$emit('trigger', model.scriptId)">
      {{ model.label || 'Action' }}
    </button>
    <p v-if="model.description" class="kycp-action__desc">{{ model.description }}</p>
  </div>
</template>

<script setup lang="ts">
import type { BaseField } from '~/types/kycp'
defineProps<{ model: BaseField }>()
defineEmits<{ (e: 'trigger', scriptId?: string): void }>()
</script>

<style scoped>
.kycp-button { padding: 8px 12px; border: 1px solid #d0d7de; border-radius: 6px; background: #0969da; color: #fff; cursor: pointer; }
.kycp-button:hover { background: #075bbd; }
.kycp-action__desc { margin: 6px 0 0; color: #555; font-size: 14px; }
</style>

