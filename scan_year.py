"""Scan a whole year of wind: on how many days does the wind point at Amadeo,
and where do the known vog days rank? Direction only (no flux, no speed rules)."""
import pandas as pd
from get_past_wind import get_wind_for_range
from rate_barangays import bearing_and_distance, angle_difference, CRATER_LAT, CRATER_LON, CONE_DEG

YEAR = 2024

if __name__ == "__main__":
    barangays = pd.read_csv("data/amadeo_barangays.csv")
    bearings = [bearing_and_distance(CRATER_LAT, CRATER_LON, r["lat"], r["lon"])[0]
                for _, r in barangays.iterrows()]

    hourly = get_wind_for_range(f"{YEAR}-01-01", f"{YEAR}-12-31")

    rows = []
    for t, s, d in zip(hourly["time"], hourly["wind_speed_10m"], hourly["wind_direction_10m"]):
        if s is None or d is None:
            continue
        wind_to = (d + 180) % 360
        pointing = any(angle_difference(b, wind_to) <= CONE_DEG for b in bearings)
        rows.append({"date": t[:10], "pointing": pointing, "speed": s})

    hours = pd.DataFrame(rows)
    daily = hours.groupby("date").agg(in_cone_hours=("pointing", "sum"),
                                      mean_speed=("speed", "mean"))
    daily["in_cone_hours"] = daily["in_cone_hours"].astype(int)
    n = len(daily)

    print(f"Days scanned in {YEAR}: {n}")
    for k in (1, 6, 9):
        print(f"  days with at least {k:2d} hours pointing at Amadeo: {(daily['in_cone_hours'] >= k).sum()}")

    events = pd.read_csv("data/vog_events.csv")
    print(f"\nKnown events from vog_events.csv in {YEAR}:")
    for _, ev in events.iterrows():
        date = str(ev["date"])
        if date.startswith(str(YEAR)) and date in daily.index:
            h = int(daily.loc[date, "in_cone_hours"])
            rank = int((daily["in_cone_hours"] > h).sum()) + 1
            print(f"  {date}  label={str(ev['amadeo_vog']):7s} hours={h:2d}  rank {rank} of {n}")

    top = daily.sort_values("in_cone_hours", ascending=False).head(15)
    print("\nDays when the wind pointed at Amadeo the most:")
    print(top.round(1).to_string())

    daily.round(1).to_csv(f"outputs/scan_{YEAR}.csv")
    print(f"\nSaved outputs/scan_{YEAR}.csv")