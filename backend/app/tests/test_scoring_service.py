from app.services.scoring_service import SectorStats, compute_import_demand_indexes


def make_stats(code, value, cagr, share, years=5):
    return SectorStats(
        hs2_code=code,
        latest_value_usd=value,
        cagr=cagr,
        share=share,
        available_year_count=years,
    )


class TestImportDemandIndex:
    def test_empty_sectors(self):
        assert compute_import_demand_indexes([], 5) == {}

    def test_best_sector_scores_100(self):
        sectors = [
            make_stats("85", 100.0, 0.10, 0.5),
            make_stats("01", 10.0, 0.01, 0.05),
        ]
        indexes = compute_import_demand_indexes(sectors, 5)
        assert indexes["85"] == 100.0
        # Worst sector still gets completeness credit (10% * 100).
        assert indexes["01"] == 10.0

    def test_missing_cagr_contributes_zero(self):
        sectors = [
            make_stats("85", 100.0, None, 0.5),
            make_stats("01", 10.0, 0.05, 0.05),
        ]
        indexes = compute_import_demand_indexes(sectors, 5)
        # 85 loses the full 30% CAGR weight despite having the top value/share.
        assert indexes["85"] == 70.0

    def test_incomplete_years_reduce_score(self):
        full = make_stats("85", 100.0, 0.10, 0.5, years=5)
        partial = make_stats("84", 100.0, 0.10, 0.5, years=2)
        indexes = compute_import_demand_indexes([full, partial], 5)
        # Identical stats normalize to 50 each; only completeness differs.
        assert indexes["85"] - indexes["84"] == 6.0

    def test_clamped_between_0_and_100(self):
        sectors = [make_stats("85", 100.0, 0.10, 0.5)]
        indexes = compute_import_demand_indexes(sectors, 5)
        assert 0 <= indexes["85"] <= 100
