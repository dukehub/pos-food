import type { Component } from 'vue'
import type { RouteRecordRaw } from 'vue-router'

/** Metadata manifest for a plugin */
export interface PluginManifest {
  /** Unique plugin identifier (e.g. 'product-export') */
  id: string
  /** Human-readable name */
  name: string
  /** Semver version */
  version: string
  /** Plugin dependencies (other plugin IDs) */
  dependencies?: string[]
  /** Target apps this plugin contributes to */
  targets?: Array<'admin' | 'pos' | 'waiter'>
}

/**
 * A component fragment contributed by a plugin to a mount point.
 *
 * mountPoint naming convention: {app}.{page|area}.{zone}.{type}
 * Examples:
 *   - admin.products.toolbar.actions
 *   - admin.product.tabs
 *   - waiter.table.sidebar.widgets
 *   - pos.sale.cart.actions
 */
export interface ComponentContribution {
  /** Mount point identifier (dotted convention) */
  mountPoint: string
  /**
   * The Vue component to render.
   * Can be a static component or a () => import('...') for async loading.
   */
  component: Component | (() => Promise<{ default: Component }>)
  /** Rendering order (lower = first, default: 100) */
  order?: number
  /** Human-readable label for devtools / debug */
  label?: string
  /**
   * Resolve props from the context passed by the ExtensionPoint.
   * If omitted, the full ctx object is spread as props.
   */
  resolveProps?: (ctx: Record<string, unknown>) => Record<string, unknown>
  /** Static props (merged with resolved props, lower priority) */
  props?: Record<string, unknown>
}

/** A route contributed by a plugin */
export interface RouteContribution {
  /** Target app */
  app: 'admin' | 'pos' | 'waiter'
  /** Vue Router route record(s) */
  routes: RouteRecordRaw[]
}

/** Full registration payload for a plugin */
export interface PluginRegistration {
  manifest: PluginManifest
  routes?: RouteContribution[]
  contributions?: ComponentContribution[]
  /** i18n messages keyed by locale */
  messages?: Record<string, Record<string, unknown>>
}
