import geopandas as gpd
from pathlib import Path

Maine_County=gpd.read_file('Maine_County_Boundary_Polygons_Dissolved_Feature.geojson')
layers_dict = {'eligible':gpd.read_file('https://raw.githubusercontent.com/ds5010/broadband/master/zipfiles/eligible-areas-2-22-layer-G8qemhB46k7dh-m1XZ2JM.zip'),
'may_unserved':gpd.read_file('https://raw.githubusercontent.com/ds5010/broadband/master/zipfiles/may-be-unserved-layer-gpC0SCaV9wS6W-zZCePjz.zip'),
'may_unserved_density':gpd.read_file('https://raw.githubusercontent.com/ds5010/broadband/master/zipfiles/density-of-unserved-may-be-layer-UKtUhvoEC95KBH6HsnWIU.zip'),
'unserved':gpd.read_file('https://raw.githubusercontent.com/ds5010/broadband/master/zipfiles/unserved-layer-R8i8goNVLFFHfh1Xun4rj.zip'),
'tier_0':gpd.read_file('https://raw.githubusercontent.com/ds5010/broadband/master/zipfiles/tier-0-no-address-range-layer-jLQPM-g3RfNthOkroK_Mf.zip'),
'tier_1':gpd.read_file('https://raw.githubusercontent.com/ds5010/broadband/master/zipfiles/tier-1-0-10-1-layer-2Vbn3XwU7ghduyFrvsX3i.zip'),
'tier_2':gpd.read_file('https://raw.githubusercontent.com/ds5010/broadband/master/zipfiles/tier-2-10-1-25-3-layer-8lhS3piFE8p5Sof4IZ4C0.zip'),
'tier_3':gpd.read_file('https://raw.githubusercontent.com/ds5010/broadband/master/zipfiles/tier-3-25-3-50-10-layer-axu8CkkozyfVxf5kjgcSY.zip'),
'tier_4':gpd.read_file('https://raw.githubusercontent.com/ds5010/broadband/master/zipfiles/tier-4-50-10-100-100-layer--pCgIFfvOkurYcKDZ1Db7.zip'),
'tier_5':gpd.read_file('https://raw.githubusercontent.com/ds5010/broadband/master/zipfiles/tier-5-100-m-layer-zo2lbPrGRte_B5Ug-kEqS.zip')}


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