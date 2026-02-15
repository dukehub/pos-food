import { reactive } from 'vue'
import type {
  PluginRegistration,
  ComponentContribution,
  RouteContribution
} from './types'

/**
 * Central plugin registry.
 * Plugins register themselves here; the host app queries contributions.
 *
 * Provided to the Vue app tree via `app.provide(REGISTRY_KEY, pluginRegistry)`.
 */
export class PluginRegistry {
  private plugins = reactive(new Map<string, PluginRegistration>())

  /**
   * Register a plugin with its manifest, routes, and UI contributions.
   */
  register(registration: PluginRegistration): void {
    const id = registration.manifest.id

    if (this.plugins.has(id)) {
      console.warn(`[PluginRegistry] Plugin "${id}" is already registered. Skipping.`)
      return
    }

    // Check dependencies
    if (registration.manifest.dependencies?.length) {
      for (const depId of registration.manifest.dependencies) {
        if (!this.plugins.has(depId)) {
          console.warn(
            `[PluginRegistry] Plugin "${id}" depends on "${depId}" which is not registered yet.`
          )
        }
      }
    }

    this.plugins.set(id, registration)
  }

  /**
   * Unregister a plugin by ID.
   */
  unregister(pluginId: string): void {
    this.plugins.delete(pluginId)
  }

  /**
   * Get all component contributions for a named mount point.
   * Results are sorted by `order` (ascending, default 100).
   */
  getContributions(mountPoint: string): ComponentContribution[] {
    const contributions: ComponentContribution[] = []

    for (const registration of this.plugins.values()) {
      if (registration.contributions) {
        for (const contribution of registration.contributions) {
          if (contribution.mountPoint === mountPoint) {
            contributions.push(contribution)
          }
        }
      }
    }

    return contributions.sort((a, b) => (a.order ?? 100) - (b.order ?? 100))
  }

  /**
   * Get all route contributions for a specific app.
   */
  getPluginRoutes(app: 'admin' | 'pos' | 'waiter'): RouteContribution[] {
    const routes: RouteContribution[] = []

    for (const registration of this.plugins.values()) {
      if (registration.routes) {
        for (const route of registration.routes) {
          if (route.app === app) {
            routes.push(route)
          }
        }
      }
    }

    return routes
  }

  /**
   * Get all i18n messages from registered plugins, merged by locale.
   */
  getPluginMessages(): Record<string, Record<string, unknown>> {
    const merged: Record<string, Record<string, unknown>> = {}

    for (const registration of this.plugins.values()) {
      if (registration.messages) {
        for (const [locale, messages] of Object.entries(registration.messages)) {
          if (!merged[locale]) {
            merged[locale] = {}
          }
          Object.assign(merged[locale], messages)
        }
      }
    }

    return merged
  }

  /**
   * Get all registered plugin IDs.
   */
  getRegisteredPlugins(): string[] {
    return Array.from(this.plugins.keys())
  }
}

/** Singleton instance */
export const pluginRegistry = new PluginRegistry()
