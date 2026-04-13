---
title: "Network Traffic Reading"
category: 01-perception
level: intermediate
stability: stable
description: "Apply network traffic reading in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-network-traffic-reading.json)

# Network Traffic Reading
Category: perception | Level: advanced | Stability: stable | Version: v1

## Description
Capture and parse network packets (PCAP) or HTTP traffic for analysis, debugging, and security auditing.

## Inputs
- `source`: pcap file path or live interface name
- `filter`: BPF filter string (e.g., `"tcp port 443"`)

## Outputs
- Stream of packet dicts with timestamp, src/dst, protocol, payload

## Example
```python
from scapy.all import rdpcap, TCP
packets = rdpcap("capture.pcap")
for pkt in packets:
    if TCP in pkt:
        print(f"{pkt.time} {pkt[TCP].sport} -> {pkt[TCP].dport}")
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `scapy`, `dpkt`, `pyshark` |
| Wireshark | TShark CLI for batch processing |

## Failure Modes
- Encrypted TLS payloads require decryption keys
- High-speed captures drop packets without ring buffers

## Related
- `sensor-reading.md` · `structured-data-reading.md`

## Changelog
- v1 (2026-04): Initial entry
