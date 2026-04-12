# Sensor Reading

**Category:** `perception`  
**Skill Level:** `intermediate`  
**Stability:** `stable`  
**Added:** 2025-03  
**Last Updated:** 2026-04

---

## Description

Ingest and interpret telemetry from physical or virtual sensors — temperature probes, accelerometers, GPS coordinates, air quality monitors, IoT MQTT streams, and industrial PLC data. The agent normalizes raw sensor payloads, detects anomalies, identifies trends, and generates human-readable status reports or alerts.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `readings` | `list` | ✅ | `[{sensor_id, type, value, unit, timestamp}]` |
| `baseline` | `dict` | ❌ | Expected normal ranges per sensor type |
| `window_minutes` | `int` | ❌ | Time window for trend analysis (default: 60) |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `status` | `string` | `normal` / `warning` / `critical` |
| `anomalies` | `list` | `[{sensor_id, value, reason}]` |
| `trends` | `list` | `[{sensor_id, direction, description}]` |
| `recommended_actions` | `list` | Actionable response steps |

---

## Example

```python
import anthropic
import json

client = anthropic.Anthropic()

def interpret_sensor_batch(readings: list[dict]) -> dict:
    """
    Interpret a batch of sensor readings and return an anomaly report.
    Each reading: {sensor_id, type, value, unit, timestamp}
    """
    payload = json.dumps(readings, indent=2)

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": (
                "Analyze this batch of sensor readings and return JSON with:\n"
                "- status: normal | warning | critical\n"
                "- anomalies: [{sensor_id, value, reason}]\n"
                "- trends: [{sensor_id, direction, description}]\n"
                "- summary: one paragraph operational status\n"
                "- recommended_actions: list of action strings\n"
                "Return ONLY valid JSON.\n\n"
                f"Readings:\n{payload}"
            )
        }]
    )
    return json.loads(response.content[0].text)

readings = [
    {"sensor_id": "T-01", "type": "temperature", "value": 87.3, "unit": "C", "timestamp": "2026-04-13T00:00:00Z"},
    {"sensor_id": "V-02", "type": "vibration", "value": 12.1, "unit": "mm/s", "timestamp": "2026-04-13T00:00:05Z"},
    {"sensor_id": "P-03", "type": "pressure", "value": 2.1, "unit": "bar", "timestamp": "2026-04-13T00:00:10Z"}
]
report = interpret_sensor_batch(readings)
print(json.dumps(report, indent=2))
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Claude claude-opus-4-5 | Direct text prompt with JSON payload | 2024-06 |
| LangGraph | Tool node consuming MQTT stream | v0.1 |

---

## Notes

- Normalize units before sending (all temperatures in °C, all pressures in bar)
- For high-frequency streams, aggregate to 1-minute windows before invoking the model
- Include historical baseline values in the prompt for relative anomaly detection

---

## Related Skills

- [Structured Data Reading](structured-data-reading.md) — JSON/CSV payload parsing
- [API Response Parsing](api-response-parsing.md) — for REST telemetry APIs

---

## Changelog

| Date | Change |
|---|---|
| `2026-04` | Expanded from stub: full description, I/O table, anomaly detection example |
| `2025-03` | Initial stub entry |
