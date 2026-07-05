import pytest

from app.schemas.dashboard import Dashboard
from app.services.dashboard_builder import build_dashboard
from app.services.trade_transformer import TradeRecord

COUNTRY = {"iso3": "USA", "name": "United States", "region": "North America"}
HS2_NAMES = {"85": "Electrical machinery and equipment", "84": "Machinery"}


def records(flow_values: dict[str, dict[int, float]]) -> list[TradeRecord]:
    return [
        TradeRecord(year=year, hs2_code=code, value_usd=value)
        for code, by_year in flow_values.items()
        for year, value in by_year.items()
    ]


def build_sample() -> dict:
    imports = records({
        "85": {2020: 100.0, 2021: 110.0, 2022: 120.0, 2023: 130.0, 2024: 140.0},
        "84": {2020: 200.0, 2021: 205.0, 2022: 210.0, 2023: 212.0, 2024: 215.0},
    })
    exports = records({
        "85": {2020: 400.0, 2021: 410.0, 2022: 420.0, 2023: 430.0, 2024: 440.0},
    })
    return build_dashboard(
        country=COUNTRY,
        import_records=imports,
        export_records=exports,
        hs2_names=HS2_NAMES,
        source="UN Comtrade",
        source_url="https://comtradeplus.un.org/",
        last_refreshed_at="2026-07-05T10:00:00+00:00",
    )


class TestBuildDashboard:
    def test_output_matches_schema(self):
        Dashboard(**build_sample())

    def test_period_window(self):
        period = build_sample()["period"]
        assert period == {
            "from_year": 2020,
            "to_year": 2024,
            "latest_available_year": 2024,
            "year_count": 5,
        }

    def test_summary_totals_and_balance(self):
        summary = build_sample()["summary"]
        assert summary["total_import_latest_usd"] == 355.0
        assert summary["total_export_latest_usd"] == 440.0
        assert summary["trade_balance_latest_usd"] == 85.0

    def test_top_sector_sorted_by_value(self):
        dashboard = build_sample()
        top_codes = [s["hs2_code"] for s in dashboard["top_import_sectors"]]
        assert top_codes == ["84", "85"]
        assert dashboard["summary"]["top_import_sector_code"] == "84"

    def test_fastest_growing_sorted_by_cagr(self):
        fastest = build_sample()["fastest_growing_import_sectors"]
        assert [s["hs2_code"] for s in fastest] == ["85", "84"]

    def test_yoy_growth_computed(self):
        imports = build_sample()["imports_timeseries"]
        assert imports[0]["yoy_growth"] is None
        assert imports[1]["yoy_growth"] == pytest.approx(0.05, abs=1e-3)

    def test_unknown_sector_gets_fallback_name(self):
        imports = records({"99": {2023: 10.0, 2024: 12.0}})
        dashboard = build_dashboard(
            country=COUNTRY,
            import_records=imports,
            export_records=[],
            hs2_names={},
            source="UN Comtrade",
            source_url="https://comtradeplus.un.org/",
            last_refreshed_at="2026-07-05T10:00:00+00:00",
        )
        assert dashboard["import_sectors"][0]["sector_name"] == "HS chapter 99"

    def test_no_imports_raises(self):
        with pytest.raises(ValueError):
            build_dashboard(
                country=COUNTRY,
                import_records=[],
                export_records=[],
                hs2_names={},
                source="UN Comtrade",
                source_url="https://comtradeplus.un.org/",
                last_refreshed_at="2026-07-05T10:00:00+00:00",
            )

    def test_missing_exports_year_defaults_to_zero_balance_base(self):
        dashboard = build_sample()
        balance_2020 = next(
            p for p in dashboard["trade_balance_timeseries"] if p["year"] == 2020
        )
        assert balance_2020["value_usd"] == 400.0 - 300.0
