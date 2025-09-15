<template>
  <div class="redirect-notice">
    <h1>Page Moved</h1>
    <p>The component showcase has been reorganized for clarity.</p>
    
    <div class="options">
      <NuxtLink to="/components" class="option-card">
        <h2>Component Library →</h2>
        <p>View the pure UI components (inputs, selects, textareas, etc.)</p>
      </NuxtLink>
      
      <NuxtLink to="/" class="option-card">
        <h2>Mission Control →</h2>
        <p>Return to the main dashboard</p>
      </NuxtLink>
    </div>
    
    <div class="note">
      <p><strong>Note:</strong> The components are now pure UI elements. All business logic (validation, visibility, etc.) comes from the data schema when rendering forms.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
// Optionally auto-redirect after a few seconds
import { useRouter } from 'vue-router'
import { onMounted } from 'vue'

const router = useRouter()

onMounted(() => {
  // Auto-redirect to components page after 3 seconds
  setTimeout(() => {
    router.push('/components')
  }, 3000)
})
</script>

<style scoped>
.redirect-notice {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  background: var(--color-bg);
}

h1 {
  margin: 0 0 16px;
  font-size: 32px;
  color: var(--color-text-primary);
}

p {
  margin: 0 0 32px;
  color: var(--color-text-secondary);
  text-align: center;
}

.options {
  display: flex;
  gap: 24px;
  margin-bottom: 48px;
}

.option-card {
  display: block;
  padding: 32px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.2s;
  max-width: 300px;
}

.option-card:hover {
  border-color: var(--color-link);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.option-card h2 {
  margin: 0 0 8px;
  font-size: 20px;
  color: var(--color-link);
}

.option-card p {
  margin: 0;
  text-align: left;
  font-size: 14px;
}

.note {
  max-width: 600px;
  padding: 24px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
}

.note p {
  margin: 0;
  text-align: left;
  font-size: 14px;
  line-height: 1.6;
}
</style>