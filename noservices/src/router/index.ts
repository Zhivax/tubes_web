import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: () => import('../views/LandingView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/dashboard',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/inventory',
      name: 'inventory',
      component: () => import('../views/InventoryView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('access_token')

  // Redirect to dashboard if trying to access landing while logged in
  if (to.name === 'landing' && isAuthenticated) {
    next('/dashboard')
    return
  }

  // Redirect to landing if trying to access protected route while not logged in
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/')
    return
  }

  next()
})

export default router
