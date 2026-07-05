---
title: "Geospatial Reading"
category: 01-perception
level: intermediate
stability: stable
description: "Enable AI agents to read and interpret geospatial data formats (GeoJSON, Shapefile, KML) into coordinate and feature objects for spatial analysis and map-based workflows."
added: "2025-03"
version: "v2"
last_updated: "2026-07"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-geospatial-reading.json)

# Geospatial Reading

**Category:** `01-perception`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Version:** `v2`
**Added:** `2025-03`
**Last Updated:** `2026-07`

---

## Description

Geospatial Reading enables an agent to ingest vector geospatial formats — GeoJSON, Shapefile, KML, GeoPackage — and convert them into structured feature collections with normalized coordinate reference systems. This skill is the entry point for location intelligence agents, route planners, and geospatial analysis pipelines. It handles CRS reprojection, mixed geometry types, and spatial bounding box queries.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `source` | `string` | ✅ | File path, URL, or raw GeoJSON string |
| `format` | `string` | ❌ | `geojson` \| `shapefile` \| `kml` \| `gpkg` (auto-detected if omitted) |
| `crs` | `string` | ❌ | Target coordinate reference system (default: `EPSG:4326` / WGS84) |
| `bbox` | `list[float]` | ❌ | Bounding box filter `[min_lon, min_lat, max_lon, max_lat]` |
| `layer` | `string` | ❌ | Layer name for multi-layer formats (GeoPackage, Shapefile) |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `features` | `list[dict]` | GeoJSON-style feature objects with `geometry` and `properties` |
| `crs` | `string` | CRS of the output data (e.g. `EPSG:4326`) |
| `geometry_types` | `list[string]` | Detected geometry types (`Point`, `Polygon`, `LineString`, etc.) |
| `bounds` | `list[float]` | Bounding box of all features `[min_lon, min_lat, max_lon, max_lat]` |
| `feature_count` | `int` | Total number of features |

---

## Example

```python
import geopandas as gpd
from shapely.geometry import box

def read_geospatial(source: str, crs: str = "EPSG:4326", bbox: list = None) -> dict:
    gdf = gpd.read_file(source)
    if gdf.crs and str(gdf.crs) != crs:
        gdf = gdf.to_crs(crs)
    if bbox:
        gdf = gdf[gdf.intersects(box(*bbox))]

    return {
        "crs": str(gdf.crs),
        "feature_count": len(gdf),
        "geometry_types": gdf.geometry.geom_type.unique().tolist(),
        "bounds": list(gdf.total_bounds),
        "features": gdf.__geo_interface__["features"],
    }

result = read_geospatial("regions.geojson")
print(result["feature_count"], result["geometry_types"])
# → 142 ['Polygon', 'MultiPolygon']
```

```python
# Extended — KML parsing and centroid extraction
import geopandas as gpd

gdf = gpd.read_file("places.kml", driver="KML")
gdf["centroid_lon"] = gdf.geometry.centroid.x
gdf["centroid_lat"] = gdf.geometry.centroid.y
print(gdf[["Name", "centroid_lon", "centroid_lat"]].head())
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Python `geopandas` | `read_file()` — unified reader for all major formats | v1 |
| Python `shapely` | Geometry operations, intersection, bounding box | v1 |
| Python `pyproj` | CRS transformation and reprojection | v1 |
| GDAL / OGR | `ogr2ogr` CLI for format conversion | v1 |
| LlamaIndex `SimpleDirectoryReader` | Can load GeoJSON as text for LLM context | v0.8 |
| Mapbox / Google Maps API | REST endpoints returning GeoJSON features | v1 |
| GPT-4o | Interprets GeoJSON feature properties natively | 2024-05 |
| Claude 3.7 Sonnet | Strong at spatial reasoning over feature descriptions | 2025-01 |

---

## Model Comparison

| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash | Notes |
|---|---|---|---|---|
| Coordinate reasoning | 4 | 4 | 3 | None natively handle raw coordinate math |
| GeoJSON interpretation | 5 | 5 | 4 | All handle well as JSON |
| Spatial relationship queries | 3 | 4 | 3 | Claude slightly better at topology reasoning |
| Instruction following | 5 | 5 | 4 | |
| Edge case handling | 3 | 3 | 3 | Mixed geometry types confuse all models |

---

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| CRS mismatch | Data in projected CRS (e.g. EPSG:3857) mixed with WGS84 | Always reproject to common CRS before processing |
| Mixed geometry types | Polygon and MultiPolygon in same layer breaks type-strict operations | Use `gdf.geometry.apply(lambda g: [g] if g.geom_type == "Polygon" else list(g.geoms))` to normalize |
| Corrupt Shapefile | Missing `.prj`, `.dbf`, or `.shx` sidecar files | Validate all sidecar files exist before opening |
| Large file OOM | Loading a 1 GB Shapefile into memory | Use `bbox` filter or chunked reading with `fiona` |
| Invalid geometries | Self-intersecting polygons fail spatial operations | Apply `gdf.geometry = gdf.geometry.buffer(0)` to fix |

---

## Prompt Patterns

### Pattern 1 — Feature Summary
```
Given the following GeoJSON feature collection:
{geojson_data}

Summarize:
1. Number of features
2. Geometry types present
3. Bounding box (min_lon, min_lat, max_lon, max_lat)
4. Key property fields available
```

### Pattern 2 — Spatial Query
```
From this GeoJSON feature collection:
{geojson_data}

Find all features where the property "{property_name}" equals "{value}".
Return as a filtered GeoJSON FeatureCollection.
```

### Pattern 3 — Location Intelligence
```
Analyze these geographic features:
{features_json}

For each feature, provide:
- Name/identifier
- Geometry type
- Approximate center coordinates
- Notable properties
Return as a JSON array.
```

---

## Notes

- `geopandas` requires `fiona`, `pyproj`, and `shapely` — install via `pip install geopandas` which pulls all dependencies.
- For very large datasets, use `fiona` directly to stream features without loading all into memory.
- KML driver in `geopandas` requires GDAL built with KML support — verify with `fiona.supported_drivers`.
- Never pass raw coordinate arrays to an LLM — summarize as natural language descriptions first for better reasoning.

---

## Related Skills

- [Structured Data Reading](./structured-data-reading.md) — GeoJSON properties are standard JSON objects
- [Image Understanding](./image-understanding.md) — satellite or map images complement vector data
- [API Response Parsing](./api-response-parsing.md) — mapping APIs return GeoJSON responses

---

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-04` | v1 | Initial entry |
| `2026-07` | v2 | Added typed I/O tables, extended examples, full frameworks table, model comparison, prompt patterns, detailed failure modes |
