const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'

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

export async function apiGet<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`)

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
