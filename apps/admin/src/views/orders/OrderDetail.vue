<script setup lang="ts">
import { ref, computed } from 'vue'
import { apiClient } from '@pos/api'

const props = defineProps<{
    order: any
}>()

const emit = defineEmits(['close', 'refresh'])

const loading = ref(false)

const statusColors: Record<string, string> = {
    draft: 'neutral',
    confirmed: 'info',
    preparation: 'warning',
    ready: 'success',
    served: 'success',
    cancelled: 'error'
}

const statusLabel = computed(() => {
    return props.order?.status.toUpperCase() || 'UNKNOWN'
})

const items = computed(() => props.order?.lines || [])

async function updateStatus(newStatus: string) {
    if (!confirm(`Change status to ${newStatus}?`)) return
    loading.value = true
    try {
        await apiClient.put(`/plugins/orders/orders/${props.order.id}`, { status: newStatus })
        emit('refresh')
        emit('close')
    } catch (e) {
        console.error(e)
        alert('Failed to update status')
    } finally {
        loading.value = false
    }
}
</script>

<template>
  <div class="h-full flex flex-col">
    <div class="flex-1 overflow-y-auto p-4 space-y-6">
        <!-- Header -->
        <div class="flex justify-between items-start">
            <div>
                <h2 class="text-xl font-bold">Order #{{ order.id.slice(0, 8) }}</h2>
                <p class="text-sm text-gray-500">{{ new Date(order.created_at).toLocaleString() }}</p>
                <p v-if="order.customer_id" class="text-sm text-gray-500 mt-1">Customer: {{ order.customer_id }}</p> 
            </div>
            <UBadge :color="(statusColors[order.status] || 'neutral') as any" size="md">
                {{ statusLabel }}
            </UBadge>
        </div>

        <UDivider />

        <!-- Items -->
        <div class="space-y-4">
            <h3 class="font-semibold text-gray-900 dark:text-white">Items</h3>
            <div v-for="line in items" :key="line.id" class="flex justify-between items-start py-2 border-b border-gray-100 dark:border-gray-800 last:border-0">
                <div class="flex-1">
                    <div class="flex items-center gap-2">
                         <span class="font-medium">{{ line.quantity }}x</span>
                         <span>{{ line.name_snapshot }}</span>
                    </div>
                    <!-- Modifiers -->
                    <div v-if="line.modifiers && line.modifiers.length > 0" class="mt-1 ps-6 text-sm text-gray-500 space-y-0.5">
                        <div v-for="mod in line.modifiers" :key="mod.id">
                            + {{ mod.item_name_snapshot }} 
                            <span v-if="mod.price_delta > 0">({{ mod.price_delta }} €)</span>
                        </div>
                    </div>
                </div>
                <div class="font-medium">
                    {{ line.line_total }} €
                </div>
            </div>
        </div>

        <UDivider />

        <!-- Totals -->
        <div class="flex justify-between items-center text-lg font-bold">
            <span>Total</span>
            <span>{{ order.total_amount }} €</span>
        </div>

        <div v-if="order.note" class="bg-gray-50 dark:bg-gray-800 p-3 rounded-md text-sm">
            <span class="font-semibold">Note:</span> {{ order.note }}
        </div>
    </div>

    <!-- Actions -->
    <div class="p-4 border-t border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900 flex gap-2 justify-end">
        <template v-if="order.status === 'draft'">
            <UButton color="error" variant="ghost" @click="updateStatus('cancelled')">Cancel</UButton>
            <UButton color="primary" @click="updateStatus('confirmed')">Confirm</UButton>
        </template>

        <template v-else-if="order.status === 'confirmed'">
             <UButton color="error" variant="ghost" @click="updateStatus('cancelled')">Cancel</UButton>
             <UButton color="warning" @click="updateStatus('preparation')">In Prep</UButton>
        </template>
        
        <template v-else-if="order.status === 'preparation'">
             <UButton color="success" @click="updateStatus('ready')">Ready</UButton>
        </template>

        <template v-else-if="order.status === 'ready'">
             <UButton color="success" @click="updateStatus('served')">Served</UButton>
        </template>
        
         <UButton variant="ghost" @click="$emit('close')">Close</UButton>
    </div>
  </div>
</template>
