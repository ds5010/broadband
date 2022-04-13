# Query URL figured out from the census website (steep learning curve)
query = "https://api.census.gov/data/2020/dec/pl?get=NAME,COUNTY,P1_001N&for=county:*&in=state:23"

# Query that URL
import urllib3
http = urllib3.PoolManager()
r = http.request('GET', query)

# Decode the data and unload it as json
import json
data = json.loads(r.data.decode('utf-8'))

# Transfer json into a pandas dataframe
import pandas as pd
df = pd.DataFrame(data[1:], columns=data[0])
df["COUNTY"] = df["NAME"].str.split(" County", expand=True)[0]

# Load the geopandas counties and merge the pandas dataframe in
import geopandas as gpd
counties = gpd.read_file("geojson/Maine_County_Boundary_Polygons_Dissolved_Feature.geojson")
counties_df = counties.merge(df, on="COUNTY") # Note: You should always run .merge() on the geodataframe not the pandas dataframe
counties_df.to_file("geojson/Maine_County_Boundary_Polygons_Dissolved_Feature_Census_Merge.geojson", driver='GeoJSON')
