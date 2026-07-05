import pytest

from app.services.trade_transformer import (
    TradeRecord,
    calculate_cagr,
    calculate_sector_share,
    calculate_trade_balance,
    calculate_yoy_growth,
    min_max_scores,
    normalize_comtrade_records,
    sector_values_by_year,
    totals_by_year,
)


class TestYoyGrowth:
    def test_positive_growth(self):
        assert calculate_yoy_growth(110, 100) == pytest.approx(0.1)

    def test_negative_growth(self):
        assert calculate_yoy_growth(90, 100) == pytest.approx(-0.1)

    def test_zero_previous_returns_none(self):
        assert calculate_yoy_growth(100, 0) is None

    def test_negative_previous_returns_none(self):
        assert calculate_yoy_growth(100, -5) is None


class TestCagr:
    def test_five_year_window_uses_four_periods(self):
        assert calculate_cagr(100, 200, 4) == pytest.approx(0.1892, abs=1e-4)

    def test_zero_first_returns_none(self):
        assert calculate_cagr(0, 200, 4) is None

    def test_zero_periods_returns_none(self):
        assert calculate_cagr(100, 200, 0) is None

    def test_decline(self):
        assert calculate_cagr(200, 100, 4) == pytest.approx(-0.1591, abs=1e-4)


class TestTradeBalance:
    def test_deficit(self):
        assert calculate_trade_balance(2100, 3200) == -1100

    def test_surplus(self):
        assert calculate_trade_balance(500, 300) == 200


class TestSectorShare:
    def test_share(self):
        assert calculate_sector_share(18, 100) == pytest.approx(0.18)

    def test_zero_total_returns_none(self):
        assert calculate_sector_share(18, 0) is None


class TestMinMaxScores:
    def test_normalizes_to_0_100(self):
        assert min_max_scores([0, 5, 10]) == [0.0, 50.0, 100.0]

    def test_single_distinct_value_scores_50(self):
        assert min_max_scores([7, 7]) == [50.0, 50.0]

    def test_none_preserved(self):
        assert min_max_scores([0, None, 10]) == [0.0, None, 100.0]

    def test_all_none(self):
        assert min_max_scores([None, None]) == [None, None]

    def test_empty(self):
        assert min_max_scores([]) == []


class TestNormalizeComtradeRecords:
    def test_keeps_hs2_rows_and_drops_total(self):
        raw = {
            "data": [
                {"cmdCode": "85", "refYear": 2024, "primaryValue": 100.0},
                {"cmdCode": "TOTAL", "refYear": 2024, "primaryValue": 999.0},
                {"cmdCode": "8542", "refYear": 2024, "primaryValue": 50.0},
                {"cmdCode": "01", "refYear": 2023, "primaryValue": None},
            ]
        }
        records = normalize_comtrade_records(raw)
        assert records == [TradeRecord(year=2024, hs2_code="85", value_usd=100.0)]

    def test_empty_response(self):
        assert normalize_comtrade_records({}) == []


class TestAggregations:
    RECORDS = [
        TradeRecord(2023, "85", 10.0),
        TradeRecord(2023, "84", 5.0),
        TradeRecord(2024, "85", 12.0),
    ]

    def test_totals_by_year(self):
        assert totals_by_year(self.RECORDS) == {2023: 15.0, 2024: 12.0}

    def test_sector_values_by_year(self):
        assert sector_values_by_year(self.RECORDS) == {
            "85": {2023: 10.0, 2024: 12.0},
            "84": {2023: 5.0},
        }
