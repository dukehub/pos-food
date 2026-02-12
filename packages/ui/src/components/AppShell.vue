<script setup lang="ts">
export interface NavigationItem {
  label: string
  icon: string
  to: string
}

defineProps<{
  title: string
  navigation: NavigationItem[]
}>()
</script>

<template>
  <div class="flex h-screen">
    <!-- Sidebar -->
    <aside class="flex w-64 flex-col border-r border-[var(--ui-border)] bg-[var(--ui-bg-elevated)]">
      <!-- App Title -->
      <div class="flex h-16 items-center gap-2 border-b border-[var(--ui-border)] px-4">
        <span class="text-xl">🍽️</span>
        <span class="text-lg font-bold">{{ title }}</span>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 space-y-1 p-3">
        <RouterLink
          v-for="item in navigation"
          :key="item.to"
          :to="item.to"
          class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors hover:bg-[var(--ui-bg-accented)]"
          active-class="bg-[var(--ui-bg-accented)] text-[var(--ui-text-highlighted)]"
        >
          <UIcon :name="item.icon" class="size-5 shrink-0" />
          <span>{{ item.label }}</span>
        </RouterLink>
      </nav>
    </aside>

    <!-- Main Content -->
    <main class="flex flex-1 flex-col overflow-hidden">
      <slot />
    </main>
  </div>
</template>
