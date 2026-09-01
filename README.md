# Addressable Towns in Burke NC

In Burke NC, the postal service has recently adopted a system which forces all area property
to identify itself using the host city of the terminating postal delivery node. In other words,
the host city of a postal code's office (that performs delivery service) is now being used for
all delivery addresses, regardless of a property's municipal jurisidiction. This leads to
ridiculous address assertions, such as the Drexel Town Hall now being identified with a
Morganton address:

```
 Drexel Town Hall
 202 Church Street
 MORGANTON NC 28655
 ```

This project seeks to analyze the scope and scale of this change.

## Burke GIS Data

New Burke GIS data was just released on 2026-08-28. This new data already reflects this new postal
address scheme, thus enabling a straight forward analysis of the impacted addresses/parcels.
The county dataset is not consistent on capitalization and case usage, so a little care must
be taken to perform case insensitive filters.

The impacted addresses are easy to identify with a SQL where clause:

`(CITYLIM LIKE '%') and (NOT CITYLIM ILIKE 'burke') and (NOT CITYLIM ILIKE CITY)`

For QGIS, the following expression can be used:

`upper("CITYLIM") != 'BURKE' and upper("CITYLIM") != upper("CITY")`

This query eliminates the parcels that are not within a municipal jurisdiction, then matches
on all addresses that do not use the jurisdictional city for address identification.

## Zip Code Mapping

The postal service does not seem to publish any data details of its routing network, other than its specific
instructions for each address. However, the nconemap.gov site does have some ZIP boundary data if maps are
desired.

- Zip Code Conty Conflicts (not sure what this is, but indicates that ncone has a ZIP boundary layer dataset)
https://www.nconemap.gov/datasets/977e2e6773ad460c95f46c803aa16722_11/explore?filters=eyJjb3VudHkiOlsiQlVSS0UiXX0%3D&location=35.785047%2C-81.658527%2C12

- The ZIP Code GDB is embedded in the following download
https://www.nconemap.gov/documents/d2d4d4e600704d4ebb7d29454f744293/explore

