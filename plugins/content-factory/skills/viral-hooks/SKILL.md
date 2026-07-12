---
name: viral-hooks
description: Generate and critique testable three-layer hooks for approved short-form ideas, using real proof, the creator's recent hook history, and spoken Israeli Hebrew constraints.
license: MIT
metadata:
  version: 1.0.0
  category: content-creation
  tags: [hooks, short-form, video, carousel, retention]
---

# Hook Experiment Designer

## Overview

Design hook hypotheses across visual, verbal, and on-screen layers. Hooks raise or lower odds; no hook guarantees distribution. For the creator's repo, hook work starts only after State Sync and story selection.

## When to Use

- Generate hook options for an approved Reel, Short, TikTok, or carousel.
- Repair an abstract, unclear, repeated, or unsupported opening.
- Plan first frame, spoken line, and on-screen text together.
- Define an A/B test for one story angle.

## Prerequisites

- Approved idea card and selected story spine.
- Current planner, ledger, last four posts, and active drafts checked.
- Real proof for every number, authority claim, result, and named source.
- Consumer project's current design lessons read when carousel work depends on them.

## Workflow

### Step 1: Run Hook Dedupe

List last four hook structures and block immediate repetition. Compare structure, not only words:

- costly mistake;
- contrarian claim;
- personal confession;
- number lead;
- direct question;
- visible broken workflow;
- result-first proof.

### Step 2: Generate Three Angles

Create three distinct angles from `references/hook-archetypes.md`. Default mix:

- one lived pain or visible symptom;
- one proof or demonstration;
- one defensible contrast or contradiction.

Do not create fake variety through synonyms.

### Step 3: Design Three Layers

For each angle, specify:

- `visual`: first frame readable when paused;
- `verbal`: spoken line that lands naturally;
- `text`: compact on-screen line that sharpens, not duplicates;
- `proof`: source, artifact, or scene supporting promise;
- `payoff`: exact beat that closes promise.

### Step 4: Enforce Truth Gate

- Use numbers only when source or artifact proves them.
- Never change round numbers into odd numbers to look measured.
- Never invent authority, demand, user results, or urgency.
- News hooks show date or current release in slide 1 or 2.
- If body cannot pay off hook, weaken hook or strengthen body.

### Step 5: Apply Creator Hebrew Gate

- Start with lived mistake, damage, or concrete scene before tool jargon.
- Reuse the creator's exact phrasing when available.
- Read line aloud. Reject translated or slogan-like Hebrew.
- Isolate Latin tokens in generated text.
- Avoid inline `AI` in Hebrew.

### Step 6: Select By Objective

Rank candidates against declared objective:

- reach: instant qualified relevance;
- retention: open question body genuinely closes;
- authority: visible proof or usable artifact;
- conversion: natural bridge to named resource.

Platform thresholds are not universal. Use account baseline from Metricool.

### Step 7: Record Test

Pick top hook and one backup. State one changed variable and comparison baseline. Do not A/B different hook, story, duration, and CTA at once.

Run the mechanical packet gate before handoff:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/viral-hooks/scripts/check_hook_packet.py" <hook-packet.md>
```

## Output Format

```markdown
# Hook Test Packet

Objective:
Story spine:
Recent-hook conflicts:

| Angle | Visual | Verbal | On-screen | Proof | Payoff |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

Top pick:
Backup:
Test variable:
Baseline:
Truth check:
Hebrew read-aloud check:
```

## Resources

- `references/hook-archetypes.md` - angle menu.
- `references/three-layer-hook.md` - visual, verbal, text, and audio alignment.
- `references/hook-anti-patterns.md` - critique vocabulary.
- `references/hook-tactics.md` - optional tactics, subordinate to truth gate.
- `references/hook-by-platform.md` - platform execution notes requiring current verification.
- `assets/hook-batch-template.md` - test packet template.
- `assets/hook-checklist.md` - truth and alignment checks.
- `assets/three-layer-worksheet.md` - shooting worksheet.
- `scripts/check_hook_packet.py` - mechanical experiment-packet gate.

## Key Principles

1. Hook validates idea, not decorates it.
2. Three aligned layers beat clever sentence.
3. Proof controls specificity.
4. Recent-hook dedupe prevents formula fatigue.
5. Account data beats universal thresholds.
