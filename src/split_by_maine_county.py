'''
Python script to take statewide layers of broadband data in geoJSON, 
including polygons, lines, and points, then split into county-level directories   
'''

import geopandas as gpd
from pathlib import Path

# returns list of files within directory
def list_files(dir):
    files = []
    for item in dir.iterdir():
        if item.is_file():
            files.append(item)
    return files

def get_files(list):
    layers_dict = {}
    for file in list:
        layers_dict[file.stem] = gpd.read_file(file)
        print(file.name, " read successfully")
    return layers_dict

def store_county_data_to_file(county_dict, county_name,layers,layer_name):
    data_layer = layers[layer_name]
    data_layer['centroid_column']=data_layer.centroid
    data_layer=data_layer.set_geometry('centroid_column')   
    gdf_list=[]
    for index,i in data_layer.iterrows(): 
        if i.centroid_column.within(county_dict[county_name]):
            gdf_list.append(i)
    gdf=gpd.GeoDataFrame(gdf_list)
    del gdf['centroid_column']
    gdf.set_geometry('geometry')

    gdf.to_file('../county/'+county_name+'/'+county_name+'_'+layer_name+'.geojson')

def main():
    # zip director is location of all raw data
    zip_dir = Path('../zip/')
    # county path is used to split up raw data into county-based subdirectories
    county_path= Path('../zip/county_boundaries/maine_counties.geojson')

    # Dissolve groups all the polygons in the same county and creates a multipolygon for each county
    # COUNTY column becomes the index
    county_polygons=gpd.read_file(county_path).dissolve(by='COUNTY', aggfunc='sum')
    county_dict={}
    for county,row in county_polygons.iterrows():
        county_dict[county]=row.geometry
    
    layers_dict = get_files(list_files(zip_dir))
    for file in layers_dict:
        for i in county_dict:
            Path("../county/"+i+'/').mkdir(parents=True, exist_ok=True)
            store_county_data_to_file(county_dict,i,layers_dict,file)

if __name__ == '__main__':
    main()
