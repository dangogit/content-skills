---
name: content-performance-review
description: Review the creator's published Instagram posts and Reels at 24 hours and 7 days using objective-specific Metricool metrics, then write evidence-backed performance notes and next experiments.
---

# Content Performance Review

## Overview

Close Content Factory feedback loop. Pull live content metrics, normalize them by
reach and duration, compare with same-format baseline, and promote only supported
lessons. Never collapse reach, retention, authority, and conversion into one score.

## When to Use

- Published asset reaches 24-hour or 7-day review window.
- the creator asks what content worked and why.
- Editorial team needs evidence for next hook, story, CTA, or format experiment.
- Research brief wants to cite past performance as proof.

## Prerequisites

- Published status verified from platform or Metricool analytics.
- Metricool analytics access for brand `<METRICOOL_BLOG_ID>`.
- Declared objective and asset metadata.
- Python 3.9+, standard library only.

## Workflow

### Step 1: Lock Review Window

Use exact publication time. Capture at 24 hours and 7 days. Do not compare a one-day
post with a two-week post without age normalization or explicit caveat.

### Step 2: Fetch Current Metric Schema

Call Metricool available-metrics tool before analytics. Use active, non-deprecated
fields only.

Instagram posts need date, id or URL, comments, likes, reach, saves, shares, views,
and interactions when available.

Instagram Reels also need average watch time, duration, retention, three-second view
rate, and reposts when available.

### Step 3: Add Funnel Metrics

For keyword CTA, add from CTA service logs:

- qualified keyword comments;
- successful DMs;
- failed deliveries;
- guide opens when available.

Do not infer successful delivery from total comment count.

### Step 4: Normalize Export

Create JSON:

```json
{
  "content_type": "reels",
  "window": "24h",
  "items": [
    {
      "id": "asset-id",
      "title": "hook",
      "date": "2026-07-05",
      "objective": "conversion",
      "reach": 2170,
      "views": 2703,
      "comments": 197,
      "likes": 26,
      "saves": 71,
      "shares": 39,
      "average_watch_time": 17.632,
      "duration_seconds": 65.308,
      "three_second_view_rate": 44.3,
      "qualified_keyword_comments": 190,
      "dm_deliveries": 185
    }
  ]
}
```

### Step 5: Analyze

```bash
python3 scripts/analyze_metricool.py \
  --input <normalized.json> \
  --output-dir content-system/performance/reports
```

Review separate objective leaders:

- reach: reach and views;
- retention: watch-time ratio and three-second view rate;
- authority: saves and shares per reach;
- conversion: qualified keyword comments per reach and DM delivery rate.

### Step 6: Explain With Controlled Variables

Compare hook type, story role, format, duration, CTA artifact, and visual treatment.
State inference, not causation, when several variables changed.

### Step 7: Write Performance Note

Create `content-system/performance/<asset>-<window>.md`. Update asset, ledger, and
timeline record only with verified status. Future research may cite performance only after
note exists.

### Step 8: Promote One Next Experiment

Recommend one changed variable and baseline. Do not convert one winner into universal
rule. Require repeated evidence before editing durable design lessons.

## Output Format

```markdown
# Performance Note

Asset:
Window:
Objective:
Age caveat:

## Raw metrics
## Normalized metrics
## Same-format baseline
## Objective result
## Supported inference
## Confounds
## Next one-variable experiment
## Lesson status: observation | repeated | durable
```

## Resources

- `scripts/analyze_metricool.py` - validate and normalize Metricool export.
- `scripts/tests/` - rate, baseline, validation, and leader tests.
- `references/metricool-fields.md` - preferred fields and interpretation.
- `content-system/templates/performance-note.md` - repo note template.

## Key Principles

1. Objective decides metric.
2. Rates beat raw totals for cross-post comparison.
3. Same-format and same-age baseline first.
4. Correlation is not causation.
5. One post creates observation, not durable rule.
