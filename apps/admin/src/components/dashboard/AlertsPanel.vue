<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const alerts = [
  {
    key: 'lowStock',
    icon: 'i-lucide-package-x',
    color: 'text-red-500',
    bgColor: 'bg-red-500/10'
  },
  {
    key: 'registerOpen',
    icon: 'i-lucide-alert-triangle',
    color: 'text-amber-500',
    bgColor: 'bg-amber-500/10'
  },
  {
    key: 'reservation',
    icon: 'i-lucide-calendar-clock',
    color: 'text-blue-500',
    bgColor: 'bg-blue-500/10'
  }
]
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center gap-2">
        <UIcon name="i-lucide-bell-ring" class="text-red-500 size-5" />
        <h3 class="text-base font-semibold">{{ t('dashboard.alerts.title') }}</h3>
        <UBadge color="error" variant="subtle" size="sm" class="ms-auto">{{ alerts.length }}</UBadge>
      </div>
    </template>

    <div class="flex flex-col gap-3">
      <div
        v-for="alert in alerts"
        :key="alert.key"
        class="flex items-start gap-3 rounded-lg p-3 bg-muted/50 transition-colors hover:bg-muted"
      >
        <div :class="['flex size-9 shrink-0 items-center justify-center rounded-lg', alert.bgColor]">
          <UIcon :name="alert.icon" :class="[alert.color, 'size-4']" />
        </div>
        <div class="min-w-0 flex-1">
          <p class="text-sm font-medium">{{ t(`dashboard.alerts.${alert.key}`) }}</p>
          <p class="text-xs text-muted truncate">{{ t(`dashboard.alerts.${alert.key}Desc`) }}</p>
        </div>
      </div>
    </div>
  </UCard>
</template>
