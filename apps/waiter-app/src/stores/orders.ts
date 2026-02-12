import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Order } from '@pos-food/core'

export const useOrdersStore = defineStore('orders', () => {
    const orders = ref<Order[]>([])
    const isLoading = ref(false)

    const activeOrders = computed(() =>
        orders.value.filter(o =>
            !['paid', 'cancelled'].includes(o.status),
        ),
    )

    const ordersByTable = computed(() => {
        const map = new Map<string, Order[]>()
        for (const order of activeOrders.value) {
            if (order.tableId) {
                const list = map.get(order.tableId) ?? []
                list.push(order)
                map.set(order.tableId, list)
            }
        }
        return map
    })

    function setOrders(data: Order[]) {
        orders.value = data
    }

    function addOrder(order: Order) {
        orders.value.push(order)
    }

    function updateOrder(updated: Order) {
        const index = orders.value.findIndex(o => o.id === updated.id)
        if (index !== -1) {
            orders.value[index] = updated
        }
    }

    function getOrderForTable(tableId: string): Order | undefined {
        return activeOrders.value.find(o => o.tableId === tableId)
    }

    return {
        orders,
        isLoading,
        activeOrders,
        ordersByTable,
        setOrders,
        addOrder,
        updateOrder,
        getOrderForTable,
    }
})
