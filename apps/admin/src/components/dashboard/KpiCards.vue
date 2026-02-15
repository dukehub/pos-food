<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const kpis = [
  {
    key: 'revenue',
    icon: 'i-lucide-banknote',
    value: '12 450 DA',
    trend: +12.5,
    color: 'text-emerald-500'
  },
  {
    key: 'orders',
    icon: 'i-lucide-shopping-cart',
    value: '84',
    trend: +8.2,
    color: 'text-blue-500'
  },
  {
    key: 'avgTicket',
    icon: 'i-lucide-receipt',
    value: '148 DA',
    trend: -2.1,
    color: 'text-amber-500'
  },
  {
    key: 'tablesOccupied',
    icon: 'i-lucide-armchair',
    value: '12 / 20',
    trend: +5.0,
    color: 'text-violet-500'
  }
]
</script>

<template>
  <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
    <UCard
      v-for="kpi in kpis"
      :key="kpi.key"
      :ui="{ body: 'flex items-center gap-4 sm:gap-5' }"
    >
      <div class="flex size-12 shrink-0 items-center justify-center rounded-lg bg-primary/10">
        <UIcon :name="kpi.icon" :class="[kpi.color, 'size-6']" />
      </div>

      <div class="min-w-0 flex-1">
        <p class="text-sm font-medium text-muted truncate">
          {{ t(`dashboard.kpi.${kpi.key}`) }}
        </p>
        <div class="flex items-center gap-2">
          <span class="text-2xl font-bold">{{ kpi.value }}</span>
          <UBadge
            :color="kpi.trend >= 0 ? 'success' : 'error'"
            variant="subtle"
            size="sm"
          >
            <UIcon
              :name="kpi.trend >= 0 ? 'i-lucide-trending-up' : 'i-lucide-trending-down'"
              class="size-3"
            />
            {{ Math.abs(kpi.trend) }}%
          </UBadge>
        </div>
      </div>
    </UCard>
  </div>
</template>
