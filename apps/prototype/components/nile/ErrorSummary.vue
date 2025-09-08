<template>
  <section v-if="errors && Object.keys(errors).length" class="error-summary" aria-labelledby="error-summary-title" tabindex="-1" ref="root">
    <h2 id="error-summary-title">There’s a problem</h2>
    <ul>
      <li v-for="(msg, fieldId) in errors" :key="fieldId">
        <a href="javascript:void(0)" @click="focusField(fieldId)">{{ msg }}</a>
      </li>
    </ul>
  </section>
</template>

<script setup lang="ts">
const props = defineProps<{ errors: Record<string, string> }>()
const root = ref<HTMLElement | null>(null)
function focusField(id: string) {
  const el = document.getElementById(id)
  if (el) el.focus()
}
onMounted(() => {
  if (root.value) root.value.focus()
})
</script>

<style scoped>
.error-summary{border:2px solid #b00020;padding:12px;border-radius:6px;background:#fff6f6;margin-bottom:16px}
.error-summary h2{margin:0 0 8px 0}
.error-summary a{color:#b00020;text-decoration:underline}
</style>

