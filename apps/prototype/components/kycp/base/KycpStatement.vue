<template>
  <div class="kycp-statement">
    <!-- Use v-html only for trusted content with links -->
    <div v-if="html" v-html="sanitizedHtml"></div>
    <div v-else>{{ text }}</div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  text?: string
  html?: string
}

const props = defineProps<Props>()

// Basic HTML sanitization - in production use a proper sanitizer
const sanitizedHtml = computed(() => {
  if (!props.html) return ''
  // Allow only basic formatting and links
  return props.html
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
    .replace(/on\w+="[^"]*"/gi, '')
    .replace(/on\w+='[^']*'/gi, '')
})
</script>

<style scoped>
.kycp-statement {
  margin-bottom: 16px;
  font-size: 13px;
  line-height: 1.5;
  color: #6b7280;
}

.kycp-statement :deep(a) {
  color: #2563eb;
  text-decoration: underline;
}

.kycp-statement :deep(a:hover) {
  color: #1d4ed8;
}

.kycp-statement :deep(strong) {
  font-weight: 600;
  color: #374151;
}

.kycp-statement :deep(p) {
  margin: 0;
}

.kycp-statement :deep(p + p) {
  margin-top: 8px;
}
</style>