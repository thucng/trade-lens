import { apiPost } from './client'

export type RefreshResponse = {
  iso3: string
  status: string
  message: string
  latest_available_year: number
  last_refreshed_at: string
}

export function refreshCountry(iso3: string): Promise<RefreshResponse> {
  return apiPost<RefreshResponse>(`/countries/${iso3}/refresh`)
}
