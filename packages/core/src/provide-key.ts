import type { InjectionKey } from 'vue'
import type { PluginRegistry } from './plugin-registry'

/**
 * Vue provide/inject key for the plugin registry.
 *
 * Usage in app main.ts:
 *   import { REGISTRY_KEY, pluginRegistry } from '@pos/core'
 *   app.provide(REGISTRY_KEY, pluginRegistry)
 *
 * Usage in components:
 *   const registry = inject(REGISTRY_KEY)!
 */
export const REGISTRY_KEY: InjectionKey<PluginRegistry> = Symbol('pos:plugin-registry')
