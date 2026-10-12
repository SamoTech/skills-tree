---
title: "Perceptual Image Hashing"
category: 08-multimodal
level: intermediate
stability: experimental
description: "Compute average-hash fingerprints from downsampled grayscale data and compare them by Hamming distance so near-duplicate images are detected without byte equality."
added: "2026-10"
version: v1
related: ["image-classification", "object-detection"]
---

# Perceptual Image Hashing

Category: Multimodal | Level: intermediate | Stability: experimental | Version: v1

## Description

Byte hashes cannot recognize the same picture after a resize or re-encode. A perceptual hash captures visual structure: downsample to a fixed grid, threshold each cell against the grid mean, and pack the bits into a fixed-width fingerprint. Two images then compare by Hamming distance, and a declared threshold turns that distance into a duplicate decision. Face or semantic similarity is out of scope; this is structural near-duplicate detection.

## When to Use

Use when a corpus must be deduplicated against resizes, crops, and re-encodes, and the decision must be explainable as a measured distance against a declared threshold.

Do not use for semantic matching — different scenes with similar histograms compare equal; use classification or embedding retrieval for meaning-level search.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `grid` | `list[integers]` | Yes | Downsampled grayscale values in row-major order |
| `threshold` | `integer` | Yes | Hamming distance at which two hashes count as duplicates |
| `hash_width` | `integer` | No | Bits per hash; derived from grid length when omitted |

## Procedure

1. Downsample every image to the same fixed grayscale grid before hashing; grid mismatch makes hashes incomparable.
2. Compute the grid mean and threshold every cell to one bit, using a strict greater-than comparison.
3. Pack the bits in row-major order into a fixed-width integer fingerprint.
4. Compare fingerprints by Hamming distance — popcount of the XOR — never by string similarity.
5. Apply the declared duplicate threshold and record the distance, not just the verdict.
6. Treat dark, flat, or synthetic grids as unhashable noise: their bits carry no structure and produce false matches.
7. Never edit images to force a match; if distances sit at the threshold, collect more evidence instead.

## Outputs

| Output | Type | Description |
|---|---|---|
| `hash` | `integer` | The perceptual fingerprint of the grid |
| `distance` | `integer` | Hamming distance between two hashes |
| `duplicate` | `boolean` | Threshold-applied verdict, recorded with its distance |

## Runnable Example

```python
def average_hash(grid):
    """Row-major grayscale grid -> packed average-hash fingerprint."""
    mean = sum(grid) / len(grid)
    value = 0
    for cell in grid:
        value = (value << 1) | (1 if cell > mean else 0)
    return value

def hamming_distance(a, b):
    return bin(a ^ b).count("1")

base = [120, 130, 110, 125, 128, 122, 119, 131] * 8
near = [121, 60, 110, 125, 128, 122, 119, 130] * 8
h1, h2 = average_hash(base), average_hash(near)
distance = hamming_distance(h1, h2)
print("distance:", distance, "duplicate:", distance <= 8)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| False positives | Flat or low-contrast images hash to noise | Flag degenerate grids and exclude them from matching |
| Grid mismatch | Images hashed at different resolutions | Downsample everything to one fixed grid first |
| Threshold guessing | Cutoff tuned on unlabeled data | Calibrate the threshold on labeled pairs and record it |
| Bit-order drift | Cells packed in inconsistent order | Pack row-major in one documented order everywhere |
| Semantic overreach | Different scenes counted as duplicates | Keep the decision structural and confirm borderline pairs |

## Security and Authority Boundary

Perceptual hashes are derived features of their source images; they inherit every access restriction of the source. A hash that survives deletion of the original can still identify it, so retention policy must cover hashes too.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia’s overview of perceptual hashing (https://en.wikipedia.org/wiki/Perceptual_hashing).
2. Python’s statistics module documentation for mean computation (https://docs.python.org/3/library/statistics.html).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Image Classification](image-classification.md) — answers what an image shows; this skill answers whether two images are structurally the same.
- [Object Detection](object-detection.md) — localizes content whose regions can be hashed for targeted deduplication.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
