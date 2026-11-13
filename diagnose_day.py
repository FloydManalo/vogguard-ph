from datetime import datetime, timedelta
import pandas as pd
from get_past_wind import get_wind_for_range
from back_test import clean_winds
from rate_barangays import rate_barangays, FLUX_RED
from stability import rate_with_stability

DATE = "2024-08-19"

if __name__ == "__main__":
    next_day = (datetime.strptime(DATE, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    hourly = get_wind_for_range(DATE, next_day)
    times = hourly["time"]
    winds = clean_winds(hourly)
    barangays = pd.read_csv("data/amadeo_barangays.csv")

    print(f"Hour-by-hour check for {DATE} (flux set high, so only wind decides)\n")
    print("time              speed  from  in-cone  arrival  result")
    for i in range(24):
        s, d = winds[i]
        if s is None or d is None:
            continue
        raw = rate_barangays(barangays, d, s, FLUX_RED)
        in_cone = raw[raw["rating"] != "GREEN"]
        final = rate_with_stability(barangays, winds, i, FLUX_RED)
        if final["rating"].isin(["YELLOW", "RED"]).any():
            outcome = "ALERT"
        elif (final["rating"] == "UNCERTAIN").any():
            outcome = "UNCERTAIN"
        else:
            outcome = "-"
        arrival = in_cone["arrival_hours"].min() if not in_cone.empty else ""
        print(f"{times[i]}  {s:5.1f}  {d:4.0f}  {len(in_cone):2d}/{len(raw)}   {str(arrival):>6}   {outcome}")