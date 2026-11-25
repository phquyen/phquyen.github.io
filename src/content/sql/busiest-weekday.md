---
# A SQL query file. Copy it to add a new query (see EDITING.md, "Add a SQL query").
title: "Busiest day of the week"
date: 2026-11-24          # YYYY-MM-DD: the day you wrote it (fills the activity grid)
difficulty: "easy"        # "easy", "medium" or "hard"
skills: ["GROUP BY", "CASE", "Dates"]
draft: true               # change to false to publish
---

Which day of the week has the most trips? Show the weekday name and the number of trips, busiest first.

```sql
SELECT
  CASE strftime('%w', requested_at)
    WHEN '0' THEN 'Sunday'    WHEN '1' THEN 'Monday'
    WHEN '2' THEN 'Tuesday'   WHEN '3' THEN 'Wednesday'
    WHEN '4' THEN 'Thursday'  WHEN '5' THEN 'Friday'
    ELSE 'Saturday'
  END AS weekday,
  COUNT(*) AS trips
FROM trips
GROUP BY strftime('%w', requested_at)
ORDER BY trips DESC;
```
