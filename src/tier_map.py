import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import glob

files = glob.glob("src/raw_data/tier-[!0]*")
# print("Found ",files)
tiers = {}
for file in files:
    print("Loading", file)
    tiers[file[13:19]] = gpd.read_file(file)
print("Using", len(tiers), "tiers.")

counties = gpd.read_file('src/county_boundaries/Maine_County_Boundary_Polygons_Dissolved_Feature.geojson')

colors = {
    # "tier-0": "#d73027",
    "tier-1": "#f46d43",
    "tier-2": "#fdae61",
    "tier-3": "#abd9e9",
    "tier-4": "#4575b4",
    "tier-5": "#3462a3"
}

names = {
    # "tier-0": "Tier 0",
    "tier-1": "Tier 1: <10 Mb/s",
    "tier-2": "Tier 2: 10-25 Mb/s",
    "tier-3": "Tier 3: 25-50 Mb/s",
    "tier-4": "Tier 4: 50-100 Mb/s",
    "tier-5": "Tier 5: >100 Mb/s"
}

fig, ax = plt.subplots(figsize=(16,10))

counties.plot(ax = ax, color='none', label="County Border")
c = ax._children[0]
c.set_edgecolors("#000000")
c.set_zorder(2)

for tier, gdf in tiers.items():
    gdf.plot(ax = ax, zorder=0, label=names[tier], color=colors[tier])

handles, labels = ax.get_legend_handles_labels()
ax.legend(reversed(handles), reversed(labels), loc='lower right')
ax.set_axis_off()
fig.savefig("docs/tiers.png", bbox_inches="tight")
fig.savefig("img/tiers.png", bbox_inches="tight")
