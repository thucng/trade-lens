import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import type { TradeTimeSeriesPoint } from '../types/dashboard'
import { formatUsd, formatUsdAxis } from '../utils/formatters'

type ImportTrendChartProps = {
  data: TradeTimeSeriesPoint[]
}

export function ImportTrendChart({ data }: ImportTrendChartProps) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <AreaChart data={data} margin={{ top: 8, right: 8, left: 8, bottom: 0 }}>
        <defs>
          <linearGradient id="importFill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#2563eb" stopOpacity={0.25} />
            <stop offset="100%" stopColor="#2563eb" stopOpacity={0.02} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
        <XAxis dataKey="year" tick={{ fontSize: 12 }} />
        <YAxis tickFormatter={formatUsdAxis} tick={{ fontSize: 12 }} width={64} />
        <Tooltip
          formatter={(value) => [formatUsd(value as number), 'Imports']}
        />
        <Area
          type="monotone"
          dataKey="value_usd"
          stroke="#2563eb"
          strokeWidth={2}
          fill="url(#importFill)"
        />
      </AreaChart>
    </ResponsiveContainer>
  )
}
