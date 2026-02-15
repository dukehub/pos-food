import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'tables',
    component: () => import('@/views/DashboardView.vue')
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})
