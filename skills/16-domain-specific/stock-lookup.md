---
title: "Stock Lookup"
category: 16-domain-specific
level: advanced
stability: stable
description: "Apply stock lookup in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-stock-lookup.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Retrieves real-time and historical OHLCV price data for equities, ETFs, and indices. Normalizes symbols across exchanges, handles corporate actions such as splits and dividends, and feeds downstream analysis or alerting pipelines.

### Example
```python
import yfinance as yf

def get_snapshot(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period="5d")
    return {
        "symbol": ticker,
        "price": info.get("currentPrice"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "5d_return": round((hist["Close"].iloc[-1] / hist["Close"].iloc[0] - 1) * 100, 2),
    }

print(get_snapshot("AAPL"))
```

### Related Skills
- [Portfolio Analysis](portfolio-analysis.md)
- [Financial Statement Analysis](financial-statement.md)
- [Time Series](../12-data/time-series.md)
