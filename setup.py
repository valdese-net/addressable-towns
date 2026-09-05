import os, csv, json, subprocess

datadir = "./_data"
webdata = "./docs/_data"
webassets = "./docs/assets"
webassetgen = f"{webassets}/dynamic"
gisdata = f"{datadir}/BurkeNC_20260828.gdb.zip"
fn_rawunaddressable = f"{datadir}/nonaddressable.csv"
fn_townlimits = f"{datadir}/townBoundaries.geojson"
fn_roads = f"{datadir}/burkeRoads.geojson"
fn_pmtiles = f"{webassetgen}/unaddressable.pmtiles"
fn_infojson = f"{webdata}/info.json"
force_pmtiles = False
info = {}
info['unaddressable'] = {} # dictionary of towns with count of unaddressable addresses

make_wrongaddresscsv = f"""
ogr2ogr -f CSV -t_srs EPSG:4326 -lco GEOMETRY=AS_XY \
-select "ADDRESS,CITY,CITYLIM,ZIPCODE" \
-where "(ADDRESS IS NOT NULL) and (CITY IS NOT NULL) and (ZIPCODE IS NOT NULL) and (CITYLIM LIKE '%') and (NOT CITYLIM ILIKE 'burke') and (NOT CITYLIM ILIKE CITY)" \
{fn_rawunaddressable} {gisdata} SiteStructureAddressPoints
"""

# using the Burke GIS data, gather the addresses that have improperly been identified with the wrong muncipality
if not os.path.exists(fn_rawunaddressable):
	force_pmtiles = True
	subprocess.run(make_wrongaddresscsv, shell=True)

class PostalAddress:
	__slots__ = ['ADDRESS', 'CITY', 'ZIPCODE',]
	def __init__(self, row: object):
		self.ADDRESS = row['ADDRESS'].upper()
		self.CITY = row['CITY'].upper()
		self.ZIPCODE = row['ZIPCODE']

byCity: dict[str, list[PostalAddress]] = {}
unAddressable: list[object] = []
with open(fn_rawunaddressable, "r") as file:
	reader = csv.DictReader(file)
	for row in reader:
		town = row['CITYLIM'].upper()
		unAddressable.append(row)
		addr = PostalAddress(row)
		byCity.setdefault(town, []).append(addr)

byCity = dict(sorted(byCity.items()))
for town, addresses in byCity.items():
	info['unaddressable'][town] = len(addresses)

	fn = f"{webdata}/unaddressable/{town}.csv"
	if not os.path.exists(fn):	
		with open(fn, "w", newline='') as out:
			writer = csv.writer(out, quoting=csv.QUOTE_MINIMAL)
			writer.writerow(['ADDRESS', 'CITY', 'ZIPCODE'])
			for addr in addresses:
				writer.writerow([addr.ADDRESS,addr.CITY,addr.ZIPCODE])

if not os.path.exists(fn_townlimits):
	force_pmtiles = True
	subprocess.run(f"ogr2ogr -f GeoJSON -t_srs EPSG:4326 -select \"NAME\" {fn_townlimits} {gisdata} city_limits", shell=True)

if not os.path.exists(fn_roads):
	force_pmtiles = True
	subprocess.run(f"ogr2ogr -f GeoJSON -t_srs EPSG:4326 -select \"SRNUM,CLASS,FULLNAME\" -where \"(CLASS IS NOT NULL)\" {fn_roads} {gisdata} RoadCenterlines", shell=True)

# make pmtiles for a map of obstacles to proper addressable towns
make_pmtiles = f"""
tippecanoe -f -Z8 -z12 -o {fn_pmtiles} \
--named-layer='burke:{datadir}/burke-boundary.geojson' \
--named-layer='water:{datadir}/BRTA-Water.geojson.gz' \
--named-layer='townlimits:{fn_townlimits}' \
--named-layer='roads:{fn_roads}' \
--named-layer='unaddressable:{fn_rawunaddressable}'
"""
if force_pmtiles or not os.path.exists(fn_pmtiles):
	subprocess.run(make_pmtiles, shell=True)

info['mapmtime'] = os.path.getmtime(fn_pmtiles)

if force_pmtiles or not os.path.exists(fn_infojson):
	with open(fn_infojson, "w") as out:
		json.dump(info, out, indent=2)
