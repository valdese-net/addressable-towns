import os, csv, json, sys, subprocess, urllib.parse

# Scratch folder for data files, including the Burke geodatabase, the town addressable lists, and raw geo layers for town boundaries and roads.
datadir = "./_data"

# Dynamic data folder used in the Jeckyll hosting of the map and the addressable town lists.
webdata = "./docs/_data"

# Web assets for the Jeckyll site
webassets = "./docs/assets"

# Dynamic web assets for the Jeckyll site that are generated from this script.
webassetgen = f"{webassets}/dynamic"

# The pmtiles file is a single file that contains all of the layers for the interactive map
fn_pmtiles = f"{webassetgen}/unaddressable.pmtiles"

# The info.json file contains metadata about the unaddressable addresses, including a count of unaddressable addresses by town and the last modified time of the pmtiles file.
fn_infojson = f"{webdata}/info.json"

# Flag to force the regeneration of dynamic files
forcegen = not (os.path.exists(fn_infojson) and os.path.exists(fn_pmtiles))

# Container for info that will be saved in the Jeckyll site `webdata`
site_info = {}

# The Burke NC towns actually span three counties: Burke, Caldwell, and Catawba. All three have ArcGIS endpoints with an address layer.
# We can retrieve address data in geojson format from their ArcGIS REST endpoints.
geojson = {
'burke': {
	'endpt': "https://gis.burkenc.org/arcgis/rest/services/BurkeMapMetricsSP/MapServer/13",
	'query': "(CITYLIM LIKE '%') and (ADDRESS LIKE '%') and (CITY LIKE '%') and (ZIPCODE LIKE '%') and (upper(CITYLIM) <> 'BURKE') and (upper(CITYLIM) <> upper(CITY))",
	'fields': ["CITYLIM","ADDRESS","CITY","ZIPCODE"]
},
'caldwell': {
	'endpt': "https://gis.caldwellcountync.org/arcgis/rest/services/OpenGov/MapServer/0",
	'query': "(City='RHOD') and (upper(AddrCity) not like '%RHODHI%')",
	'fields': ["City","Address","AddrCity","AddrZip"]
},
'catawba': {
	'endpt': "https://arcgis2.catawbacountync.gov/arcgis/rest/services/catawba/Basemap/FeatureServer/0",
	'query': "(MAINTAINED_BY='LV') and (upper(POSTAL_CITY) not like '%LONG%')",
	'fields': ["MAINTAINED_BY","ADDRESS_FULL","POSTAL_CITY","ZIP"]
}}

# The Burke NC geodatabase is a zipped file containing a offline copy of a geodatabase for Burke County, NC.
gis_burke = f"{datadir}/BurkeNC_20260828.gdb.zip"

# The jurisdictional town is abbreviated when arriving from Caldwell or Catawba counties, so we need to translate the town name to the full name for our purposes.
xlateTownAbbreviation = {'LV': 'LONG VIEW', 'RHOD': 'RHODHISS'}

# for each town, maintain a list of addresses that are not properly addressable to the town
class PostalAddress:
	__slots__ = ['LNGLAT','ADDRESS', 'CITY', 'ZIPCODE']
	def __init__(self, lnglat: tuple[float, float], addr: str, city: str, zip: str):
		self.LNGLAT = lnglat
		self.ADDRESS = addr.upper()
		self.CITY = city.upper()
		self.ZIPCODE = zip

byCity: dict[str, list[PostalAddress]] = {}

