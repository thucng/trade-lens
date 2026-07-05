const sections: Array<{ title: string; body: string }> = [
  {
    title: 'Data Source',
    body: 'TradeLens uses official merchandise trade data from configured public trade data sources. The MVP focuses on annual HS2-level trade data reported to UN Comtrade, with all values expressed in USD.',
  },
  {
    title: 'Latest Available Official Data',
    body: 'Official trade data may lag behind the current calendar year, so the dashboard displays the latest available official year rather than claiming transaction-level real-time coverage. Each dashboard shows its source, classification, latest available year, and last refresh time.',
  },
  {
    title: 'What HS2 Means',
    body: 'The Harmonized System (HS) is an international product classification. HS2 refers to its 2-digit chapter level (96 chapters), which groups products into broad sectors such as "84 — Machinery and mechanical appliances" or "85 — Electrical machinery and equipment".',
  },
  {
    title: 'How Trade Balance Is Calculated',
    body: 'Trade balance = total exports − total imports for the same year. A negative value indicates a trade deficit; a positive value indicates a trade surplus.',
  },
  {
    title: 'How Import CAGR Is Calculated',
    body: 'CAGR (compound annual growth rate) = (last value / first value)^(1 / number of periods) − 1. With 5 years of data there are 4 periods. If the first value is zero or missing, CAGR is shown as N/A.',
  },
  {
    title: 'How Import Demand Index Is Calculated',
    body: 'The Import Demand Index scores each HS2 sector from 0 to 100 by combining: latest import value (40%), 5-year CAGR (30%), latest-year share of total imports (20%), and data completeness (10%). Sub-scores are min-max normalized across sectors within the country.',
  },
  {
    title: 'Limitations',
    body: 'The MVP covers annual HS2 merchandise trade with the world as partner. It does not include services trade, monthly data, partner-country detail, tariffs, or forecasts. The Import Demand Index is a relative indicator within one country, not a guarantee of market opportunity.',
  },
]

export function AboutDataPage() {
  return (
    <section className="max-w-3xl">
      <h1 className="text-2xl font-semibold">About Data</h1>
      <p className="mt-2 text-slate-600">
        How TradeLens sources, processes, and presents trade data.
      </p>
      <div className="mt-6 space-y-6">
        {sections.map((s) => (
          <div key={s.title}>
            <h2 className="text-lg font-medium">{s.title}</h2>
            <p className="mt-1 text-sm leading-6 text-slate-600">{s.body}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
