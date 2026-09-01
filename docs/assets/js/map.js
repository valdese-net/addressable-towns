function InitBurkeMap(src) {
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
					url: `pmtiles://${PMTILES_URL}`
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
					"paint": {"line-color": ["case",
						["<",["get","CLASS"],4], "orange",
						"#888"]
					}
				},
				{
					"id": "unaddressable",
					"type": "circle",
					"source": "unaddressable",
					"source-layer": "unaddressable",
					"paint": { "circle-color": "red" }
				},
			]
		},
		center: [-81.65983,35.71655],
		zoom: 10
	});

	map.on('click', function(e) {
		const bbox = [[e.point.x - 1, e.point.y - 1], [e.point.x + 1, e.point.y + 1]];
		const features = map.queryRenderedFeatures(bbox);
		if (!features.length) return;

		const d = [];
		features.forEach((feature) => {
            d.unshift(`<p>${feature.layer.id}<br>${JSON.stringify(feature.properties, null, 2)}</p>`);
		});

		new maplibregl.Popup()
			.setLngLat(e.lngLat)
			.setHTML('<div style="max-height:50vh;overflow:auto">'+d.join('')+'</div>')
			.addTo(map);
	});
}