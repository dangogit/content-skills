---
name: israeli-social-content
description: Localize approved social content for Israeli audiences using spoken Hebrew, RTL-safe formatting, cultural timing awareness, and account-specific analytics instead of hardcoded posting folklore.
license: MIT
---

# Israeli Social Content Locale Layer

## Overview

Localize strategy and copy for Israeli audiences. This skill does not choose topics, invent platform strategy, or schedule posts by itself. It converts approved content into natural Hebrew and flags local calendar, RTL, and cultural risks.

## When to Use

- Rewrite approved copy into spoken Israeli Hebrew.
- Review mixed Hebrew, English, emoji, numbers, mentions, and hashtags.
- Check culturally sensitive dates or local context.
- Adapt one approved idea across Israeli-facing networks.

## Prerequisites

- Approved idea, story role, and proof.
- Current Metricool planner and account analytics when timing matters.
- Current official platform documentation for limits, labels, and formats.
- Consumer project pipeline and ledger when configured; otherwise an explicit
  objective, recent-content summary, duplicate check, and brand positioning.

## Workflow

### Step 1: Preserve Message

Keep original claim, proof, and promise. Do not add Israeli stereotypes, invented slang, unsupported statistics, or generic local references.

### Step 2: Rewrite In Creator Voice

- Spoken, direct, second-person Hebrew.
- Prefer the creator's accepted phrases from transcripts and feedback.
- Start from lived pain before tool name.
- Reject translated slogan symmetry and invented framework names.
- Keep technical English only when needed.
- Isolate short Latin tokens on their own line or bidi-safe element.
- No inline `AI` in Hebrew.
- No em dashes.

### Step 3: Validate RTL

- Start each Hebrew line with Hebrew character.
- Put Latin hashtags and mentions on separate final lines.
- Use `<bdi dir="ltr">` in HTML for code and commands.
- Use directional marks only when target surface supports them reliably.
- Test in actual composer or final rendered pixels before publishing.

### Step 4: Check Cultural Timing

- Block insensitive commercial content on Yom Kippur and Yom HaZikaron unless the creator explicitly chooses another treatment.
- Check current Hebrew-calendar dates from live source.
- Treat Shabbat, holidays, August, and election periods as hypotheses, not universal engagement laws.
- Use Metricool best-time and the creator's performance data before recommending schedule.

### Step 5: Adapt Platform Surface

- Adapt only networks configured or requested for this asset.
- Preserve one core promise while adapting title, caption, and media requirements.
- Do not hardcode posting frequency, best time, ideal length, hashtag count, or network mix.
- Do not claim Hebrew always outperforms English without account evidence.

### Step 6: Check AI Disclosure

- TikTok requires labeling realistic AI-generated images, audio, or video and encourages broader disclosure.
- Meta requires disclosure for photorealistic generated video and realistic-sounding generated audio; label detection depends on metadata and platform systems.
- Verify current official policy before production handoff.
- Do not claim compliant labels automatically reduce reach.

Run the mechanical copy gate before handoff:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/israeli-social-content/scripts/check_hebrew_copy.py" <copy.md>
```

It catches em dashes, generic share CTAs, and inline `AI` mixed into Hebrew.
It does not replace a native-speaker read, rendered RTL inspection, or live
platform-policy verification.

## Output Format

```markdown
# Israeli Localization Review

Localized copy:
Creator voice check:
RTL risks:
Latin-token treatment:
Calendar risks:
Platform checks requiring live verification:
Unsupported claims removed:
```

## Resources

- `${CLAUDE_PLUGIN_ROOT}/skills/israeli-social-content/references/locale-checklist.md` - concise localization and policy checklist.
- `${CLAUDE_PLUGIN_ROOT}/skills/israeli-social-content/references/israeli-social-platforms.md` - directional audience context with methodology caveats.
- `${CLAUDE_PLUGIN_ROOT}/skills/israeli-social-content/evidence.json` - dated claim registry with confidence and expiry.
- Configured `pipeline_path`, `ledger_path`, and `design_lessons_path` when present.
- `${CLAUDE_PLUGIN_ROOT}/references/configuration.md` - optional project paths.

## Key Principles

1. Locale layer does not replace editorial strategy.
2. Creator's spoken phrasing beats generic Israeli slang.
3. RTL correctness is production requirement.
4. Account analytics beat hardcoded timing.
5. Platform policy claims expire and require verification.