# Fetch the addresses from the ArcGIS REST endpoint for the given county, store them in a CSV file, and load for further processing.
def fetchWrongTownAddresses(county: str, endpt: str, query: str, fields: list[str]):
	global forcegen
	fn = f"{datadir}/geoAddressable{county.title()}.csv"
	url = f"{endpt}/query?where={urllib.parse.quote(query)}&outFields={urllib.parse.quote(','.join(fields))}&outSR=4326&f=geojson"
	if not os.path.exists(fn):
		subprocess.run(f"ogr2ogr -f CSV -t_srs EPSG:4326 -lco GEOMETRY=AS_XY {fn} \"{url}\" OGRGeoJSON", shell=True)
		forcegen = True
	with open(fn, "r") as file:
		reader = csv.DictReader(file)
		for row in reader:
			lnglat = (row['X'], row['Y'])
			town = row[fields[0]].upper()
			town = xlateTownAbbreviation.get(town, town)
			streetaddress = row[fields[1]].upper()
			postalcity = row[fields[2]].upper()
			zipcode = row[fields[3]]
			byCity.setdefault(town, []).append(PostalAddress(lnglat, streetaddress, postalcity, zipcode))

for county, data in geojson.items():
	fetchWrongTownAddresses(county, **data)

# these are the layers that will be included in the interactive map
mapLayer = {
	'burke': f"{datadir}/burke-boundary.geojson",
	'water': f"{datadir}/BRTA-Water.geojson.gz",
	'townlimits': f"{datadir}/townBoundaries.geojson",
	'roads': f"{datadir}/burkeRoads.geojson",
	'unaddressable': f"{datadir}/geoAddressableBRTA.csv"
}

site_info['unaddressable'] = {} # dictionary of towns with count of unaddressable addresses

byCity = dict(sorted(byCity.items()))

if forcegen or not os.path.exists(mapLayer['unaddressable']):
	with open(mapLayer['unaddressable'], "w", newline='') as out:
		writer = csv.writer(out, quoting=csv.QUOTE_MINIMAL)
		writer.writerow(['X','Y','CITYLIM', 'ADDRESS', 'CITY', 'ZIPCODE'])
		for town, addrs in byCity.items():
			for addr in addrs:
				writer.writerow([addr.LNGLAT[0],addr.LNGLAT[1],town,addr.ADDRESS,addr.CITY,addr.ZIPCODE])

for town, addresses in byCity.items():
	site_info['unaddressable'][town] = len(addresses)

	fn = f"{webdata}/unaddressable/{town}.csv"
	if forcegen or not os.path.exists(fn):
		with open(fn, "w", newline='') as out:
			writer = csv.writer(out, quoting=csv.QUOTE_MINIMAL)
			writer.writerow(['ADDRESS', 'CITY', 'ZIPCODE'])
			for addr in sorted(addresses, key=lambda x: (x.ZIPCODE, x.ADDRESS)):
				writer.writerow([addr.ADDRESS,addr.CITY,addr.ZIPCODE])

if forcegen or not os.path.exists(mapLayer['townlimits']):
	subprocess.run(f"ogr2ogr -f GeoJSON -t_srs EPSG:4326 -select \"NAME\" {mapLayer['townlimits']} {gis_burke} city_limits", shell=True)

if forcegen or not os.path.exists(mapLayer['roads']):
	subprocess.run(f"ogr2ogr -f GeoJSON -t_srs EPSG:4326 -select \"SRNUM,CLASS,FULLNAME\" -where \"(CLASS IS NOT NULL)\" {mapLayer['roads']} {gis_burke} RoadCenterlines", shell=True)

# construct a list of the named pmtiles layers
pmtileLayers = []
for layer, fn in mapLayer.items():
	if os.path.exists(fn):
		pmtileLayers.append(f"--named-layer='{layer}:{fn}'")

# make pmtiles for a map of obstacles to proper addressable towns
make_pmtiles = f"tippecanoe -f -Z8 -z12 -o {fn_pmtiles} {' '.join(pmtileLayers)}"
if forcegen or not os.path.exists(fn_pmtiles):
	subprocess.run(make_pmtiles, shell=True)

site_info['mapmtime'] = os.path.getmtime(fn_pmtiles)

if forcegen or not os.path.exists(fn_infojson):
	with open(fn_infojson, "w") as out:
		json.dump(site_info, out, indent=2)
