---
title: "Network Traffic Reading"
category: 01-perception
level: intermediate
stability: stable
version: v3
description: "Read authorized packet captures or bounded network telemetry to identify protocols, endpoints, timing, and transport behavior for debugging and security analysis."
related: []
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-network-traffic-reading.json)

# Network Traffic Reading

## Description
Read authorized packet captures (PCAP) or bounded network telemetry to identify protocols, endpoints, timing, and transport behavior for debugging and security analysis. Never capture or retain traffic without explicit authorization.

## When to Use
- Debugging service-to-service connectivity, latency, or reset behavior from a capture
- Security analysis of authorized captures (unexpected endpoints, beaconing, protocol misuse)
- Building structured summaries of transport behavior for incident reports

## Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | `source` | pcap path or live interface name | Capture to read; live capture requires documented authorization |
| Input | `filter` | BPF filter string | Scoping filter such as `"tcp port 443"`; apply before parsing |
| Input | `keys` | optional TLS keylog | Required only to inspect encrypted payloads; store separately |
| Output | `packets` | list of packet records | Timestamp, src/dst, protocol, ports, and bounded payload per record |
| Output | `flows` | aggregated per-connection summary | Endpoint pairs, byte counts, timing, and reset/error flags |
| Output | `limitations` | list of strings | Encrypted or dropped segments that could not be analyzed |

## Example
```python
# pip install scapy
from scapy.all import rdpcap, TCP

def summarize_flows(pcap_path: str, max_packets: int = 10000) -> dict:
    packets = rdpcap(pcap_path)
    flows: dict[tuple, int] = {}
    for pkt in packets[:max_packets]:
        if TCP in pkt:
            key = (pkt[TCP].sport, pkt[TCP].dport)
            flows[key] = flows.get(key, 0) + 1
    return dict(sorted(flows.items(), key=lambda kv: -kv[1])[:10])

print(summarize_flows("capture.pcap"))
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `scapy`, `dpkt`, `pyshark` |
| Wireshark | TShark CLI for batch processing |

## Procedure
1. Verify written authorization for the capture source and scope before reading anything.
2. Apply the narrowest BPF filter that answers the question; record the filter with the results.
3. Parse the capture and aggregate packets into flows with timing and byte counts.
4. Identify protocols and endpoints; flag unexpected destinations or beacon-like periodicity.
5. Treat encrypted payloads as opaque unless keys were provided through an authorized channel.
6. Report findings with the capture window, filter, and any dropped-packet limitations.

## Failure Modes
- Encrypted TLS payloads cannot be inspected without keys: report the limitation rather than guessing at contents.
- High-speed captures drop packets without ring buffers: state the drop rate and treat flow counts as lower bounds.
- Unscoped live capture exceeds authorization: stop at the documented scope and record what was collected.
- Reassembled streams mislead when packets arrive out of order: use sequence numbers to reorder before interpreting application data.
- Sensitive payload retention violates data-minimization rules: aggregate or redact payloads before storing results.

## Related
- [Sensor Reading](sensor-reading.md)
- [Structured Data Reading](structured-data-reading.md)

## Changelog
- v3 (2026-11): Structural modernization; added the input/output contract table, procedure, authorization-first failure modes, and removed the stale body metadata line that contradicted frontmatter.
- v1 (2026-04): Initial entry.

## Evidence

- https://scapy.readthedocs.io/
- https://www.wireshark.org/docs/man-pages/tshark.html

Evidence status: these references support implementation guidance; no performance benchmark is claimed without reproducible benchmark data.
