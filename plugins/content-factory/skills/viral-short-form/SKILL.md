---
name: viral-short-form
description: Design or critique short-form scripts and carousel story structures after Content Factory State Sync, with explicit objective, proof, story role, and platform constraints.
license: MIT
metadata:
  version: 1.0.0
  category: content-creation
  tags: [short-form, video, carousel, retention, storytelling]
---

# Short-Form Story Architect

## Overview

Turn an approved content idea into a clear short-form story. Generate testable creative hypotheses, not virality predictions. For the creator's content repo, this skill supplies story structure only. Final Hebrew copy, production, scheduling, and analytics remain separate gates.

## When to Use

- Build a Reel, TikTok, Short, or carousel script from an approved idea card.
- Diagnose where an existing script loses clarity, tension, proof, or payoff.
- Repurpose one proven idea into distinct formats without duplicating its promise.
- Compare several story angles before production.

## Prerequisites

- Read configured pipeline and ledger files when present and complete their State
  Sync. Otherwise collect recent assets, duplicate risk, current planner status,
  and story-role sequence in the packet.
- Start from an approved idea card with audience, objective, story role, proof, and duplicate risk.
- Read configured brand positioning. If absent, preserve user's stated niche and ask
  before introducing a different topic domain.

## Workflow

### Step 1: Lock Success Objective

Choose one primary objective:

- `reach`: earn initial viewing and qualified reach.
- `retention`: hold attention through payoff.
- `authority`: earn saves and shares through useful proof.
- `conversion`: earn qualified keyword comments and successful DM delivery.

Do not call views vanity. Objective decides metric.

### Step 2: Validate Story Material

Require:

```text
Recognizable situation
Concrete damage or stake
Surprising cause
Creator proof or source-backed proof
Named method or artifact
Visible payoff
One next action
```

If proof is missing, use commentary or tactical role. Do not frame unsupported material as proof or case study.

### Step 3: Generate Three Story Hypotheses

Create three meaningfully different angles. Vary story mechanism, not wording:

1. `pain-to-fix`: mistake -> damage -> system fix -> artifact.
2. `proof`: result -> evidence -> mechanism -> repeatable lesson.
3. `teardown`: broken setup -> diagnosis -> corrected setup -> verification.

For each, state why it fits audience, objective, and current story arc. Do not generate ten superficial hooks.

### Step 4: Build Narrative Spine

Use smallest structure that carries message:

```text
Hook -> Context -> Escalation -> Proof -> Payoff -> CTA
```

- Hook names visible symptom or stake.
- Context identifies exact situation.
- Escalation adds consequence or obstacle.
- Proof shows artifact, source, screenshot, log, demo, or real workflow.
- Payoff closes original promise.
- CTA offers one relevant next action.

Read `references/formats.md` only for selected format. Treat pacing numbers as starting hypotheses, then calibrate from the creator's analytics.

### Step 5: Apply Hebrew And Brand Layer

Do not translate English copy literally. Pass structure to the creator's Hebrew copy layer:

- Spoken Israeli Hebrew.
- Reuse the creator's phrasing when available.
- Start from lived pain before tool name.
- Isolate required Latin tokens.
- No invented framework names or cosmetic precision.
- No em dashes.

### Step 6: Critique Against Failure Modes

Mark exact beat where script fails:

- weak or abstract hook;
- repeated beat with no new information;
- proof arrives too late or never arrives;
- payoff does not answer hook;
- CTA promises unnamed or unavailable resource;
- structure repeats recent posts.

Rewrite weak beats. Preserve strong material.

### Step 7: Declare Experiment

Record one variable being tested, expected signal, and comparison baseline. Examples:

- concrete scene hook vs abstract claim;
- proof-first vs pain-first;
- named artifact CTA vs generic guide;
- 30-second vs 60-second cut.

Change one main variable per test when possible.

Run the mechanical packet gate before handoff:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/viral-short-form/scripts/check_story_packet.py" <story-packet.md>
```

## Output Format

```markdown
# Short-Form Story Packet

Objective:
Audience:
Story role:
Content family:
Proof:
Relationship to recent posts:

## Three hypotheses
1. Angle / rationale
2. Angle / rationale
3. Angle / rationale

## Selected spine
Hook:
Context:
Escalation:
Proof:
Payoff:
CTA:

## Experiment
Variable:
Expected signal:
Baseline:
```

## Resources

- `references/formats.md` - format-specific story patterns.
- `references/hooks.md` - hook shapes without platform guarantees.
- `references/retention.md` - narrative failure diagnosis.
- `references/platforms.md` - current-doc and analytics verification checklist.
- `references/metrics-honesty.md` - objective-aware measurement.
- `assets/script-template.md` - script packet template.
- `assets/carousel-outline.md` - generic outline, subordinate to any configured
  project carousel pipeline.
- `scripts/check_story_packet.py` - mechanical story-packet gate.

## Key Principles

1. Story selection beats hook volume.
2. Proof beats generic authority language.
3. Objective decides metric.
4. Platform claims require current verification.
5. Creator analytics override creator folklore.
