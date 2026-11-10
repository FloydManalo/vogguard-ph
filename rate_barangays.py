import pandas as pd
from math import radians, degrees, sin, cos, atan2, sqrt

CRATER_LAT, CRATER_LON = 14.002, 120.993
CONE_DEG = 30            # placeholder: how far off the wind line still counts as downwind
FLUX_YELLOW = 5000       # placeholder (tonnes/day), not from a source
FLUX_RED = 10000         # placeholder (tonnes/day), not from a source
MAX_RELIABLE_HOURS = 3   # placeholder: arrival estimates longer than this are not trusted


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
    return abs((a - b + 180) % 360 - 180)


def rate_barangays(barangays, wind_from, wind_speed, flux):
    wind_to = (wind_from + 180) % 360
    rows = []
    for _, r in barangays.iterrows():
        bearing, distance = bearing_and_distance(CRATER_LAT, CRATER_LON, r["lat"], r["lon"])
        downwind = angle_difference(bearing, wind_to) <= CONE_DEG
        hours = round(distance * 1000 / wind_speed / 3600, 1)

        if not downwind or flux < FLUX_YELLOW:
            rating = "GREEN"
        elif hours > MAX_RELIABLE_HOURS:
            rating = "UNCERTAIN"
        elif flux >= FLUX_RED:
            rating = "RED"
        else:
            rating = "YELLOW"

        rows.append({"barangay": r["barangay"], "rating": rating, "arrival_hours": hours})
    return pd.DataFrame(rows)


def make_sms(barangay, rating, hours):
    if rating == "RED":
        return f"VogGuard RED: Taal vog may reach {barangay} in ~{hours} hr. Run sprinklers or hoses now."
    if rating == "YELLOW":
        return f"VogGuard YELLOW: Taal vog may reach {barangay} in ~{hours} hr. Prepare pumps and hoses."
    if rating == "UNCERTAIN":
        return f"VogGuard NOTICE: Taal vog possible at {barangay} but wind is light, so timing is unclear. Watch for haze."
    return f"VogGuard GREEN: no vog expected at {barangay}."


if __name__ == "__main__":
    barangays = pd.read_csv("data/amadeo_barangays.csv")

    scenarios = [
        ("Today-like wind, high flux", 50, 5.0, 18638),
        ("Wind toward Amadeo, low flux", 160, 5.0, 2000),
        ("Wind toward Amadeo, medium flux", 160, 5.0, 7000),
        ("Wind toward Amadeo, high flux", 160, 5.0, 18638),
        ("Light wind toward Amadeo, high flux", 160, 1.0, 18638),
        ("Weak wind toward Amadeo, high flux", 160, 1.6, 18638),
    ]

    for name, wind_from, wind_speed, flux in scenarios:
        result = rate_barangays(barangays, wind_from, wind_speed, flux)
        print(f"\n{name}: wind from {wind_from} deg, {wind_speed} m/s, flux {flux} t/day")
        print(result["rating"].value_counts().to_string())

        alerts = result[result["rating"] != "GREEN"].sort_values("arrival_hours")
        if not alerts.empty:
            first = alerts.iloc[0]
            sms = make_sms(first["barangay"], first["rating"], first["arrival_hours"])
            print("Sample SMS:", sms, f"({len(sms)} characters)")