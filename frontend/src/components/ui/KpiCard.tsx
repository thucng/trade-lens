import type { ReactNode } from 'react'

type KpiCardProps = {
  label: string
  value: string
  hint?: string
  icon?: ReactNode
}

export function KpiCard({ label, value, hint, icon }: KpiCardProps) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-500">{label}</p>
        {icon}
      </div>
      <p className="mt-1 truncate text-2xl font-semibold" title={value}>
        {value}
      </p>
      {hint ? <p className="mt-1 text-xs text-slate-500">{hint}</p> : null}
    </div>
  )
}
