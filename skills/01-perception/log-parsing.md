![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-log-parsing.json)

# Log Parsing
Category: perception | Level: intermediate | Stability: stable | Version: v1

## Description
Parse structured and unstructured log files (syslog, JSON logs, Apache/Nginx) into queryable event streams.

## Inputs
- `log_source`: file path, stdin, or log string
- `format`: `json` | `syslog` | `apache` | `auto`

## Outputs
- List of parsed log events with timestamp, level, message, metadata

## Example
```python
import re
from datetime import datetime
LINE_RE = re.compile(r'(?P<ts>[\d\-T:Z]+) (?P<level>\w+) (?P<msg>.*)')
def parse_log(line):
    m = LINE_RE.match(line)
    if m:
        return {"ts": datetime.fromisoformat(m["ts"].replace("Z","+00:00")), "level": m["level"], "msg": m["msg"]}
with open("app.log") as f:
    events = [e for line in f if (e := parse_log(line.strip()))]
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `loguru`, `python-json-logger` |
| LangChain | Custom document loader |
| OpenTelemetry | Structured log collector |

## Failure Modes
- Mixed formats within a single file
- Multi-line stack traces split across events

## Related
- `text-reading.md` · `structured-data-reading.md`

## Changelog
- v1 (2026-04): Initial entry
