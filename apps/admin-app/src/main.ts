import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import ui from '@nuxt/ui/vue-plugin'

import App from './App.vue'
import i18n from './i18n'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: () => import('./pages/index.vue'),
        },
        {
            path: '/products',
            component: () => import('./pages/products/index.vue'),
        },
        {
            path: '/products/new',
            component: () => import('./pages/products/new.vue'),
        },
        {
            path: '/categories',
            component: () => import('./pages/categories/index.vue'),
        },
        {
            path: '/orders',
            component: () => import('./pages/orders/index.vue'),
        },
        {
            path: '/settings',
            component: () => import('./pages/settings.vue'),
        },
    ],
})

const app = createApp(App)

app.use(router)
app.use(createPinia())
app.use(i18n)
app.use(ui)

app.mount('#app')
