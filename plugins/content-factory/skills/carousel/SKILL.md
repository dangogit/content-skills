---
name: carousel
description: Produce or revise Hebrew Instagram carousels from approved ideas through copy, visual blueprint, QA, resource delivery, and verified scheduling. Use for carousel, slides, קרוסלה, or carousel revisions.
---

# Hebrew Carousel Producer

## Overview

Turn an approved idea into a reviewable carousel. This skill owns structure,
copy handoff, visual planning, and proof gates. Renderer and publishing tools
remain supplied by the consumer's content repo.

## When to Use

- Approved idea needs a Hebrew carousel.
- Existing carousel needs copy, slide, visual, or QA revision.
- Carousel needs resource CTA or Metricool handoff review.

## Prerequisites

- State Sync completed in `<content-repo>`.
- Approved idea card with objective, audience, promise, story role, proof, and duplicate check.
- Current design system, lessons, and platform constraints read.
- No scheduling or publishing without explicit current-turn approval.

## Workflow

### Step 1: Lock Editorial Contract

Record content family, objective, audience, primary promise, proof, CTA, recent
similarity check, schedule intent, and current planner status.

### Step 2: Finalize Copy Before Images

- Maximum ten slides: hook, re-hook, body, proof, payoff, CTA or recap.
- One focal line and one visual anchor per body slide.
- Use spoken Hebrew. Keep Latin tokens isolated for RTL safety.
- Use Tadam copy and visual prompt passes when available.
- Resolve factual flags before image generation.

### Step 3: Build Visual Blueprint

For every slide record scene, object or face role, focal line, safe-zone position,
palette, and text treatment. Generated typography must remain readable; HTML
fallback is allowed when generated Hebrew fails.

### Step 4: Render And Inspect

Export review assets at 1080x1350. Inspect every slide at phone scale for Hebrew
spelling, bidi order, contrast, object collisions, safe zones, and text budget.

### Step 5: Run CTA Gate

If slide or caption promises a guide, checklist, template, prompt pack, or DM
resource, run `carousel-guide` before upload or scheduling. Generic promises fail.

### Step 6: Schedule Only With Proof

Use current Metricool documentation and planner state. Refetch after create and
record id, uuid, date, timezone, network status, media count, draft state, and
auto-publish state. Never silently drop a rejected network.

Run packet validation:

```bash
python3 scripts/check_carousel_packet.py <packet.md>
```

## Output

```markdown
# Carousel Handoff
Objective:
Audience:
Promise:
Story role:
Proof:
Slides:
Visual blueprint:
CTA/resource status:
Pixel QA:
Planner status:
Next action:
```

## Resources

- `references/carousel-qa.md` - slide, safe-zone, copy, and scheduling acceptance criteria.
- `scripts/check_carousel_packet.py` - mechanical handoff gate.
- `carousel-with-face` - selected face-slide delta layer.
- `carousel-guide` - named-resource delivery gate.

## Key Principles

1. Approved idea before production.
2. Copy before image generation.
3. Proof before authority claims.
4. Pixel QA before upload.
5. Planner refetch before schedule is called done.
