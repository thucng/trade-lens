"""HTTP client for the UN Comtrade API.

Uses the authenticated data endpoint when COMTRADE_API_KEY is set,
otherwise falls back to the public preview endpoint (max 500 records
per call, which is enough for HS2 world-partner queries: ~97 rows).
"""

from typing import Literal

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.core.config import COMTRADE_API_KEY

PUBLIC_BASE_URL = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"
DATA_BASE_URL = "https://comtradeapi.un.org/data/v1/get/C/A/HS"

FLOW_CODES = {"imports": "M", "exports": "X"}

Flow = Literal["imports", "exports"]


class ComtradeError(Exception):
    """The Comtrade API is unavailable or returned an unusable response."""


class _RetryableComtradeError(ComtradeError):
    """Transient failure (5xx / rate limit) worth retrying."""


class ComtradeClient:
    def __init__(self, api_key: str | None = COMTRADE_API_KEY, timeout: float = 30.0):
        self._api_key = api_key
        self._timeout = timeout

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.TransportError, _RetryableComtradeError)),
        reraise=True,
    )
    async def fetch_annual_hs2_trade(
        self,
        reporter_code: int,
        year: int,
        flow: Flow,
    ) -> dict:
        """Fetch one country/year/flow of annual HS2 trade with the world."""
        params = {
            "reporterCode": reporter_code,
            "period": str(year),
            "flowCode": FLOW_CODES[flow],
            "cmdCode": "AG2",
            "partnerCode": 0,
            "partner2Code": 0,
            "customsCode": "C00",
            "motCode": 0,
        }
        headers = {}
        base_url = PUBLIC_BASE_URL
        if self._api_key:
            base_url = DATA_BASE_URL
            headers["Ocp-Apim-Subscription-Key"] = self._api_key

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.get(base_url, params=params, headers=headers)

        if response.status_code == 429 or response.status_code >= 500:
            raise _RetryableComtradeError(
                f"Comtrade returned status {response.status_code}."
            )
        if response.status_code != 200:
            raise ComtradeError(
                f"Comtrade returned status {response.status_code}: {response.text[:200]}"
            )

        try:
            payload = response.json()
        except ValueError as exc:
            raise ComtradeError("Comtrade returned a non-JSON response.") from exc

        if "data" not in payload:
            raise ComtradeError("Comtrade response is missing the 'data' field.")
        return payload
