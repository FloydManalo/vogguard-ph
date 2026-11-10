"""Check whether the wind stays steady long enough for smog to reach a barangay."""
import pandas as pd
from rate_barangays import (rate_barangays, bearing_and_distance, angle_difference,
                            CRATER_LAT, CRATER_LON, CONE_DEG)


def stays_downwind(bearing, arrival_hours, winds, start):
    """True if the barangay stays inside the downwind cone at every hourly wind
    reading from `start` until the smog should arrive.
    `winds` is a list of (speed, direction) pairs, one per hour."""
    last = min(start + int(arrival_hours), len(winds) - 1)
    for i in range(start, last + 1):
        speed, direction = winds[i]
        if speed is None or direction is None:
            continue
        wind_to = (direction + 180) % 360
        if angle_difference(bearing, wind_to) > CONE_DEG:
            return False
    return True


def rate_with_stability(barangays, winds, start, flux):
    """Rate every barangay for hour `start`, then downgrade YELLOW/RED to
    UNCERTAIN if the wind turns away before the smog could arrive."""
    speed, direction = winds[start]
    result = rate_barangays(barangays, direction, speed, flux)
    for i in range(len(result)):
        if result.loc[i, "rating"] in ("YELLOW", "RED"):
            b = barangays.iloc[i]
            bearing, _ = bearing_and_distance(CRATER_LAT, CRATER_LON, b["lat"], b["lon"])
            if not stays_downwind(bearing, result.loc[i, "arrival_hours"], winds, start):
                result.loc[i, "rating"] = "UNCERTAIN"
    return result