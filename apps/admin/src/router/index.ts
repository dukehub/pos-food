import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { pluginRegistry } from '@pos/core'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'dashboard',
    component: () => import('@/views/DashboardView.vue')
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})

export function setupPluginRoutes() {
  const contributions = pluginRegistry.getPluginRoutes('admin')
  contributions.forEach(contribution => {
    contribution.routes.forEach(route => {
      router.addRoute(route)
    })
  })
}
