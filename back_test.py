"""Back-test VogGuard on real days listed in data/vog_events.csv.

For each day it measures three things:
  1) in_cone_hours   : hours the wind pointed at Amadeo (direction only)
  2) wind_only_hours : hours with a firm alert, after the speed and stability rules
  3) full_model_hours: firm-alert hours when the day's real flux is also used
Then it compares them with what was actually observed."""
from datetime import datetime, timedelta
import pandas as pd
from get_past_wind import get_wind_for_range
from rate_barangays import rate_barangays, FLUX_RED
from stability import rate_with_stability


def clean_winds(hourly):
    """Pair up speed and direction. Speeds of 0 are raised to 0.1 m/s so the
    travel-time formula never divides by zero."""
    winds = []
    for s, d in zip(hourly["wind_speed_10m"], hourly["wind_direction_10m"]):
        winds.append((max(s, 0.1) if s is not None else None, d))
    return winds


def hours_in_cone(barangays, winds):
    """Count hours (out of the first 24) when the wind points at one or more
    barangays, ignoring speed, arrival time and stability."""
    count = 0
    for i in range(24):
        s, d = winds[i]
        if s is None or d is None:
            continue
        result = rate_barangays(barangays, d, s, FLUX_RED)
        if (result["rating"] != "GREEN").any():
            count += 1
    return count


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

        in_cone = hours_in_cone(barangays, winds)
        wind_only = hours_with_alert(barangays, winds, FLUX_RED)   # flux set high, so only wind decides
        if pd.notna(ev["flux_t_per_day"]):
            full_model = hours_with_alert(barangays, winds, float(ev["flux_t_per_day"]))
        else:
            full_model = None                                       # no flux recorded for this day

        rows.append({
            "date": date,
            "observed": observed,
            "flux": ev["flux_t_per_day"],
            "in_cone_hours": in_cone,
            "wind_only_hours": wind_only,
            "full_model_hours": full_model,
        })

    results = pd.DataFrame(rows)

    if results["observed"].nunique() < 2:
        print("\nWARNING: every day is labeled the same ('" + results["observed"].iloc[0] + "').")
        print("False alarms can't be measured. Check the amadeo_vog column in data/vog_events.csv.")

    print()
    print(results.to_string(index=False))

    print("\nAverage hours the wind pointed at Amadeo (out of 24):")
    print(results.groupby("observed")["in_cone_hours"].mean().round(1).to_string())

    score(results, "wind_only_hours", "WIND ONLY (after speed and stability rules)")
    score(results, "full_model_hours", "FULL MODEL (with placeholder flux thresholds)")

    results.to_csv("outputs/back_test_results.csv", index=False)
    print("\nSaved outputs/back_test_results.csv")
    print("Small sample: these numbers are a first look, not proof.")