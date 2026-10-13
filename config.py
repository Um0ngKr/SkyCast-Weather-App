import os
from dotenv import load_dotenv

# Loads .env from the project root.
load_dotenv()

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
