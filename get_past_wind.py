import requests
import pandas as pd
from rate_barangays import rate_barangays, CRATER_LAT, CRATER_LON


def get_wind_for_date(date):
    resp = requests.get(
        "https://archive-api.open-meteo.com/v1/archive",
        params={
            "latitude": CRATER_LAT,
            "longitude": CRATER_LON,
            "start_date": date,
            "end_date": date,
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

    barangays = pd.read_csv("data/amadeo_barangays.csv")
    hourly = get_wind_for_date(DATE)

    alerted_hours = 0
    uncertain_hours = 0
    for t, s, d in zip(hourly["time"], hourly["wind_speed_10m"], hourly["wind_direction_10m"]):
        if s is None or d is None:
            continue
        result = rate_barangays(barangays, d, s, FLUX)
        firm = result[result["rating"].isin(["YELLOW", "RED"])]
        unsure = result[result["rating"] == "UNCERTAIN"]

        if not firm.empty:
            alerted_hours += 1
            earliest = firm["arrival_hours"].min()
            print(t, "| wind from", d, "deg,", s, "m/s | ALERT, arrival ~", earliest, "hr")
        elif not unsure.empty:
            uncertain_hours += 1
            earliest = unsure["arrival_hours"].min()
            print(t, "| wind from", d, "deg,", s, "m/s | UNCERTAIN, wind too light (~", earliest, "hr)")
        else:
            print(t, "| wind from", d, "deg,", s, "m/s | ok")

    print(f"\nOn {DATE}: {alerted_hours} alert hours, {uncertain_hours} uncertain hours, of 24")