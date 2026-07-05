const USD_UNITS: Array<[number, string]> = [
  [1e12, 'T'],
  [1e9, 'B'],
  [1e6, 'M'],
  [1e3, 'K'],
]

export function formatUsd(value: number | null): string {
  if (value === null) return 'N/A'
  const sign = value < 0 ? '-' : ''
  const abs = Math.abs(value)
  for (const [unit, suffix] of USD_UNITS) {
    if (abs >= unit) {
      return `${sign}$${(abs / unit).toFixed(2)}${suffix}`
    }
  }
  return `${sign}$${abs.toFixed(0)}`
}

/** Compact form for chart axes, e.g. $3.2T, $576B. */
export function formatUsdAxis(value: number): string {
  const sign = value < 0 ? '-' : ''
  const abs = Math.abs(value)
  for (const [unit, suffix] of USD_UNITS) {
    if (abs >= unit) {
      const scaled = abs / unit
      return `${sign}$${scaled >= 100 ? scaled.toFixed(0) : scaled.toFixed(1)}${suffix}`
    }
  }
  return `${sign}$${abs.toFixed(0)}`
}

export function formatPercent(value: number | null, digits = 1): string {
  if (value === null) return 'N/A'
  return `${(value * 100).toFixed(digits)}%`
}

export function formatNumber(value: number | null): string {
  if (value === null) return 'N/A'
  return new Intl.NumberFormat('en-US').format(value)
}

export function formatYear(value: number | null): string {
  if (value === null) return 'N/A'
  return String(value)
}

export function formatDate(iso: string | null): string {
  if (!iso) return 'N/A'
  return new Date(iso).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}
