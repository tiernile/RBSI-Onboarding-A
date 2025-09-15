<template>
  <div class="kycp-group">
    <div class="kycp-group__header">
      <h3>{{ model.label || model.key }}</h3>
      <button type="button" class="kycp-button" @click="$emit('add')">Add new</button>
    </div>
    <div v-for="(row, i) in rows" :key="i" class="kycp-group__row">
      <slot name="row" :row="row" :index="i"></slot>
      <div class="kycp-group__row-actions">
        <button type="button" class="kycp-button kycp-button-secondary" @click="$emit('remove', i)">Remove</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ComplexGroup } from '~/types/kycp'

defineProps<{ model: ComplexGroup; rows: Record<string, unknown>[] }>()
defineEmits<{ (e: 'add'): void; (e: 'remove', index: number): void }>()
</script>

<style scoped>
.kycp-group { border: 1px solid #e1e4e8; border-radius: 8px; padding: 16px; background: #fff; }
.kycp-group__header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.kycp-group__row { padding: 12px; border: 1px solid #eaecef; border-radius: 6px; margin-bottom: 10px; background: #fafbfc; }
.kycp-button { padding: 6px 10px; border: 1px solid #d0d7de; border-radius: 6px; background: #f6f8fa; cursor: pointer; }
.kycp-button-secondary { background: #fff; }
</style>

