---
name: carousel-guide
description: Build and prove a named-resource comment-to-DM contract for a carousel or Reel before upload or scheduling. Use whenever content promises a guide, checklist, template, prompt pack, or DM resource.
---

# Comment Resource Gate

## Overview

Convert a comment keyword promise into a durable artifact, safe route, delivery
proof, and write-back record. Compatibility name remains `carousel-guide`; apply
it to Reels too.

## When to Use

- Caption or slide asks viewers to comment a keyword.
- Content promises a guide, checklist, template, prompt pack, rule, or file.
- Existing asset has a missing, broken, or unverified route.

## Prerequisites

- Approved asset and CTA.
- Website repo or hosting surface for `<your-domain>`.
- CTA automation service and route registry.
- Platform policy permits requested reply flow.
- Explicit approval before deployment, message changes, scheduling, or publishing.

## Workflow

### Step 1: Lock Contract

Record asset, named artifact, exact promise, keyword, guide slug, language,
scheduled id/uuid, and current route status. Reject generic `guide` promises.

### Step 2: Validate Keyword

- Short and easy to type.
- Exact whole-word match where supported.
- No collision with active routes or common casual comments.
- One typo recovery only when unique.

### Step 3: Build A Beginner-First Artifact

Assume the reader is not technical unless the approved audience explicitly says
otherwise. The guide must help the reader act before it explains how the system
works.

- Open with the outcome and, when relevant, a simple choice between the user's
  product, device, or screen.
- Put the first useful action before history, architecture, bug analysis,
  evidence, and credits.
- Remove unnecessary jargon. Explain every necessary term at first use.
- For downloads and setup, name the exact icon, button, menu item, file ending,
  and normal file location.
- Make the primary destination a clickable action, not only a raw URL in a copy
  box.
- Include one short success check with the exact expected result.
- Follow it with a small, ordered troubleshooting section.
- Move optional developer instructions and technical sources to the end.
- For hidden or unfamiliar controls, include a current screenshot when
  available. Otherwise describe the icon, location, and visible label.

Run the 10-second test before publishing: can a non-technical reader tell whether
the guide applies to them and identify the first click within 10 seconds? If not,
rewrite it.

Publish the approved guide at a stable URL. Verify HTTP `200`, expected content,
correct language, clickable actions, copy controls, and the complete path on
mobile and desktop.

### Step 4: Activate Delivery Route

Validate locally, deploy through the user's approved process, check the configured
`cta_automation_base_url`, and run a synthetic dry
run. Required result: exact keyword and `status:"sent"`. Record route version and
timestamp. Synthetic test must target controlled test account or non-sending mock,
never uninvolved third party.

Enforce one-request-one-response consent. Deduplicate events, cap retries and
send rate, honor opt-out, and avoid storing comment text, usernames, or recipient
identifiers longer than delivery and audit require. Never turn resource request
into unrelated marketing sequence without separate consent.

### Step 5: Write Back And Release

Write `guide_url`, `cta_keyword`, `automation_status: active`, and proof to the
asset record plus every configured ledger or timeline. If no ledger or timeline
is configured, retain the complete handoff packet. Only then permit upload or
scheduling.

Run contract validation:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/carousel-guide/scripts/check_resource_contract.py" <resource-record.md>
```

## Output

```markdown
# Resource Gate
Asset:
Named artifact:
Guide URL:
Keyword:
Route collision check:
Local validation:
Remote validation:
Health:
Synthetic delivery:
Consent scope:
Dedupe/rate limit:
Write-back:
Status:
```

## Resources

- `references/instagram-agent-routing.md` - route safety patterns.
- `scripts/check_resource_contract.py` - mechanical resource proof gate.
- `${CLAUDE_PLUGIN_ROOT}/references/configuration.md` - endpoint and domain configuration.

## Key Principles

1. Named artifact, not vague promise.
2. Action first, technical background last.
3. Live URL, not draft path.
4. Exact route, not assumed automation.
5. Synthetic delivery, not green config.
6. Write-back, not verbal completion.
7. One requested resource, not hidden outreach funnel.
