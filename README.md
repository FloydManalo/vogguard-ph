# VogGuard PH

An early-warning idea to help farmers know when volcanic smog (vog) from Taal Volcano is heading toward their farms, so they can wash their crops in time.

Built by Francis Floyd G. Manalo, a 1st-year BS Computer Science student at Batangas State University, for the PhilSA Space Business Innovation Camp (SBIC) 2026.

## The problem
Taal Volcano has been releasing large amounts of sulfur dioxide (SO₂) gas since 2021. The gas mixes with moisture in the air and forms acidic smog called vog, which can damage crops like coffee in Amadeo and pineapple in Silang. A vog episode in September 2023 was reported to cause about ₱1.9 million in agricultural damage in Balete, Batangas (Manila Bulletin).

PHIVOLCS publishes the crater's daily SO₂ output and general Taal-region warnings. But these don't say when vog will reach a specific barangay or farm, because that depends on the wind. Farmers often only notice vog by smell or eye irritation, when it has already arrived.

## Who it's for
LGU agriculture and disaster risk reduction officers in Cavite and Batangas, and farming cooperative leaders. The idea is that local governments pay for the service, so the alerts are free for farmers.

## The idea
VogGuard PH combines the crater's daily SO₂ output, wind forecasts, and barangay locations to work out which barangays are downwind and how soon the vog could arrive. Each barangay gets a Green, Yellow or Red rating, and the alert is sent by SMS to basic phones, so farmers don't need a smartphone or mobile data.

The target is 1 to 3 hours of warning, which is meant to give farmers time to run their pumps or sprinklers. A pineapple farmer quoted in a GMA News report after the 2020 eruption said crops can be saved if washed right away.

Satellite data (Sentinel-5P, through PhilSA's CopPhil) comes into the plan later, to check the predictions against what actually happened. It passes over only once a day, so it can't trigger a morning alert.

## Where I am now
The business concept is written up in my SBIC workbook, where the project is at TRL 1 (research and idea only, no code). I'm now building a small Python prototype to show that the core logic can work with real data.

So far, I can load the barangays of Amadeo, Cavite and show them on a map with the Taal crater. Next is wind data and the downwind check.

## Files
- `inspect_columns.py`: shows the column names in the barangay shapefile
- `extract_barangays.py`: saves one lat/lon point per Amadeo barangay to a CSV
- `plot_map.py`: draws the barangays and the crater on an interactive map
- `data/amadeo_barangays.csv`: the 26 barangays of Amadeo with coordinates

## How to run it
1. Install Python, then run: `pip install geopandas pandas folium requests`
2. Download the barangay boundaries (SHP zip) from data.humdata.org and put the adm4 files in `data/`
3. Run `python extract_barangays.py`, then `python plot_map.py`
4. Open the map from the `outputs/` folder in your browser

## Limits so far
The risk thresholds are not decided yet, the 1 to 3 hour warning is a goal and not a proven result, and nothing has been tested against a real vog event. I haven't interviewed farmers myself yet. The farmer accounts in my workbook come from news reports.

## Data sources
Barangay boundaries from HDX (COD-AB), map background from Esri. Planned: PHIVOLCS Taal bulletins, a weather API, and Sentinel-5P via CopPhil.