"""Combine normalized trade records into the processed dashboard JSON."""

from app.services.scoring_service import SectorStats, compute_import_demand_indexes
from app.services.trade_transformer import (
    TradeRecord,
    calculate_cagr,
    calculate_sector_share,
    calculate_trade_balance,
    calculate_yoy_growth,
    sector_values_by_year,
    totals_by_year,
)

FRESHNESS_NOTES = "Official trade data may lag behind the current calendar year."


def _timeseries_with_yoy(values_by_year: dict[int, float], years: list[int]) -> list[dict]:
    points = []
    previous: float | None = None
    for year in years:
        value = values_by_year.get(year)
        if value is None:
            previous = None
            continue
        yoy = calculate_yoy_growth(value, previous) if previous is not None else None
        points.append({
            "year": year,
            "value_usd": value,
            "yoy_growth": round(yoy, 4) if yoy is not None else None,
        })
        previous = value
    return points


def _window_cagr(values_by_year: dict[int, float], years: list[int]) -> float | None:
    present = [y for y in years if y in values_by_year]
    if len(present) < 2:
        return None
    first_year, last_year = present[0], present[-1]
    cagr = calculate_cagr(
        values_by_year[first_year],
        values_by_year[last_year],
        last_year - first_year,
    )
    return round(cagr, 4) if cagr is not None else None


def build_dashboard(
    *,
    country: dict,
    import_records: list[TradeRecord],
    export_records: list[TradeRecord],
    hs2_names: dict[str, str],
    source: str,
    source_url: str,
    last_refreshed_at: str,
    year_window: int = 5,
) -> dict:
    import_totals = totals_by_year(import_records)
    export_totals = totals_by_year(export_records)

    if not import_totals:
        raise ValueError("No import records available to build a dashboard.")

    latest_year = max(import_totals)
    years = list(range(latest_year - year_window + 1, latest_year + 1))

    # --- sectors ---
    sectors_by_code = sector_values_by_year(import_records)
    total_latest = import_totals[latest_year]

    stats: list[SectorStats] = []
    for code, values in sorted(sectors_by_code.items()):
        latest_value = values.get(latest_year)
        if latest_value is None:
            continue
        stats.append(SectorStats(
            hs2_code=code,
            latest_value_usd=latest_value,
            cagr=_window_cagr(values, years),
            share=calculate_sector_share(latest_value, total_latest),
            available_year_count=sum(1 for y in years if y in values),
        ))

    indexes = compute_import_demand_indexes(stats, expected_year_count=year_window)

    import_sectors = []
    for s in stats:
        values = sectors_by_code[s.hs2_code]
        previous = values.get(latest_year - 1)
        yoy = (
            calculate_yoy_growth(s.latest_value_usd, previous)
            if previous is not None
            else None
        )
        import_sectors.append({
            "hs2_code": s.hs2_code,
            "sector_name": hs2_names.get(s.hs2_code, f"HS chapter {s.hs2_code}"),
            "latest_import_value_usd": s.latest_value_usd,
            "share_of_total_imports": round(s.share, 4) if s.share is not None else 0.0,
            "cagr_5y": s.cagr,
            "latest_yoy_growth": round(yoy, 4) if yoy is not None else None,
            "import_demand_index": indexes[s.hs2_code],
            "timeseries": [
                {"year": y, "value_usd": values[y]} for y in years if y in values
            ],
        })

    top_import_sectors = sorted(
        import_sectors, key=lambda s: s["latest_import_value_usd"], reverse=True,
    )
    fastest_growing = sorted(
        (s for s in import_sectors if s["cagr_5y"] is not None),
        key=lambda s: s["cagr_5y"],
        reverse=True,
    )[:10]

    # --- summary ---
    top = top_import_sectors[0] if top_import_sectors else None
    export_latest = export_totals.get(latest_year)

    return {
        "country": {
            "iso3": country["iso3"],
            "name": country["name"],
            "region": country["region"],
        },
        "period": {
            "from_year": years[0],
            "to_year": latest_year,
            "latest_available_year": latest_year,
            "year_count": year_window,
        },
        "summary": {
            "total_import_latest_usd": import_totals[latest_year],
            "total_export_latest_usd": export_latest if export_latest is not None else 0.0,
            "trade_balance_latest_usd": calculate_trade_balance(
                export_latest or 0.0, import_totals[latest_year],
            ),
            "import_cagr_5y": _window_cagr(import_totals, years),
            "export_cagr_5y": _window_cagr(export_totals, years),
            "top_import_sector_code": top["hs2_code"] if top else None,
            "top_import_sector_name": top["sector_name"] if top else None,
            "top_import_sector_share": top["share_of_total_imports"] if top else None,
        },
        "imports_timeseries": _timeseries_with_yoy(import_totals, years),
        "exports_timeseries": _timeseries_with_yoy(export_totals, years),
        "trade_balance_timeseries": [
            {
                "year": y,
                "value_usd": calculate_trade_balance(
                    export_totals.get(y, 0.0), import_totals[y],
                ),
            }
            for y in years
            if y in import_totals
        ],
        "import_sectors": import_sectors,
        "top_import_sectors": top_import_sectors,
        "fastest_growing_import_sectors": fastest_growing,
        "data_freshness": {
            "source": source,
            "source_url": source_url,
            "frequency": "Annual",
            "classification": "HS2",
            "last_refreshed_at": last_refreshed_at,
            "latest_available_year": latest_year,
            "notes": FRESHNESS_NOTES,
        },
    }
