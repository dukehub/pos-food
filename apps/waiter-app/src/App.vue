<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const tabs = [
  { label: t('waiter.nav.tables'), icon: 'i-lucide-grid-2x2', to: '/' },
  { label: t('waiter.nav.orders'), icon: 'i-lucide-receipt', to: '/orders' },
  { label: t('waiter.nav.account'), icon: 'i-lucide-user', to: '/account' },
]
</script>

<template>
  <UApp>
    <div class="flex h-screen flex-col">
      <!-- Top header -->
      <header class="flex h-14 items-center gap-3 border-b border-[var(--ui-border)] bg-[var(--ui-bg-elevated)] px-4">
        <span class="text-xl">🍽️</span>
        <span class="text-lg font-bold">{{ t('waiter.title') }}</span>
      </header>

      <!-- Main content -->
      <main class="flex-1 overflow-auto">
        <RouterView />
      </main>

      <!-- Bottom tabs (mobile-first) -->
      <nav class="flex border-t border-[var(--ui-border)] bg-[var(--ui-bg-elevated)]">
        <RouterLink
          v-for="tab in tabs"
          :key="tab.to"
          :to="tab.to"
          class="flex flex-1 flex-col items-center gap-1 py-3 text-xs font-medium transition-colors hover:text-[var(--ui-primary)]"
          active-class="text-[var(--ui-primary)]"
        >
          <UIcon :name="tab.icon" class="size-5" />
          <span>{{ tab.label }}</span>
        </RouterLink>
      </nav>
    </div>
  </UApp>
</template>
