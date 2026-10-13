
# SkyCast Modular Weather App (Windows)

SkyCast is a desktop weather application built with Python, CustomTkinter, and the OpenWeatherMap API. It displays current weather conditions, upcoming forecasts, and location-based weather information in a modern graphical interface.

## Project Structure

```text
SkyCast_Modular/
├── main.py
├── config.py
├── location_server.py
├── requirements.txt
├── .env.example
├── .gitignore
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

### Main Components

- `main.py` — Application entry point.
- `config.py` — Loads environment variables and stores API settings, URLs, and theme colors.
- `services/weather_api.py` — Retrieves current weather and forecast data from OpenWeatherMap.
- `services/location.py` — Detects an approximate location using the public IP address.
- `location_server.py` — Provides a local web server for browser-based geolocation.
- `components/weather_icons.py` — Downloads and processes weather icons.
- `components/cards.py` — Provides reusable UI cards and labels.
- `ui/app.py` — Implements the main CustomTkinter dashboard.
- `.env.example` — Template for the required environment variable.
- `.env` — Stores your private API key locally.

## Features

- Search for weather by city name.
- Display current temperature, humidity, wind speed, and precipitation.
- Switch between Celsius and Fahrenheit.
- View upcoming forecast entries for the next six hours, when available.
- View a daily summary of the available five-day forecast.
- Retrieve weather using browser-based location permission.
- Optionally detect an approximate city using IP-based location.
- Display readable error messages for common API and network failures.

## Requirements

- Windows
- Python 3.10 or later
- An OpenWeatherMap API key
- An active internet connection

## Installation and Setup

### 1. Open the Project

Extract the project files and open the `SkyCast_Modular` folder in Visual Studio Code.

### 2. Create the Environment File

Copy `.env.example` and rename the copy to `.env`.

Open `.env` and replace the placeholder with your own OpenWeatherMap API key:

```dotenv
OPENWEATHERMAP_API_KEY=your_api_key_here
```

Keep the actual API key private. Do not commit or share the `.env` file.

### 3. Install Dependencies

Open the VS Code terminal in the project folder and run:

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the Application

Start SkyCast with:

```powershell
python main.py
```

## Location Features

### Browser-Based Geolocation

Click **Detect My Location** in the application. Your browser will open a local SkyCast page and request permission to access your location. Allow permission to retrieve weather for the detected coordinates.

If permission is denied or the location cannot be retrieved, use the city search field instead.

### IP-Based Location

The `services/location.py` module provides an approximate city lookup based on your public IP address. IP-based location may be inaccurate and depends on the location service and network configuration.

## Forecast Information

OpenWeatherMap's standard five-day forecast endpoint provides data at three-hour intervals.

SkyCast uses this data to display upcoming forecast entries and group available entries by calendar day. Forecast coverage depends on the data returned by the API.

The six-hour forecast section displays forecast entries that fall within the next six hours; it does not provide hourly observations for every hour.

## Troubleshooting

- **API key error:** Check that `.env` exists in the project root and contains the correct key.
- **Location not found:** Check the spelling of the city name or use a supported ZIP code.
- **Network error:** Verify your internet connection.
- **Browser location unavailable:** Allow location access in your browser and check your device's location settings.
- **Missing dependencies:** Run `python -m pip install -r requirements.txt` again.
- **Port conflict:** If the local location server cannot start, check whether another application is using port `8765`.

## Security

- Never upload `.env` to GitHub.
- Keep `.env.example` free of real API keys.
- The `.gitignore` file should exclude `.env`, Python cache files, and virtual environments.

## License

Add a license file if you plan to distribute this project publicly.
```

### Final recommendation

- Agar README sirf project ke liye hai, toh ise **`README.md`** naam dena best rahega.
- Tumhara `README_HINGLISH.md` bhi rakh sakte ho agar Hinglish documentation baad mein chahiye.
- Ek important correction: purane README mein “next six entries” likha tha, lekin tumhare current code mein forecast **next six hours** ke hisaab se filter hota hai. Naye README mein ye distinction sahi kar diya hai.

Ab README bhi ready hai. Agla step final project audit hai—especially dependencies install karke fresh run aur Git security checks.