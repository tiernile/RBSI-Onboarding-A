<template>
  <div class="kycp-statement">
    <p class="kycp-statement__label" v-if="model.label">{{ model.label }}</p>
    <p class="kycp-statement__desc" v-if="model.description">{{ model.description }}</p>
  </div>
</template>

<script setup lang="ts">
import type { BaseField } from '~/types/kycp'
defineProps<{ model: BaseField }>()
</script>

<style scoped>
.kycp-statement { padding: 8px 0; }
.kycp-statement__label { font-weight: 600; margin: 0 0 4px; }
.kycp-statement__desc { margin: 0; color: #555; }
</style>

