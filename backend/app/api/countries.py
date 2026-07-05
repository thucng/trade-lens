from fastapi import APIRouter, HTTPException

from app.schemas.country import Country
from app.services.country_service import CountryService

router = APIRouter(tags=["countries"])

country_service = CountryService()


@router.get("/countries", response_model=list[Country])
def list_countries() -> list[Country]:
    return country_service.list_countries()


@router.get("/countries/cached", response_model=list[Country])
def list_cached_countries() -> list[Country]:
    return country_service.list_cached_countries()


@router.get("/countries/{iso3}", response_model=Country)
def get_country(iso3: str) -> Country:
    country = country_service.get_country(iso3)
    if country is None:
        raise HTTPException(
            status_code=404,
            detail={"code": "COUNTRY_NOT_FOUND", "message": "Country not found."},
        )
    return country
