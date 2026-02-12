import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { RestaurantTable, TableStatus } from '@pos-food/core'

export const useTablesStore = defineStore('tables', () => {
    const tables = ref<RestaurantTable[]>([])
    const isLoading = ref(false)

    const activeTables = computed(() =>
        tables.value.filter(t => t.isActive),
    )

    const tablesByZone = computed(() => {
        const map = new Map<string, RestaurantTable[]>()
        for (const table of activeTables.value) {
            const zone = table.zone ?? 'default'
            const list = map.get(zone) ?? []
            list.push(table)
            map.set(zone, list)
        }
        return map
    })

    const freeTables = computed(() =>
        activeTables.value.filter(t => t.status === 'free'),
    )

    const occupiedTables = computed(() =>
        activeTables.value.filter(t => t.status === 'occupied'),
    )

    function setTables(data: RestaurantTable[]) {
        tables.value = data
    }

    function updateTableStatus(tableId: string, status: TableStatus) {
        const table = tables.value.find(t => t.id === tableId)
        if (table) {
            table.status = status
        }
    }

    function setTableOrder(tableId: string, orderId: string | undefined) {
        const table = tables.value.find(t => t.id === tableId)
        if (table) {
            table.currentOrderId = orderId
            table.status = orderId ? 'occupied' : 'free'
        }
    }

    return {
        tables,
        isLoading,
        activeTables,
        tablesByZone,
        freeTables,
        occupiedTables,
        setTables,
        updateTableStatus,
        setTableOrder,
    }
})
