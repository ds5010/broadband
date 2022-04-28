'''
Flexible plotting function for gathering broadband tiers 
and plots on a basemap, then saves to img/ directory
'''
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx
from pathlib import Path

def list_files(dir):
    files = []
    for item in dir.iterdir():
        if item.is_file():
            if 'tier' in item.stem:
                files.append(item)
    return files

def plot(lines, state, basemap, cmap, lw, dpi):
    
    # dictionary of basemap tile servers
    tile_urls ={
        'mapnik':'http://a.tile.osm.org/{z}/{x}/{y}.png',
        'hot':'http://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', 
        'arc_darkgray':'http://services.arcgisonline.com/arcgis/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}', 
        'arc_oceanbase': 'http://services.arcgisonline.com/arcgis/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}',
        'arc_worldstreetmap': 'http://services.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
        'arc_imagery': 'http://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        'arc_physical': 'http://services.arcgisonline.com/arcgis/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}',
        'arc_worldtopo': 'http://services.arcgisonline.com/arcgis/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
        'dark': 'http://a.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}.png'
        }
    
    # default cmap matches oberservable map
    if cmap == 'default':
        color_mapping = {
            'Tier 0 (No Address Range)' : '#d73027',
            'Tier 1 (0 - 10/1)': "#f46d43",
            'Tier 2 (10/1 - 25/3)': "#fdae61",
            'Tier 3 (25/3 -50/10)': "#abd9e9",
            'Tier 4 (50/10 - 100/100)': "#4575b4",
            'Tier 5 (> 100M)': "#3462a3",}
        color = lines['v_layer'].map(color_mapping)
        ax = lines.plot(figsize=(8,12), color=color, categorical=True, linewidth=lw, legend=True)
    else:
        ax = lines.plot('v_layer', figsize=(8,12), cmap=cmap, categorical=True, linewidth=lw, legend=True)
        # move legend to bottom right over labels
        leg = ax.get_legend()
        leg.set_bbox_to_anchor((0.85,0.17))    
        leg.set_zorder(100)
    # first basemap provides actual basemap
    cx.add_basemap(ax, source=tile_urls[basemap])
    
    # Some base maps don't include state border
    # add light state boundary on dark basemaps:
    if basemap in ['arc_darkgray', 'arc_imagery', 'dark_nolabel']:
        border_color = 'lightgray'
    # add dark boundary on light basemaps:
    else:
        border_color = '#00222B'
    state.plot(ax=ax, color=border_color, linewidth=1, linestyle='solid')
    
    # turn off borders
    ax.tick_params(axis='both', bottom=False, left=False, labelbottom=False, labelleft=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    plt.tight_layout()
    
    # unique file name with parameters
    save_path = '..//img//' + basemap + '_' + cmap + '_' + '_' + str(lw) +  '_' + str(dpi) + 'dpi.png'

    plt.savefig(save_path, dpi=dpi)
    plt.close('all')

def main():
    zip_dir = Path('../zip/')
    files = list_files(zip_dir)
    # convert CRS to webmercator for using contextlilly basemaps
    lines = gpd.read_file(files[0]).to_crs(3857)
    print(files[0], 'read successfully')
    for file in files[1:]:
        lines = pd.concat([lines, gpd.read_file(file).to_crs(3857)])
        print(file, 'read successfully')

    state = gpd.read_file('../zip/county_boundaries/maine_counties.geojson').dissolve().boundary.to_crs(3857)    
    print('File read complete')
    
    # single plot
    plot(lines, state, 'arc_oceanbase', 'viridis', lw=1, dpi=72)
    plot(lines, state, 'arc_physical', 'default', lw=1, dpi=72)
    plot(lines, state, 'arc_imagery', 'default', lw=1, dpi=72)
    plot(lines, state, 'arc_oceanbase', 'default', lw=1, dpi=72)
    plot(lines, state, 'dark', 'default', lw=1, dpi=72)
    plot(lines, state, 'dark', 'viridis', lw=1, dpi=72)

if __name__ == "__main__":
    main()
