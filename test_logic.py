import pandas as pd
from rate_barangays import bearing_and_distance, angle_difference, rate_barangays, make_sms

# 1) Angles must wrap around the compass
assert angle_difference(350, 10) == 20
assert angle_difference(10, 350) == 20
assert angle_difference(90, 90) == 0

# 2) One degree north of the equator is ~111 km, due north (bearing 0)
b, d = bearing_and_distance(0, 0, 1, 0)
assert abs(b - 0) < 0.1 and abs(d - 111.2) < 1

# 3) Due east is bearing 90
b, d = bearing_and_distance(0, 0, 0, 1)
assert abs(b - 90) < 0.1

# 4) A fake barangay north-northwest of the crater (like Amadeo), ~20 km away
fake = pd.DataFrame([{"barangay": "Test", "lat": 14.17, "lon": 120.92}])


def rating_for(wind_from, flux, speed=5.0):
    return rate_barangays(fake, wind_from, speed, flux).loc[0, "rating"]


assert rating_for(160, 18638) == "RED"      # wind blows toward it, high flux
assert rating_for(160, 7000) == "YELLOW"    # wind blows toward it, medium flux
assert rating_for(160, 2000) == "GREEN"     # wind toward it, but low flux
assert rating_for(340, 18638) == "GREEN"    # wind blows away, high flux
assert rating_for(90, 18638) == "GREEN"     # wind from the east

# 5) Low-confidence rule: slow wind means a long, untrustworthy travel time
assert rating_for(160, 18638, speed=2.0) == "RED"        # ~2.8 hr, still trusted
assert rating_for(160, 18638, speed=1.8) == "UNCERTAIN"  # ~3.1 hr, over the cutoff
assert rating_for(160, 18638, speed=0.5) == "UNCERTAIN"  # ~11 hr
assert rating_for(160, 2000, speed=0.5) == "GREEN"       # low flux stays GREEN
assert rating_for(340, 18638, speed=0.5) == "GREEN"      # blowing away stays GREEN

# 6) SMS messages: right label, and short enough for one text (160 characters)
for rating in ("RED", "YELLOW", "UNCERTAIN", "GREEN"):
    sms = make_sms("Test", rating, 1.5)
    assert len(sms) <= 160
assert "RED" in make_sms("Test", "RED", 1.5)
assert "YELLOW" in make_sms("Test", "YELLOW", 1.5)

print("All tests passed")