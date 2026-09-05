const town2latlng = {
	"glen alpine": [-81.778793,35.727702],
	"morganton": [-81.685066,35.745119],
	"drexel": [-81.605051,35.757474],
	"valdese": [-81.562843,35.74289],
	"rutherford college": [-81.523876,35.750552],
	"connelly springs": [-81.502762,35.740382],
	"rhodhiss": [-81.432206,35.76711],
	"hildebran": [-81.421223,35.71488],
	"long view": [-81.39204,35.730767],
	"hickory": [-81.342856,35.733153]
};

function InitBurkeMap(src) {
	const queryString = window.location.search;
	const urlParams = new URLSearchParams(queryString);
	const showOnlyTown = urlParams.get('town');

	const protocol = new pmtiles.Protocol();
	maplibregl.addProtocol("pmtiles", protocol.tile);
	const PMTILES_URL = src; 
	const p = new pmtiles.PMTiles(PMTILES_URL);
	protocol.add(p);
	const map = new maplibregl.Map({
		container: 'map',
		style: {
			version: 8,
			sources: {
				"unaddressable": {
					type: "vector",
					url: `pmtiles://${PMTILES_URL}`,
					attribution: '<a href="https://burkerivertrail.net/whats-in-an-address/">Burke River Trail</a> | <a href="https://www.burkenc.org/2495/Data-Sets">Burke NC</a> | <a href="./">Addressable Towns</a>'
				}
			},
			layers: [
				{
					"id": "background",
					"type": "background",
					"paint": { "background-color": "#000000" }
				},
				{
					"id": "county",
					"type": "line",
					"source": "unaddressable",
					"source-layer": "burke", 
					"paint": { "line-color": "#ffffff" }
				},
				{
					"id": "town",
					"type": "fill",
					"source": "unaddressable",
					"source-layer": "townlimits", 
					"paint": {
						"fill-color": ["match", ["upcase", ["get","NAME"]],
"GLEN ALPINE","#773408",
"MORGANTON","#614e04",
"DREXEL","#1e4063",
"VALDESE","#04a1a1",
"RUTHERFORD COLLEGE","#096628",
"CONNELLY SPRINGS","#34347c",
"RHODHISS","#61398a",
"HILDEBRAN","#546475",
"LONG VIEW","#614e04",
"HICKORY","#773408",
"#888"],
						"fill-opacity":0.5,
						"fill-outline-color": "white"
					}
				},
				{
					"id": "water",
					"type": "fill",
					"source": "unaddressable",
					"source-layer": "water", 
					"paint": { "fill-color": "#1229fa", "fill-opacity":1 }
				},
				{
					"id": "road",
					"type": "line",
					"source": "unaddressable",
					"source-layer": "roads",
					"paint": {
						"line-color": ["case",["<",["get","CLASS"],4], "orange","#888"],
						"line-width": ["interpolate",["exponential", 2],["zoom"],12,1,22,250]
					}
				},
				{
					"id": "roadlabel",
					"type": "symbol",
					"source": "unaddressable",
					"source-layer": "roads",
					"filter": ["all",[">",["zoom"],11],["has","FULLNAME"]],
					"layout": {
						"text-field": ["get","FULLNAME"],
						"text-size": ["interpolate",["exponential", 2],["zoom"],11,8,22,300],
						"symbol-placement": "line",
						"symbol-spacing": 500,
					},
					"paint": {
						"text-color": "white",
						"text-halo-color": "black",
						"text-halo-width": 2,
						"text-halo-blur": 3
					}
				},
				{
					"id": "unaddressable",
					"type": "circle",
					"source": "unaddressable",
					"source-layer": "unaddressable",
					"filter": showOnlyTown ? ['==', ['upcase', ['get','CITYLIM']], showOnlyTown.toUpperCase()] : true,
					"paint": {
						"circle-color": "red",
						"circle-radius": ["interpolate",["exponential", 2],["zoom"],12,3,22,350]
					}
				},
			]
		},
		center: [-81.65983,35.71655],
		zoom: 10
	});

	map.addControl(new maplibregl.FullscreenControl(), 'top-right');

	map.on('click', function(e) {
		const bbox = [[e.point.x - 1, e.point.y - 1], [e.point.x + 1, e.point.y + 1]];
		const features = map.queryRenderedFeatures(bbox);
		if (!features.length) return;

		const d = [];
		features.forEach((feature) => {
			let prop = feature.properties;
			const p = [];
			p.push('<p>');
            p.push(`<b>${feature.layer.id}</b>`);
			if (prop.NAME) p.push(`: ${prop.NAME}`);
			else if (prop.FULLNAME) p.push(`: ${prop.FULLNAME}`);
			else if (prop.ADDRESS) p.push(`<br><span>${prop.ADDRESS}<br><s>${prop.CITYLIM}</s> <i>${prop.CITY}</i><br>${prop.ZIPCODE}</span>`);
			else if (prop.length) p.push(`<br><span>${JSON.stringify(feature.properties, null, 2)}</span>`);
			p.push('</p>');
			d.unshift(p.join(''));
		});

		new maplibregl.Popup()
			.setLngLat(e.lngLat)
			.setHTML('<div class="addrpop">'+d.join('')+'</div>')
			.addTo(map);
	});
	
	if (showOnlyTown) {
		const townname = showOnlyTown.toLowerCase();
		if (town2latlng[townname]) {
			map.flyTo({center: town2latlng[townname], zoom: 14, duration:3500});
		}
	}

	return map;
}