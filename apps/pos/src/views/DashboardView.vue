<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <div class="min-h-screen flex flex-col items-center justify-center gap-6 p-8">
    <UIcon name="i-lucide-shopping-cart" class="size-16 text-primary" />
    <h1 class="text-3xl font-bold text-primary">
      POS — {{ t('nav.dashboard') }}
    </h1>
    <p class="text-lg text-muted">
      {{ t('common.loading') }}
    </p>
    <div class="flex gap-4">
      <UButton :label="t('nav.products')" variant="soft" icon="i-lucide-package" />
      <UButton :label="t('nav.orders')" variant="soft" icon="i-lucide-clipboard-list" />
    </div>
  </div>
</template>
