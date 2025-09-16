<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-box">
        <div class="login-header">
          <h1>RBSI Onboarding Prototype</h1>
          <p>Please enter the password to access the site</p>
        </div>
        
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="password">Password</label>
            <input 
              id="password"
              v-model="password" 
              type="password"
              class="password-input"
              placeholder="Enter password"
              autofocus
              @keyup.enter="handleLogin"
            />
            <div v-if="error" class="error-message">
              {{ error }}
            </div>
          </div>
          
          <button 
            type="submit"
            class="login-button"
          >
            Login
          </button>
        </form>
        
        <div class="login-footer">
          <p>For access, please contact the Nile team</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// Use auth composable
const { login, checkAuth } = useAuth()

// State
const password = ref('')
const error = ref('')

// Handle login
const handleLogin = () => {
  if (login(password.value)) {
    error.value = ''
    password.value = ''
    navigateTo('/')
  } else {
    error.value = 'Incorrect password. Please try again.'
  }
}

// Auto-check on mount
onMounted(() => {
  if (checkAuth()) {
    navigateTo('/')
  }
})
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 400px;
}

.login-box {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  padding: 40px;
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-header h1 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 700;
  color: #1a202c;
}

.login-header p {
  margin: 0;
  color: #718096;
  font-size: 14px;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #4a5568;
}

.password-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.2s;
  outline: none;
}

.password-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgb(102 126 234 / 0.1);
}

.error-message {
  margin-top: 8px;
  color: #f56565;
  font-size: 13px;
}

.login-button {
  width: 100%;
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.login-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
}

.login-button:active {
  transform: translateY(0);
}

.login-footer {
  margin-top: 32px;
  text-align: center;
}

.login-footer p {
  margin: 0;
  color: #a0aec0;
  font-size: 12px;
}
</style>