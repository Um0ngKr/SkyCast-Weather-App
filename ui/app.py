
import threading
import time
from datetime import datetime
from pathlib import Path

import customtkinter as ctk

from config import BG, CARD, CARD_LIGHT, TEXT, MUTED, BORDER, ERROR
from components.weather_icons import download_icon, make_ctk_image
from services.weather_api import fetch_weather
from location_server import start_location_server, request_location


# SkyCast dark theme.
BLACK = "#0B0C0F"
PANEL = "#15171C"
PANEL_LIGHT = "#1D2027"
BLUE = "#B8DDF5"
BLUE_HOVER = "#9CCBEA"
WHITE = "#F4F6FA"
GREY = "#A5ACB8"
RED = "#FF8585"
OUTLINE = "#30343D"

ASSET_DIR = Path(__file__).resolve().parent.parent / "assets" / "weather"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SkyCastApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SkyCast | Weather")
        self.geometry("1120x900")
        self.minsize(820, 680)
        self.configure(fg_color=BLACK)

        self.unit = "C"
        self.current = None
        self.forecast = None
        self.icon_image = None
        self.request_in_progress = False
        self._icon_images = []
        self._request_id = 0

        self.city_var = ctk.StringVar(value="Patna")

        try:
            start_location_server()
        except Exception as exc:
            print(f"Location server notice: {exc}")

        self.build_ui()
        self.after(300, self.get_weather)

    # --------------------------------------------------
    # Reusable UI helpers
    # --------------------------------------------------

    def make_label(
        self, parent, text, size=13, color=WHITE, weight="normal"
    ):
        return ctk.CTkLabel(
            parent,
            text=text,
            font=("Segoe UI", size, weight),
            text_color=color,
        )

    def make_panel(self, parent, radius=18, color=PANEL):
        return ctk.CTkFrame(
            parent,
            fg_color=color,
            corner_radius=radius,
            border_width=1,
            border_color=OUTLINE,
        )

    def make_section_title(self, text):
        self.make_label(
            self.page, text, 15, WHITE, "bold"
        ).pack(anchor="w", padx=26, pady=(20, 9))

    # --------------------------------------------------
    # Main interface
    # --------------------------------------------------

    def build_ui(self):
        self.page = ctk.CTkScrollableFrame(
            self,
            fg_color=BLACK,
            corner_radius=0,
        )
        self.page.pack(fill="both", expand=True)

        # Header
        header = ctk.CTkFrame(self.page, fg_color="transparent")
        header.pack(fill="x", padx=26, pady=(22, 15))

        self.make_label(
            header, "SKYCAST", 28, WHITE, "bold"
        ).pack(side="left")

        self.make_label(
            header, "WEATHER", 11, BLUE, "bold"
        ).pack(side="left", padx=(13, 0), pady=(9, 0))

        self.unit_button = ctk.CTkButton(
            header,
            text="°C  /  °F",
            width=100,
            height=36,
            corner_radius=18,
            fg_color=PANEL_LIGHT,
            hover_color="#303642",
            text_color=WHITE,
            border_width=1,
            border_color=OUTLINE,
            command=self.toggle_unit,
        )
        self.unit_button.pack(side="right")

        # Search bar
        search = ctk.CTkFrame(self.page, fg_color="transparent")
        search.pack(fill="x", padx=26, pady=(0, 8))
        search.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            search,
            textvariable=self.city_var,
            placeholder_text="Search city or ZIP code...",
            height=46,
            corner_radius=15,
            border_width=1,
            border_color=OUTLINE,
            fg_color=PANEL,
            text_color=WHITE,
            placeholder_text_color=GREY,
            font=("Segoe UI", 13),
        )
        self.search_entry.grid(
            row=0, column=0, sticky="ew", padx=(0, 10)
        )
        self.search_entry.bind(
            "<Return>", lambda event: self.get_weather()
        )

        self.search_button = ctk.CTkButton(
            search,
            text="Search",
            width=115,
            height=46,
            corner_radius=15,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            text_color="#11151B",
            font=("Segoe UI", 13, "bold"),
            command=self.get_weather,
        )
        self.search_button.grid(row=0, column=1)

        # Browser location
        self.location_button = ctk.CTkButton(
            self.page,
            text="⌖  Detect My Location",
            height=35,
            corner_radius=12,
            fg_color=PANEL_LIGHT,
            hover_color="#303642",
            text_color=WHITE,
            border_width=1,
            border_color=OUTLINE,
            command=self.detect_location,
        )
        self.location_button.pack(
            anchor="w", padx=27, pady=(0, 3)
        )

        self.status = self.make_label(
            self.page,
            "Search for a city or ZIP code to view live weather.",
            12,
            GREY,
        )
        self.status.pack(anchor="w", padx=29, pady=(5, 7))

        # Current weather hero
        self.hero = self.make_panel(self.page, 22)
        self.hero.pack(fill="x", padx=26, pady=(7, 4))

        hero_top = ctk.CTkFrame(
            self.hero, fg_color="transparent"
        )
        hero_top.pack(fill="x", padx=22, pady=(18, 3))

        self.city_label = self.make_label(
            hero_top, "CITY", 22, WHITE, "bold"
        )
        self.city_label.pack(side="left")

        self.date_label = self.make_label(
            hero_top,
            datetime.now().strftime("%A, %d %B"),
            12,
            GREY,
        )
        self.date_label.pack(side="right", pady=5)

        hero_body = ctk.CTkFrame(
            self.hero, fg_color="transparent"
        )
        hero_body.pack(fill="x", padx=22, pady=(4, 22))

        self.icon_label = ctk.CTkLabel(
            hero_body,
            text="",
            width=145,
            height=130,
            fg_color="transparent",
        )
        self.icon_label.pack(side="left", padx=(0, 17))

        temperature_box = ctk.CTkFrame(
            hero_body, fg_color="transparent"
        )
        temperature_box.pack(side="left", anchor="center")

        self.temp_label = self.make_label(
            temperature_box, "--°", 52, WHITE, "bold"
        )
        self.temp_label.pack(anchor="w")

        self.condition_label = self.make_label(
            temperature_box, "Waiting for weather", 15, BLUE
        )
        self.condition_label.pack(anchor="w", pady=(0, 5))

        self.feels_label = self.make_label(
            temperature_box, "Feels like --", 12, GREY
        )
        self.feels_label.pack(anchor="w")

        # Today's conditions
        self.make_section_title("TODAY'S CONDITIONS")

        metrics = ctk.CTkFrame(
            self.page, fg_color="transparent"
        )
        metrics.pack(fill="x", padx=23)
        for col in range(3):
            metrics.grid_columnconfigure(col, weight=1, uniform="metric")

        self.humidity_value = self.make_metric(
            metrics, 0, "HUMIDITY", "--%", "💧"
        )
        self.wind_value = self.make_metric(
            metrics, 1, "WIND SPEED", "-- m/s", "≋"
        )
        self.rain_value = self.make_metric(
            metrics, 2, "PRECIPITATION", "-- mm", "☂"
        )

        # Six-hour forecast
        self.make_section_title("UPCOMING FORECAST · NEXT 6 HOURS")

        self.hourly_frame = ctk.CTkFrame(
            self.page, fg_color="transparent"
        )
        self.hourly_frame.pack(fill="x", padx=23)

        # Five-day forecast
        self.make_section_title("NEXT 5 DAYS")

        self.daily_frame = ctk.CTkFrame(
            self.page, fg_color="transparent"
        )
        self.daily_frame.pack(
            fill="x", padx=23, pady=(0, 24)
        )

    def make_metric(self, parent, column, title, value, symbol):
        panel = self.make_panel(parent, 15)
        panel.grid(
            row=0, column=column, sticky="nsew",
            padx=3, pady=3,
        )

        self.make_label(
            panel, f"{symbol}  {title}", 10, GREY, "bold"
        ).pack(anchor="w", padx=13, pady=(13, 7))

        value_label = self.make_label(
            panel, value, 21, WHITE, "bold"
        )
        value_label.pack(anchor="w", padx=13, pady=(0, 14))
        return value_label

    # --------------------------------------------------
    # Temperature units
    # --------------------------------------------------

    def temperature(self, celsius):
        try:
            value = float(celsius)
        except (TypeError, ValueError):
            return "--°C" if self.unit == "C" else "--°F"

        if self.unit == "F":
            return f"{value * 9 / 5 + 32:.1f}°F"
        return f"{value:.1f}°C"

    def toggle_unit(self):
        self.unit = "F" if self.unit == "C" else "C"

        if self.current is not None and self.forecast is not None:
            self.display_weather(self.current, self.forecast)

    # --------------------------------------------------
    # Request state and errors
    # --------------------------------------------------

    def set_loading(self, message):
        self.request_in_progress = True
        self._request_id += 1

        self.search_button.configure(
            state="disabled", text="Loading..."
        )
        self.location_button.configure(state="disabled")
        self.status.configure(text=message, text_color=BLUE)

    def finish_request(self):
        self.request_in_progress = False
        self.search_button.configure(
            state="normal", text="Search"
        )
        self.location_button.configure(state="normal")

    def show_error(self, message):
        self.finish_request()
        self.status.configure(
            text=f"Error: {message}", text_color=RED
        )

    # --------------------------------------------------
    # Search by city or ZIP code
    # --------------------------------------------------

    def get_weather(self):
        if self.request_in_progress:
            return

        city = self.city_var.get().strip()
        if not city:
            self.show_error("Please enter a city name or ZIP code.")
            return

        self.set_loading("Fetching live weather...")
        request_id = self._request_id

        def worker():
            try:
                current, forecast = fetch_weather(city)
                self.after(
                    0,
                    lambda c=current, f=forecast, rid=request_id:
                    self._finish_weather_request(c, f, rid),
                )
            except Exception as exc:
                message = str(exc) or "Unable to fetch weather data."
                self.after(
                    0,
                    lambda msg=message, rid=request_id:
                    self._finish_error_request(msg, rid),
                )

        threading.Thread(target=worker, daemon=True).start()

    def _finish_weather_request(self, current, forecast, request_id):
        if request_id != self._request_id:
            return
        self.display_weather(current, forecast)

    def _finish_error_request(self, message, request_id):
        if request_id != self._request_id:
            return
        self.show_error(message)

    # --------------------------------------------------
    # Browser location
    # --------------------------------------------------

    def detect_location(self):
        if self.request_in_progress:
            return

        self.set_loading("Waiting for browser location permission...")
        request_id = self._request_id

        def worker():
            try:
                location = request_location(timeout=60)
                if not location:
                    raise RuntimeError(
                        "Location was not received. Allow browser "
                        "location access and try again."
                    )

                latitude = location.get("latitude")
                longitude = location.get("longitude")
                if latitude is None or longitude is None:
                    raise RuntimeError(
                        "The browser did not provide valid coordinates."
                    )

                self.after(
                    0,
                    lambda lat=latitude, lon=longitude, rid=request_id:
                    self.get_weather_at_coordinates(lat, lon, rid),
                )
            except Exception as exc:
                message = str(exc) or "Unable to detect your location."
                self.after(
                    0,
                    lambda msg=message, rid=request_id:
                    self._finish_error_request(msg, rid),
                )

        threading.Thread(target=worker, daemon=True).start()

    def get_weather_at_coordinates(
        self, latitude, longitude, request_id=None
    ):
        if request_id is not None and request_id != self._request_id:
            return

        self.status.configure(
            text="Fetching weather for your location...",
            text_color=BLUE,
        )

        def worker():
            try:
                current, forecast = fetch_weather(
                    latitude=latitude, longitude=longitude
                )
                city_name = current.get("name", "My Location")

                self.after(
                    0,
                    lambda c=current, f=forecast, name=city_name,
                    rid=request_id:
                    self._finish_location_weather(c, f, name, rid),
                )
            except Exception as exc:
                message = str(exc) or "Unable to fetch local weather."
                self.after(
                    0,
                    lambda msg=message, rid=request_id:
                    self._finish_error_request(msg, rid),
                )

        threading.Thread(target=worker, daemon=True).start()

    def _finish_location_weather(
        self, current, forecast, city_name, request_id
    ):
        if request_id is not None and request_id != self._request_id:
            return
        self.city_var.set(city_name)
        self.display_weather(current, forecast)

    # --------------------------------------------------
    # Display current weather
    # --------------------------------------------------

    def display_weather(self, current, forecast):
        self.current = current
        self.forecast = forecast
        self.finish_request()

        self.status.configure(
            text="Live weather updated successfully.",
            text_color=BLUE,
        )

        country = current.get("sys", {}).get("country", "")
        city_name = current.get("name", "Unknown")
        title = city_name.upper()
        if country:
            title = f"{title}, {country}"

        self.city_label.configure(text=title)
        self.date_label.configure(
            text=datetime.now().strftime("%A, %d %B")
        )

        weather_list = current.get("weather") or [{}]
        weather = weather_list[0]
        main = current.get("main", {})

        self.temp_label.configure(
            text=self.temperature(main.get("temp"))
        )
        self.condition_label.configure(
            text=weather.get("description", "Unknown").title()
        )
        self.feels_label.configure(
            text=f"Feels like {self.temperature(main.get('feels_like'))}"
        )

        self.humidity_value.configure(
            text=f"{main.get('humidity', '--')}%"
        )

        wind = current.get("wind", {}).get("speed")
        self.wind_value.configure(
            text=f"{wind:g} m/s"
            if isinstance(wind, (int, float))
            else "-- m/s"
        )

        rain = current.get("rain", {}).get("1h", 0)
        snow = current.get("snow", {}).get("1h", 0)
        if not isinstance(rain, (int, float)):
            rain = 0
        if not isinstance(snow, (int, float)):
            snow = 0
        self.rain_value.configure(text=f"{rain + snow:.1f} mm")

        self.icon_image = None
        self.icon_label.configure(image=None, text="")

        icon_code = weather.get("icon")
        if icon_code:
            self._load_main_icon(icon_code)

        self.show_hourly(forecast)
        self.show_daily(forecast)

    def _load_main_icon(self, icon_code):
        def callback(image, code):
            self.after(
                0,
                lambda img=image, ic=code: self.set_icon(img, ic),
            )

        def on_error():
            self.after(
                0,
                lambda: self.icon_label.configure(
                    image=None, text="Weather icon unavailable"
                ),
            )

        download_icon(
            icon_code, (132, 132), callback, on_error=on_error
        )

    def set_icon(self, image, icon_code):
        if not self.current:
            return

        weather = self.current.get("weather") or [{}]
        if weather[0].get("icon") != icon_code:
            return

        self.icon_image = make_ctk_image(image, (132, 132))
        self.icon_label.configure(image=self.icon_image, text="")
        self.icon_label.image = self.icon_image

    # --------------------------------------------------
    # Forecast icons
    # --------------------------------------------------

    def add_small_icon(self, parent, icon_code, size=(58, 58)):
        def callback(image, code):
            def put_image():
                try:
                    if not parent.winfo_exists():
                        return

                    photo = make_ctk_image(image, size)
                    label = ctk.CTkLabel(
                        parent, text="", image=photo
                    )
                    label.image = photo
                    label.pack(pady=2)
                    self._icon_images.append(photo)
                except Exception:
                    pass

            self.after(0, put_image)

        download_icon(icon_code, size, callback)

    # --------------------------------------------------
    # Forecast within the next six hours
    # --------------------------------------------------

    def show_hourly(self, forecast):
        for child in self.hourly_frame.winfo_children():
            child.destroy()

        now = time.time()
        end_time = now + 6 * 60 * 60

        entries = [
            item for item in forecast.get("list", [])
            if isinstance(item.get("dt"), (int, float))
            and now <= item["dt"] <= end_time
        ]

        if not entries:
            self.make_label(
                self.hourly_frame,
                "No forecast data available for the next six hours.",
                12,
                GREY,
            ).pack(anchor="w", pady=10)
            return

        for item in entries:
            stamp = item["dt"]
            time_text = datetime.fromtimestamp(stamp).strftime("%I %p")
            weather = (item.get("weather") or [{}])[0]

            panel = self.make_panel(self.hourly_frame, 15)
            panel.pack(
                side="left", fill="both", expand=True,
                padx=3, pady=3,
            )

            self.make_label(
                panel, time_text, 11, GREY
            ).pack(pady=(12, 4))

            icon_code = weather.get("icon")
            if icon_code:
                self.add_small_icon(panel, icon_code, (58, 58))

            self.make_label(
                panel,
                weather.get("description", "Unknown").title(),
                10,
                BLUE,
            ).pack(padx=4, pady=3)

            self.make_label(
                panel,
                self.temperature(item.get("main", {}).get("temp")),
                15,
                WHITE,
                "bold",
            ).pack(pady=(5, 12))

    # --------------------------------------------------
    # Five-day forecast
    # --------------------------------------------------

    def show_daily(self, forecast):
        for child in self.daily_frame.winfo_children():
            child.destroy()

        grouped = {}
        for item in forecast.get("list", []):
            dt_txt = item.get("dt_txt", "")
            if not dt_txt:
                continue
            date_key = dt_txt.split(" ")[0]
            grouped.setdefault(date_key, []).append(item)

        today = datetime.now().date()
        future_days = []

        for date_key, entries in sorted(grouped.items()):
            try:
                date_value = datetime.strptime(
                    date_key, "%Y-%m-%d"
                ).date()
            except ValueError:
                continue

            if date_value >= today:
                future_days.append((date_key, entries))

        days = future_days[:5]

        if not days:
            self.make_label(
                self.daily_frame,
                "No five-day forecast data available.",
                12,
                GREY,
            ).pack(anchor="w", pady=10)
            return

        for date_key, entries in days:
            valid_entries = [
                item for item in entries
                if isinstance(item.get("main"), dict)
                and isinstance(item["main"].get("temp"), (int, float))
            ]
            if not valid_entries:
                continue

            low = min(
                item["main"].get("temp_min", item["main"]["temp"])
                for item in valid_entries
            )
            high = max(
                item["main"].get("temp_max", item["main"]["temp"])
                for item in valid_entries
            )

            def get_hour(item):
                try:
                    return int(item["dt_txt"].split()[1][:2])
                except (KeyError, IndexError, ValueError):
                    return 12

            midday = min(
                valid_entries,
                key=lambda item: abs(get_hour(item) - 12),
            )

            day_name = datetime.strptime(
                date_key, "%Y-%m-%d"
            ).strftime("%a, %d %b")

            row = self.make_panel(self.daily_frame, 13)
            row.pack(fill="x", pady=3)

            self.make_label(
                row, day_name, 12, WHITE, "bold"
            ).pack(side="left", padx=14, pady=10)

            weather = (midday.get("weather") or [{}])[0]
            icon_code = weather.get("icon")
            if icon_code:
                self.add_small_icon(row, icon_code, (48, 48))

            self.make_label(
                row,
                weather.get("description", "Unknown").title(),
                12,
                GREY,
            ).pack(side="left", padx=10)

            self.make_label(
                row,
                f"{self.temperature(low)} – {self.temperature(high)}",
                12,
                BLUE,
                "bold",
            ).pack(side="right", padx=14)


if __name__ == "__main__":
    app = SkyCastApp()
    app.mainloop()
