# Postal Service Research

## Zip Code Mapping

The postal service does not seem to publish any data details of its routing network, other than its specific
instructions for each address. However, the nconemap.gov site does have some ZIP boundary data if maps are
desired.

- Zip Code Conty Conflicts (not sure what this is, but indicates that ncone has a ZIP boundary layer dataset)
https://www.nconemap.gov/datasets/977e2e6773ad460c95f46c803aa16722_11/explore?filters=eyJjb3VudHkiOlsiQlVSS0UiXX0%3D&location=35.785047%2C-81.658527%2C12

- The ZIP Code GDB is embedded in the following download
https://www.nconemap.gov/documents/d2d4d4e600704d4ebb7d29454f744293/explore

## Rhodhiss Addresses in Caldwell County

There are ArcGIS MapServers for its Address Points:

https://gis.caldwellcountync.org/arcgis/rest/services/OpenGov/MapServer/0
https://arcgis.hickorync.gov/server/rest/services/CaldwellCounty

The City, AddrCity, AddrZip, and Address can be queried from this dataset. Rhodhiss property are coded as City of RHOD. A suitable search for
Rhodhiss addresses that are now considered to be Granite Falls:

`("City" = 'RHOD') AND ("AddrCity" = 'GRANITE FALLS')`

The following link can be used to request a geojson dataset for Rhodhiss:

- https://arcgis.hickorync.gov/server/rest/services/CaldwellCounty/Caldwell_Address_Points/MapServer/0/query?where=City='RHOD'&outFields=*&outSR=4326&f=geojson

Municipal boundaries can be found at:

https://gis.caldwellcountync.org/arcgis/rest/services/BaseMap/MapServer/2

`CITY_NAME='RHODHISS'`

## Long View in Catawba County

GIS service includes a variety of downloads:

https://www.catawbacountync.gov/online-services/datasets/

There is an ArcGIS MapServer at:

https://arcgis2.catawbacountync.gov/arcgis/rest/services/catawba/Basemap/FeatureServer

The addresses for Long View can be extracted by applying the following query where clause to the `Address Point` layer:

- Where: `MAINTAINED_BY='LV'`
- geojson: https://arcgis2.catawbacountync.gov/arcgis/rest/services/catawba/Basemap/FeatureServer/0//query?where=MAINTAINED_BY='LV'&outFields=*&outSR=4326&f=geojson
