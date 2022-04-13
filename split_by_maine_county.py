import geopandas as gpd
Maine_County=gpd.read_file('Maine_County_Boundary_Polygons_Dissolved_Feature.geojson')
Street_level=gpd.read_file('eligible-areas-2-22-layer-G8qemhB46k7dh-m1XZ2JM.zip')

maine_county_dict={}
for i,row in Maine_County.iterrows():
    maine_county_dict[row['COUNTY']]=row.geometry
maine_county_dict

Street_level['centroid_column']=Street_level.centroid
Street_level=Street_level.set_geometry('centroid_column')

def store_county_street_to_file_v2(county_name):   
    gdf_list=[]
    for index,i in Street_level.iterrows(): 
        if i.centroid_column.within(maine_county_dict[county_name]):
            gdf_list.append(i)
            count+=1
    gdf=gpd.GeoDataFrame(gdf_list)
    del gdf['centroid_column']
    gdf.set_geometry('geometry')
    gdf.to_file('county/'+county_name+'.geojson')
    
for i in maine_county_dict:
    store_county_street_to_file_v2(i)