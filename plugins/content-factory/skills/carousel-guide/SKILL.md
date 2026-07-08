---
name: carousel-guide
description: Use when a carousel CTA asks viewers to comment a keyword for a guide, checklist, template, prompt pack, or DM resource. Creates and verifies the matching guide page, keyword routing, and active Instagram CTA automation before upload or scheduling.
---

# Carousel Guide

## Overview

Build the promised guide behind an Instagram carousel comment CTA. This skill turns a CTA keyword into a published guide page, safe DM routing, and an active route in the user's Instagram CTA automation service.

## When to Use

- A carousel says "comment <keyword>" or promises a guide by DM.
- A caption contains a comment keyword CTA.
- A Metricool carousel is about to be scheduled with a promised guide.
- the user asks to create guide pages for carousel CTAs.
- Existing carousel assets need matching guide URLs or Instagram AI-agent setup.

## Prerequisites

- No API keys required for planning.
- For publishing guide pages: access to `<website-repo>`.
- For carousel source: access to `<content-repo>/carousels/<slug>/`.
- For production deploy: use that website repo's existing Vercel/Git workflow.
- For CTA automation: access to `tools/instagram-cta-automation` and SSH host `mini` for `~/instagram-cta-automation`.

## Workflow

### Step 1: Extract CTA Contract

Read carousel `source.md`, `copy.md`, `caption.md`, or slide copy. Record:

- Carousel slug
- CTA keyword
- Viewer promise
- Target language
- Existing guide URL, if any
- Scheduled post id/uuid, if already scheduled

If no guide is promised, stop. Do not create guide work for a generic CTA.

### Step 2: Validate Keyword Safety

Apply `references/instagram-agent-routing.md`.

- Require one short keyword, easy to type.
- Reject keywords that are substrings of another active keyword.
- Reject broad words that collide with brand terms or common comments.
- Prefer exact whole-word triggers.
- If automation UI only supports "contains", use collision-proof keywords.

Example: `AGENT` collides with `AGENTIC`; use `SUBAGENT` for sub-agent guide.

### Step 3: Create Guide Source

Create or update guide source under the carousel folder:

```text
carousels/<slug>/guide.md
```

Required frontmatter:

```yaml
---
title: ""
slug: ""
created: YYYY-MM-DD
lang: he
cta_keyword: ""
carousel: "carousels/<slug>"
guide_url: "https://<your-domain>/guides/<guide-slug>"
status: draft
---
```

Guide body must include:

- What reader gets
- When to use it
- Copyable prompt or template boxes, if relevant
- Short checklist
- Common mistakes
- Next action

Keep Hebrew RTL natural. Use spoken Israeli Hebrew. Keep Latin tokens isolated in published HTML.

### Step 4: Publish Guide Page

Use website repo:

```bash
cd <website-repo>
```

Add or update:

- `app/guides/<guide-slug>/page.tsx`
- `app/guides/<guide-slug>/en/page.tsx` only when English version exists or fallback is needed
- `app/guides/guides.ts`
- `app/sitemap.ts`
- `components/nav.tsx` only if guide registry is not already powering nav
- `public/guides/<guide-slug>/` assets, if needed

Follow current site conventions. Prefer existing guide components/data patterns over new abstractions.

### Step 5: Verify Page

Run in website repo:

```bash
npx tsc --noEmit
npm run build
```

Verify:

- Guide URL returns 200.
- Hebrew page is RTL.
- Prompt/template boxes are copyable.
- Toolbar guide dropdown includes guide title.
- No keyword label appears in nav menu.
- Sitemap includes guide route.
- Production URL on `https://<your-domain>/guides/<guide-slug>/` still returns 200 after the final Vercel deploy. Dirty local Vercel deploys can overwrite a guide route; if production returns 404, redeploy from a clean website worktree that contains the guide.

### Step 6: Activate Instagram CTA Automation

Create or update:

```text
carousels/<slug>/dm-automation.md
```

Use `references/instagram-agent-routing.md` format:

- Trigger name
- Exact keyword
- Matching rule
- DM text
- Public reply, if any
- Guide URL
- Collision notes
- Agent knowledge snippet
- Q&A examples

Then wire the route into the automation service:

```bash
cd <content-repo>/tools/instagram-cta-automation
npm run add:route -- KEYWORD https://<your-domain>/guides/<guide-slug>/
npm run validate:routes
scp routes.json <host>:~/instagram-cta-automation/routes.json
ssh <host> 'cd ~/instagram-cta-automation && source ~/.nvm/nvm.sh && npm run validate:routes'
ssh <host> 'curl -s http://127.0.0.1:18787/health'
```

Verify the remote host health has:

- `dry_run:false`
- `poll_enabled:true`
- `last_error:null`

Run a synthetic dry-run on the the remote host, with no real Instagram send:

```bash
ssh <host> 'cd ~/instagram-cta-automation && source ~/.nvm/nvm.sh && DRY_RUN=1 STATE_FILE=/tmp/<keyword>-cta-test-events.jsonl node --input-type=module - <<'"'"'NODE'"'"'
import { processComments } from "./src/server.mjs";
const results = await processComments([{ commentId: "test-comment-<keyword>", mediaId: "test-media", text: "KEYWORD", fromId: null, followerState: true }]);
console.log(JSON.stringify(results, null, 2));
NODE'
```

The synthetic result must include the exact keyword and `status:"sent"`.

Mark `automation_status: active` only after the route is synced to the the remote host, route validation passes, health is clean, and the synthetic dry-run matches. If any step is missing, keep `automation_status: blocked` and do not upload or schedule unless the user explicitly waives it in the current turn.

### Step 7: Block Upload Until Contract Complete

Before Metricool scheduling, Instagram upload, or final "ship":

- Guide URL must be live or explicitly waived by the user in current turn.
- `dm-automation.md` must exist.
- CTA route must be active in `tools/instagram-cta-automation` locally and on the the remote host.
- the remote host health must be clean and synthetic dry-run must return `status:"sent"` for the exact keyword.
- CTA keyword must be collision-checked.
- Carousel `caption.md` must include the same keyword and guide promise.
- Asset `source.md` or `copy.md` must record `guide_url`, `cta_keyword`, and `automation_status`.
- Repo ledger and Obsidian timeline must record `automation_status: active` before final schedule handoff.

Do not ship a carousel that promises a guide when the guide does not exist or the CTA automation route is not active.

## Output Format

Write a short handoff:

```markdown
# Carousel Guide Handoff

Carousel:
Keyword:
Guide URL:
Automation status:
Trigger:
DM text:
Collision check:
Verified:
the remote host route:
Health:
Synthetic dry-run:
```

## Resources

- `references/instagram-agent-routing.md` - keyword, DM, Q&A, and knowledge-base rules for Instagram AI-agent setup.

## Key Principles

1. A promised guide is part of the carousel, not optional follow-up work.
2. Keyword safety matters. Avoid substring collisions.
3. Links, knowledge, and Q&A have different jobs in the Instagram agent.
4. Schedule is not done until guide URL and active the remote host CTA automation proof are recorded.
