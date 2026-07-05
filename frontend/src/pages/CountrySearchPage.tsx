import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Search } from 'lucide-react'
import { getCountries } from '../api/countries'
import { LoadingState } from '../components/ui/LoadingState'
import { ErrorState } from '../components/ui/ErrorState'
import { EmptyState } from '../components/ui/EmptyState'
import type { Country } from '../types/country'

function StatusBadge({ cached }: { cached: boolean }) {
  return cached ? (
    <span className="rounded-full bg-emerald-100 px-2 py-0.5 text-xs font-medium text-emerald-700">
      Ready
    </span>
  ) : (
    <span className="rounded-full bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-500">
      Not cached
    </span>
  )
}

function CountryCard({ country }: { country: Country }) {
  const body = (
    <div className="flex h-full flex-col rounded-lg border border-slate-200 bg-white p-4 shadow-sm transition group-hover:border-blue-300 group-hover:shadow">
      <div className="flex items-start justify-between gap-2">
        <div>
          <p className="font-semibold">{country.name}</p>
          <p className="text-sm text-slate-500">
            {country.region} · <span className="font-mono">{country.iso3}</span>
          </p>
        </div>
        <StatusBadge cached={country.is_cached} />
      </div>
      <p className="mt-3 text-sm">
        {country.is_cached ? (
          <span className="font-medium text-blue-600">Open dashboard →</span>
        ) : (
          <span className="text-slate-400">Data is not prepared yet — open to refresh</span>
        )}
      </p>
    </div>
  )

  return (
    <Link to={`/countries/${country.iso3}`} className="group block h-full">
      {body}
    </Link>
  )
}

export function CountrySearchPage() {
  const [search, setSearch] = useState('')
  const { data, isPending, isError, error, refetch } = useQuery({
    queryKey: ['countries'],
    queryFn: getCountries,
  })

  const filtered = useMemo(() => {
    if (!data) return []
    const q = search.trim().toLowerCase()
    if (!q) return data
    return data.filter(
      (c) =>
        c.name.toLowerCase().includes(q) ||
        c.iso3.toLowerCase().includes(q) ||
        c.region.toLowerCase().includes(q),
    )
  }, [data, search])

  if (isPending) return <LoadingState message="Loading countries…" />
  if (isError) {
    return (
      <ErrorState
        title="Could not load countries"
        message={error.message}
        onRetry={() => refetch()}
      />
    )
  }

  return (
    <section>
      <h1 className="text-2xl font-semibold">Countries</h1>
      <p className="mt-1 text-slate-600">
        Search a country to explore its import/export overview.
      </p>

      <div className="relative mt-4 max-w-md">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
        <input
          type="search"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search countries by name, ISO3, or region"
          className="w-full rounded-md border border-slate-300 bg-white py-2 pl-9 pr-3 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
        />
      </div>

      {filtered.length === 0 ? (
        <EmptyState
          title="No countries match your search"
          message="Try a different name, ISO3 code, or region."
        />
      ) : (
        <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {filtered.map((country) => (
            <CountryCard key={country.iso3} country={country} />
          ))}
        </div>
      )}
    </section>
  )
}
