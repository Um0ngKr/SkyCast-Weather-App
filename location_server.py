import logging
import socket
import threading
import webbrowser

from flask import Flask, jsonify, render_template_string, request
from werkzeug.serving import make_server


app = Flask(__name__)

HOST = "127.0.0.1"
PORT = 8765
LOCATION_URL = f"http://{HOST}:{PORT}/"

location_data = None
location_event = threading.Event()
location_lock = threading.Lock()
server_lock = threading.Lock()
server_instance = None
server_ready = threading.Event()


HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>SkyCast Location Access</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px 20px;
            background: #101411;
            color: #F5F5EC;
        }

        h2 {
            color: #D5F27A;
        }

        p {
            color: #AEB5A7;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <h2>SkyCast Location Access</h2>
    <p id="status">Waiting for location permission...</p>

    <script>
        const statusText = document.getElementById("status");

        if (!navigator.geolocation) {
            statusText.textContent =
                "Geolocation is not supported by this browser.";
        } else {
            navigator.geolocation.getCurrentPosition(
                async (position) => {
                    statusText.textContent =
                        "Location received. Sending it to SkyCast...";

                    try {
                        const response = await fetch("/set-location", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({
                                latitude: position.coords.latitude,
                                longitude: position.coords.longitude,
                                accuracy: position.coords.accuracy
                            })
                        });

                        if (!response.ok) {
                            throw new Error("Location submission failed.");
                        }

                        statusText.textContent =
                            "Location received successfully. Return to SkyCast.";
                    } catch (error) {
                        statusText.textContent =
                            "Could not send the location to SkyCast. Please try again.";
                    }
                },
                (error) => {
                    if (error.code === 1) {
                        statusText.textContent =
                            "Location permission was denied. Allow location access in browser settings.";
                    } else if (error.code === 2) {
                        statusText.textContent =
                            "Location is unavailable. Check your device location settings.";
                    } else {
                        statusText.textContent =
                            "Location request timed out. Please try again.";
                    }
                },
                {
                    enableHighAccuracy: true,
                    timeout: 25000,
                    maximumAge: 0
                }
            );
        }
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_PAGE)


@app.route("/health")
def health():
    return jsonify({"status": "ready"})


@app.route("/set-location", methods=["POST"])
def set_location():
    global location_data

    data = request.get_json(silent=True) or {}

    try:
        latitude = float(data["latitude"])
        longitude = float(data["longitude"])
        accuracy = data.get("accuracy")

        if not (-90 <= latitude <= 90):
            return jsonify({"error": "Invalid latitude."}), 400

        if not (-180 <= longitude <= 180):
            return jsonify({"error": "Invalid longitude."}), 400

        with location_lock:
            location_data = {
                "latitude": latitude,
                "longitude": longitude,
                "accuracy": accuracy,
            }
            location_event.set()

        return jsonify({"success": True})

    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid coordinates."}), 400


def _port_is_available():
    try:
        with socket.create_connection(
            (HOST, PORT), timeout=0.3
        ):
            return False
    except OSError:
        return True


def start_location_server():
    global server_instance

    with server_lock:
        if server_ready.is_set():
            return

        if not _port_is_available():
            # The server may already be running in another process.
            try:
                import requests

                response = requests.get(
                    f"{LOCATION_URL}health",
                    timeout=1,
                )
                if response.ok:
                    server_ready.set()
                    return
            except Exception:
                pass

            raise RuntimeError(
                "Port 8765 is already in use by another application."
            )

        logging.getLogger("werkzeug").setLevel(logging.ERROR)

        try:
            server_instance = make_server(HOST, PORT, app)
        except OSError as exc:
            raise RuntimeError(
                f"Could not start the location server: {exc}"
            ) from exc

        def serve():
            try:
                server_instance.serve_forever()
            finally:
                server_ready.clear()

        threading.Thread(
            target=serve,
            daemon=True,
        ).start()

        server_ready.set()


def request_location(timeout=60):
    global location_data

    start_location_server()

    with location_lock:
        location_data = None
        location_event.clear()

    try:
        webbrowser.open(LOCATION_URL)
    except Exception as exc:
        raise RuntimeError(
            "Could not open the browser. Visit "
            f"{LOCATION_URL} manually."
        ) from exc

    if location_event.wait(timeout):
        with location_lock:
            if location_data is not None:
                return location_data

    raise RuntimeError(
        "Location was not received within the time limit. "
        "Allow browser location access and try again."
    )


if __name__ == "__main__":
    start_location_server()
    print(f"Location server ready at {LOCATION_URL}")
    threading.Event().wait()