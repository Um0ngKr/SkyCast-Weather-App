import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Resolve the application directory for source and packaged modes.
if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).resolve().parent
else:
    APP_DIR = Path(__file__).resolve().parent

# Load the environment file located beside the executable.
load_dotenv(APP_DIR / ".env")

API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "").strip()
BASE_URL = "https://api.openweathermap.org/data/2.5"
ICON_URL = "https://openweathermap.org/img/wn/{}@2x.png"

BG = "#101411"
CARD = "#20251F"
CARD_LIGHT = "#2B3129"
TEXT = "#F5F5EC"
MUTED = "#AEB5A7"
GREEN = "#D5F27A"
BORDER = "#3A4235"
ERROR = "#FF9999"