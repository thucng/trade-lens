import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import type { TradeBalancePoint } from '../types/dashboard'
import { formatUsd, formatUsdAxis } from '../utils/formatters'

type TradeBalanceChartProps = {
  data: TradeBalancePoint[]
}

export function TradeBalanceChart({ data }: TradeBalanceChartProps) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data} margin={{ top: 8, right: 8, left: 8, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
        <XAxis dataKey="year" tick={{ fontSize: 12 }} />
        <YAxis tickFormatter={formatUsdAxis} tick={{ fontSize: 12 }} width={64} />
        <Tooltip
          formatter={(value) => [formatUsd(value as number), 'Trade balance']}
        />
        <ReferenceLine y={0} stroke="#94a3b8" />
        <Bar dataKey="value_usd" radius={[3, 3, 0, 0]}>
          {data.map((point) => (
            <Cell
              key={point.year}
              fill={point.value_usd < 0 ? '#f43f5e' : '#10b981'}
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
