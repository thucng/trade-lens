import { apiGet } from './client'
import type { Country } from '../types/country'

export function getCountries(): Promise<Country[]> {
  return apiGet<Country[]>('/countries')
}

export function getCountry(iso3: string): Promise<Country> {
  return apiGet<Country>(`/countries/${iso3}`)
}
