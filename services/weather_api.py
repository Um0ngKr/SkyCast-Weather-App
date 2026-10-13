import requests

from config import API_KEY, BASE_URL


class WeatherAPIError(Exception):
    """Readable error raised by the weather service."""


def fetch_weather(
    city: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
) -> tuple[dict, dict]:

    if not API_KEY:
        raise WeatherAPIError(
            "API key is missing. Add OPENWEATHERMAP_API_KEY "
            "to your .env file."
        )

    if (latitude is None) != (longitude is None):
        raise WeatherAPIError(
            "Both latitude and longitude are required."
        )

    if latitude is not None and longitude is not None:
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (TypeError, ValueError) as exc:
            raise WeatherAPIError(
                "Invalid location coordinates."
            ) from exc

        if not -90 <= latitude <= 90:
            raise WeatherAPIError("Invalid latitude.")
        if not -180 <= longitude <= 180:
            raise WeatherAPIError("Invalid longitude.")

        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": API_KEY,
            "units": "metric",
        }
    else:
        city = (city or "").strip()

        if not city:
            raise WeatherAPIError(
                "Please enter a city name or ZIP code."
            )

        # OpenWeatherMap accepts ZIP codes with a country code,
        # for example: 800001,IN. City names are also supported.
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric",
        }

    try:
        current_response = requests.get(
            f"{BASE_URL}/weather",
            params=params,
            timeout=12,
        )

        if current_response.status_code == 404:
            raise WeatherAPIError(
                "Location not found. Check the city name or ZIP code."
            )

        if current_response.status_code in (401, 403):
            raise WeatherAPIError(
                "The API key is invalid, inactive, or not authorized."
            )

        current_response.raise_for_status()
        current = current_response.json()

        if not isinstance(current, dict) or "main" not in current:
            raise WeatherAPIError(
                "The weather service returned unexpected data."
            )

        coords = current.get("coord", {})

        if "lat" not in coords or "lon" not in coords:
            raise WeatherAPIError(
                "Location coordinates were missing from the API response."
            )

        forecast_response = requests.get(
            f"{BASE_URL}/forecast",
            params={
                "lat": coords["lat"],
                "lon": coords["lon"],
                "appid": API_KEY,
                "units": "metric",
            },
            timeout=12,
        )

        if forecast_response.status_code == 404:
            raise WeatherAPIError(
                "Forecast data is not available for this location."
            )

        if forecast_response.status_code in (401, 403):
            raise WeatherAPIError(
                "The forecast API is not authorized. Check your API key."
            )

        forecast_response.raise_for_status()
        forecast = forecast_response.json()

        if not isinstance(forecast, dict):
            raise WeatherAPIError(
                "The forecast service returned unexpected data."
            )

        return current, forecast

    except WeatherAPIError:
        raise

    except requests.exceptions.Timeout as exc:
        raise WeatherAPIError(
            "The request timed out. Please try again."
        ) from exc

    except requests.exceptions.ConnectionError as exc:
        raise WeatherAPIError(
            "Network connection failed. Check your internet connection."
        ) from exc

    except requests.exceptions.HTTPError as exc:
        raise WeatherAPIError(
            f"Weather API request failed: {exc}"
        ) from exc

    except requests.exceptions.JSONDecodeError as exc:
        raise WeatherAPIError(
            "The weather service returned an invalid response."
        ) from exc

    except requests.exceptions.RequestException as exc:
        raise WeatherAPIError(
            f"Weather request failed: {exc}"
        ) from exc

    except (KeyError, TypeError, ValueError) as exc:
        raise WeatherAPIError(
            "The weather service returned unexpected data."
        ) from exc