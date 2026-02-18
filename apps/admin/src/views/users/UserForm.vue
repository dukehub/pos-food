<script setup lang="ts">
import { ref, reactive } from 'vue'
import { apiClient } from '@pos/api'

const emit = defineEmits(['close', 'refresh'])

const state = reactive({
    username: '',
    full_name: '',
    pin_code: '',
    role: 'waiter',
    language: 'fr'
})

const loading = ref(false)
const error = ref('')

const roles = [
    { label: 'Admin', value: 'admin' },
    { label: 'Waiter', value: 'waiter' },
    { label: 'Cashier', value: 'cashier' }
]

async function handleSubmit() {
    loading.value = true
    error.value = ''
    try {
        await apiClient.post('/plugins/users/users', state)
        emit('refresh')
        emit('close')
    } catch (e: any) {
        error.value = e.message || 'Failed to create user'
    } finally {
        loading.value = false
    }
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <UFormGroup label="Username" name="username" required>
        <UInput v-model="state.username" />
    </UFormGroup>
    
    <UFormGroup label="Full Name" name="full_name">
        <UInput v-model="state.full_name" />
    </UFormGroup>

    <UFormGroup label="PIN Code" name="pin_code" required>
        <UInput v-model="state.pin_code" type="password" placeholder="4-6 digits" />
    </UFormGroup>

    <UFormGroup label="Role" name="role" required>
        <USelect v-model="state.role" :options="roles" />
    </UFormGroup>

    <UFormGroup label="Language" name="language">
        <USelect v-model="state.language" :options="['fr', 'ar', 'en']" />
    </UFormGroup>

    <div v-if="error" class="text-red-500 text-sm">
        {{ error }}
    </div>

    <div class="flex justify-end gap-3 pt-4">
        <UButton color="neutral" variant="ghost" @click="$emit('close')">Cancel</UButton>
        <UButton type="submit" :loading="loading">Create User</UButton>
    </div>
  </form>
</template>
