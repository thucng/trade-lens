export type TradeTimeSeriesPoint = {
  year: number
  value_usd: number
  yoy_growth: number | null
}

export type TradeBalancePoint = {
  year: number
  value_usd: number
}

export type ImportSector = {
  hs2_code: string
  sector_name: string
  latest_import_value_usd: number
  share_of_total_imports: number
  cagr_5y: number | null
  latest_yoy_growth: number | null
  import_demand_index: number
  timeseries: Array<{
    year: number
    value_usd: number
  }>
}

export type Dashboard = {
  country: {
    iso3: string
    name: string
    region: string
  }
  period: {
    from_year: number
    to_year: number
    latest_available_year: number
    year_count: number
  }
  summary: {
    total_import_latest_usd: number
    total_export_latest_usd: number
    trade_balance_latest_usd: number
    import_cagr_5y: number | null
    export_cagr_5y: number | null
    top_import_sector_code: string | null
    top_import_sector_name: string | null
    top_import_sector_share: number | null
  }
  imports_timeseries: TradeTimeSeriesPoint[]
  exports_timeseries: TradeTimeSeriesPoint[]
  trade_balance_timeseries: TradeBalancePoint[]
  import_sectors: ImportSector[]
  top_import_sectors: ImportSector[]
  fastest_growing_import_sectors: ImportSector[]
  data_freshness: {
    source: string
    source_url: string
    frequency: string
    classification: string
    last_refreshed_at: string | null
    latest_available_year: number | null
    notes: string
  }
}
