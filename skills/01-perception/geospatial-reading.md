---
title: "Geospatial Reading"
category: 01-perception
level: intermediate
stability: stable
description: "Apply geospatial reading in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-geospatial-reading.json)

# Geospatial Reading
Category: perception | Level: intermediate | Stability: stable | Version: v1

## Description
Read and interpret geospatial data formats (GeoJSON, Shapefile, KML) into coordinate and feature objects.

## Inputs
- `source`: file path or GeoJSON string
- `crs`: coordinate reference system (default WGS84)

## Outputs
- GeoDataFrame or list of GeoJSON features

## Example
```python
import geopandas as gpd
gdf = gpd.read_file("regions.geojson")
print(gdf.columns.tolist())
print(gdf.geometry.type.value_counts())
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `geopandas`, `shapely` |
| LlamaIndex | Custom loader |
| GDAL | `ogr2ogr` for format conversion |

## Failure Modes
- Mixed geometry types in same layer
- CRS mismatch causes coordinate shifts

## Related
- `structured-data-reading.md` · `image-understanding.md`

## Changelog
- v1 (2026-04): Initial entry
