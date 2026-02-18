<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiClient } from '@pos/api'
import ZoneForm from './ZoneForm.vue'

interface Zone {
    id: string
    name: string
    display_order: number
    is_active: boolean
}

const zones = ref<Zone[]>([])
const loading = ref(false)
const isModalOpen = ref(false)
const selectedZone = ref<Zone | null>(null)

const columns = [
    { key: 'name', label: 'Name' },
    { key: 'display_order', label: 'Order' },
    { key: 'is_active', label: 'Status' },
    { key: 'actions', label: 'Actions' }
] as any[]

async function loadZones() {
    loading.value = true
    try {
        const res = await apiClient.get<Zone[]>('/plugins/floor_plan/zones')
        zones.value = res.data
    } catch (e) {
        console.error(e)
    } finally {
        loading.value = false
    }
}

function openCreate() {
    selectedZone.value = null
    isModalOpen.value = true
}

function openEdit(zone: Zone) {
    selectedZone.value = { ...zone }
    isModalOpen.value = true
}

async function deleteZone(zone: Zone) {
    if (!confirm(`Delete zone "${zone.name}"?`)) return
    try {
        await apiClient.delete(`/plugins/floor_plan/zones/${zone.id}`)
        loadZones()
    } catch (e) {
        console.error(e)
        alert('Failed to delete zone')
    }
}

onMounted(() => {
    loadZones()
})
</script>

<template>
  <div class="space-y-4">
    <div class="flex justify-end">
        <UButton icon="i-heroicons-plus" @click="openCreate">Add Zone</UButton>
    </div>

    <UCard>
        <UTable :rows="zones" :columns="columns" :loading="loading">
            <template #is_active-data="props">
                <UBadge :color="(props as any).row.is_active ? 'success' : 'neutral'" variant="subtle">
                    {{ (props as any).row.is_active ? 'Active' : 'Inactive' }}
                </UBadge>
            </template>
            <template #actions-data="props">
                <UDropdown :items="[
                    [{ label: 'Edit', icon: 'i-heroicons-pencil-square', click: () => openEdit((props as any).row) }],
                    [{ label: 'Delete', icon: 'i-heroicons-trash', color: 'red', click: () => deleteZone((props as any).row) }]
                ]">
                    <UButton color="neutral" variant="ghost" icon="i-heroicons-ellipsis-horizontal" />
                </UDropdown>
            </template>
        </UTable>
    </UCard>

    <UModal v-model="isModalOpen">
        <div class="p-6">
            <h3 class="text-lg font-semibold mb-4">{{ selectedZone ? 'Edit Zone' : 'New Zone' }}</h3>
            <ZoneForm :zone="selectedZone" @close="isModalOpen = false" @refresh="loadZones" />
        </div>
    </UModal>
  </div>
</template>
