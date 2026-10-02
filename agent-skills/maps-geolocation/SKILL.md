---
name: maps-geolocation
description: Use geocoding, place search, distance, and routing APIs with explicit geographic scope, provider attribution, and coordinate validation.
metadata:
  source: skills/07-tool-use/maps-geolocation.md
  category: 07-tool-use
---

# Maps & Geolocation

## Description
Use mapping and geolocation services as an agent tool for address lookup, geocoding, reverse geocoding, place discovery, distance calculations, and routing. Treat coordinates and addresses as location-sensitive data and validate them before downstream actions.

## When to Use
- Convert a user-approved address into coordinates.
- Resolve coordinates into a human-readable location.
- Find places or calculate a route using a documented provider.
- Supply normalized location data to another tool.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Address | Preserve user-provided text and provider-specific normalization separately. |
| Coordinates | Validate latitude and longitude ranges before use. |
| Search scope | Apply country, region, radius, or bounding-box constraints when appropriate. |
| Output | Coordinates, place identifiers, address components, distance, or route geometry. |
| Privacy | Minimize retention and avoid exposing precise location unnecessarily. |
| Verification | Check result confidence and provider status before acting. |
| Failure modes | Ambiguous address, no result, quota error, stale place data, or incorrect coordinate assumptions. |

## Runnable Example

```python
import os, requests

r = requests.get(
    "https://maps.googleapis.com/maps/api/geocode/json",
    params={"address": "Giza, Egypt", "key": os.environ["MAPS_API_KEY"]},
    timeout=20,
)
r.raise_for_status()
body = r.json()
assert body["status"] == "OK" and body["results"]
location = body["results"][0]["geometry"]["location"]
assert -90 <= location["lat"] <= 90
assert -180 <= location["lng"] <= 180
print(location)
```

## Failure modes
- Conflating a place name with a precise address.
- Assuming the first geocoding result is always correct.
- Retaining precise coordinates beyond the workflow need.
- Omitting provider terms, attribution, or usage limits.
- Using stale coordinates for safety-critical navigation.

## Evidence
- Google Maps Platform Geocoding documentation: https://developers.google.com/maps/documentation/geocoding/overview
- Repository schema and validation workflows define local conformance requirements.

## Related
- custom-api-wrapper
- web-search
- input-guardrails
