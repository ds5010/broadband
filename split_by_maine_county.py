import geopandas as gpd
from pathlib import Path

Maine_County=gpd.read_file('Maine_County_Boundary_Polygons_Dissolved_Feature.geojson')
layers_dict = {'elegible':gpd.read_file('raw_data/eligible-areas-2-226PEr9ZEyBEne5G8zrdRmw.geojson'),
'may_unserved':gpd.read_file('raw_data/may-be-unservedveRiwozU-mCkVlnM1I0Ws.geojson'),
'may_unserved_density':gpd.read_file('raw_data/density-of-unserved-may-beEr3WqXHjaEbB1uH91G5er.geojson'),
'unserved':gpd.read_file('raw_data/unservedUEfZlG3Iw4sDF1-p0bhd7.geojson'),
'tier_0':gpd.read_file('raw_data/tier-0-no-address-rangeTpaEYbait8-Yk8cZSlGjw.geojson'),
'tier_1':gpd.read_file('raw_data/tier-1-0-10-1eyO0LU3Hynhs_hq1WOHYo.geojson'),
'tier_2':gpd.read_file('raw_data/tier-2-10-1-25-3OMjm9BbhtUEg_fRDGonen.geojson'),
'tier_3':gpd.read_file('raw_data/tier-3-25-3-50-105YDhz7L_Rz7XU2DzCfkHE.geojson'),
'tier_4':gpd.read_file('raw_data/tier-4-50-10-100-100wodTCY31PZSAamyPHzuOK.geojson'),
'tier_5':gpd.read_file('raw_data/tier-5-100-mDTPWKD7cFoVB_Nm37ynAA.geojson')}

maine_county_dict={}
for i,row in Maine_County.iterrows():
    maine_county_dict[row['COUNTY']]=row.geometry

def store_county_data_to_file(county_name,layers,layer_name):
    data_layer = layers[layer_name]
    data_layer['centroid_column']=data_layer.centroid
    data_layer=data_layer.set_geometry('centroid_column')   
    gdf_list=[]
    for index,i in data_layer.iterrows(): 
        if i.centroid_column.within(maine_county_dict[county_name]):
            gdf_list.append(i)
    gdf=gpd.GeoDataFrame(gdf_list)
    del gdf['centroid_column']
    gdf.set_geometry('geometry')

    gdf.to_file('county/'+county_name+'/'+county_name+'_'+layer_name+'.geojson')

for file in layers_dict:
    for i in maine_county_dict:
        Path("county/"+i+'/').mkdir(parents=True, exist_ok=True)
        store_county_data_to_file(i,layers_dict,file)