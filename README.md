# SkyCast Modular Weather App

SkyCast is a Windows desktop weather application built with Python, CustomTkinter, and the OpenWeatherMap API. It features a modern dark interface, soft blue accents, realistic 3D-style weather icons, current weather details, and forecast information.

## Features

- Search weather by city name or supported ZIP/postal code.
- Display current temperature and weather conditions.
- View humidity, wind speed, and precipitation.
- Switch between Celsius and Fahrenheit.
- View forecast entries within the next six hours, when available.
- View a daily summary of the available five-day forecast.
- Retrieve weather using browser-based geolocation.
- Support approximate IP-based city detection.
- Load local weather icons with an online fallback.
- Display readable errors for common API, location, and network issues.

## Project Structure

```text
SkyCast_Modular/
├── main.py
├── config.py
├── location_server.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── assets/
│   └── weather/
│       ├── sun.png
│       ├── moon.png
│       ├── partly_cloudy_day.png
│       ├── partly_cloudy_night.png
│       ├── cloudy.png
│       ├── overcast.png
│       ├── rain.png
│       ├── thunderstorm.png
│       ├── snow.png
│       └── fog.png
├── components/
│   ├── __init__.py
│   ├── cards.py
│   └── weather_icons.py
├── services/
│   ├── __init__.py
│   ├── location.py
│   └── weather_api.py
└── ui/
    ├── __init__.py
    └── app.py
```

## Main Components

- `main.py` — Starts the application.
- `config.py` — Loads environment variables and stores API configuration.
- `ui/app.py` — Implements the main dashboard, search, current conditions, metrics, and forecasts.
- `services/weather_api.py` — Fetches current weather and forecast data from OpenWeatherMap.
- `services/location.py` — Provides approximate city detection based on public IP.
- `location_server.py` — Runs the local server used for browser-based geolocation.
- `components/weather_icons.py` — Maps weather codes to local icons, processes images, and provides an online fallback.
- `components/cards.py` — Provides reusable UI cards and labels.
- `assets/weather/` — Stores the local weather icon PNG files.
- `.env.example` — Provides a template for the API key environment variable.
- `.gitignore` — Excludes sensitive files and generated files from version control.

## Weather Icons

The application uses local PNG icons stored in `assets/weather/`.

Supported icon assets:

- `sun.png`
- `moon.png`
- `partly_cloudy_day.png`
- `partly_cloudy_night.png`
- `cloudy.png`
- `overcast.png`
- `rain.png`
- `thunderstorm.png`
- `snow.png`
- `fog.png`

The icon loader maps OpenWeatherMap condition codes to these files, converts images to RGBA, and resizes them for display. If a matching local icon is unavailable, the application attempts to download an online icon.

Keep the icon files in `assets/weather/` so the application can load them correctly.

## Requirements

- Windows
- Python 3.10 or later
- An OpenWeatherMap API key
- An active internet connection

The project uses these Python packages:

- `requests`
- `customtkinter`
- `Pillow`
- `python-dotenv`
- `Flask` for the local location server

## Installation and Setup

### 1. Open the Project

Open the `SkyCast_Modular` folder in Visual Studio Code.

### 2. Create a Virtual Environment

Open the VS Code terminal and run:

```powershell
python -m venv .venv
```

Activate the environment in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Configure the API Key

Copy `.env.example` to a new file named `.env` in the project root.

Add your OpenWeatherMap API key:

```dotenv
OPENWEATHERMAP_API_KEY=your_api_key_here
```

Replace the placeholder with your actual API key. Keep the real key private.

### 4. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Run the Application

```powershell
python main.py
```

## Location Features

### Browser-Based Geolocation

Select **Detect My Location** in the application. A local SkyCast page opens in your browser and requests permission to access your location.

Allow permission to retrieve weather for the detected coordinates.

If location access is denied or unavailable, use the city or ZIP/postal-code search instead.

The local location server uses `127.0.0.1` on port `8765`. If another application is using this port, the location server may not start.

### IP-Based Location

The `services/location.py` module supports approximate city detection based on your public IP address. This method may be inaccurate and depends on the location service and network configuration.

## Forecast Information

OpenWeatherMap's standard five-day forecast endpoint provides forecast data at three-hour intervals.

SkyCast uses the available data to display upcoming forecast entries and group entries by calendar day.

The six-hour forecast section displays forecast entries that fall within the next six hours. It does not provide a separate forecast value for every hour. The amount of available forecast information depends on the API response.

## Troubleshooting

- **API key error:** Check that `.env` exists in the project root and contains a valid API key.
- **Location not found:** Check the spelling of the city name or try a supported ZIP/postal code.
- **Network error:** Check your internet connection.
- **Browser location unavailable:** Allow location access in your browser and check your device's location settings.
- **Missing dependencies:** Run `python -m pip install -r requirements.txt` in the correct Python environment.
- **Port conflict:** Check whether another application is using port `8765`.
- **Weather icons missing:** Confirm that the PNG files exist in `assets/weather/`. An internet connection may be needed for the online icon fallback.

## Security

- Store the real API key in `.env`.
- Keep `.env.example` limited to placeholder values.
- Make sure `.gitignore` excludes `.env`, Python cache files, and virtual environments.
- If an API key is accidentally exposed, revoke or rotate it through the API provider.

## License

No license is included by default. Add a `LICENSE` file if you plan to distribute the project publicly.
