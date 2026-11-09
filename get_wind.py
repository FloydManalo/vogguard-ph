import requests

CRATER_LAT, CRATER_LON = 14.002, 120.993

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": CRATER_LAT,
    "longitude": CRATER_LON,
    "hourly": "wind_speed_10m,wind_direction_10m",
    "wind_speed_unit": "ms",
    "timezone": "Asia/Manila",
    "forecast_days": 1,
}
headers = {"User-Agent": "VogGuardPH-student-prototype/0.1"}

r = requests.get(url, params=params, headers=headers, timeout=30)
r.raise_for_status()
data = r.json()

times = data["hourly"]["time"]
speeds = data["hourly"]["wind_speed_10m"]
directions = data["hourly"]["wind_direction_10m"]

for t, s, d in zip(times, speeds, directions):
    print(f"{t}   speed = {s} m/s   wind from = {d} degrees")