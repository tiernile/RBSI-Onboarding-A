export default defineNuxtRouteMiddleware((to, from) => {
  // Skip auth check for login page
  if (to.path === '/login') {
    return
  }

  // Use auth composable
  const { checkAuth } = useAuth()

  // Redirect to login if not authenticated
  if (!checkAuth()) {
    return navigateTo('/login')
  }
})