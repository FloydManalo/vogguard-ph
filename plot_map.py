import pandas as pd
import folium

CRATER_LAT, CRATER_LON = 14.002, 120.993

df = pd.read_csv("data/amadeo_barangays.csv")

m = folium.Map(
    location=[14.09, 120.96],
    zoom_start=10,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",
)

title_html = """
<h3 style="position:fixed; top:10px; left:60px; z-index:9999; background:white;
           padding:6px 10px; border-radius:4px; font-family:sans-serif;">
VogGuard PH: Amadeo barangays and Taal main crater
</h3>
"""
m.get_root().html.add_child(folium.Element(title_html))

folium.Marker([CRATER_LAT, CRATER_LON], popup="Taal main crater",
              icon=folium.Icon(color="red", icon="fire")).add_to(m)

for _, r in df.iterrows():
    folium.CircleMarker([r["lat"], r["lon"]], radius=5,
                        popup=r["barangay"], color="blue", fill=True).add_to(m)

m.save("outputs/amadeo_barangays_map.html")
print("Saved outputs/amadeo_barangays_map.html")