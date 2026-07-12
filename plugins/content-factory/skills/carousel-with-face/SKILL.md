---
name: carousel-with-face
description: Add the creator's verified likeness to selected hook, proof, or CTA carousel slides while following the canonical carousel pipeline. Use for carousel with my face, put me in the slides, or face-slide revisions.
---

# Carousel Face Mode

## Overview

Delta layer over `carousel`. It changes selected image generation only. Copy,
blueprint, CTA gate, export, QA, scheduling, and learning remain base workflow.

## When to Use

- Creator should appear beyond the default CTA treatment.
- Story needs personal proof, reaction, teaching, or authority scene.
- Existing face slide needs likeness, scene, or text correction.

## Prerequisites

- Read `carousel` skill completely.
- Approved copy and visual blueprint.
- Usable face references in an access-controlled location chosen by the user.
- Explicit, documented permission from depicted adult for this use. For minors,
  require verified guardian permission and project policy allowing minor likenesses.
- Model/provider terms allow intended commercial use and required privacy level.

## Workflow

### Step 1: Choose Face Mode

- `cta-only`: canonical default.
- `hook-cta`: face supports personal hook and ask.
- `proof-cta`: face appears beside real artifact or workflow proof.
- `custom`: only when creator specifies slides.

Keep face slides within the deck's hero cap. Face is not decoration.

### Step 2: Assign Scene Job

For each face slide record reference, scale, action, expression, wardrobe, prop,
lighting, text plane, and reason the creator belongs in scene.

### Step 3: Generate And QA

Use approved image-to-image tooling. Preserve likeness without random labels,
shirt text, hats, or props. Inspect face, Hebrew text, safe zones, contrast, and
scene fit at phone scale. Regenerate only failing slides.

Do not upload third-party likeness without permission. Strip unnecessary metadata,
store references in access-controlled project location, do not reuse them for other
people or projects, and honor deletion request. Do not enable model training on
private references unless depicted person explicitly accepted that use.

### Step 4: Return To Base Pipeline

Run carousel CTA gate, export QA, planner proof, and write-back exactly as base
skill requires.

Run face-mode validation:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/carousel-with-face/scripts/check_face_packet.py" <face-packet.md>
```

## Output

```markdown
# Face Mode Handoff
Mode:
Slides:
References:
Consent:
Reference retention:
Scene jobs:
Likeness QA:
Text/pixel QA:
Base carousel status:
```

## Resources

- `references/face-slide-qa.md` - likeness, scene, and text acceptance criteria.
- `scripts/check_face_packet.py` - mechanical face-mode gate.
- `carousel` - canonical production workflow.
- `${CLAUDE_PLUGIN_ROOT}/references/configuration.md` - project configuration.

## Key Principles

1. Face supports story job.
2. Face does not replace proof.
3. Never randomize identity details.
4. Keep copy and image generation separate.
5. Return to base carousel gates.
6. Consent and deletion rights travel with every likeness.
