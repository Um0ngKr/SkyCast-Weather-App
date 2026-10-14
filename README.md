# 🌤️ SkyCast — Modular Weather App

**A modern Windows desktop weather application built with Python, CustomTkinter, and the OpenWeatherMap API.**

SkyCast brings current weather conditions and forecast information into a clean, dark-themed desktop dashboard with soft blue accents, realistic weather icons, location detection, and temperature conversion.

The project supports both Python-based development and a packaged Windows application, including a custom SkyCast icon and a Windows installer with Start Menu and Desktop shortcuts.

---

## ✨ Features

### 🌦️ Weather Dashboard
- Search for weather by city name or supported ZIP/postal code.
- Display current temperature and weather conditions.
- View humidity, wind speed, and precipitation.
- Show feels-like temperature and weather descriptions.
- Switch between Celsius and Fahrenheit.
- View available forecast entries within the next six hours.
- Explore a daily summary of the available five-day forecast.

### 📍 Location Services
- Browser-based geolocation using device location permission.
- Approximate city detection based on public IP address.
- Search manually by city or supported ZIP/postal code when location detection is unavailable.
- Local browser-location server running on `127.0.0.1:8765`.

### 🎨 Interface and Icons
- Modern dark dashboard with soft blue accents.
- Reusable UI components and weather cards.
- Local weather icons with an online fallback.
- Custom SkyCast application icon in Windows ICO format.
- Scrollable dashboard layout.

### 🪟 Windows Application
- Packaged Windows executable using PyInstaller.
- Windows installer created with Inno Setup.
- Start Menu shortcut.
- Optional Desktop shortcut.
- Application uninstall support.
- Separate development and packaged-app workflows.

---

## 🖥️ Application Preview

SkyCast provides a desktop dashboard featuring current weather, weather metrics, temperature controls, location search, and forecast information.

The application uses a dark interface with high-contrast typography and weather icons to keep important information easy to read.

---

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Application logic |
| CustomTkinter | Desktop interface |
| Requests | HTTP requests to weather services |
| Pillow | Image loading and processing |
| python-dotenv | Environment-variable configuration |
| Flask | Local browser-geolocation server |
| OpenWeatherMap API | Current weather and forecast data |
| PyInstaller | Packaging Python into a Windows executable |
| Inno Setup | Building the Windows installer |

---

## 📁 Project Structure

```text
SkyCast_Modular/
├── main.py
├── config.py
├── location_server.py
├── requirements.txt
├── README.md
├── .env
├── .env.example
├── .gitignore
├── SkyCast.spec
├── SkyCastInstaller.iss
│
├── assets/
│   ├── SkyCast.ico
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
│
├── components/
│   ├── __init__.py
│   ├── cards.py
│   └── weather_icons.py
│
├── services/
│   ├── __init__.py
│   ├── location.py
│   └── weather_api.py
│
├── ui/
│   ├── __init__.py
│   └── app.py
│
├── dist/
├── dist_fixed/
├── dist_icon/
├── build/
├── build_fixed/
├── build_icon/
└── installer_output/
```

**Note:** Build folders and generated executables are local development artifacts. They may differ between machines and should not be assumed to exist in a fresh Git clone. The `.env` file is private and must not be committed to the repository.

---

## 🧩 Main Components

| File | Responsibility |
|---|---|
| `main.py` | Application entry point |
| `config.py` | API configuration, environment variables, and theme constants |
| `ui/app.py` | Main dashboard, search, current weather, metrics, and forecasts |
| `services/weather_api.py` | Retrieves current weather and forecast data |
| `services/location.py` | Approximate IP-based city detection |
| `location_server.py` | Local server for browser-based geolocation |
| `components/cards.py` | Reusable cards, labels, and UI elements |
| `components/weather_icons.py` | Weather-code mapping, local icons, image processing, and online fallback |
| `assets/weather/` | Local weather icon images |
| `assets/SkyCast.ico` | Custom Windows application icon |
| `config.py` | Loads the API key and defines reusable configuration |
| `SkyCast.spec` | PyInstaller build configuration generated for the project |
| `SkyCastInstaller.iss` | Inno Setup installer configuration |

