<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiClient } from '@pos/api'
import UserForm from './UserForm.vue'

interface User {
    id: string
    username: string
    full_name: string
    role: string
    is_active: boolean
    language: string
}

const users = ref<User[]>([])
const loading = ref(false)
const isCreateModalOpen = ref(false)

const columns = [
    { key: 'username', label: 'Username' },
    { key: 'full_name', label: 'Full Name' },
    { key: 'role', label: 'Role' },
    { key: 'language', label: 'Lang' },
    { key: 'is_active', label: 'Status' }
] as any[]

async function loadUsers() {
    loading.value = true
    try {
        const res = await apiClient.get<User[]>('/plugins/users/users')
        users.value = res.data
    } catch (e) {
        console.error(e)
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    loadUsers()
})
</script>

<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center">
        <h2 class="text-lg font-semibold">Users</h2>
        <UButton icon="i-heroicons-plus" @click="isCreateModalOpen = true">
            New User
        </UButton>
    </div>

    <UCard>
        <UTable :rows="users" :columns="columns" :loading="loading">
            <template #role-data="props">
                <UBadge :color="(props as any).row.role === 'admin' ? 'primary' : 'neutral'" variant="subtle">
                    {{ (props as any).row.role }}
                </UBadge>
            </template>
            <template #is_active-data="props">
                <UBadge :color="(props as any).row.is_active ? 'success' : 'error'" variant="subtle">
                    {{ (props as any).row.is_active ? 'Active' : 'Inactive' }}
                </UBadge>
            </template>
        </UTable>
    </UCard>

    <UModal v-model="isCreateModalOpen">
        <div class="p-6">
            <h3 class="text-lg font-semibold mb-4">Add New User</h3>
            <UserForm @close="isCreateModalOpen = false" @refresh="loadUsers" />
        </div>
    </UModal>
  </div>
</template>
