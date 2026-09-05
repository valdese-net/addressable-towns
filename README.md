# Addressable Towns in Burke NC

In Burke NC, the postal service has recently adopted a system which forces all area property
to identify itself using the host city of the terminating postal delivery node. In other words,
the host city of a postal code's office (that performs delivery service) is now being used for
all delivery addresses, regardless of a property's municipal jurisidiction. This leads to
ridiculous address assertions, such as the Drexel Town Hall now being identified with a
Morganton address:

> Drexel Town Hall<br>202 Church Street<br>~~DREXEL~~ MORGANTON NC 28655

This project seeks to analyze the scope and scale of this change.

Inspired by [What’s in an Address?](https://burkerivertrail.net/whats-in-an-address/) post by the Burke River Trail Association.

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