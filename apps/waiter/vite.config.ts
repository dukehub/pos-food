import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { createUiVitePlugin } from '@pos/ui/vite'
import { resolve } from 'node:path'

const root = import.meta.dirname
const monorepoRoot = resolve(root, '../..')

export default defineConfig({
  plugins: [
    vue(),
    createUiVitePlugin()
  ],
  resolve: {
    alias: [
      { find: '@', replacement: resolve(root, './src') },
      { find: /^@pos\/ui\/(.*)$/, replacement: resolve(monorepoRoot, 'packages/ui/src/$1') },
      { find: /^@pos\/ui$/, replacement: resolve(monorepoRoot, 'packages/ui/src/index.ts') },
      { find: /^@pos\/core$/, replacement: resolve(monorepoRoot, 'packages/core/src/index.ts') },
      { find: /^@pos\/i18n$/, replacement: resolve(monorepoRoot, 'packages/i18n/src/index.ts') },
      { find: /^@pos\/validation$/, replacement: resolve(monorepoRoot, 'packages/validation/src/index.ts') },
      { find: /^@pos\/api$/, replacement: resolve(monorepoRoot, 'packages/api/src/index.ts') },
      // Plugin (waiter)
      { find: /^@pos\/plugin-table-info$/, replacement: resolve(monorepoRoot, 'plugins/table-info/contribute.ts') }
    ],
    dedupe: ['vue', 'vue-router', 'pinia', 'vue-i18n']
  }
})
