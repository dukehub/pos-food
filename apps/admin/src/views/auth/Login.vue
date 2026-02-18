<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@pos/core'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
    loading.value = true
    error.value = ''
    try {
        const success = await authStore.login(username.value, password.value)
        if (success) {
            router.push('/')
        } else {
            error.value = 'Invalid credentials'
        }
    } catch (e) {
        error.value = 'Login failed'
    } finally {
        loading.value = false
    }
}
</script>

<template>
  <UCard class="w-full">
    <template #header>
        <h1 class="text-xl font-bold text-center">Login</h1>
    </template>
    
    <form @submit.prevent="handleLogin" class="space-y-4">
        <UFormGroup label="Username" name="username">
            <UInput v-model="username" icon="i-heroicons-user" autofocus />
        </UFormGroup>
        
        <UFormGroup label="Password" name="password">
            <UInput v-model="password" type="password" icon="i-heroicons-lock-closed" />
        </UFormGroup>

        <div v-if="error" class="text-red-500 text-sm text-center">
            {{ error }}
        </div>
        
        <UButton type="submit" block :loading="loading">
            Sign In
        </UButton>
    </form>
  </UCard>
</template>
