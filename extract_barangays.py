import geopandas as gpd

path = "data/phl_admin4.shp"
MUNI_COL = "adm3_name"
BRGY_COL = "adm4_name"

amadeo = gpd.read_file(path, where=f"{MUNI_COL} LIKE '%Amadeo%'")
print("Rows loaded:", len(amadeo))
print("Province(s) found:", amadeo["adm2_name"].unique())

pts = amadeo.to_crs(epsg=32651).geometry.representative_point().to_crs(epsg=4326)
amadeo["lat"] = pts.y
amadeo["lon"] = pts.x

out = amadeo[[BRGY_COL, "lat", "lon"]].rename(columns={BRGY_COL: "barangay"})
out.to_csv("data/amadeo_barangays.csv", index=False)
print(out)
print("Count:", len(out))