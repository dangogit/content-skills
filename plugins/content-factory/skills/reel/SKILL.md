---
name: reel
description: Route talking-head Reel requests to the canonical Hebrew captioned-video workflow. Use for raw video, captions, hook, music, correction, or Metricool scheduling.
---

# Reel Compatibility Router

## Overview

Avoid competing Reel pipelines. Canonical implementation lives in
`hebrew-captioned-video-reels`. This skill selects that workflow and prevents
quick overlay shortcuts from bypassing caption, audio, CTA, or planner QA.

## When to Use

- User asks to make, caption, edit, correct, or schedule a Reel.
- Raw talking-head or podcast video needs production.
- Existing scheduled Reel needs exact-target replacement.

## Prerequisites

- Content repo and canonical Reel skill available.
- Source clip identified unambiguously.
- Current-turn approval before scheduling or live replacement.

## Workflow

1. Read `hebrew-captioned-video-reels` completely.
2. Confirm source, target date, hook, objective, and caption source.
3. Render through canonical caption, audio, and frame-zero workflow.
4. Run media, caption, phone-listen, CTA, and planner gates.
5. Record exact target id/uuid and returned network state before calling done.

Run handoff validation:

```bash
python3 scripts/check_reel_handoff.py <handoff.md>
```

## Output

Return the canonical Reel handoff with source, final MP4, duration/codecs,
caption QA, audio proof, frame-zero proof, CTA status, upload MIME, Metricool
id/uuid, networks, planner refetch, and final status.

## Resources

- `references/reel-routing.md` - routing and no-duplicate-pipeline rules.
- `scripts/check_reel_handoff.py` - mechanical handoff gate.
- `hebrew-captioned-video-reels` - canonical implementation.

## Key Principles

1. One Reel pipeline.
2. Render complete is not publish complete.
3. Frame zero matters.
4. Audio must be heard, not inferred.
5. Planner refetch proves scheduling.
