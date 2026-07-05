from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = APP_DIR / "data"
METADATA_DIR = DATA_DIR / "metadata"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

COUNTRIES_FILE = METADATA_DIR / "countries.json"
HS2_CODES_FILE = METADATA_DIR / "hs2_codes.json"
UPDATE_STATE_FILE = METADATA_DIR / "update_state.json"


def processed_dashboard_path(iso3: str) -> Path:
    return PROCESSED_DIR / iso3.upper() / "dashboard_5y.json"
