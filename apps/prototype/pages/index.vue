<template>
  <div class="container">
    <header class="header">
      <h1>Mission Control</h1>
      <div class="actions">
        <NuxtLink class="link" to="/kycp-components">Components</NuxtLink>
        <NuxtLink class="link" to="/about">About</NuxtLink>
        <button v-if="!isAdmin" @click="showLogin=true">Admin</button>
        <span v-else class="badge">Admin</span>
      </div>
    </header>

    <div v-if="error" class="error">{{ error }}</div>

    <div class="grid">
      <div v-for="j in cards" :key="j.key" class="card">
        <h2>{{ j.name }}</h2>
        <p class="muted">{{ j.key }} · v{{ j.version }} · Variant {{ j.variant || 'A' }}</p>
        <p v-if="j.source?.file" class="muted source">Source: {{ j.source.file }}<span v-if="j.source.sheet"> — {{ j.source.sheet }}</span></p>
        <div class="pills">
          <span class="pill" :class="`status-${j.display?.status || 'alpha'}`">{{ j.display?.status || 'alpha' }}</span>
          <span class="pill status-hidden" v-if="!j.display?.visible">hidden</span>
        </div>
        <NuxtLink class="btn" :to="j.variant === 'KYCP' ? `/preview-kycp/${j.key}` : `/preview/${j.key}`">Open</NuxtLink>
        <div v-if="isAdmin" class="admin-actions">
          <a :href="`/api/diff/${j.key}`" target="_blank" rel="noopener" class="link">View Diff</a>
          <a :href="`/api/export/${j.key}`" class="link">Export CSV</a>
        </div>
      </div>
    </div>

    <dialog v-if="showLogin" open>
      <form @submit.prevent="login">
        <h3>Admin Login</h3>
        <input type="password" v-model="password" placeholder="Password" />
        <div class="row">
          <button type="button" @click="showLogin=false">Cancel</button>
          <button type="submit">Login</button>
        </div>
        <p v-if="loginError" class="error">{{ loginError }}</p>
      </form>
    </dialog>
  </div>
</template>

<script setup lang="ts">
const { data, error } = await useManifest()
const isAdmin = computed(() => data.value?.isAdmin)
const cards = computed(() => {
  const all = data.value?.active || []
  if (isAdmin.value) return all
  return all.filter((j: any) => j.display?.visible !== false)
})

const showLogin = ref(false)
const password = ref('')
const loginError = ref('')

async function login() {
  loginError.value = ''
  try {
    const res = await $fetch('/api/auth/login', { method: 'POST', body: { password: password.value } })
    if ((res as any).ok) {
      showLogin.value = false
      await refreshNuxtData('manifest')
    } else {
      loginError.value = (res as any).error || 'Login failed'
    }
  } catch (e: any) {
    loginError.value = e?.data?.message || e?.message || 'Login error'
  }
}
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--space-xl) var(--space-lg);
  min-height: 100vh;
  font-family: var(--font-system);
  color: var(--color-text-primary);
  background: var(--color-bg);
}

/* Header */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-xl);
}

.header h1 {
  font-size: 1.75rem;
  font-weight: 600;
  margin: 0;
  color: var(--color-text-primary);
  letter-spacing: -0.02em;
}

.actions {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.actions .link {
  color: var(--color-link);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  padding: 6px 12px;
  border-radius: 4px;
  transition: all 150ms ease-in-out;
}

.actions .link:hover {
  color: var(--color-link-hover);
  text-decoration: underline;
}

.actions button {
  background: transparent;
  color: var(--color-link);
  border: none;
  font-size: 0.875rem;
  font-weight: 500;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 150ms ease-in-out;
}

.actions button:hover {
  color: var(--color-link-hover);
  text-decoration: underline;
}

.badge {
  background: var(--status-hidden-bg);
  color: var(--status-hidden-text);
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

/* Grid Layout */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: var(--space-lg);
}

/* Cards */
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 24px;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  transition: all 200ms ease-in-out;
  position: relative;
}

.card:hover {
  border-color: var(--color-border-hover);
  transform: translateY(-2px);
}

.card h2 {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0 0 var(--space-sm) 0;
  color: var(--color-text-primary);
  line-height: 1.3;
}

.muted {
  color: var(--color-text-muted);
  font-size: 0.8125rem;
  font-weight: 400;
  margin-bottom: var(--space-md);
  line-height: 1.4;
}

/* Status Pills */
.pills {
  display: flex;
  gap: var(--space-sm);
  margin-bottom: auto;
}

.pill {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.pill.status-alpha {
  background: var(--status-alpha-bg);
  color: var(--status-alpha-text);
}

.pill.status-beta {
  background: var(--status-beta-bg);
  color: var(--status-beta-text);
}

.pill.status-live {
  background: var(--status-live-bg);
  color: var(--status-live-text);
}

.pill.status-hidden {
  background: var(--status-hidden-bg);
  color: var(--status-hidden-text);
}

/* Primary Button */
.btn {
  display: inline-block;
  margin-top: var(--space-lg);
  padding: 10px 20px;
  background: var(--color-text-primary);
  border: 1px solid var(--color-text-primary);
  color: white;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  text-decoration: none;
  text-align: center;
  cursor: pointer;
  transition: all 150ms ease-in-out;
}

.btn:hover {
  background: var(--color-text-secondary);
  border-color: var(--color-text-secondary);
  transform: translateY(-1px);
}

.btn:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

/* Admin Actions */
.admin-actions {
  display: flex;
  gap: 12px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--color-border);
}

.admin-actions .link {
  font-size: 0.8125rem;
  color: var(--color-link);
  text-decoration: none;
  transition: all 150ms ease-in-out;
}

.admin-actions .link:hover {
  color: var(--color-link-hover);
  text-decoration: underline;
}

/* Dialog */
dialog {
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: var(--space-lg);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

dialog h3 {
  margin: 0 0 var(--space-md) 0;
  font-size: 1.125rem;
  font-weight: 500;
}

dialog input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-size: 0.875rem;
  font-family: var(--font-system);
}

dialog input:focus {
  outline: 2px solid var(--color-focus);
  outline-offset: -1px;
}

.row {
  display: flex;
  gap: var(--space-sm);
  justify-content: flex-end;
  margin-top: var(--space-md);
}

.row button {
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 150ms ease-in-out;
}

.row button[type="button"] {
  background: transparent;
  border: 1px solid var(--color-border);
  color: var(--color-text-secondary);
}

.row button[type="submit"] {
  background: var(--color-text-primary);
  border: 1px solid var(--color-text-primary);
  color: white;
}

.row button:hover {
  opacity: 0.9;
}

/* Error State */
.error {
  color: var(--status-alpha-text);
  font-size: 0.875rem;
  margin-top: var(--space-sm);
}

/* Responsive */
@media (max-width: 1024px) {
  .grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }
}

@media (max-width: 640px) {
  .container {
    padding: var(--space-md);
  }
  
  .header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-md);
  }
  
  .grid {
    grid-template-columns: 1fr;
  }
  
  .admin-actions {
    flex-direction: column;
    gap: var(--space-sm);
  }
}
</style>
