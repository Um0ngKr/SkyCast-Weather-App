
import threading
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image
import customtkinter as ctk

from config import ICON_URL


# Local weather icon assets are stored in the project root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
WEATHER_ICON_DIR = PROJECT_ROOT / "assets" / "weather"

# OpenWeatherMap icon codes cover day and night conditions.
ICON_FILES = {
    "01d": "sun.png",
    "01n": "moon.png",
    "02d": "partly_cloudy_day.png",
    "02n": "partly_cloudy_night.png",
    "03d": "cloudy.png",
    "03n": "cloudy.png",
    "04d": "overcast.png",
    "04n": "overcast.png",
    "09d": "rain.png",
    "09n": "rain.png",
    "10d": "rain.png",
    "10n": "rain.png",
    "11d": "thunderstorm.png",
    "11n": "thunderstorm.png",
    "13d": "snow.png",
    "13n": "snow.png",
    "50d": "fog.png",
    "50n": "fog.png",
}


def _load_local_icon(icon_code, size):
    """Load a local weather icon when its asset is available."""
    filename = ICON_FILES.get(icon_code)

    if not filename:
        return None

    icon_path = WEATHER_ICON_DIR / filename

    if not icon_path.is_file():
        return None

    with Image.open(icon_path) as source:
        image = source.convert("RGBA")

    image.thumbnail(size, Image.Resampling.LANCZOS)
    return image


def download_icon(
    icon_code: str,
    size: tuple[int, int],
    callback,
    on_error=None,
):
    """Load a local icon or download an OpenWeatherMap fallback."""

    def worker():
        try:
            image = _load_local_icon(icon_code, size)

            if image is None:
                response = requests.get(
                    ICON_URL.format(icon_code),
                    timeout=10,
                )
                response.raise_for_status()

                with Image.open(BytesIO(response.content)) as source:
                    image = source.convert("RGBA")

                image.thumbnail(size, Image.Resampling.LANCZOS)

            callback(image, icon_code)

        except (
            requests.RequestException,
            OSError,
            ValueError,
        ):
            if on_error:
                on_error()

    threading.Thread(
        target=worker,
        daemon=True,
    ).start()


def make_ctk_image(image, size: tuple[int, int]):
    """Convert a Pillow image into a CustomTkinter-compatible image."""
    return ctk.CTkImage(
        light_image=image,
        dark_image=image,
        size=size,
    )
