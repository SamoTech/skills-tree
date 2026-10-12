---
title: "IoT Telemetry Parsing"
category: 01-perception
level: intermediate
stability: experimental
description: "Parse IoT telemetry streams — MQTT, CoAP, and device events — into timestamped, typed records with schema validation, unit normalization, and out-of-order handling."
added: "2026-10"
version: v1
related: ["sensor-reading", "log-parsing"]
---

# IoT Telemetry Parsing

Category: Perception | Level: intermediate | Stability: experimental | Version: v1

## Description

Device telemetry arrives as compact binary or JSON payloads over constrained transports, often out of order and sometimes duplicated. This skill turns raw telemetry into analysis-ready records: decode the payload, validate it against the device schema, normalize units and timestamps, and keep malformed messages visible instead of dropping them silently.

## When to Use

Use when consuming device or sensor streams — MQTT topics, CoAP observations, gateway exports — that feed monitoring, alerting, or analysis.

Do not assume ordering, uniqueness, or unit consistency across devices; each message carries its own clock, schema version, and encoding.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `payload` | `bytes` | Yes | The raw telemetry message |
| `transport` | `enum` | Yes | mqtt, coap, or gateway export |
| `device_schema` | `map` | Yes | Expected fields, types, and units for the device |
| `schema_version` | `string` | No | Payload schema version declared by the device |

## Procedure

1. Identify the device and its schema version from the topic or payload header before decoding.
2. Decode the payload with the schema — field order for binary encodings, key paths for JSON — and record the encoding used.
3. Validate fields for type, range, and unit, converting to canonical units with the conversion recorded.
4. Normalize timestamps to UTC from the device clock and flag messages with implausible clock drift.
5. Handle duplicates and out-of-order arrival explicitly — dedupe by device sequence number, sort by event time, and report reordering.
6. Route malformed messages to a dead-letter record with the raw payload preserved rather than a silent drop.

## Outputs

| Output | Type | Description |
|---|---|---|
| `records` | `list` | Typed, validated, unit-normalized telemetry records |
| `drops` | `list` | Malformed or unmatched-schema messages with reasons |
| `stats` | `map` | Counts by device plus dedupe and reordering statistics |

## Runnable Example

```python
def parse_telemetry(message, schema):
    fields = {}
    for name, kind in schema.items():
        value = message[name]
        if kind == "int" and not isinstance(value, int):
            raise ValueError(f"type mismatch on {name}")
        fields[name] = value
    if "temperature_c" in fields:
        fields["temperature_f"] = round(fields["temperature_c"] * 9 / 5 + 32, 2)
    return {"fields": fields, "ts": message["ts"]}

msg = {"temperature_c": 21, "ts": "2026-10-12T05:00:00Z"}
print(parse_telemetry(msg, {"temperature_c": "int"}))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Silent drops | Malformed messages are discarded before analysis | Dead-letter with raw payload and reason |
| Unit confusion | Devices report the same field in different units | Normalize to canonical units and record conversions |
| Clock drift | Device timestamps are implausible against arrival time | Flag drift and prefer gateway receive time when required |
| Duplicate delivery | Transport retries deliver the same event twice | Dedupe on device sequence numbers |
| Schema drift | A firmware update changes the payload layout | Version schemas and reject unknown versions explicitly |

## Security and Authority Boundary

Telemetry topics can be published to by compromised devices. Validate provenance where the transport provides it, bound payload sizes, and never treat a device-reported identity as authenticated without transport-layer credentials.

## Evidence

This skill is grounded in dated public implementation references:

1. The Paho Python MQTT client documentation (https://pypi.org/project/paho-mqtt/).
2. The MQTT protocol overview maintained by the protocol community (https://mqtt.org/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Sensor Reading](sensor-reading.md) — the perception layer that interprets individual device readings.
- [Log Parsing](log-parsing.md) — the same malformed-record discipline applied to service logs.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
