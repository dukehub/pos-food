<script setup lang="ts">
/**
 * ExtensionPoint — renders plugin-contributed components for a named mount point.
 *
 * Features:
 *   - Async component loading via defineAsyncComponent
 *   - #loading slot fallback (defaults to USkeleton)
 *   - #empty slot fallback when no contributions exist
 *   - resolveProps(ctx) for context-aware prop injection
 *   - Accesses registry via provide/inject (REGISTRY_KEY)
 *
 * Usage:
 *   <ExtensionPoint name="admin.products.toolbar.actions" :ctx="{ search }" />
 *   <ExtensionPoint name="admin.product.tabs" :ctx="{ product }" tag="div" class="flex gap-2" />
 */
import { computed, defineAsyncComponent, inject, type Component } from 'vue'
import { REGISTRY_KEY } from '@pos/core'
import type { ComponentContribution } from '@pos/core'

const props = withDefaults(
  defineProps<{
    /** Mount point identifier (dotted convention) */
    name: string
    /** Context object passed to each contributed component */
    ctx?: Record<string, unknown>
    /** Wrapper HTML tag. If omitted, renders fragments (no wrapper) */
    tag?: string
  }>(),
  {
    ctx: () => ({}),
    tag: undefined
  }
)

const registry = inject(REGISTRY_KEY)

if (!registry) {
  console.error(
    `[ExtensionPoint] No registry provided. Did you forget app.provide(REGISTRY_KEY, pluginRegistry) in main.ts?`
  )
}

/** Raw contributions from the registry (reactive) */
const contributions = computed(() =>
  registry ? registry.getContributions(props.name) : []
)

/** Whether there are contributions to render */
const hasContributions = computed(() => contributions.value.length > 0)

/**
 * Wrap a contribution's component in defineAsyncComponent for lazy loading.
 */
function toAsyncComponent(contrib: ComponentContribution): Component {
  const loader = contrib.component

  // If the component is a function (dynamic import), wrap it
  if (typeof loader === 'function') {
    return defineAsyncComponent({
      loader: loader as () => Promise<{ default: Component }>,
      delay: 200,
      timeout: 10000
    })
  }

  // Already a resolved component
  return loader
}

/**
 * Resolve the final props for a contributed component.
 */
function resolvedProps(contrib: ComponentContribution): Record<string, unknown> {
  const staticProps = contrib.props ?? {}
  const resolvedFromCtx = contrib.resolveProps
    ? contrib.resolveProps(props.ctx)
    : props.ctx
  return { ...staticProps, ...resolvedFromCtx }
}
</script>

<template>
  <component :is="tag ?? 'template'" v-if="tag" :class="$attrs.class">
    <!-- No contributions: render #empty slot -->
    <slot v-if="!hasContributions" name="empty" />

    <!-- Render each contribution -->
    <template v-for="(contrib, idx) in contributions" :key="`${name}-${idx}`">
      <Suspense>
        <component
          :is="toAsyncComponent(contrib)"
          v-bind="resolvedProps(contrib)"
        />
        <template #fallback>
          <slot name="loading">
            <USkeleton class="h-8 w-24" />
          </slot>
        </template>
      </Suspense>
    </template>
  </component>

  <!-- Fragment mode (no wrapper tag) -->
  <template v-else>
    <slot v-if="!hasContributions" name="empty" />
    <template v-for="(contrib, idx) in contributions" :key="`${name}-${idx}`">
      <Suspense>
        <component
          :is="toAsyncComponent(contrib)"
          v-bind="resolvedProps(contrib)"
        />
        <template #fallback>
          <slot name="loading">
            <USkeleton class="h-8 w-24" />
          </slot>
        </template>
      </Suspense>
    </template>
  </template>
</template>
