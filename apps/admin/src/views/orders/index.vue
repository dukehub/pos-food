<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { apiClient } from '@pos/api'
import OrderDetail from './OrderDetail.vue'

interface Order {
    id: string
    tenant_id: string
    status: string
    total_amount: number
    created_at: string
    lines: any[]
}

const orders = ref<Order[]>([])
const loading = ref(false)
const selectedOrder = ref<Order | null>(null)
const isSlideoverOpen = ref(false)

const filters = [
    { label: 'All', value: 'all' },
    { label: 'Draft', value: 'draft' },
    { label: 'Confirmed', value: 'confirmed' },
    { label: 'In Prep', value: 'preparation' }, // Matches backend status? Need to verify standard. usually standard in kitchen is preparation
    { label: 'Ready', value: 'ready' },
    { label: 'Served', value: 'served' },
    { label: 'Cancelled', value: 'cancelled' }
]
const activeFilter = ref('all')

const columns = [
    { key: 'id', label: 'Order #' },
    { key: 'created_at', label: 'Date' },
    { key: 'total_amount', label: 'Total' },
    { key: 'status', label: 'Status' },
    { key: 'actions', label: '' }
] as any[]

async function loadOrders() {
    loading.value = true
    try {
        const res = await apiClient.get<Order[]>('/plugins/orders/orders')
        // Sort by date desc locally for now, backend order_by created_at asc usually in list_orders unless generated differently
        orders.value = res.data.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    } catch (e) {
        console.error(e)
    } finally {
        loading.value = false
    }
}

const filteredOrders = computed(() => {
    if (activeFilter.value === 'all') return orders.value
    return orders.value.filter(o => o.status === activeFilter.value)
})

function openOrder(order: Order) {
    selectedOrder.value = order
    isSlideoverOpen.value = true
}

const statusColors: Record<string, string> = {
    draft: 'neutral',
    confirmed: 'info',
    preparation: 'warning',
    ready: 'success',
    served: 'success',
    cancelled: 'error'
}

onMounted(() => loadOrders())
</script>

<template>
  <div class="h-full flex flex-col space-y-4">
    <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold">Kitchen / Orders</h1>
        <div class="flex gap-2">
            <UButton icon="i-heroicons-arrow-path" variant="ghost" @click="loadOrders" />
        </div>
    </div>

    <!-- Filters -->
    <div class="flex gap-2 mb-4 overflow-x-auto pb-2">
        <UButton 
            v-for="filter in filters" 
            :key="filter.value"
            :variant="activeFilter === filter.value ? 'solid' : 'ghost'"
            :color="activeFilter === filter.value ? 'primary' : 'neutral'"
            size="xs"
            @click="activeFilter = filter.value"
        >
            {{ filter.label }}
        </UButton>
    </div>

    <UCard class="flex-1 flex flex-col" :ui="{ body: 'flex-1 overflow-hidden p-0' }">
        <UTable 
            :rows="filteredOrders" 
            :columns="columns" 
            :loading="loading"
            class="h-full"
        >
            <template #id-data="props">
                <span class="font-mono text-xs">{{ (props as any).row.id.slice(0, 8) }}</span>
            </template>
            <template #created_at-data="props">
                <span class="text-sm text-gray-500">
                    {{ new Date((props as any).row.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }}
                </span>
            </template>
             <template #total_amount-data="props">
                <span class="font-semibold">{{ (props as any).row.total_amount }} €</span>
            </template>
            <template #status-data="props">
                <UBadge :color="(statusColors[(props as any).row.status] || 'neutral') as any" variant="subtle" size="xs">
                    {{ (props as any).row.status.toUpperCase() }}
                </UBadge>
            </template>
            <template #actions-data="props">
                <UButton icon="i-heroicons-eye" variant="ghost" size="xs" @click="openOrder((props as any).row)" />
            </template>
        </UTable>
    </UCard>

    <USlideover v-model="isSlideoverOpen" :ui="{ content: 'w-screen max-w-lg' }">
        <OrderDetail 
            v-if="selectedOrder" 
            :order="selectedOrder" 
            @close="isSlideoverOpen = false" 
            @refresh="loadOrders" 
        />
    </USlideover>
  </div>
</template>
