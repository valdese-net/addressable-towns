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

## US Postal Service Municipal Address Delivery

### via Google Gemini:

> The primary federal statute governing the U.S. Postal Service is
> Title 39 of the United States Code (39 U.S.C.), enacted under the
> Postal Reorganization Act of 1970, though specific rules for
> address formatting and delivery points fall under Title 39 of the
> Code of Federal Regulations (CFR) and operational guidelines like
> the [Domestic Mail Manual (DMM)](https://pe.usps.com/text/dmm300/508.htm).
> <br>
> Note that actual physical street naming and municipal address assignment
> are controlled by local and county government authorities (such as local
> 911 dispatch or planning departments) rather than federal postal statutes,
> with USPS mapping addresses operationally to optimize carrier routes.

### via US overnment Accountability Office, dated 1990:
- [Conflicts Between Postal and Municipal Boundaries](https://www.gao.gov/products/t-ggd-90-47)

### According to the [Domestic Mail Manual (DMM)](https://pe.usps.com/text/dmm300/508.htm)

> 2.0 Conditions of Delivery<br>
> 2.1 City Delivery Service<br>
> 2.1.1 Establishment<br>
> <br>
> City delivery is provided according to USPS policies and procedures, the characteristics of the
> area to be served, and the methods needed to provide adequate service. Requests or petitions to
> establish, change, or extend city delivery service must be made to the local postmaster.

The US Postal Service has a mechanism to support delivery to other jurisdictional towns
outside of the the delivery office's host city. This can be looked up individually here:

- https://tools.usps.com/zip-code-lookup.htm?citybyzipcode

This is the key to solving this addressing issue. A service request that can be forwarded to the
local postmaster is published in the [published doc](https://valdese-net.github.io/addressable-towns/request.html) of this project.