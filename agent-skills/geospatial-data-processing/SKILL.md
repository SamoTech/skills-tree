---
name: geospatial-data-processing
description: Load, project, and analyze geospatial data, handling coordinate reference systems, geometry validation, spatial joins, and distance and area computations without silent projection errors.
metadata:
  source: skills/12-data/geospatial-data-processing.md
  category: 12-data
  version: "v1"
---

# Geospatial Data Processing

Category: Data | Level: intermediate | Stability: experimental | Version: v1

## Description

Geospatial work fails quietly when layers sit in different coordinate reference systems or when planar math is applied to unprojected degrees. The skill covers parsing geometries with their declared CRS, validating topology, reprojecting before any measurement, joining points to regions by explicit predicate, and writing outputs with the CRS recorded so downstream consumers cannot misread them.

## When to Use

Use when records carry locations that must be mapped, joined by proximity or containment, aggregated by region, or measured for distance and area.

Do not compute distances in unprojected degrees. Reproject to a planar system first, or the numbers will be silently wrong.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `features` | `table` | Yes | Geometries or coordinates with their source coordinate reference system |
| `target_crs` | `string` | No | Projection for measurement; required for distance or area computation |
| `regions` | `table` | No | Boundary polygons for spatial joins and regional aggregation |

## Procedure

1. Parse geometries and record the coordinate reference system declared for each source.
2. Validate geometry topology; repair or drop self-intersecting and invalid shapes.
3. Reproject to the target CRS before any distance, area, or density computation.
4. Perform spatial joins by predicate, with within, intersects, or nearest stated explicitly.
5. Aggregate attributes by region and report unmatched features separately.
6. Write outputs with the CRS recorded so downstream consumers cannot misread them.

## Outputs

| Output | Type | Description |
|---|---|---|
| `projected_features` | `table` | Geometries in the target CRS with validation status |
| `join_report` | `object` | Match counts per region and unmatched features |
| `aggregates` | `table` | Per-region attribute summaries |

## Runnable Example

```python
def haversine_km(lat1, lon1, lat2, lon2):
    import math
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return round(2 * r * math.asin(math.sqrt(a)), 2)

def validate_extent(minx, miny, maxx, maxy):
    if not (-180 <= minx <= maxx <= 180 and -90 <= miny <= maxy <= 90):
        return {"valid": False, "reason": "bounds or ordering violated"}
    return {"valid": True}

print(haversine_km(36.8, -122.75, 37.8, -122.35))
print(validate_extent(-122.75, 36.8, -122.35, 37.8))
print(validate_extent(-122.35, 36.8, -122.75, 37.8))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Degrees treated as distance | Planar math on unprojected coordinates | Reproject first, or use great-circle formulas |
| CRS mismatch join | Layers in different projections overlaid silently | Reproject all layers to one CRS before joining |
| Invalid geometries | Self-intersections break spatial predicates | Validate and repair topology before joining |
| Point-in-polygon edge cases | Boundary points counted inconsistently | Define an explicit boundary policy and apply it |
| Unmatched features hidden | Points outside all regions dropped | Report unmatched features separately from matches |

## Security and Authority Boundary

Precise location data re-identifies individuals and reveals sensitive movement patterns. Aggregate or fuzz coordinates to the resolution the task needs, restrict access to raw tracks, and never publish joins that attach identities to sensitive locations.

## Evidence

This skill is grounded in dated public implementation references:

1. The GeoPandas documentation (https://geopandas.org/en/stable/).
2. The Shapely geometry library documentation (https://shapely.readthedocs.io/en/stable/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Data Validation](data-validation.md) — the gate that catches invalid and out-of-bounds geometries.
- [Data Visualization](data-visualization.md) — the cartographic layer where projected results are rendered.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
