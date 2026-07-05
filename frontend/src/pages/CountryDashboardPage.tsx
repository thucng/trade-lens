import { Link, useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { ArrowLeft } from 'lucide-react'
import { getCountryDashboard } from '../api/dashboard'
import { ApiError } from '../api/client'
import { LoadingState } from '../components/ui/LoadingState'
import { ErrorState } from '../components/ui/ErrorState'
import { EmptyState } from '../components/ui/EmptyState'
import { KpiCard } from '../components/ui/KpiCard'
import { DataFreshnessBanner } from '../components/ui/DataFreshnessBanner'
import { ChartCard } from '../charts/ChartCard'
import { ImportTrendChart } from '../charts/ImportTrendChart'
import { ExportImportChart } from '../charts/ExportImportChart'
import { TradeBalanceChart } from '../charts/TradeBalanceChart'
import { ImportSectorDonutChart } from '../charts/ImportSectorDonutChart'
import { TopSectorsBarChart } from '../charts/TopSectorsBarChart'
import type { ImportSector } from '../types/dashboard'
import { formatPercent, formatUsd, formatYear } from '../utils/formatters'

function FastestGrowingTable({ sectors }: { sectors: ImportSector[] }) {
  if (sectors.length === 0) {
    return (
      <p className="py-6 text-center text-sm text-slate-500">
        No sector-level import data is available for this country and period.
      </p>
    )
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-slate-200 text-left text-xs uppercase tracking-wide text-slate-500">
            <th className="py-2 pr-4">HS2</th>
            <th className="py-2 pr-4">Sector</th>
            <th className="py-2 pr-4 text-right">Latest imports</th>
            <th className="py-2 pr-4 text-right">CAGR (5y)</th>
            <th className="py-2 pr-4 text-right">YoY</th>
            <th className="py-2 text-right">Demand index</th>
          </tr>
        </thead>
        <tbody>
          {sectors.map((s) => (
            <tr key={s.hs2_code} className="border-b border-slate-100">
              <td className="py-2 pr-4 font-mono">{s.hs2_code}</td>
              <td className="py-2 pr-4">{s.sector_name}</td>
              <td className="py-2 pr-4 text-right">
                {formatUsd(s.latest_import_value_usd)}
              </td>
              <td className="py-2 pr-4 text-right">{formatPercent(s.cagr_5y)}</td>
              <td className="py-2 pr-4 text-right">
                {formatPercent(s.latest_yoy_growth)}
              </td>
              <td className="py-2 text-right">{s.import_demand_index.toFixed(1)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export function CountryDashboardPage() {
  const { iso3 = '' } = useParams<{ iso3: string }>()
  const { data, isPending, isError, error, refetch } = useQuery({
    queryKey: ['dashboard', iso3],
    queryFn: () => getCountryDashboard(iso3),
    retry: (failureCount, err) =>
      !(err instanceof ApiError && err.status === 404) && failureCount < 2,
  })

  if (isPending) return <LoadingState message="Loading dashboard…" />

  if (isError) {
    if (error instanceof ApiError && error.code === 'COUNTRY_NOT_CACHED') {
      return (
        <EmptyState
          title="Dashboard data is not cached yet."
          message="This country is available in the search index, but its dashboard data has not been prepared. Refresh data to generate the dashboard."
          action={
            <Link to="/countries" className="mt-2 text-sm font-medium text-blue-600">
              ← Back to countries
            </Link>
          }
        />
      )
    }
    return (
      <ErrorState
        title="Something went wrong while loading this dashboard."
        message={error.message}
        onRetry={() => refetch()}
      />
    )
  }

  const { country, period, summary, data_freshness } = data

  return (
    <section className="space-y-6">
      <div>
        <Link
          to="/countries"
          className="inline-flex items-center gap-1 text-sm text-slate-500 hover:text-slate-900"
        >
          <ArrowLeft className="h-4 w-4" /> Countries
        </Link>
        <div className="mt-2 flex flex-wrap items-baseline gap-x-3 gap-y-1">
          <h1 className="text-2xl font-semibold">{country.name}</h1>
          <span className="font-mono text-sm text-slate-500">{country.iso3}</span>
          <span className="text-sm text-slate-500">{country.region}</span>
        </div>
        <p className="mt-1 text-sm text-slate-600">
          Import demand overview · {period.from_year}–{period.to_year}
        </p>
      </div>

      <DataFreshnessBanner freshness={data_freshness} />

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <KpiCard
          label="Total Imports"
          value={formatUsd(summary.total_import_latest_usd)}
          hint={`Latest year (${formatYear(period.latest_available_year)})`}
        />
        <KpiCard
          label="Total Exports"
          value={formatUsd(summary.total_export_latest_usd)}
          hint={`Latest year (${formatYear(period.latest_available_year)})`}
        />
        <KpiCard
          label="Trade Balance"
          value={formatUsd(summary.trade_balance_latest_usd)}
          hint={summary.trade_balance_latest_usd < 0 ? 'Trade deficit' : 'Trade surplus'}
        />
        <KpiCard
          label="Import CAGR (5y)"
          value={formatPercent(summary.import_cagr_5y)}
          hint={`Exports: ${formatPercent(summary.export_cagr_5y)}`}
        />
        <KpiCard
          label="Top Import Sector"
          value={summary.top_import_sector_name ?? 'N/A'}
          hint={
            summary.top_import_sector_share !== null
              ? `${formatPercent(summary.top_import_sector_share)} of total imports`
              : undefined
          }
        />
        <KpiCard
          label="Latest Available Year"
          value={formatYear(period.latest_available_year)}
          hint={`${period.year_count} years of data`}
        />
      </div>

      <ChartCard title="Import Trend">
        <ImportTrendChart data={data.imports_timeseries} />
      </ChartCard>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <ChartCard title="Exports vs Imports">
          <ExportImportChart
            imports={data.imports_timeseries}
            exports={data.exports_timeseries}
          />
        </ChartCard>
        <ChartCard title="Trade Balance">
          <TradeBalanceChart data={data.trade_balance_timeseries} />
        </ChartCard>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <ChartCard title="Import Structure (latest year)">
          <ImportSectorDonutChart
            sectors={data.import_sectors}
            totalImports={summary.total_import_latest_usd}
          />
        </ChartCard>
        <ChartCard title="Top Imported Sectors">
          <TopSectorsBarChart sectors={data.top_import_sectors} />
        </ChartCard>
      </div>

      <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <h2 className="mb-3 text-sm font-semibold text-slate-700">
          Fastest Growing Import Sectors
        </h2>
        <FastestGrowingTable sectors={data.fastest_growing_import_sectors} />
      </div>

      <div className="rounded-lg border border-slate-200 bg-slate-100 p-4 text-xs text-slate-600">
        <p className="font-medium text-slate-700">Methodology</p>
        <p className="mt-1">
          Values are merchandise trade in USD from {data_freshness.source} at the{' '}
          {data_freshness.classification} classification level. CAGR is computed
          over the {period.year_count}-year window. The Import Demand Index
          combines latest import value (40%), 5-year CAGR (30%), sector share
          (20%), and data completeness (10%), normalized to 0–100. See{' '}
          <Link to="/about-data" className="text-blue-600 underline">
            About Data
          </Link>{' '}
          for details.
        </p>
      </div>
    </section>
  )
}
