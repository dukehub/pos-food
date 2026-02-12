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
            path: '/orders',
            component: () => import('./pages/orders.vue'),
        },
    ],
})

const app = createApp(App)

app.use(router)
app.use(createPinia())
app.use(i18n)
app.use(ui)

app.mount('#app')
