import { Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts'
import type { ImportSector } from '../types/dashboard'
import { formatUsd } from '../utils/formatters'

const COLORS = [
  '#2563eb',
  '#10b981',
  '#f59e0b',
  '#8b5cf6',
  '#ec4899',
  '#14b8a6',
  '#f97316',
  '#6366f1',
  '#94a3b8', // Other
]

type ImportSectorDonutChartProps = {
  sectors: ImportSector[]
  totalImports: number
}

export function ImportSectorDonutChart({
  sectors,
  totalImports,
}: ImportSectorDonutChartProps) {
  const sorted = [...sectors].sort(
    (a, b) => b.latest_import_value_usd - a.latest_import_value_usd,
  )
  const top = sorted.slice(0, 8)
  const shownTotal = top.reduce((sum, s) => sum + s.latest_import_value_usd, 0)
  const otherValue = Math.max(totalImports - shownTotal, 0)

  const data = [
    ...top.map((s) => ({ name: s.sector_name, value: s.latest_import_value_usd })),
    ...(otherValue > 0 ? [{ name: 'Other', value: otherValue }] : []),
  ]

  return (
    <ResponsiveContainer width="100%" height="100%">
      <PieChart>
        <Pie
          data={data}
          dataKey="value"
          nameKey="name"
          innerRadius="55%"
          outerRadius="80%"
          paddingAngle={1}
        >
          {data.map((entry, index) => (
            <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip formatter={(value) => formatUsd(value as number)} />
        <Legend
          layout="vertical"
          align="right"
          verticalAlign="middle"
          wrapperStyle={{ fontSize: 11, maxWidth: '45%' }}
        />
      </PieChart>
    </ResponsiveContainer>
  )
}
