# Metricool Field Guide

Updated: 2026-07-10

Always call available-metrics tool before analytics because fields deprecate.

## Instagram Posts

- date, post id or URL;
- comments, likes, reach, saves, shares, views;
- interactions and engagement only as supplemental fields.

## Instagram Reels

- date, Reel id or URL;
- comments, likes, reach, saves, shares, views, reposts;
- average watch time;
- duration;
- retention and three-second view rate when returned.

## Derived Metrics

```text
comment_rate = comments / reach
save_rate = saves / reach
share_rate = shares / reach
interaction_rate = (comments + likes + saves + shares) / reach
watch_time_ratio = average_watch_time / duration
keyword_comment_rate = qualified_keyword_comments / reach
dm_delivery_rate = dm_deliveries / qualified_keyword_comments
```

Keep `null` when denominator missing or zero. Never coerce missing metric to zero.
Metricool sometimes returns `null` for retention fields. Record missingness honestly.
