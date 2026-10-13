import requests


def detect_city_from_ip() -> str:
    """Return an approximate city based on the public IP address."""

    try:
        response = requests.get(
            "https://ipinfo.io/json",
            timeout=8,
        )
        response.raise_for_status()

        data = response.json()
        city = (data.get("city") or "").strip()

        if not city:
            raise ValueError(
                "The IP location service did not return a city."
            )

        return city

    except (requests.RequestException, ValueError) as exc:
        raise RuntimeError(
            "Could not detect the approximate location. "
            "Please enter a city manually."
        ) from exc