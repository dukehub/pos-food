<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiClient } from '@pos/api'
import CustomerForm from './CustomerForm.vue'

interface Customer {
    id: string
    name: string
    phone: string
    email: string
    current_balance: number
    is_active: boolean
}

const customers = ref<Customer[]>([])
const loading = ref(false)
const isModalOpen = ref(false)
const selectedCustomer = ref<Customer | null>(null)

const columns = [
    { key: 'name', label: 'Name' },
    { key: 'phone', label: 'Phone' },
    { key: 'email', label: 'Email' },
    { key: 'current_balance', label: 'Balance' },
    { key: 'is_active', label: 'Status' },
    { key: 'actions', label: '' }
] as any[]

async function loadCustomers() {
    loading.value = true
    try {
        const res = await apiClient.get<Customer[]>('/plugins/customers/customers')
        customers.value = res.data
    } catch (e) {
        console.error(e)
    } finally {
        loading.value = false
    }
}

function openCreate() {
    selectedCustomer.value = null
    isModalOpen.value = true
}

function openEdit(customer: Customer) {
    selectedCustomer.value = customer
    isModalOpen.value = true
}

async function deleteCustomer(customer: Customer) {
    if (!confirm(`Delete customer "${customer.name}"?`)) return
    try {
        await apiClient.delete(`/plugins/customers/customers/${customer.id}`)
        loadCustomers()
    } catch {
        alert('Failed to delete customer')
    }
}

onMounted(() => loadCustomers())
</script>

<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold">Customers</h1>
        <UButton icon="i-heroicons-plus" @click="openCreate">Add Customer</UButton>
    </div>

    <UCard>
        <UTable :rows="customers" :columns="columns" :loading="loading">
            <template #current_balance-data="props">
                <span :class="(props as any).row.current_balance > 0 ? 'text-red-500' : 'text-green-500'">
                    {{ (props as any).row.current_balance }} €
                </span>
            </template>
            <template #is_active-data="props">
                <UBadge :color="(props as any).row.is_active ? 'success' : 'neutral'" variant="subtle" size="xs">
                    {{ (props as any).row.is_active ? 'Active' : 'Inactive' }}
                </UBadge>
            </template>
            <template #actions-data="props">
                <div class="flex gap-2 justify-end">
                    <UButton icon="i-heroicons-pencil-square" variant="ghost" size="xs" @click="openEdit((props as any).row)" />
                    <UButton icon="i-heroicons-trash" color="error" variant="ghost" size="xs" @click="deleteCustomer((props as any).row)" />
                </div>
            </template>
        </UTable>
    </UCard>

    <UModal v-model="isModalOpen">
        <div class="p-6">
            <h3 class="text-lg font-semibold mb-4">{{ selectedCustomer ? 'Edit Customer' : 'New Customer' }}</h3>
            <CustomerForm :customer="selectedCustomer" @close="isModalOpen = false" @refresh="loadCustomers" />
        </div>
    </UModal>
  </div>
</template>
