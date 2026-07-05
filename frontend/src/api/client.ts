// Dev requests go through the Vite proxy (same origin), so no CORS is needed.
// Set VITE_API_BASE_URL to point at a remote backend in other environments.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api'

export class ApiError extends Error {
  status: number
  code: string

  constructor(status: number, code: string, message: string) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.code = code
  }
}

export function apiGet<T>(path: string): Promise<T> {
  return request<T>(path)
}

export function apiPost<T>(path: string): Promise<T> {
  return request<T>(path, { method: 'POST' })
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, init)

  if (!response.ok) {
    let code = 'UNKNOWN_ERROR'
    let message = `Request failed with status ${response.status}.`
    try {
      const body = await response.json()
      if (body?.detail?.code) {
        code = body.detail.code
        message = body.detail.message
      }
    } catch {
      // Non-JSON error body; keep defaults.
    }
    throw new ApiError(response.status, code, message)
  }

  return response.json() as Promise<T>
}
