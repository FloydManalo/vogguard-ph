import pandas as pd
from rate_barangays import bearing_and_distance, angle_difference, rate_barangays

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

# 4) A fake barangay north-northwest of the crater (like Amadeo)
fake = pd.DataFrame([{"barangay": "Test", "lat": 14.17, "lon": 120.92}])

def rating_for(wind_from, flux):
    return rate_barangays(fake, wind_from, 5.0, flux).loc[0, "rating"]

assert rating_for(160, 18638) == "RED"      # wind blows toward it, high flux
assert rating_for(160, 7000) == "YELLOW"    # wind blows toward it, medium flux
assert rating_for(160, 2000) == "GREEN"     # wind toward it, but low flux
assert rating_for(340, 18638) == "GREEN"    # wind blows away, high flux
assert rating_for(90, 18638) == "GREEN"     # wind from the east

print("All tests passed")