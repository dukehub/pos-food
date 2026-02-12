import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, UserRole } from '@pos-food/core'

export const useAuthStore = defineStore('auth', () => {
    const user = ref<User | null>(null)
    const token = ref<string | null>(null)

    const isAuthenticated = computed(() => !!token.value)
    const userRole = computed(() => user.value?.role ?? null)

    function can(permission: string): boolean {
        if (!user.value) return false

        const rolePermissions: Record<UserRole, string[]> = {
            admin: ['*'],
            manager: [
                'products:read', 'products:write',
                'categories:read', 'categories:write',
                'orders:read', 'orders:write', 'orders:close',
                'tables:read', 'tables:write',
                'users:read',
                'reports:read',
            ],
            cashier: [
                'products:read',
                'categories:read',
                'orders:read', 'orders:write', 'orders:close',
                'tables:read',
            ],
            waiter: [
                'products:read',
                'categories:read',
                'orders:read', 'orders:write',
                'tables:read',
            ],
        }

        const perms = rolePermissions[user.value.role]
        return perms.includes('*') || perms.includes(permission)
    }

    function setAuth(userData: User, accessToken: string) {
        user.value = userData
        token.value = accessToken
    }

    function logout() {
        user.value = null
        token.value = null
    }

    return {
        user,
        token,
        isAuthenticated,
        userRole,
        can,
        setAuth,
        logout,
    }
})
