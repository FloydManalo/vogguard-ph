"""Known-answer tests for the wind-stability check."""
import pandas as pd
from stability import stays_downwind, rate_with_stability

# Wind from 160 degrees blows toward 340, so a barangay at bearing 340 is downwind.
steady = [(5.0, 160)] * 8
assert stays_downwind(340, 1.1, steady, 0)

# Wind turns to 250 (blowing toward 70, away from the barangay) at hour 2
turning = [(5.0, 160), (5.0, 160), (5.0, 250), (5.0, 250), (5.0, 250)]
assert not stays_downwind(340, 2.5, turning, 0)   # smog still travelling at hour 2
assert stays_downwind(340, 1.0, turning, 0)       # smog arrives before the turn

# Near the end of the data we only check the hours we have
assert stays_downwind(340, 5.0, [(5.0, 160), (5.0, 160)], 0)

# A missing reading (None) is skipped, not treated as a crash
assert stays_downwind(340, 2.0, [(5.0, 160), (None, None), (5.0, 160)], 0)

# Full rating: same fake barangay as test_logic.py, about 20 km away
fake = pd.DataFrame([{"barangay": "Test", "lat": 14.17, "lon": 120.92}])
steady_winds = [(5.0, 160)] * 6
turning_winds = [(5.0, 160), (5.0, 250), (5.0, 250), (5.0, 250), (5.0, 250), (5.0, 250)]

assert rate_with_stability(fake, steady_winds, 0, 18638).loc[0, "rating"] == "RED"
assert rate_with_stability(fake, turning_winds, 0, 18638).loc[0, "rating"] == "UNCERTAIN"
assert rate_with_stability(fake, steady_winds, 0, 2000).loc[0, "rating"] == "GREEN"

print("Stability tests passed")