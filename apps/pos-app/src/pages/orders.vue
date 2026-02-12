<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const demoOrders = [
  { id: '1', table: 3, items: 4, total: 45.50, status: 'paid', time: '18:30' },
  { id: '2', table: 7, items: 2, total: 23.00, status: 'paid', time: '18:45' },
  { id: '3', table: null, items: 1, total: 3.50, status: 'paid', time: '17:15' },
]

const statusColors: Record<string, string> = {
  paid: 'success',
  cancelled: 'error',
}
</script>

<template>
  <div class="flex flex-1 flex-col overflow-auto p-6">
    <div class="mb-4 flex items-center justify-between">
      <h1 class="text-xl font-bold">{{ t('pos.nav.orders') }}</h1>
      <UButton
        label="Retour à la caisse"
        icon="i-lucide-arrow-left"
        variant="ghost"
        to="/"
      />
    </div>

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
            <th class="pb-3 font-medium">{{ t('common.actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="order in demoOrders"
            :key="order.id"
            class="border-b border-[var(--ui-border)] last:border-0"
          >
            <td class="py-3 font-mono">{{ order.id }}</td>
            <td class="py-3">{{ order.table ?? '—' }}</td>
            <td class="py-3">{{ order.items }}</td>
            <td class="py-3 font-medium">{{ order.total.toFixed(2) }} €</td>
            <td class="py-3">
              <UBadge :color="(statusColors[order.status] as any) ?? 'neutral'">
                {{ order.status }}
              </UBadge>
            </td>
            <td class="py-3 text-[var(--ui-text-muted)]">{{ order.time }}</td>
            <td class="py-3">
              <UButton variant="ghost" icon="i-lucide-printer" size="xs" />
            </td>
          </tr>
        </tbody>
      </table>
    </UCard>
  </div>
</template>
