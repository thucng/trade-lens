import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import type { ImportSector } from '../types/dashboard'
import { formatUsd, formatUsdAxis } from '../utils/formatters'

type TopSectorsBarChartProps = {
  sectors: ImportSector[]
}

export function TopSectorsBarChart({ sectors }: TopSectorsBarChartProps) {
  const data = sectors.slice(0, 8).map((s) => ({
    label: `HS ${s.hs2_code}`,
    sector_name: s.sector_name,
    value_usd: s.latest_import_value_usd,
  }))

  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart
        data={data}
        layout="vertical"
        margin={{ top: 8, right: 16, left: 8, bottom: 0 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
        <XAxis type="number" tickFormatter={formatUsdAxis} tick={{ fontSize: 12 }} />
        <YAxis type="category" dataKey="label" tick={{ fontSize: 12 }} width={56} />
        <Tooltip
          formatter={(value) => [formatUsd(value as number), 'Imports']}
          labelFormatter={(label, payload) =>
            payload?.[0]?.payload?.sector_name ?? label
          }
        />
        <Bar dataKey="value_usd" fill="#2563eb" radius={[0, 3, 3, 0]} />
      </BarChart>
    </ResponsiveContainer>
  )
}
