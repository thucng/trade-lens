from pydantic import BaseModel


class CountryRef(BaseModel):
    iso3: str
    name: str
    region: str


class Period(BaseModel):
    from_year: int
    to_year: int
    latest_available_year: int
    year_count: int


class Summary(BaseModel):
    total_import_latest_usd: float
    total_export_latest_usd: float
    trade_balance_latest_usd: float
    import_cagr_5y: float | None
    export_cagr_5y: float | None
    top_import_sector_code: str | None
    top_import_sector_name: str | None
    top_import_sector_share: float | None


class TradeTimeSeriesPoint(BaseModel):
    year: int
    value_usd: float
    yoy_growth: float | None


class TradeBalancePoint(BaseModel):
    year: int
    value_usd: float


class SectorTimeSeriesPoint(BaseModel):
    year: int
    value_usd: float


class ImportSector(BaseModel):
    hs2_code: str
    sector_name: str
    latest_import_value_usd: float
    share_of_total_imports: float
    cagr_5y: float | None
    latest_yoy_growth: float | None
    import_demand_index: float
    timeseries: list[SectorTimeSeriesPoint]


class DataFreshness(BaseModel):
    source: str
    source_url: str
    frequency: str
    classification: str
    last_refreshed_at: str | None
    latest_available_year: int | None
    notes: str


class Dashboard(BaseModel):
    country: CountryRef
    period: Period
    summary: Summary
    imports_timeseries: list[TradeTimeSeriesPoint]
    exports_timeseries: list[TradeTimeSeriesPoint]
    trade_balance_timeseries: list[TradeBalancePoint]
    import_sectors: list[ImportSector]
    top_import_sectors: list[ImportSector]
    fastest_growing_import_sectors: list[ImportSector]
    data_freshness: DataFreshness
