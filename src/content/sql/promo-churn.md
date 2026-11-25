---
# A SQL query file. Copy it to add a new query (see EDITING.md, "Add a SQL query").
title: "Do promo sign-ups churn more?"
date: 2026-11-25          # YYYY-MM-DD: the day you wrote it (fills the activity grid)
difficulty: "medium"      # "easy", "medium" or "hard"
skills: ["CTE", "JOIN", "Aggregation"]
draft: true               # change to false to publish
---

Riders can sign up through a promo, a friend, a social ad or on their own. Do promo sign-ups stop riding sooner?

For each referral source, show how many riders took at least one trip and the **share who churned**, counting a rider as churned if their last trip was before 1 October 2025.

```sql
WITH last_trip AS (
  SELECT rider_id, MAX(requested_at) AS last_trip_at
  FROM trips
  GROUP BY rider_id
)
SELECT
  r.referral_source,
  COUNT(*) AS riders,
  ROUND(100.0 * SUM(l.last_trip_at < '2025-10-01') / COUNT(*), 1) AS pct_churned
FROM riders AS r
JOIN last_trip AS l USING (rider_id)
GROUP BY r.referral_source
ORDER BY pct_churned DESC;
```