---

## ⚙️ Requirements

- Windows 10 or later
- Python 3.10 or later
- An OpenWeatherMap API key
- An active internet connection
- Inno Setup, if building the Windows installer
- PyInstaller, if packaging the executable

### Python Dependencies

The project uses the following packages:

- `requests`
- `customtkinter`
- `Pillow`
- `python-dotenv`
- `Flask`

Install the project dependencies using the supplied `requirements.txt` file.

---

## 🚀 Getting Started

### 1. Clone the Repository

```powershell
git clone https://github.com/Um0ngKr/SkyCast-Weather-App.git
cd SkyCast-Weather-App
```

Alternatively, download the repository as a ZIP file and extract it.

### 2. Create a Virtual Environment

```powershell
python -m venv .venv
```

Activate the environment in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks environment activation, use Command Prompt and run:

```bat
.venv\Scripts\activate.bat
```

### 3. Configure the API Key

Create a file named `.env` in the project root. You can use `.env.example` as a template.

Add your OpenWeatherMap API key:

```dotenv
OPENWEATHERMAP_API_KEY=your_api_key_here
```

Replace the placeholder with your own API key.

**Security reminder:** Never upload your real `.env` file or API key to GitHub.

### 4. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Run SkyCast

```powershell
python main.py
```

The SkyCast desktop window should open. Weather information requires a valid API key and an internet connection.

---

## 📍 Location Features

### Browser-Based Geolocation

1. Click **Detect My Location** in SkyCast.
2. Allow the browser to access your location when prompted.
3. SkyCast uses the returned coordinates to retrieve weather information.

The local location server uses `127.0.0.1` on port `8765`.

If the browser does not grant location access, use the manual city search instead.

### Approximate IP-Based Location

SkyCast also supports approximate city detection based on the public IP address through `services/location.py`.

IP-based location may not identify your exact physical location. Results depend on the network and the location service.

---

## 🌤️ Forecast Information

SkyCast uses OpenWeatherMap current-weather and five-day forecast data.

The standard five-day forecast endpoint supplies forecast entries at three-hour intervals.

SkyCast uses the available forecast data to:
- Display upcoming forecast entries within the next six hours, when available.
- Group available entries by calendar day for a daily forecast summary.
- Show weather descriptions and temperatures for forecast entries.

Forecast availability and accuracy depend on the API response and the selected location.

---

## 🖼️ Weather Icons and Application Branding

SkyCast includes local weather icons in `assets/weather/` and a custom Windows application icon at `assets/SkyCast.ico`.

### Local Weather Icons

The supported icon files include:

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

The icon loader maps weather conditions to local image assets, processes images for display, and attempts an online fallback when a local icon is unavailable.

Keep the original image files in `assets/weather/` when running or packaging the application.

### Windows Application Icon

The custom `assets/SkyCast.ico` file is used when building the Windows executable with PyInstaller.

The Desktop shortcut icon can also be changed through Windows shortcut properties. Updating the shortcut icon alone does not change the executable's embedded icon.

---

## 📦 Building the Windows Executable

SkyCast uses PyInstaller to package the Python application.

First, make sure the virtual environment is activated and the dependencies are installed.

### Build with the Default Application Icon

```powershell
python -m PyInstaller --noconfirm --clean --windowed --name SkyCast --add-data "assets;assets" main.py
```

### Build with the Custom SkyCast Icon

```powershell
python -m PyInstaller --noconfirm --clean --windowed --name SkyCast --icon "assets\SkyCast.ico" --add-data "assets;assets" --distpath ".\dist_icon" --workpath ".\build_icon" main.py
```

The custom-icon build produces the application under:

```text
dist_icon/
└── SkyCast/
    ├── SkyCast.exe
    └── _internal/
```

The complete output folder must be retained. The executable depends on its packaged support files.

### Test the Packaged Application

Run the generated executable and verify:

