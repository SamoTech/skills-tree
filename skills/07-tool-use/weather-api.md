---
title: "Weather API"
category: 07-tool-use
level: basic
stability: stable
description: "Apply weather api in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-weather-api.json)

# Weather API

**Category:** `tool-use`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Fetch current weather conditions, forecasts, and historical weather data for any location.

### Example

```python
import httpx

r = httpx.get(
    'https://api.openweathermap.org/data/2.5/weather',
    params={'q': 'Giza,EG', 'appid': OWM_KEY, 'units': 'metric'}
)
data = r.json()
print(f"{data['main']['temp']}°C, {data['weather'][0]['description']}")
```

### Related Skills

- [Custom API Wrapper](custom-api-wrapper.md)
- [Structured Data Reading](../01-perception/structured-data-reading.md)
