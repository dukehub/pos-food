import '@pos/ui/assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ui from '@nuxt/ui/vue-plugin'
import { createAppI18n } from '@pos/i18n'
import { REGISTRY_KEY, pluginRegistry } from '@pos/core'
import App from './App.vue'
import { router } from './router'

// --- Register plugins before mounting ---
import { registerProductExportPlugin } from '@pos/plugin-product-export'
import { registerProductNutritionPlugin } from '@pos/plugin-product-nutrition'
registerProductExportPlugin(pluginRegistry)
registerProductNutritionPlugin(pluginRegistry)

const app = createApp(App)
const pinia = createPinia()
const i18n = createAppI18n()

app.use(pinia)
app.use(router)
app.use(i18n)
app.use(ui)

// Provide the registry to all components in the tree
app.provide(REGISTRY_KEY, pluginRegistry)

app.mount('#app')
