import { apiGet } from './client'
import type { Dashboard } from '../types/dashboard'

export function getCountryDashboard(iso3: string): Promise<Dashboard> {
  return apiGet<Dashboard>(`/countries/${iso3}/dashboard?years=5`)
}
