"""Back-test VogGuard on real days listed in data/vog_events.csv.

For each day it asks two questions:
  1) Wind only: did the wind point at Amadeo (steadily, with a trusted arrival time)?
  2) Full model: would the placeholder flux thresholds also have triggered an alert?
Then it compares both answers with what was actually observed."""
from datetime import datetime, timedelta
import pandas as pd
from get_past_wind import get_wind_for_range
from rate_barangays import FLUX_RED
from stability import rate_with_stability


def clean_winds(hourly):
    """Pair up speed and direction. Speeds of 0 are raised to 0.1 m/s so the
    travel-time formula never divides by zero."""
    winds = []
    for s, d in zip(hourly["wind_speed_10m"], hourly["wind_direction_10m"]):
        winds.append((max(s, 0.1) if s is not None else None, d))
    return winds


def hours_with_alert(barangays, winds, flux):
    """Count the hours (out of the first 24) in which at least one barangay
    would be YELLOW or RED."""
    count = 0
    for i in range(24):
        s, d = winds[i]
        if s is None or d is None:
            continue
        result = rate_with_stability(barangays, winds, i, flux)
        if result["rating"].isin(["YELLOW", "RED"]).any():
            count += 1
    return count


def score(results, hours_col, label):
    sub = results.dropna(subset=[hours_col])
    alerted = sub[hours_col] > 0
    happened = sub["observed"] == "yes"
    print(f"\n{label}  ({len(sub)} days scored)")
    print("  caught real events :", int((alerted & happened).sum()), "of", int(happened.sum()))
    print("  missed real events :", int((~alerted & happened).sum()))
    print("  false alarms       :", int((alerted & ~happened).sum()), "of", int((~happened).sum()), "quiet days")


if __name__ == "__main__":
    events = pd.read_csv("data/vog_events.csv")
    barangays = pd.read_csv("data/amadeo_barangays.csv")

    rows = []
    for _, ev in events.iterrows():
        date = ev["date"]
        observed = str(ev.get("amadeo_vog", "unknown")).strip().lower()
        if observed not in ("yes", "no"):
            print(date, "skipped: amadeo_vog is not yes or no")
            continue

        next_day = (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
        winds = clean_winds(get_wind_for_range(date, next_day))
        if len(winds) < 24:
            print(date, "skipped: not enough wind data")
            continue

        wind_only = hours_with_alert(barangays, winds, FLUX_RED)   # flux set high, so only wind decides
        if pd.notna(ev["flux_t_per_day"]):
            full_model = hours_with_alert(barangays, winds, float(ev["flux_t_per_day"]))
        else:
            full_model = None                                       # no flux recorded for this day

        rows.append({
            "date": date,
            "observed": observed,
            "flux": ev["flux_t_per_day"],
            "wind_only_hours": wind_only,
            "full_model_hours": full_model,
        })

    results = pd.DataFrame(rows)
    print()
    print(results.to_string(index=False))

    score(results, "wind_only_hours", "WIND ONLY (does the direction logic match reality?)")
    score(results, "full_model_hours", "FULL MODEL (with placeholder flux thresholds)")

    results.to_csv("outputs/back_test_results.csv", index=False)
    print("\nSaved outputs/back_test_results.csv")
    print("Small sample: these numbers are a first look, not proof.")