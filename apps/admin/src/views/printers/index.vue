<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiClient } from '@pos/api'
import PrinterForm from './PrinterForm.vue'

interface Printer {
    id: string
    name: string
    driver_type: string
    system_printer_name?: string
    ip_address?: string
    is_active: boolean
}

const printers = ref<Printer[]>([])
const loading = ref(false)
const isModalOpen = ref(false)
const selectedPrinter = ref<Printer | null>(null)

const columns = [
    { key: 'name', label: 'Name' },
    { key: 'driver_type', label: 'Type' },
    { key: 'connection', label: 'Connection' },
    { key: 'is_active', label: 'Status' },
    { key: 'actions', label: '' }
] as any[]

async function loadPrinters() {
    loading.value = true
    try {
        const res = await apiClient.get<Printer[]>('/plugins/printer/printers')
        printers.value = res.data
    } catch (e) {
        console.error(e)
    } finally {
        loading.value = false
    }
}

function openCreate() {
    selectedPrinter.value = null
    isModalOpen.value = true
}

function openEdit(printer: Printer) {
    selectedPrinter.value = printer
    isModalOpen.value = true
}

async function deletePrinter(printer: Printer) {
    if (!confirm(`Delete printer "${printer.name}"?`)) return
    try {
        await apiClient.delete(`/plugins/printer/printers/${printer.id}`)
        loadPrinters()
    } catch {
        alert('Failed to delete printer')
    }
}

onMounted(() => loadPrinters())
</script>

<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold">Printers</h1>
        <UButton icon="i-heroicons-plus" @click="openCreate">Add Printer</UButton>
    </div>

    <UCard>
        <UTable :rows="printers" :columns="columns" :loading="loading">
            <template #driver_type-data="props">
                <UBadge color="neutral" variant="subtle" size="xs">
                    {{ (props as any).row.driver_type.toUpperCase() }}
                </UBadge>
            </template>
            <template #connection-data="props">
                <span v-if="(props as any).row.driver_type === 'network'">
                    {{ (props as any).row.ip_address }}
                </span>
                <span v-else-if="(props as any).row.driver_type === 'windows'">
                     {{ (props as any).row.system_printer_name }}
                </span>
                <span v-else class="text-gray-400">-</span>
            </template>
            <template #is_active-data="props">
                <UBadge :color="(props as any).row.is_active ? 'success' : 'neutral'" variant="subtle" size="xs">
                    {{ (props as any).row.is_active ? 'Active' : 'Inactive' }}
                </UBadge>
            </template>
            <template #actions-data="props">
                <div class="flex gap-2 justify-end">
                    <UButton icon="i-heroicons-pencil-square" variant="ghost" size="xs" @click="openEdit((props as any).row)" />
                    <UButton icon="i-heroicons-trash" color="error" variant="ghost" size="xs" @click="deletePrinter((props as any).row)" />
                </div>
            </template>
        </UTable>
    </UCard>

    <UModal v-model="isModalOpen">
        <div class="p-6">
            <h3 class="text-lg font-semibold mb-4">{{ selectedPrinter ? 'Edit Printer' : 'New Printer' }}</h3>
            <PrinterForm :printer="selectedPrinter" @close="isModalOpen = false" @refresh="loadPrinters" />
        </div>
    </UModal>
  </div>
</template>
