---
name: viral-captions-and-ctas
description: Draft and audit captions, on-screen text, hashtags, pinned comments, and CTAs for the creator's Hebrew short-form content. Use after story and copy direction exist, before render or scheduling.
license: MIT
metadata:
  category: content-creation
  version: 2.0.0
  scope: framework-only
---

# Captions and CTAs

Framework layer only. Do not override a configured project pipeline, the creator's Hebrew voice, live CTA automation, or publishing rules.

## When to Use

- Caption needs platform adaptation.
- CTA needs stronger artifact naming or lower friction.
- On-screen text needs safe-zone and RTL review.
- Hashtags or pinned comment need a factual, non-spam audit.

Do not use this skill to choose topic, story role, proof, schedule, or publish state.

## Prerequisites

- State Sync completed.
- Approved idea card or existing asset.
- Final or near-final Hebrew message.
- Content objective: reach, saves, shares, comments, lead capture, or watch-through.
- For guide or DM CTA: `carousel-guide` contract and active route status.

## Core Rules

1. One primary objective per asset. Do not optimize saves, comments, shares, follows, and clicks equally.
2. Caption adds context or payoff. It may echo the promise, but must not blindly duplicate on-screen copy.
3. Comment-keyword CTAs are allowed when they request a real resource or response, name the artifact, and route to a live automation. They are not automatically engagement bait.
4. Reject meaningless bait: fake urgency, forced likes, numbered tagging requests, empty `YES` comments, or a promised resource that is not delivered first.
5. For configured keyword-resource flows, use comment plus one requested DM delivery.
   Do not assume every account uses this funnel or turn it into unrelated outreach.
6. Hashtags are optional metadata, not a reach guarantee. Use only relevant tags and verify current platform limits before publishing.
7. Do not invent metrics, rankings, audience numbers, or platform penalties. Mark claims as hypothesis, source them, or remove them.
8. Hebrew lines start with Hebrew where possible. Isolate short Latin tokens with `<bdi dir="ltr">` or place them on their own line. Never put inline `AI` in a Hebrew line.
9. Every platform gets native copy. Metricool cross-network scheduling still needs platform-specific title fields where required.

## Workflow

1. Read State Sync, story role, audience, proof, and objective.
2. Choose one CTA action: named artifact comment, save, share, stance comment, watch-through, or no CTA.
3. Draft caption in spoken Israeli Hebrew. Put payoff or tension first.
4. Draft platform variants for Instagram, TikTok, and YouTube. Treat limits as current documentation checks, not permanent truths.
5. Run RTL, claim, bait, and promised-delivery checks.
6. For comment-resource CTAs, run the resource gate before upload or scheduling.
7. Save copy with content family, primary promise, audience, CTA keyword, similarity check, schedule intent, and Metricool status.

Run the mechanical packet gate before handoff:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/viral-captions-and-ctas/scripts/check_caption_packet.py" <copy.md>
```

## Output

Return:

```markdown
# Caption And CTA Packet
Objective: <one objective>
Caption: <inline copy or reviewed asset path>
CTA: <one action or none>
CTA rationale: <why this action fits objective>
On-screen text: <copy and safe-zone placement>
Hashtags: <small relevant set or none>
Pinned comment: <copy or none>
Risk flags: <none or exact unresolved proof/policy issue>
```

## Resources

- `references/caption-craft.md`
- `references/on-screen-text.md`
- `references/hashtag-reality.md`
- `references/ctas-that-work.md`
- `references/pinned-comments.md`
- `references/anti-patterns.md`
- `assets/bait-check.md`
- `assets/caption-template.md`
- `assets/cta-picker.md`
- `assets/on-screen-text-spec.md`
- `assets/pinned-comment-template.md`
- `scripts/check_caption_packet.py` - mechanical packet gate.

## Evidence Boundary

Platform algorithms, limits, labels, and ranking signals change. Link current official documentation when making a platform claim. Account performance beats generic creator folklore.
