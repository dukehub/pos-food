<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <UApp>
    <div class="flex h-screen flex-col">
      <!-- Top bar -->
      <header class="flex h-14 items-center justify-between border-b border-[var(--ui-border)] bg-[var(--ui-bg-elevated)] px-4">
        <div class="flex items-center gap-3">
          <span class="text-xl">🍽️</span>
          <span class="text-lg font-bold">{{ t('pos.title') }}</span>
        </div>

        <div class="flex items-center gap-2">
          <UButton
            :label="t('pos.nav.orders')"
            icon="i-lucide-receipt"
            variant="ghost"
            size="sm"
          />
          <UButton
            :label="t('pos.nav.close_register')"
            icon="i-lucide-lock"
            variant="ghost"
            size="sm"
          />
        </div>
      </header>

      <!-- Main content -->
      <main class="flex-1 overflow-hidden">
        <RouterView />
      </main>
    </div>
  </UApp>
</template>
