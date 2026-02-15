<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

type OrderStatus = 'pending' | 'preparing' | 'ready' | 'delivered'

const statusColors: Record<OrderStatus, 'warning' | 'info' | 'success' | 'neutral'> = {
  pending: 'warning',
  preparing: 'info',
  ready: 'success',
  delivered: 'neutral'
}

const columns = [
  { accessorKey: 'orderNum', header: () => t('dashboard.recentOrders.orderNum') },
  { accessorKey: 'table', header: () => t('dashboard.recentOrders.table') },
  { accessorKey: 'status', header: () => t('dashboard.recentOrders.status') },
  { accessorKey: 'total', header: () => t('dashboard.recentOrders.total') },
  { accessorKey: 'time', header: () => t('dashboard.recentOrders.time') }
]

const rows = [
  { orderNum: '#1084', table: 'T-05', status: 'preparing' as OrderStatus, total: '2 400 DA', time: '12:34' },
  { orderNum: '#1083', table: 'T-12', status: 'pending' as OrderStatus, total: '1 850 DA', time: '12:28' },
  { orderNum: '#1082', table: 'T-03', status: 'ready' as OrderStatus, total: '3 200 DA', time: '12:15' },
  { orderNum: '#1081', table: 'T-08', status: 'delivered' as OrderStatus, total: '1 600 DA', time: '12:02' },
  { orderNum: '#1080', table: 'T-01', status: 'delivered' as OrderStatus, total: '4 100 DA', time: '11:45' }
]
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center gap-2">
        <UIcon name="i-lucide-clock" class="text-blue-500 size-5" />
        <h3 class="text-base font-semibold">{{ t('dashboard.recentOrders.title') }}</h3>
      </div>
    </template>

    <UTable :data="rows" :columns="columns">
      <template #status-cell="{ row }">
        <UBadge
          :color="statusColors[row.original.status as OrderStatus]"
          variant="subtle"
          size="sm"
        >
          {{ t(`dashboard.recentOrders.status${row.original.status.charAt(0).toUpperCase() + row.original.status.slice(1)}`) }}
        </UBadge>
      </template>
    </UTable>
  </UCard>
</template>