- The application opens successfully.
- The custom icon appears where expected.
- The API key loads correctly.
- Current weather and forecasts work.
- Search and temperature conversion work.
- Location features behave as expected.

For a packaged application, configuration files must be available at the path expected by `config.py`. The application code loads `.env` from the executable's directory when running in PyInstaller's frozen mode.

Do not assume that a fresh build automatically contains your private `.env` file.

---

## 🪟 Building the Windows Installer

SkyCast uses Inno Setup to create a Windows installer.

The installer configuration is maintained in `SkyCastInstaller.iss`.

### Installer Features

- Installs the packaged application.
- Creates a Start Menu shortcut.
- Supports an optional Desktop shortcut.
- Registers an uninstall entry.
- Offers to launch SkyCast after installation.

### Build the Installer

1. Build and test the latest executable with PyInstaller.
2. Open `SkyCastInstaller.iss` in Inno Setup Compiler.
3. Ensure that the script's source path points to the intended build folder.
4. Compile the script using **Build → Compile** or `Ctrl + F9`.
5. Locate the generated installer in the configured output directory.

The installer source must include the entire packaged application directory, including `_internal`.

**Important:** If the build output changes from `dist\SkyCast` to `dist_icon\SkyCast`, update the source path in `SkyCastInstaller.iss` before compiling.

### API Key Configuration After Installation

The installer does not automatically provide a valid personal API key.

For the current configuration approach, `config.py` loads `.env` from beside the executable. A fresh installation therefore needs a valid `.env` in the installed application's directory, or an alternative configuration mechanism implemented in the application.

Never distribute an installer containing your personal API key.

---

## 🛠️ Troubleshooting

### API Key Missing

- Verify that `.env` exists in the expected application directory.
- Confirm that the variable is named `OPENWEATHERMAP_API_KEY`.
- Make sure the key is not empty and that the file is named `.env`, not `.env.txt`.
- Restart the application after changing the configuration.

### Invalid API Key or API Error

- Check the API key in your OpenWeatherMap account.
- Confirm internet connectivity.
- Check whether the API key is active and whether the requested API endpoint is available to your account.

### City Not Found

- Check the spelling of the city name.
- Try a supported ZIP/postal code and the appropriate country code if required.

### Location Detection Not Working

- Allow browser location permission.
- Check Windows location settings.
- Verify that the local server can use port `8765`.
- Use manual city search if location access is unavailable.

### Missing Weather Icons

- Verify that the PNG assets are present in `assets/weather/`.
- Rebuild the executable after changing packaged assets.
- Check internet connectivity if the online icon fallback is needed.

### PyInstaller Access Denied

- Close all running SkyCast processes.
- Check whether another application is using files inside the build output.
- Use separate build and distribution directories if existing files cannot be cleaned safely.

### Desktop Shortcut Still Shows an Old Icon

- Confirm that the shortcut points to the intended executable.
- Reapply the icon through **Properties → Shortcut → Change Icon**.
- Refresh the Desktop or recreate the shortcut if Windows continues to show a cached icon.

---

## 🔐 Security

- Keep the real API key in `.env`.
- Commit only placeholder values in `.env.example`.
- Ensure `.gitignore` excludes `.env`, Python cache files, and virtual environments.
- Never publish personal API keys in source code, screenshots, or installer files.
- Rotate the key if it is accidentally exposed.

An API key included in a distributed desktop application cannot be treated as a fully secret credential. For public distribution, consider a separate backend service or an appropriate restricted-key strategy.

---

## 🗺️ Roadmap

Potential future improvements include:

- Light and dark theme switching.
- Additional weather metrics and improved forecast visualizations.
- More robust first-run API-key configuration.
- Better location-permission handling.
- Automated release builds.
- Expanded application branding and documentation.

---

## 📄 License

No license is included by default. Add a `LICENSE` file before granting others permission to reuse, modify, or distribute the project.

---

## 👨‍💻 Author

**Umang Kr**

GitHub Repository: [SkyCast Weather App](https://github.com/Um0ngKr/SkyCast-Weather-App)

---

*SkyCast — Weather at a glance.* 🌤️