from pydantic import BaseModel


class RefreshResponse(BaseModel):
    iso3: str
    status: str
    message: str
    latest_available_year: int
    last_refreshed_at: str


class RefreshStatus(BaseModel):
    iso3: str
    cached: bool
    status: str
    last_refreshed_at: str | None
    latest_available_year: int | None
    error: str | None
