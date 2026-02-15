/**
 * Factorized Nuxt UI Vite plugin configuration.
 * Each app imports this in its vite.config.ts.
 * @ts-expect-error — @nuxt/ui/vite has no declaration file; types come from the consuming app's vite env
 */

import uiVitePlugin from '@nuxt/ui/vite'

export interface PosUiOptions {
  /** Additional npm packages to scan for Nuxt UI components */
  scanPackages?: string[]
}

export function createUiVitePlugin(options?: PosUiOptions) {
  return uiVitePlugin({
    ui: {
      colors: {
        primary: 'green',
        neutral: 'slate'
      }
    },
    colorMode: true,
    theme: {
      transitions: true
    },
    scanPackages: options?.scanPackages
  })
}

export default createUiVitePlugin
