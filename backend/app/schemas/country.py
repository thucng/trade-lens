from pydantic import BaseModel


class Country(BaseModel):
    iso3: str
    name: str
    region: str
    is_supported: bool
    is_cached: bool
