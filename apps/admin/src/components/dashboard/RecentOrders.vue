<script setup lang="ts">
const orders = [
  { id: '#ORD-001', customer: 'Walk-in', total: '$45.00', status: 'completed', time: '10 min ago' },
  { id: '#ORD-002', customer: 'Table 5', total: '$120.50', status: 'pending', time: '25 min ago' },
  { id: '#ORD-003', customer: 'Uber Eats', total: '$32.00', status: 'cooking', time: '40 min ago' },
  { id: '#ORD-004', customer: 'Walk-in', total: '$15.00', status: 'completed', time: '1 hr ago' },
  { id: '#ORD-005', customer: 'Table 2', total: '$85.00', status: 'cancelled', time: '2 hrs ago' },
]

const columns = [
  { key: 'id', label: 'Order ID', id: 'id' },
  { key: 'customer', label: 'Customer', id: 'customer' },
  { key: 'status', label: 'Status', id: 'status' },
  { key: 'total', label: 'Total', id: 'total' },
] as any[]

const getStatusColor = (status: string) => {
  switch (status) {
    case 'completed': return 'success'
    case 'pending': return 'warning'
    case 'cooking': return 'primary'
    case 'cancelled': return 'error'
    default: return 'neutral'
  }
}
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center justify-between">
        <h3 class="text-base font-semibold">Recent Orders</h3>
        <UButton variant="ghost" color="neutral" to="/orders" size="xs">View all</UButton>
      </div>
    </template>

    <UTable :rows="orders" :columns="columns">
      <template #status-data="props">
        <UBadge :color="getStatusColor((props as any).row.status)" variant="subtle" size="xs">
          {{ (props as any).row.status }}
        </UBadge>
      </template>
    </UTable>
  </UCard>
</template>
