export const useAuth = () => {
  const isAuthenticated = useState('auth', () => false)

  const login = (password: string): boolean => {
    const CORRECT_PASSWORD = 'Monday1'
    
    if (password === CORRECT_PASSWORD) {
      isAuthenticated.value = true
      if (process.client) {
        sessionStorage.setItem('site-auth', 'authenticated')
      }
      return true
    }
    return false
  }

  const logout = () => {
    isAuthenticated.value = false
    if (process.client) {
      sessionStorage.removeItem('site-auth')
    }
    navigateTo('/login')
  }

  const checkAuth = () => {
    if (process.client) {
      const authStatus = sessionStorage.getItem('site-auth')
      if (authStatus === 'authenticated') {
        isAuthenticated.value = true
        return true
      }
    }
    return isAuthenticated.value
  }

  return {
    isAuthenticated: readonly(isAuthenticated),
    login,
    logout,
    checkAuth
  }
}