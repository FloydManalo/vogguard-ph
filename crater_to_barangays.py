import pandas as pd
from math import radians, degrees, sin, cos, atan2, sqrt

CRATER_LAT, CRATER_LON = 14.002, 120.993


def bearing_and_distance(lat1, lon1, lat2, lon2):
    p1, p2 = radians(lat1), radians(lat2)
    dlat = p2 - p1
    dlon = radians(lon2 - lon1)

    # compass direction from point 1 to point 2 (0 = north, 90 = east)
    y = sin(dlon) * cos(p2)
    x = cos(p1) * sin(p2) - sin(p1) * cos(p2) * cos(dlon)
    bearing = (degrees(atan2(y, x)) + 360) % 360

    # straight-line distance in km over the curved earth
    a = sin(dlat / 2) ** 2 + cos(p1) * cos(p2) * sin(dlon / 2) ** 2
    distance_km = 6371 * 2 * atan2(sqrt(a), sqrt(1 - a))
    return bearing, distance_km


df = pd.read_csv("data/amadeo_barangays.csv")

rows = []
for _, r in df.iterrows():
    bearing, distance = bearing_and_distance(CRATER_LAT, CRATER_LON, r["lat"], r["lon"])
    rows.append({
        "barangay": r["barangay"],
        "bearing_deg": round(bearing, 1),
        "distance_km": round(distance, 1),
    })

result = pd.DataFrame(rows).sort_values("distance_km")
print(result.to_string(index=False))