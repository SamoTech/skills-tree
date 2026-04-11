# Sensor Reading

**Category:** `perception`  
**Skill Level:** `advanced`  
**Stability:** `experimental`

### Description

Read real-time data from physical or virtual sensors (temperature, GPS, accelerometer, IoT devices) and interpret their signals.

### Example

```python
import serial
port = serial.Serial('/dev/ttyUSB0', 9600)
reading = port.readline().decode().strip()
print(f'Sensor value: {reading}')
```

### Related Skills

- [Structured Data Reading](structured-data-reading.md)
- [Time Series](../12-data/time-series.md)
