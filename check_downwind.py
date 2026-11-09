import requests
import pandas as pd
from math import radians, degrees, sin, cos, atan2, sqrt

CRATER_LAT, CRATER_LON = 14.002, 120.993
CONE_DEG = 30   # placeholder: how far off the wind line still counts as downwind


def bearing_and_distance(lat1, lon1, lat2, lon2):
    p1, p2 = radians(lat1), radians(lat2)
    dlat = p2 - p1
    dlon = radians(lon2 - lon1)
    y = sin(dlon) * cos(p2)
    x = cos(p1) * sin(p2) - sin(p1) * cos(p2) * cos(dlon)
    bearing = (degrees(atan2(y, x)) + 360) % 360
    a = sin(dlat / 2) ** 2 + cos(p1) * cos(p2) * sin(dlon / 2) ** 2
    distance_km = 6371 * 2 * atan2(sqrt(a), sqrt(1 - a))
    return bearing, distance_km


def angle_difference(a, b):
    """Smallest gap between two compass directions (0 to 180 degrees)."""
    return abs((a - b + 180) % 360 - 180)


def check_downwind(barangays, wind_from, wind_speed):
    wind_to = (wind_from + 180) % 360   # wind is reported as where it comes FROM
    rows = []
    for _, r in barangays.iterrows():
        bearing, distance = bearing_and_distance(CRATER_LAT, CRATER_LON, r["lat"], r["lon"])
        off = angle_difference(bearing, wind_to)
        if off <= CONE_DEG:
            hours = distance * 1000 / wind_speed / 3600
            rows.append({
                "barangay": r["barangay"],
                "distance_km": round(distance, 1),
                "off_line_deg": round(off, 1),
                "arrival_hours": round(hours, 1),
            })
    return pd.DataFrame(rows)


barangays = pd.read_csv("data/amadeo_barangays.csv")

# 1) Real forecast for today
resp = requests.get(
    "https://api.open-meteo.com/v1/forecast",
    params={
        "latitude": CRATER_LAT,
        "longitude": CRATER_LON,
        "hourly": "wind_speed_10m,wind_direction_10m",
        "wind_speed_unit": "ms",
        "timezone": "Asia/Manila",
        "forecast_days": 1,
    },
    headers={"User-Agent": "VogGuardPH-student-prototype/0.1"},
    timeout=30,
)
resp.raise_for_status()
hourly = resp.json()["hourly"]

print("Real forecast for today")
for t, s, d in zip(hourly["time"], hourly["wind_speed_10m"], hourly["wind_direction_10m"]):
    result = check_downwind(barangays, d, s)
    print(t, "| wind from", d, "deg | downwind barangays:", len(result))

# 2) Test scenario: wind that blows straight toward Amadeo
print("\nTest: wind from 160 degrees at 5 m/s")
test = check_downwind(barangays, 160, 5)
print(test.sort_values("arrival_hours").to_string(index=False))