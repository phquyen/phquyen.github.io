---
title: "Example SQL note"
summary: "A template showing how to add highlighted code. Copy this file to start a new SQL note."
date: 2026-11-25
draft: true   # change to false to publish
---

This note is a **template**. It's a draft, so it only shows in `npm run dev`.

## Writing code

Put code between three backticks, and name the language after the first three
to get colour highlighting:

```sql
-- Average price per day
SELECT
  DATE(interval_start) AS day,
  AVG(price)           AS avg_price
FROM prices
GROUP BY DATE(interval_start)
ORDER BY day;
```

Other languages work too:

```python
import pandas as pd

daily = prices.groupby(prices["interval_start"].dt.date)["price"].mean()
```

Short code inside a sentence uses single backticks: `SELECT * FROM prices`.
