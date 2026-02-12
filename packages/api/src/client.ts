/**
 * @pos-food/api
 * Typed HTTP client with auth, error normalization, and retry.
 */

export interface ApiError {
    code: 'VALIDATION_ERROR' | 'UNAUTHORIZED' | 'FORBIDDEN' | 'NOT_FOUND' | 'CONFLICT' | 'SERVER_ERROR' | 'NETWORK_ERROR' | 'TIMEOUT' | 'UNKNOWN'
    message: string
    fieldErrors?: Record<string, string>
    status?: number
}

export interface ApiClientConfig {
    baseUrl: string
    getAccessToken?: () => string | null
    onUnauthorized?: () => void
    timeout?: number
}

function normalizeError(error: unknown, status?: number): ApiError {
    if (error instanceof Error) {
        if (error.name === 'AbortError') {
            return { code: 'TIMEOUT', message: 'errors.timeout' }
        }
        if (error.message.includes('fetch')) {
            return { code: 'NETWORK_ERROR', message: 'errors.network' }
        }
    }

    if (status) {
        if (status === 401) return { code: 'UNAUTHORIZED', message: 'errors.unauthorized', status }
        if (status === 403) return { code: 'FORBIDDEN', message: 'errors.forbidden', status }
        if (status === 404) return { code: 'NOT_FOUND', message: 'errors.not_found', status }
        if (status === 409) return { code: 'CONFLICT', message: 'errors.conflict', status }
        if (status === 422) return { code: 'VALIDATION_ERROR', message: 'errors.validation', status }
        if (status >= 500) return { code: 'SERVER_ERROR', message: 'errors.server_unavailable', status }
    }

    return { code: 'UNKNOWN', message: 'errors.unknown' }
}

export function createApiClient(config: ApiClientConfig) {
    const { baseUrl, getAccessToken, onUnauthorized, timeout = 10000 } = config

    async function request<T>(
        method: string,
        path: string,
        options?: {
            body?: unknown
            params?: Record<string, string>
            signal?: AbortSignal
        },
    ): Promise<{ data: T | null; error: ApiError | null }> {
        const url = new URL(path, baseUrl)

        if (options?.params) {
            for (const [key, value] of Object.entries(options.params)) {
                url.searchParams.set(key, value)
            }
        }

        const headers: Record<string, string> = {
            'Content-Type': 'application/json',
        }

        const token = getAccessToken?.()
        if (token) {
            headers['Authorization'] = `Bearer ${token}`
        }

        const controller = new AbortController()
        const timeoutId = setTimeout(() => controller.abort(), timeout)

        try {
            const response = await fetch(url.toString(), {
                method,
                headers,
                body: options?.body ? JSON.stringify(options.body) : undefined,
                signal: options?.signal ?? controller.signal,
            })

            clearTimeout(timeoutId)

            if (!response.ok) {
                if (response.status === 401) {
                    onUnauthorized?.()
                }

                let errorBody: Record<string, unknown> = {}
                try {
                    errorBody = await response.json() as Record<string, unknown>
                }
                catch {
                    // ignore parse errors
                }

                const error = normalizeError(null, response.status)
                if (errorBody['message'] && typeof errorBody['message'] === 'string') {
                    error.message = errorBody['message']
                }
                if (errorBody['fieldErrors'] && typeof errorBody['fieldErrors'] === 'object') {
                    error.fieldErrors = errorBody['fieldErrors'] as Record<string, string>
                }

                return { data: null, error }
            }

            const data = (await response.json()) as T
            return { data, error: null }
        }
        catch (err) {
            clearTimeout(timeoutId)
            return { data: null, error: normalizeError(err) }
        }
    }

    return {
        get<T>(path: string, params?: Record<string, string>) {
            return request<T>('GET', path, { params })
        },
        post<T>(path: string, body?: unknown) {
            return request<T>('POST', path, { body })
        },
        put<T>(path: string, body?: unknown) {
            return request<T>('PUT', path, { body })
        },
        patch<T>(path: string, body?: unknown) {
            return request<T>('PATCH', path, { body })
        },
        delete<T>(path: string) {
            return request<T>('DELETE', path)
        },
    }
}

export type ApiClient = ReturnType<typeof createApiClient>
