"""Fetch real past wind at the Taal crater for one date and show whether
Amadeo would have been alerted. DATE and FLUX here are only for testing."""
from datetime import datetime, timedelta
import requests
import pandas as pd
from rate_barangays import CRATER_LAT, CRATER_LON
from stability import rate_with_stability


def get_wind_for_range(start_date, end_date):
    resp = requests.get(
        "https://archive-api.open-meteo.com/v1/archive",
        params={
            "latitude": CRATER_LAT,
            "longitude": CRATER_LON,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": "wind_speed_10m,wind_direction_10m",
            "wind_speed_unit": "ms",
            "timezone": "Asia/Manila",
        },
        headers={"User-Agent": "VogGuardPH-student-prototype/0.1"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["hourly"]


if __name__ == "__main__":
    DATE = "2023-09-20"   # replace with a real event date later
    FLUX = 10000          # placeholder (tonnes/day)

    # fetch the chosen day plus the next one, so late-evening alerts can be checked
    next_day = (datetime.strptime(DATE, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    hourly = get_wind_for_range(DATE, next_day)
    times = hourly["time"]
    winds = list(zip(hourly["wind_speed_10m"], hourly["wind_direction_10m"]))

    barangays = pd.read_csv("data/amadeo_barangays.csv")

    alerted_hours = 0
    uncertain_hours = 0
    for i in range(24):
        t = times[i]
        s, d = winds[i]
        if s is None or d is None:
            continue
        result = rate_with_stability(barangays, winds, i, FLUX)
        firm = result[result["rating"].isin(["YELLOW", "RED"])]
        unsure = result[result["rating"] == "UNCERTAIN"]

        if not firm.empty:
            alerted_hours += 1
            earliest = firm["arrival_hours"].min()
            print(t, "| wind from", d, "deg,", s, "m/s | ALERT, arrival ~", earliest, "hr")
        elif not unsure.empty:
            uncertain_hours += 1
            earliest = unsure["arrival_hours"].min()
            print(t, "| wind from", d, "deg,", s, "m/s | UNCERTAIN (~", earliest, "hr)")
        else:
            print(t, "| wind from", d, "deg,", s, "m/s | ok")

    print(f"\nOn {DATE}: {alerted_hours} alert hours, {uncertain_hours} uncertain hours, of 24")