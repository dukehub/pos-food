<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const actions = [
  { key: 'newProduct', icon: 'i-lucide-package-plus', color: 'primary' as const },
  { key: 'openRegister', icon: 'i-lucide-calculator', color: 'success' as const },
  { key: 'addZone', icon: 'i-lucide-map-pin-plus', color: 'info' as const },
  { key: 'exportReport', icon: 'i-lucide-file-down', color: 'neutral' as const }
]
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center gap-2">
        <UIcon name="i-lucide-zap" class="text-primary size-5" />
        <h3 class="text-base font-semibold">{{ t('dashboard.quickActions.title') }}</h3>
      </div>
    </template>

    <div class="grid grid-cols-2 gap-2">
      <UButton
        v-for="action in actions"
        :key="action.key"
        :icon="action.icon"
        :label="t(`dashboard.quickActions.${action.key}`)"
        :color="action.color"
        variant="soft"
        block
        class="justify-start"
      />
    </div>
  </UCard>
</template>
