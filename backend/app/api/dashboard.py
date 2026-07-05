from fastapi import APIRouter, HTTPException, Query

from app.core.paths import processed_dashboard_path
from app.schemas.dashboard import Dashboard
from app.services.cache_service import CacheService
from app.services.country_service import CountryService

router = APIRouter(tags=["dashboard"])

cache_service = CacheService()
country_service = CountryService(cache_service)


@router.get("/countries/{iso3}/dashboard", response_model=Dashboard)
def get_country_dashboard(
    iso3: str,
    years: int = Query(default=5, ge=5, le=5, description="Only 5-year window is supported in MVP."),
) -> Dashboard:
    country = country_service.get_country(iso3)
    if country is None:
        raise HTTPException(
            status_code=404,
            detail={"code": "COUNTRY_NOT_FOUND", "message": "Country not found."},
        )

    dashboard_path = processed_dashboard_path(iso3)
    if not cache_service.exists(dashboard_path):
        raise HTTPException(
            status_code=404,
            detail={
                "code": "COUNTRY_NOT_CACHED",
                "message": (
                    f"Dashboard data is not cached for {country.name} yet. "
                    "Trigger a refresh to prepare this country."
                ),
            },
        )

    return Dashboard(**cache_service.read_json(dashboard_path))
