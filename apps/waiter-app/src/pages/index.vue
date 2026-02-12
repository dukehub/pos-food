<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useTablesStore } from '../stores/tables'
import type { RestaurantTable } from '@pos-food/core'

const { t } = useI18n()
const tablesStore = useTablesStore()

// Demo tables
const demoTables: RestaurantTable[] = Array.from({ length: 12 }, (_, i) => ({
  id: String(i + 1),
  number: i + 1,
  name: `Table ${i + 1}`,
  seats: [2, 4, 4, 6, 2, 4, 8, 2, 4, 6, 4, 2][i],
  zone: i < 6 ? 'Salle' : 'Terrasse',
  status: (['free', 'occupied', 'free', 'occupied', 'free', 'reserved', 'free', 'free', 'occupied', 'free', 'free', 'cleaning'] as const)[i],
  isActive: true,
  createdAt: '',
  updatedAt: '',
}))

tablesStore.setTables(demoTables)

const statusConfig: Record<string, { color: string; label: string }> = {
  free: { color: 'success', label: t('waiter.tables.free') },
  occupied: { color: 'error', label: t('waiter.tables.occupied') },
  reserved: { color: 'warning', label: t('waiter.tables.reserved') },
  cleaning: { color: 'neutral', label: 'Nettoyage' },
}
</script>

<template>
  <div class="flex flex-1 flex-col p-4">
    <h1 class="mb-4 text-xl font-bold">{{ t('waiter.tables.title') }}</h1>

    <!-- Zone groups -->
    <div v-for="[zone, tables] in tablesStore.tablesByZone" :key="zone" class="mb-6">
      <h2 class="mb-3 text-sm font-medium text-[var(--ui-text-muted)] uppercase">{{ zone }}</h2>

      <div class="grid grid-cols-3 gap-3 sm:grid-cols-4">
        <RouterLink
          v-for="table in tables"
          :key="table.id"
          :to="`/table/${table.id}`"
          class="block"
        >
          <UCard
            class="cursor-pointer text-center transition-transform active:scale-95"
            :class="{
              'border-green-500/50': table.status === 'free',
              'border-red-500/50': table.status === 'occupied',
              'border-amber-500/50': table.status === 'reserved',
            }"
          >
            <p class="text-2xl font-bold">{{ table.number }}</p>
            <p class="mb-1 text-xs text-[var(--ui-text-muted)]">{{ table.seats }} places</p>
            <UBadge :color="(statusConfig[table.status]?.color as any) ?? 'neutral'" size="xs">
              {{ statusConfig[table.status]?.label ?? table.status }}
            </UBadge>
          </UCard>
        </RouterLink>
      </div>
    </div>
  </div>
</template>
