<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { apiClient } from '@pos/api'
import TableForm from './TableForm.vue'

interface Zone {
    id: string
    name: string
}

interface Table {
    id: string
    code: string
    zone_id: string
    capacity: number
    status: string
    is_active: boolean
}

const tables = ref<Table[]>([])
const zones = ref<Zone[]>([])
const loading = ref(false)
const isModalOpen = ref(false)
const selectedTable = ref<Table | null>(null)
const filterZoneId = ref<string | undefined>(undefined)

const columns = [
    { key: 'code', label: 'Code' },
    { key: 'zone_id', label: 'Zone' },
    { key: 'capacity', label: 'Capacity' },
    { key: 'status', label: 'Status' },
    { key: 'actions', label: 'Actions' }
] as any[]

async function loadZones() {
    try {
        const res = await apiClient.get<Zone[]>('/plugins/floor_plan/zones')
        zones.value = res.data
    } catch {}
}

async function loadTables() {
    loading.value = true
    try {
        const query = new URLSearchParams()
        if (filterZoneId.value && filterZoneId.value !== 'all') {
            query.append('zone_id', filterZoneId.value)
        }
        const url = `/plugins/floor_plan/tables?${query.toString()}`
        const res = await apiClient.get<Table[]>(url)
        tables.value = res.data
    } catch (e) {
        console.error(e)
    } finally {
        loading.value = false
    }
}

watch(filterZoneId, () => {
    loadTables()
})

function getZoneName(id: string) {
    return zones.value.find(z => z.id === id)?.name || id
}

function openCreate() {
    selectedTable.value = null
    isModalOpen.value = true
}

function openEdit(table: Table) {
    selectedTable.value = { ...table }
    isModalOpen.value = true
}

async function deleteTable(table: Table) {
    if (!confirm(`Delete table "${table.code}"?`)) return
    try {
        await apiClient.delete(`/plugins/floor_plan/tables/${table.id}`)
        loadTables()
    } catch (e) {
        console.error(e)
        alert('Failed to delete table')
    }
}

onMounted(async () => {
    await loadZones()
    loadTables()
})

const zoneOptions = computed(() => {
    return [
        { label: 'All Zones', id: 'all' },
        ...zones.value.map(z => ({ label: z.name, id: z.id }))
    ]
})
</script>

<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center">
        <!-- Replaced USelectMenu with standard select or just wait for fix? USelectMenu is fine if options structure is correct -->
        <div class="w-48">
             <USelectMenu 
                v-model="filterZoneId" 
                :options="zoneOptions" 
                value-attribute="id"
                option-attribute="label"
                placeholder="Filter by Zone" 
            />
        </div>
        <UButton icon="i-heroicons-plus" @click="openCreate">Add Table</UButton>
    </div>

    <UCard>
        <UTable :rows="tables" :columns="columns" :loading="loading">
            <template #zone_id-data="props">
                {{ getZoneName((props as any).row.zone_id) }}
            </template>
            <template #actions-data="props">
                <UDropdown :items="[
                    [{ label: 'Edit', icon: 'i-heroicons-pencil-square', click: () => openEdit((props as any).row) }],
                    [{ label: 'Delete', icon: 'i-heroicons-trash', color: 'red', click: () => deleteTable((props as any).row) }]
                ]">
                    <UButton color="neutral" variant="ghost" icon="i-heroicons-ellipsis-horizontal" />
                </UDropdown>
            </template>
        </UTable>
    </UCard>

    <UModal v-model="isModalOpen">
        <div class="p-6">
            <h3 class="text-lg font-semibold mb-4">{{ selectedTable ? 'Edit Table' : 'New Table' }}</h3>
            <TableForm :table="selectedTable" :zones="zones" @close="isModalOpen = false" @refresh="loadTables" />
        </div>
    </UModal>
  </div>
</template>
