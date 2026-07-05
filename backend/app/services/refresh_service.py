"""Orchestrates fetching, saving, and processing trade data for a country."""

import asyncio
from datetime import datetime, timezone

from app.core.paths import (
    COUNTRIES_FILE,
    HS2_CODES_FILE,
    RAW_DIR,
    UPDATE_STATE_FILE,
    processed_dashboard_path,
)
from app.services.cache_service import CacheService
from app.services.comtrade_client import ComtradeClient, ComtradeError, Flow
from app.services.dashboard_builder import build_dashboard
from app.services.trade_transformer import TradeRecord, normalize_comtrade_records

SOURCE_NAME = "UN Comtrade"
SOURCE_URL = "https://comtradeplus.un.org/"
YEAR_WINDOW = 5
MAX_YEAR_PROBES = 4
# Public API rate limit is strict; pause between calls.
CALL_DELAY_SECONDS = 1.1


class CountryNotFoundError(Exception):
    pass


class CountryNotSupportedError(Exception):
    pass


class RefreshInProgressError(Exception):
    pass


class NoDataAvailableError(Exception):
    pass


class RefreshService:
    _in_progress: set[str] = set()

    def __init__(
        self,
        cache: CacheService | None = None,
        client: ComtradeClient | None = None,
    ) -> None:
        self._cache = cache or CacheService()
        self._client = client or ComtradeClient()

    # ---------- state ----------

    def get_state(self, iso3: str) -> dict:
        iso3 = iso3.upper()
        state = self._read_state().get(iso3, {})
        return {
            "iso3": iso3,
            "cached": self._cache.exists(processed_dashboard_path(iso3)),
            "status": state.get("status", "not_cached"),
            "last_refreshed_at": state.get("last_refreshed_at"),
            "latest_available_year": state.get("latest_available_year"),
            "error": state.get("error"),
        }

    def _read_state(self) -> dict:
        if not self._cache.exists(UPDATE_STATE_FILE):
            return {}
        return self._cache.read_json(UPDATE_STATE_FILE)

    def _update_state(self, iso3: str, **fields) -> None:
        state = self._read_state()
        entry = state.setdefault(iso3, {
            "classification": "HS2",
            "frequency": "Annual",
            "source": SOURCE_NAME,
        })
        entry.update(fields)
        self._cache.write_json(UPDATE_STATE_FILE, state)

    # ---------- refresh ----------

    async def refresh_country(self, iso3: str) -> dict:
        iso3 = iso3.upper()
        country = self._find_country(iso3)

        if iso3 in RefreshService._in_progress:
            raise RefreshInProgressError(iso3)
        RefreshService._in_progress.add(iso3)
        try:
            self._update_state(iso3, status="refreshing", error=None)
            result = await self._do_refresh(iso3, country)
            self._update_state(
                iso3,
                cached=True,
                status="ready",
                last_refreshed_at=result["last_refreshed_at"],
                latest_available_year=result["latest_available_year"],
                error=None,
            )
            return result
        except Exception as exc:
            was_cached = self._cache.exists(processed_dashboard_path(iso3))
            self._update_state(
                iso3,
                cached=was_cached,
                status="ready" if was_cached else "error",
                error=str(exc),
            )
            raise
        finally:
            RefreshService._in_progress.discard(iso3)

    async def _do_refresh(self, iso3: str, country: dict) -> dict:
        reporter_code = country["comtrade_code"]

        latest_year, latest_raw = await self._find_latest_year(reporter_code)
        years = list(range(latest_year - YEAR_WINDOW + 1, latest_year + 1))

        import_records: list[TradeRecord] = []
        export_records: list[TradeRecord] = []
        for year in years:
            for flow, records in (("imports", import_records), ("exports", export_records)):
                if flow == "imports" and year == latest_year:
                    raw = latest_raw  # already fetched during the probe
                else:
                    await asyncio.sleep(CALL_DELAY_SECONDS)
                    raw = await self._client.fetch_annual_hs2_trade(
                        reporter_code, year, flow,  # type: ignore[arg-type]
                    )
                self._save_raw(iso3, flow, year, raw)
                records.extend(normalize_comtrade_records(raw))

        if not import_records:
            raise NoDataAvailableError(f"No import data available for {iso3}.")

        now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
        dashboard = build_dashboard(
            country=country,
            import_records=import_records,
            export_records=export_records,
            hs2_names=self._hs2_names(),
            source=SOURCE_NAME,
            source_url=SOURCE_URL,
            last_refreshed_at=now_iso,
            year_window=YEAR_WINDOW,
        )
        self._cache.write_json(processed_dashboard_path(iso3), dashboard)

        return {
            "iso3": iso3,
            "status": "ready",
            "message": "Refresh completed successfully.",
            "latest_available_year": latest_year,
            "last_refreshed_at": now_iso,
        }

    async def _find_latest_year(self, reporter_code: int) -> tuple[int, dict]:
        """Probe backwards from last year for the most recent year with data."""
        start_year = datetime.now(timezone.utc).year - 1
        for year in range(start_year, start_year - MAX_YEAR_PROBES, -1):
            raw = await self._client.fetch_annual_hs2_trade(
                reporter_code, year, "imports",
            )
            if raw.get("data"):
                return year, raw
            await asyncio.sleep(CALL_DELAY_SECONDS)
        raise NoDataAvailableError(
            f"No annual import data found in the last {MAX_YEAR_PROBES} years."
        )

    # ---------- helpers ----------

    def _find_country(self, iso3: str) -> dict:
        for entry in self._cache.read_json(COUNTRIES_FILE):
            if entry["iso3"] == iso3:
                if "comtrade_code" not in entry:
                    raise CountryNotSupportedError(iso3)
                return entry
        raise CountryNotFoundError(iso3)

    def _hs2_names(self) -> dict[str, str]:
        return {
            entry["code"]: entry["name"]
            for entry in self._cache.read_json(HS2_CODES_FILE)
        }

    def _save_raw(self, iso3: str, flow: Flow, year: int, raw: dict) -> None:
        path = RAW_DIR / "comtrade" / iso3 / f"{flow}_hs2_annual_{year}.json"
        self._cache.write_json(path, raw)
