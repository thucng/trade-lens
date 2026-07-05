import os

from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "TradeLens")
COMTRADE_API_KEY = os.getenv("COMTRADE_API_KEY") or None
if COMTRADE_API_KEY == "replace_me":
    COMTRADE_API_KEY = None
