import { useParams } from 'react-router-dom'

export function CountryDashboardPage() {
  const { iso3 } = useParams<{ iso3: string }>()

  return (
    <section>
      <h1 className="text-2xl font-semibold">Country Dashboard</h1>
      <p className="mt-2 text-slate-600">
        Dashboard for <span className="font-mono">{iso3}</span> will appear here.
      </p>
    </section>
  )
}
