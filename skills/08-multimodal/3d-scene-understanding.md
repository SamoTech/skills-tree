---
title: "3D Scene Understanding"
category: 08-multimodal
level: advanced
stability: experimental
description: "Apply 3D scene understanding in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-08-multimodal-3d-scene-understanding.json)

# 3D Scene Understanding

**Category:** `multimodal`  
**Skill Level:** `advanced`  
**Stability:** `experimental`
**Added:** 2025-03

### Description

Reason about the three-dimensional structure of a scene from images, point clouds, or depth maps. Extracts spatial relationships, object positions, orientations, distances, and scene geometry. Used in robotics, AR/VR, autonomous navigation, and spatial reasoning pipelines.

### Example

```python
import torch
from transformers import pipeline

# Monocular depth estimation from a single image
depth_estimator = pipeline('depth-estimation', model='Intel/dpt-large')
result = depth_estimator('https://example.com/room.jpg')
depth_map = result['depth']  # PIL Image of per-pixel depth
depth_map.save('depth.png')
```

### Point Cloud Processing

```python
import open3d as o3d
import numpy as np

# Load and analyze a point cloud
pcd = o3d.io.read_point_cloud('scan.ply')
print(f'Points: {len(pcd.points)}')

# Estimate normals
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

# Segment plane (e.g., floor detection)
plane_model, inliers = pcd.segment_plane(distance_threshold=0.01, ransac_n=3, num_iterations=1000)
[a, b, c, d] = plane_model
print(f'Plane: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0')

floor = pcd.select_by_index(inliers)
objects = pcd.select_by_index(inliers, invert=True)
o3d.visualization.draw_geometries([floor, objects])
```

### Frameworks / Models

- DPT / Depth Anything (monocular depth from single image)
- Open3D (point cloud processing, mesh reconstruction)
- NeRF / Gaussian Splatting (neural scene reconstruction)
- GPT-4o (spatial reasoning from images in natural language)
- COLMAP (structure-from-motion, 3D reconstruction from photos)

### Related Skills

- [Image Understanding](../01-perception/image-understanding.md)
- [Object Detection](object-detection.md)
- [Video Frame Extraction](video-frame-extraction.md)
- [Sensor Reading](../01-perception/sensor-reading.md)
