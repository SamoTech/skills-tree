---
title: "Portfolio Analysis"
category: 16-domain-specific
level: advanced
stability: stable
description: "Apply portfolio analysis in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-portfolio-analysis.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Evaluates a portfolio's return, volatility, Sharpe ratio, and concentration risk across asset classes. Supports rebalancing recommendations, scenario stress-testing, and correlation-aware diversification analysis.

### Example
```python
import numpy as np

weights = np.array([0.4, 0.35, 0.25])
returns = np.array([0.12, 0.08, 0.20])
cov_matrix = np.array([[0.04, 0.01, 0.02],
                        [0.01, 0.03, 0.01],
                        [0.02, 0.01, 0.05]])

port_return = weights @ returns
port_variance = weights @ cov_matrix @ weights
port_std = np.sqrt(port_variance)
sharpe = (port_return - 0.04) / port_std

print(f"Return: {port_return:.2%}, Std: {port_std:.2%}, Sharpe: {sharpe:.2f}")
```

### Related Skills
- [Financial Statement Analysis](financial-statement.md)
- [Stock Price Lookup](stock-lookup.md)
- [Risk Assessment](../02-reasoning/risk-assessment.md)
