import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import type { TradeTimeSeriesPoint } from '../types/dashboard'
import { formatUsd, formatUsdAxis } from '../utils/formatters'

type ExportImportChartProps = {
  imports: TradeTimeSeriesPoint[]
  exports: TradeTimeSeriesPoint[]
}

export function ExportImportChart({ imports, exports: exportsData }: ExportImportChartProps) {
  const data = imports.map((point) => ({
    year: point.year,
    imports_usd: point.value_usd,
    exports_usd: exportsData.find((e) => e.year === point.year)?.value_usd ?? null,
  }))

  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data} margin={{ top: 8, right: 8, left: 8, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
        <XAxis dataKey="year" tick={{ fontSize: 12 }} />
        <YAxis tickFormatter={formatUsdAxis} tick={{ fontSize: 12 }} width={64} />
        <Tooltip formatter={(value) => formatUsd(value as number)} />
        <Legend />
        <Bar dataKey="imports_usd" name="Imports" fill="#2563eb" radius={[3, 3, 0, 0]} />
        <Bar dataKey="exports_usd" name="Exports" fill="#10b981" radius={[3, 3, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  )
}
