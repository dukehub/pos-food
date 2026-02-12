<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const demoOrders = [
  { id: '1', table: 3, items: ['Burger Classic', 'Coca-Cola'], status: 'sent_to_kitchen', time: '19:05' },
  { id: '2', table: 9, items: ['Pizza Margherita', 'Eau Minérale'], status: 'in_preparation', time: '19:02' },
  { id: '3', table: 4, items: ['Steak Frites', 'Salade César', 'Tiramisu'], status: 'ready', time: '18:50' },
]

const statusConfig: Record<string, { color: string; label: string }> = {
  sent_to_kitchen: { color: 'warning', label: t('waiter.order.sent') },
  in_preparation: { color: 'info', label: 'En préparation' },
  ready: { color: 'success', label: 'Prêt' },
  served: { color: 'neutral', label: 'Servi' },
}
</script>

<template>
  <div class="flex flex-1 flex-col p-4">
    <h1 class="mb-4 text-xl font-bold">{{ t('waiter.nav.orders') }}</h1>

    <div class="space-y-3">
      <UCard
        v-for="order in demoOrders"
        :key="order.id"
      >
        <div class="flex items-start justify-between">
          <div>
            <div class="flex items-center gap-2">
              <span class="text-lg font-bold">Table {{ order.table }}</span>
              <UBadge :color="(statusConfig[order.status]?.color as any) ?? 'neutral'" size="xs">
                {{ statusConfig[order.status]?.label ?? order.status }}
              </UBadge>
            </div>
            <p class="mt-1 text-sm text-[var(--ui-text-muted)]">
              {{ order.items.join(', ') }}
            </p>
            <p class="mt-1 text-xs text-[var(--ui-text-dimmed)]">{{ order.time }}</p>
          </div>

          <div class="flex gap-2">
            <UButton
              v-if="order.status === 'ready'"
              label="Servir"
              icon="i-lucide-check"
              size="sm"
              color="primary"
            />
            <UButton
              v-if="order.status === 'sent_to_kitchen' || order.status === 'in_preparation'"
              label="Détail"
              variant="outline"
              size="sm"
            />
          </div>
        </div>
      </UCard>
    </div>

    <div v-if="demoOrders.length === 0" class="flex flex-1 items-center justify-center py-12 text-[var(--ui-text-muted)]">
      <p>{{ t('common.no_results') }}</p>
    </div>
  </div>
</template>
