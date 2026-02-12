<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { PageHeader } from '@pos-food/ui'

const { t } = useI18n()

const demoOrders = [
  { id: '1', table: 3, items: 4, total: 45.50, status: 'served', time: '18:30' },
  { id: '2', table: 7, items: 2, total: 23.00, status: 'in_preparation', time: '18:45' },
  { id: '3', table: 1, items: 6, total: 67.80, status: 'paid', time: '17:15' },
  { id: '4', table: 5, items: 3, total: 34.00, status: 'sent_to_kitchen', time: '19:00' },
]

const statusColors: Record<string, string> = {
  draft: 'neutral',
  open: 'info',
  sent_to_kitchen: 'warning',
  in_preparation: 'warning',
  ready: 'success',
  served: 'success',
  paid: 'neutral',
  cancelled: 'error',
}
</script>

<template>
  <div class="flex flex-1 flex-col overflow-auto">
    <PageHeader :title="t('admin.nav.orders')" />

    <div class="flex-1 p-6">
      <UCard>
        <table class="w-full text-left text-sm">
          <thead>
            <tr class="border-b border-[var(--ui-border)]">
              <th class="pb-3 font-medium">#</th>
              <th class="pb-3 font-medium">Table</th>
              <th class="pb-3 font-medium">Articles</th>
              <th class="pb-3 font-medium">{{ t('common.total') }}</th>
              <th class="pb-3 font-medium">{{ t('common.status') }}</th>
              <th class="pb-3 font-medium">Heure</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="order in demoOrders"
              :key="order.id"
              class="border-b border-[var(--ui-border)] last:border-0"
            >
              <td class="py-3 font-mono">{{ order.id }}</td>
              <td class="py-3">{{ order.table }}</td>
              <td class="py-3">{{ order.items }}</td>
              <td class="py-3 font-medium">{{ order.total.toFixed(2) }} €</td>
              <td class="py-3">
                <UBadge :color="(statusColors[order.status] as any) ?? 'neutral'">
                  {{ order.status }}
                </UBadge>
              </td>
              <td class="py-3 text-[var(--ui-text-muted)]">{{ order.time }}</td>
            </tr>
          </tbody>
        </table>
      </UCard>
    </div>
  </div>
</template>
