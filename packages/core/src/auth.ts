import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiClient, setAuthToken, clearAuthToken } from '@pos/api'

interface User {
    id: string
    username: string
    full_name?: string
    role: string
    tenant_id: string
    permissions: string[]
}

interface AuthResponse {
    access_token: string
    token_type: string
    user: User
}

export const useAuthStore = defineStore('auth', () => {
    const user = ref<User | null>(null)
    const token = ref<string | null>(localStorage.getItem('auth_token'))

    const isAuthenticated = computed(() => !!token.value)

    // Initialize API token if present
    if (token.value) {
        setAuthToken(token.value)
    }

    async function login(username: string, password: string): Promise<boolean> {
        try {
            // For URLSearchParams (application/x-www-form-urlencoded) which is standard for OAuth2/FastAPI
            const formData = new URLSearchParams()
            formData.append('username', username)
            formData.append('password', password)

            const response = await apiClient.post<AuthResponse>('/auth/token', { username, password })

            const result = response.data
            token.value = result.access_token
            user.value = result.user

            localStorage.setItem('auth_token', result.access_token)
            setAuthToken(result.access_token)

            return true
        } catch (error) {
            console.error('Login error:', error)
            throw error
        }
    }

    function logout() {
        token.value = null
        user.value = null
        localStorage.removeItem('auth_token')
        clearAuthToken()
    }

    async function fetchUser() {
        if (!token.value) return
        try {
            const response = await apiClient.get<User>('/auth/me')
            user.value = response.data
        } catch (e) {
            logout()
        }
    }

    return {
        user,
        token,
        isAuthenticated,
        login,
        logout,
        fetchUser
    }
})
