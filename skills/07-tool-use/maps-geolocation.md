![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-maps-geolocation.json)

# Maps & Geolocation

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Look up locations, geocode addresses, calculate routes, and retrieve place information via maps APIs.

### Example

```python
import httpx

r = httpx.get(
    'https://maps.googleapis.com/maps/api/geocode/json',
    params={'address': 'Giza, Egypt', 'key': MAPS_KEY}
)
coords = r.json()['results'][0]['geometry']['location']
print(coords)  # {'lat': 29.9792, 'lng': 31.1342}
```

### Related Skills

- [Custom API Wrapper](custom-api-wrapper.md)
