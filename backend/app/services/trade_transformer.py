"""Normalization and calculation utilities for trade data."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TradeRecord:
    year: int
    hs2_code: str
    value_usd: float


def calculate_yoy_growth(current: float, previous: float) -> float | None:
    if previous <= 0:
        return None
    return (current - previous) / previous


def calculate_cagr(first: float, last: float, periods: int) -> float | None:
    if first <= 0 or last < 0 or periods <= 0:
        return None
    return (last / first) ** (1 / periods) - 1


def calculate_trade_balance(exports: float, imports: float) -> float:
    return exports - imports


def calculate_sector_share(sector_value: float, total_value: float) -> float | None:
    if total_value <= 0:
        return None
    return sector_value / total_value


def min_max_scores(values: list[float | None]) -> list[float | None]:
    """Min-max normalize to 0-100, ignoring None entries (kept as None)."""
    present = [v for v in values if v is not None]
    if not present:
        return list(values)
    lo, hi = min(present), max(present)
    if hi == lo:
        return [50.0 if v is not None else None for v in values]
    return [
        (v - lo) / (hi - lo) * 100 if v is not None else None for v in values
    ]


def normalize_comtrade_records(raw: dict) -> list[TradeRecord]:
    """Extract HS2 records from a raw Comtrade response.

    Keeps only 2-digit commodity chapters (drops TOTAL and any deeper
    aggregation levels) and rows with a usable primary value.
    """
    records: list[TradeRecord] = []
    for row in raw.get("data", []):
        cmd_code = str(row.get("cmdCode", ""))
        if len(cmd_code) != 2 or not cmd_code.isdigit():
            continue
        year = row.get("refYear")
        value = row.get("primaryValue")
        if year is None or value is None:
            continue
        records.append(TradeRecord(year=int(year), hs2_code=cmd_code, value_usd=float(value)))
    return records


def totals_by_year(records: list[TradeRecord]) -> dict[int, float]:
    totals: dict[int, float] = {}
    for record in records:
        totals[record.year] = totals.get(record.year, 0.0) + record.value_usd
    return totals


def sector_values_by_year(records: list[TradeRecord]) -> dict[str, dict[int, float]]:
    sectors: dict[str, dict[int, float]] = {}
    for record in records:
        years = sectors.setdefault(record.hs2_code, {})
        years[record.year] = years.get(record.year, 0.0) + record.value_usd
    return sectors
