import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import ui from '@nuxt/ui/vue-plugin'
import App from './App.vue'
import './assets/main.css'
import { createPinia } from 'pinia'

const app = createApp(App)
const pinia = createPinia()
const router = createRouter({
  routes: [],
  history: createWebHistory()
})

app.use(router)
app.use(pinia)
app.use(ui)

app.mount('#app')
