/**
 * Lightweight fetch-based HTTP client with auth interceptor and error handling.
 *
 * Uses native fetch — no external dependency needed.
 */

export interface ApiError {
  status: number
  message: string
  detail?: unknown
}

export interface ApiResponse<T = unknown> {
  data: T
  status: number
}

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api'

let authToken: string | null = null

export function setAuthToken(token: string): void {
  authToken = token
}

export function clearAuthToken(): void {
  authToken = null
}

async function request<T>(
  method: string,
  path: string,
  body?: unknown
): Promise<ApiResponse<T>> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    Accept: 'application/json'
  }

  if (authToken) {
    headers['Authorization'] = `Bearer ${authToken}`
  }

  const response = await fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined
  })

  if (!response.ok) {
    const error: ApiError = {
      status: response.status,
      message: response.statusText
    }

    try {
      error.detail = await response.json()
    } catch {
      // body is not JSON
    }

    throw error
  }

  const data = (await response.json()) as T
  return { data, status: response.status }
}

export const apiClient = {
  get: <T>(path: string) => request<T>('GET', path),
  post: <T>(path: string, body?: unknown) => request<T>('POST', path, body),
  put: <T>(path: string, body?: unknown) => request<T>('PUT', path, body),
  patch: <T>(path: string, body?: unknown) => request<T>('PATCH', path, body),
  delete: <T>(path: string) => request<T>('DELETE', path)
}
