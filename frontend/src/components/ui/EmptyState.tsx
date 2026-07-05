import { Database } from 'lucide-react'
import type { ReactNode } from 'react'

type EmptyStateProps = {
  title: string
  message?: string
  action?: ReactNode
}

export function EmptyState({ title, message, action }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-16 text-center">
      <Database className="h-8 w-8 text-slate-400" />
      <p className="text-lg font-medium">{title}</p>
      {message ? (
        <p className="max-w-md text-sm text-slate-500">{message}</p>
      ) : null}
      {action}
    </div>
  )
}
