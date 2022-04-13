# broadband

data for the broadband project

## data

More data will be coming our way at some point, so we should be thinking about making updates easy.

Right now, there are 3 data sources:

1. Sewall data -- Okay for public use
* This data comes from a private company -- there are no attributes (probably because of PII issues)
* Poly-line data, tiers zero-five

<img src="figs/image.png" width="400px">

2. Grant rounds data -- NOT FOR PUBLIC USE
* "Fabric" dataset (i.e., points, Lat/Lon) -- These should not be used
* Polygons (eligible areas) -- These *can* be used
* Each datum typically has an address and the connection type (that's the "raw" format)
* These were further processed into "served" (e.g., fiber connection) and "unserved" (e.g., DSL connection)
* These kind of info helps inform program for "last-mile" grants

<img src="figs/image2.png" width="400px">

3. Broadband Investment Zone data -- Okay for public use
* ConnectMaine creates polygons based on point data -- polygons are "eligible areas"
* this is processed data based on grant-rounds data
* unserved or maybe unserved

<img src="figs/image3.png" width="400px">

* Issues
  * No data dictionary
  * No information about processing, need documentation about updates
  * For public visualizations:
    * Sewall -- okay
    * Grand Round -- **NO** - do not use point data!
    * Broadband Investment Zones -- okay

## Related sites

* StoryMap made by Sewall https://storymaps.arcgis.com/stories/c0571d8a3ccb4116acd0f84eb18ad52e
* "Dashboard" made for Waldo County https://experience.arcgis.com/experience/914684b75a1049fabec5e9840ebd7c62

