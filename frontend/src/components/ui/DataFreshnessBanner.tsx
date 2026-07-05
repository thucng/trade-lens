import { Info } from 'lucide-react'
import type { Dashboard } from '../../types/dashboard'
import { formatDate, formatYear } from '../../utils/formatters'

type DataFreshnessBannerProps = {
  freshness: Dashboard['data_freshness']
}

export function DataFreshnessBanner({ freshness }: DataFreshnessBannerProps) {
  const meta: Array<[string, string]> = [
    ['Source', freshness.source],
    ['Classification', freshness.classification],
    ['Frequency', freshness.frequency],
    ['Latest available year', formatYear(freshness.latest_available_year)],
    ['Last refreshed', formatDate(freshness.last_refreshed_at)],
  ]

  return (
    <div className="rounded-lg border border-blue-200 bg-blue-50 p-4">
      <div className="flex items-start gap-2">
        <Info className="mt-0.5 h-4 w-4 shrink-0 text-blue-600" />
        <p className="text-sm text-blue-900">
          This dashboard uses the latest available official annual trade data.
          Official trade data may lag behind the current calendar year.
        </p>
      </div>
      <dl className="mt-3 flex flex-wrap gap-x-6 gap-y-1 text-xs text-blue-800">
        {meta.map(([label, value]) => (
          <div key={label} className="flex gap-1">
            <dt className="font-medium">{label}:</dt>
            <dd>{value}</dd>
          </div>
        ))}
      </dl>
    </div>
  )
}
