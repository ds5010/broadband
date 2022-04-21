import geopandas
cumberland = geopandas.read_file(
    'https://raw.githubusercontent.com/ds5010/broadband/main/county/Cumberland/Cumberland_elegible.geojson')

cumberland.columns
cumberland['#Total Subscribers'] = cumberland['#Total Subscribers'].astype(
    'int64')

a = cumberland.explore(
    column="#Total Subscribers",  # make choropleth based on "BoroName" column
    scheme="naturalbreaks",  # use mapclassify's natural breaks scheme
    legend=True,  # show legend
    cmap="Reds",
    k=10,  # use 10 bins
    legend_kwds=dict(colorbar=False),  # do not use colorbar
)
a.save('prototype_cumberland.html')
