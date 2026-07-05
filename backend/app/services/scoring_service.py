"""Import Demand Index scoring."""

from dataclasses import dataclass

from app.services.trade_transformer import min_max_scores

WEIGHT_VALUE = 0.40
WEIGHT_CAGR = 0.30
WEIGHT_SHARE = 0.20
WEIGHT_COMPLETENESS = 0.10


@dataclass(frozen=True)
class SectorStats:
    hs2_code: str
    latest_value_usd: float
    cagr: float | None
    share: float | None
    available_year_count: int


def compute_import_demand_indexes(
    sectors: list[SectorStats],
    expected_year_count: int,
) -> dict[str, float]:
    """Score each sector 0-100 using min-max normalization across sectors.

    Missing CAGR or share contributes 0 to the weighted sum. Data
    completeness is the fraction of expected years with data.
    """
    if not sectors:
        return {}

    value_scores = min_max_scores([s.latest_value_usd for s in sectors])
    cagr_scores = min_max_scores([s.cagr for s in sectors])
    share_scores = min_max_scores([s.share for s in sectors])

    indexes: dict[str, float] = {}
    for i, sector in enumerate(sectors):
        completeness = (
            sector.available_year_count / expected_year_count * 100
            if expected_year_count > 0
            else 0.0
        )
        index = (
            WEIGHT_VALUE * (value_scores[i] or 0.0)
            + WEIGHT_CAGR * (cagr_scores[i] or 0.0)
            + WEIGHT_SHARE * (share_scores[i] or 0.0)
            + WEIGHT_COMPLETENESS * completeness
        )
        indexes[sector.hs2_code] = round(min(max(index, 0.0), 100.0), 1)
    return indexes
