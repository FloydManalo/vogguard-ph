# VogGuard PH

An early-warning system concept exploring how farmers can receive localized alerts about volcanic smog (vog) from Taal Volcano, helping them prepare for potential agricultural impacts.

Developed by **Francis Floyd G. Manalo**, a 1st-year BS Computer Science student at **Batangas State University - Alangilan**, as an independent project that began during the **PhilSA Space Business Innovation Camp (SBIC) 2026**.

## The Problem

Taal Volcano releases sulfur dioxide (SO₂), which can react with moisture and other substances in the atmosphere to form volcanic smog, commonly known as vog. Volcanic activity can also produce ashfall, which may affect crops and disrupt agricultural activities.

Farmers in communities surrounding Taal may experience different volcanic hazards depending on their location and environmental conditions.

PHIVOLCS provides information about Taal Volcano's activity, including daily SO₂ emission measurements and volcanic bulletins. However, translating these sources into useful, localized information for individual farming communities remains a challenge.

VogGuard PH explores how volcanic, weather, and geographic data can be combined to provide more localized agricultural warnings.

## The Idea

VogGuard PH aims to combine:

- **SO₂ emission data** - Daily sulfur dioxide measurements from Taal Volcano.
- **Wind and weather data** - Wind direction and forecasts to help estimate possible downwind areas.
- **Geographic data** - Barangay boundaries and locations of agricultural communities.
- **Satellite observations** - Additional monitoring and validation using Sentinel-5P data.

The proposed system would estimate which barangays may be affected based on available environmental data and assign a **Green, Yellow, or Red** risk classification.

Warnings could then be distributed through SMS, allowing farmers to receive updates without requiring a smartphone or mobile data connection.

The initial goal is to explore whether the system could provide **1–3 hours of advance warning**. This is a development target, not yet a demonstrated capability.

Sentinel-5P observations, potentially accessed through PhilSA's Copernicus Philippines (CopPhil), are also being considered for monitoring and retrospective validation. Since satellite observations are not continuously available, they would not serve as the sole trigger for immediate alerts.

## Preliminary Field Research

Initial field interviews were conducted during **Calabarzon Cacao and Coffee Congress 2026**, held at the **Batangas Province Events Center** on November 12, 2026.

The event provided me an opportunity to speak with representatives of agricultural organizations and cooperatives about their experiences with Taal Volcano, agricultural impacts, existing warning channels, and possible solutions.

The interviews were conducted during the second day of the two-day event. Most of the exhibitors I encountered appeared to be from Batangas. Although there were designated stalls for Cavite and Rizal, these were unoccupied when I visited. This limited my opportunity to gather perspectives from agricultural communities in those areas.

### Organizations Interviewed

**1. BAMAHGACO - San Pascual, Batangas**

- Reported limited agricultural impact from Taal Volcano due to their location.
- Recalled the 2020 eruption, when crops were covered with white ash.
- No specific information about their warning and update channels was obtained.

**2. San Jose Workers Multi-Purpose Cooperative**

- Recalled ashfall events associated with Taal Volcano and reported that these affected their crops and farming activities.
- Reported receiving updates through SMS alerts, Facebook, and similar channels.
- Suggested that protective tents or coverings against ashfall could help protect agricultural crops.

### Initial Observations

- **Agricultural impacts:** The respondents mainly recalled ashfall events and their effects on crops and farming activities.
- **Vog awareness:** Respondents were generally more familiar with ashfall than with the term vog. This does not necessarily mean they have never experienced vog, as they may describe or recognize volcanic haze differently.
- **Existing warning channels:** SMS alerts and Facebook are already being used by at least one interviewed cooperative to receive updates.
- **Additional farmer needs:** The suggestion of protective tents or coverings highlights that physical crop protection may also be an important concern, alongside early-warning information.

### Research Limitations

These interviews provide preliminary firsthand information about agricultural concerns and existing warning channels. However, the findings do not yet establish the extent of vog-specific agricultural impacts or validate the need for a dedicated vog early-warning system.

The interviews were conducted opportunistically during an agricultural exhibit and involved only two organizations. The limited availability of exhibitors from Cavite and Rizal also meant that perspectives from some of the intended target communities were not gathered.

Further interviews, particularly with agricultural communities in Amadeo and Silang, Cavite, are needed to better understand farmers' experiences with vog, ashfall, and existing warning systems.

These findings are preliminary and should not be treated as representative of all agricultural communities surrounding Taal Volcano.

## Current Development Progress

The business concept was initially documented in my SBIC 2026 workbook, where it was classified at **Technology Readiness Level (TRL) 1**.

Development has since progressed into an early geospatial prototype.

### Completed

- Downloaded and inspected Philippine administrative boundary shapefiles.
- Used GeoPandas to extract barangay geographic information for Amadeo, Cavite.
- Generated a CSV containing coordinates for Amadeo's 26 barangays.
- Created an interactive HTML map displaying the barangays and Taal Volcano's crater location.
- Conducted preliminary field interviews with agricultural organizations.

### Next Steps

- Integrate wind direction and weather data.
- Explore a basic downwind estimation method.
- Investigate how SO₂ emission measurements could contribute to risk estimation.
- Develop an initial barangay-level risk classification.
- Test the approach against historical volcanic events and available observations.
- Explore SMS alert integration.

**Current limitation:** The existing prototype focuses on geographic data preparation and visualization. It does not yet perform vog forecasting, risk classification, or SMS alert delivery.

## Project Files

| File | Description |
|---|---|
| `inspect_columns.py` | Shows the column names in the barangay shapefile. |
| `extract_barangays.py` | Extracts one representative latitude/longitude point per Amadeo barangay into a CSV. |
| `plot_map.py` | Generates an interactive map of the barangays and Taal crater. |
| `data/amadeo_barangays.csv` | Contains geographic coordinates for Amadeo's 26 barangays. |

## How to Run

### 1. Install Python

Make sure Python is installed on your computer.

### 2. Install the Required Packages

```bash
pip install geopandas pandas folium requests
```

### 3. Download the Barangay Boundaries

Download the administrative boundary shapefile (SHP ZIP) from [HDX](https://data.humdata.org/) and place the required administrative boundary files inside the `data/` folder.

### 4. Extract the Barangay Information

```bash
python extract_barangays.py
```

### 5. Generate the Interactive Map

```bash
python plot_map.py
```

### 6. View the Map

Open the generated HTML file from the `outputs/` folder in your browser.

## Data Sources

### Currently Used

- **HDX - Common Operational Datasets (COD-AB):** Administrative boundaries used for geographic data extraction.
- **Esri:** Interactive map basemap.

### Planned Data Sources

- **PHIVOLCS:** Taal Volcano bulletins and SO₂ emission measurements.
- **Weather API:** Wind direction and weather information.
- **PhilSA Copernicus Philippines (CopPhil):** Sentinel-5P satellite observations.

## Project Status

VogGuard PH is an early-stage, independently developed student project.

Its current focus is on geographic data preparation, preliminary field research, and exploring the feasibility of localized volcanic hazard warnings for agricultural communities.

The concept, technical approach, and proposed warning capabilities are still under development.

---