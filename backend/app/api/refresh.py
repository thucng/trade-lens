from fastapi import APIRouter, HTTPException

from app.schemas.refresh import RefreshResponse, RefreshStatus
from app.services.comtrade_client import ComtradeError
from app.services.refresh_service import (
    CountryNotFoundError,
    CountryNotSupportedError,
    NoDataAvailableError,
    RefreshInProgressError,
    RefreshService,
)

router = APIRouter(tags=["refresh"])

refresh_service = RefreshService()


@router.post("/countries/{iso3}/refresh", response_model=RefreshResponse)
async def refresh_country(iso3: str) -> RefreshResponse:
    try:
        result = await refresh_service.refresh_country(iso3)
    except CountryNotFoundError:
        raise HTTPException(
            status_code=404,
            detail={"code": "COUNTRY_NOT_FOUND", "message": "Country not found."},
        )
    except CountryNotSupportedError:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "COUNTRY_NOT_SUPPORTED",
                "message": "This country cannot be refreshed from the data source yet.",
            },
        )
    except RefreshInProgressError:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "REFRESH_IN_PROGRESS",
                "message": "A refresh is already in progress for this country.",
            },
        )
    except (ComtradeError, NoDataAvailableError):
        raise HTTPException(
            status_code=502,
            detail={
                "code": "SOURCE_API_ERROR",
                "message": "The external trade data source is temporarily unavailable.",
            },
        )
    return RefreshResponse(**result)


@router.get("/countries/{iso3}/refresh/status", response_model=RefreshStatus)
def get_refresh_status(iso3: str) -> RefreshStatus:
    return RefreshStatus(**refresh_service.get_state(iso3))
