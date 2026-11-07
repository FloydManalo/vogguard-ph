import geopandas as gpd

path = "data/phl_admin4.shp"
preview = gpd.read_file(path, rows=5)
print(preview.columns)