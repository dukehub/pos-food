import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { pluginRegistry, useAuthStore } from '@pos/core'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { layout: 'auth' }
  },
  {
    path: '/',
    name: 'dashboard',
    component: () => import('@/views/dashboard/Home.vue'),
    meta: { layout: 'default', auth: true }
  },
  {
    path: '/floor-plan',
    component: () => import('../views/floor-plan/index.vue'),
    meta: { layout: 'default', auth: true }
  },
  {
    path: '/catalog',
    component: () => import('../views/catalog/index.vue'),
    meta: { layout: 'default', auth: true }
  },
  {
    path: '/customers',
    component: () => import('../views/customers/index.vue'),
    meta: { layout: 'default', auth: true }
  },
  {
    path: '/orders',
    component: () => import('../views/orders/index.vue'),
    meta: { layout: 'default', auth: true }
  },
  {
    path: '/printers',
    component: () => import('../views/printers/index.vue'),
    meta: { layout: 'default', auth: true }
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('@/views/settings/Settings.vue'),
    meta: { layout: 'default', auth: true }
  },
  {
    path: '/users',
    name: 'users',
    component: () => import('@/views/users/List.vue'),
    meta: { layout: 'default', requiresAuth: true }
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' })
  } else if (to.name === 'login' && authStore.isAuthenticated) {
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

export function setupPluginRoutes() {
  const contributions = pluginRegistry.getPluginRoutes('admin')
  contributions.forEach(contribution => {
    // Ensure plugin routes also have layout meta if needed, defaulting to default layout
    contribution.routes.forEach(route => {
      if (!route.meta) route.meta = {}
      if (!route.meta.layout) route.meta.layout = 'default'
      router.addRoute(route)
    })
  })
}
