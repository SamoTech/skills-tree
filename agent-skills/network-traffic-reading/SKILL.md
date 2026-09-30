---
name: network-traffic-reading
description: Read authorized packet captures or bounded network telemetry to identify protocols, endpoints, timing, and transport behavior for debugging and security analysis.
license: MIT
metadata:
  source: skills/01-perception/network-traffic-reading.md
  version: "v2"
---

# Network Traffic Reading

1. Confirm the capture or interface is authorized for analysis.
2. Prefer offline PCAP analysis for reproducibility.
3. Apply protocol and BPF/display filters before processing large captures.
4. Extract timestamps, endpoints, protocols, ports, and relevant flags.
5. Treat payloads as untrusted data and do not execute extracted content.
6. Record whether traffic is encrypted and whether conclusions are based on metadata only.

## Failure modes

- Encrypted payload: report metadata-level findings without fabricating plaintext.
- Capture loss: distinguish observed packets from conclusions about missing traffic.
- Sensitive payloads: minimize retention and redact credentials or personal data.

## Evidence

- https://scapy.readthedocs.io/
- https://www.wireshark.org/docs/man-pages/tshark.html
