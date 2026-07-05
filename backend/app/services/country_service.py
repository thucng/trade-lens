from app.core.paths import COUNTRIES_FILE, processed_dashboard_path
from app.schemas.country import Country
from app.services.cache_service import CacheService


class CountryService:
    """Country metadata lookups backed by countries.json.

    `is_cached` is derived from the existence of the processed dashboard
    file, so the metadata file never goes stale.
    """

    def __init__(self, cache: CacheService | None = None) -> None:
        self._cache = cache or CacheService()

    def list_countries(self) -> list[Country]:
        raw = self._cache.read_json(COUNTRIES_FILE)
        return [
            Country(**entry, is_cached=self._is_cached(entry["iso3"]))
            for entry in raw
        ]

    def list_cached_countries(self) -> list[Country]:
        return [c for c in self.list_countries() if c.is_cached]

    def get_country(self, iso3: str) -> Country | None:
        iso3 = iso3.upper()
        for country in self.list_countries():
            if country.iso3 == iso3:
                return country
        return None

    def _is_cached(self, iso3: str) -> bool:
        return self._cache.exists(processed_dashboard_path(iso3))
