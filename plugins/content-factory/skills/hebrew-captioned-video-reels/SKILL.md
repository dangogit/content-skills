---
name: hebrew-captioned-video-reels
description: Produce or correct Hebrew-captioned talking-head Reels with transcript fidelity, cut review, frame-zero, audio, rights, privacy, upload, and verified scheduling gates. Use for raw talking-head video, podcast cuts, Hebrew captions, Reel corrections, or Metricool Reel scheduling.
---

# Hebrew Captioned Video Reels

Turn the creator's raw talking-head clips into scheduled Hebrew reels.

## Overview

Transcribe, edit, caption, render, and verify Hebrew talking-head video. Production
and publishing remain separate gates: rendering may proceed from approved source,
but scheduling requires explicit current-turn approval and complete CTA/resource proof.

## When to Use

- Creator supplies raw talking-head video for Hebrew captions and hook treatment.
- Long podcast or interview needs reviewable candidate cuts.
- Existing scheduled Reel needs exact-target correction or replacement.
- Final Reel needs Metricool verification for every network selected in configuration.

## Prerequisites

- A project renderer and transcription workflow, or an existing finished video
  that needs only QA and scheduling.
- `ffmpeg`, `ffprobe`, and the dependencies required by the selected project
  workflow.
- Metricool and configured public-upload provider access required only for publish phase.
- `.content-factory.json` configured before upload or scheduling.
- Source footage, music, SFX, logos, and B-roll cleared for intended public use.
- Current-turn approval required before scheduling or replacing live records.

## Default Output

- 1080x1920 MP4, H.264/AAC.
- Full-frame video. No split screen.
- Captions overlay video only, lower-third, never over the creator's face.
- No topic/title label unless the creator explicitly asks.
- Opening beat: readable Hebrew hook in a verified safe region. Do not assume a
  fixed five-second duration.
- B-roll must be big enough to read on a phone. Prefer a large window for UI or
  site demos, then validate it against face, captions, and platform chrome.
- Spoken Israeli Hebrew. Short caption groups. Highlight one key word with `*word*`.
- Cut obvious silence and dead tails. Do not cut meaning.

## Caption CTA And Music Rules

- If a reel uses a CTA keyword or guide/resource route, the social caption must not include the public resource URL. Caption asks for the keyword comment only, for example `כתבו DESIGN ואשלח לכם בפרטי.` The link is delivered by DM automation.
- Do not add music sound names, music credits, or attribution text to the social caption unless the creator explicitly approves visible credit in the current turn.
- Do not use CC-BY music for scheduled reels unless the creator approves the required visible attribution first. If visible attribution is not approved, use no-attribution licensed music, platform-native audio after upload, or no music.
- Before scheduling, inspect every `music` and `sfx` source referenced by the render job, not only the main music bed. Every audio source must have an approved license record or the creator's explicit current-turn rights approval. If any source is marked unknown or blocked, do not schedule that render.
- If a final render contains unapproved music or SFX, create a publish-safe copy before upload: keep the approved video pixels, replace audio with the original voice track only, preserve cuts and playback speed, and record the difference in the schedule proof. Do not describe that publish-safe file as having music or SFX.
- If music is expected, verify the final MP4 has an actual mixed music bed. An AAC stream or voice audio is not proof. Do not claim music is included from the filename, notes, or an earlier version.
- Music must be human-audible on phone speakers. Do not rely on sub-bass drones or very low sine tones; include mid-range musical/pulse content and verify the generated bed itself is not buried before mixing. If the creator cannot hear the bed, treat the music as missing.
- When the creator wants music options, make short preview variants, present them in a local review page, wait for the creator's selected option, then render only the selected mix into the final asset. Record the selected option name and source file in the reel README.
- Do not put public resource links, music sound names, or music credits into the social caption unless the creator explicitly asks for visible caption text in the current turn.

### Keyword CTA Ship Gate

Keyword CTA blocks scheduling until all pass:

- Named artifact, not generic "guide".
- Production guide URL returns `200`.
- Exact collision-safe keyword exists in local route registry.
- Route deployed through the approved process.
- Route validation passes in the deployment environment.
- Configured `cta_automation_base_url` reports ready, non-dry-run state with no
  current error.
- Controlled synthetic test returns the exact keyword and configured success
  status without contacting an uninvolved account.
- Dedupe and rate limits pass; logs and retention follow the resource-gate policy.
- Asset notes, ledger, and timeline record `guide_url`, `cta_keyword`, and
  `automation_status: active`.

Use `carousel-guide` resource/automation workflow until generalized
`comment-resource-gate` replaces it. It applies to Reels too.

## Motion Preset

- Preserve natural speech speed unless the creator requests a change. Compare the
  requested speed with intelligibility and caption timing before accepting it.
- Use a subtle zoom only when it supports the scene. Keep scale within crop-safe
  bounds and inspect the complete loop instead of relying on a fixed preset.
- Keep zoom centered and crop-safe: no black edges, no face cut-off, no caption-face collision.
- When the creator asks for tension background music and visible attribution is not approved, generate or use no-attribution bed and mix it audibly under voice. QA with `volumedetect`, `silencedetect`, and voice-only-vs-final audio difference before claiming music is present.

Minimum audio proof:

```bash
ffprobe -v error -show_entries stream=index,codec_type,codec_name,channels,sample_rate \
  -of json <final.mp4>
ffmpeg -v error -i <final.mp4> -af volumedetect -f null - 2>&1
ffmpeg -v error -i <final.mp4> -af silencedetect=noise=-40dB:d=1 -f null - 2>&1
```

Also compare voice-only and final mixes at same timestamp on phone speakers. Reject
clipping, unintended silence, buried bed, or voice masking. Record measured values and
human listen result. No single loudness number proves good mix.

Run the fast media gate before upload:

```bash
"${CLAUDE_PLUGIN_ROOT}/skills/hebrew-captioned-video-reels/scripts/check-reel-media.sh" <final.mp4>
```

This checks the machine-verifiable media contract only. Complete the human
frame, caption, phone-listen, CTA, and planner checks below as well.

Check the handoff record before calling the reel complete:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/hebrew-captioned-video-reels/scripts/check_reel_manifest.py" <handoff.md>
```

## Thumbnail And Cover

- Exact frame `0` of the final MP4 must already include the hook, because Metricool/platform cover selection may use the first frame and the connector may not expose a separate thumbnail field.
- Keep the hook inside the Instagram-safe readable band, not at the very top. Default final-render hook position should use `brand.hookTop` around `230-300`, then QA frame `0` in feed-safe context. If the creator says the hook is too high, lower `brand.hookTop`, do not shrink text first.
- Before upload, export and inspect frame `0` plus a 1-second opener frame. Frame `0` must have a readable hook and a usable face frame: eyes open, not mid-blink, not awkward, not hidden by motion blur. If frame `0` lacks the hook or has closed eyes, fix the renderer or prepend a short real hook cover before updating Metricool.
- For single-clip fixes where the video is otherwise approved, a `0.5s` cover freeze from a nearby clean frame is acceptable. Re-run media gate and regenerate the frame-zero contact sheet after adding it. Do not rely on a good `t=1s` frame as proof that the platform preview is good.
- For YouTube, target Shorts. Metricool may show `youtubeData.type:"video"` even for vertical short-form uploads when the connector lacks a Shorts field. Use a vertical `1080x1920` video under 3 minutes and, when update payload supports it, set YouTube type to `short`. Do not claim "Shorts verified" until Metricool/provider returns `short` or YouTube confirms it.

## Targeting And Folder Discipline

- Before trimming or replacing a scheduled video, verify exact target by schedule date, hook/title, Metricool id, uuid, and local filename. If the creator says "June" but the active schedule is July, treat it as ambiguous until the planner proves the intended future post.
- If the wrong scheduled post was changed, restore from the last verified good asset first, then apply the requested edit only to the intended date/uuid.
- When the project provides lifecycle folders, keep scheduled/published,
  superseded, and ready-but-unscheduled assets separate. Do not infer those
  states from file location alone.
- If the publish time has passed and the post leaves the pending planner, do not claim the correction is scheduled. Record it as `ready-unscheduled` with the failed update reason and planner proof boundary.

## Workflow

### Required Context

Before production or scheduling, follow repo `AGENTS.md` and read only configured,
existing project files:

1. Read configured pipeline and ledger files when present. Otherwise record
   recent assets, duplicate risk, planner state, and objective in the handoff.
2. Read configured design system and design lessons when present.
3. For music, require a license record. Read configured `music_licenses_path`
   when present.
4. For publishing fallback, use only a user-approved, documented project
   integration. Never infer credentials or targets.
5. Read `.content-factory.json`. If publishing target, timezone, or approved
   networks are missing, stop before upload or scheduling.

## Transcribe

Use local Hebrew ASR:

```bash
python3 "${CLAUDE_PROJECT_DIR}/scripts/transcribe-hebrew-captions.py" \
  "${CLAUDE_PROJECT_DIR}/videos-to-caption/<file>.MOV"
```

Preferred model: `ivrit-ai/whisper-large-v3-turbo-ct2` through `faster-whisper`.

Write:

- `<file>.captions.auto.json`
- `<file>.captions.auto.srt`
- `<file>.transcript.auto.txt`
- `<file>.captions.clean.json`

Clean captions manually before render. Keep each group short enough for one or two lines.

Hard rule: caption text must match what the creator says. Do not rewrite captions into marketing copy, summaries, or improved phrasing. Only fix ASR mistakes, punctuation, obvious names, and bidi-safe Latin tokens such as `Claude Code`, `DESIGN.md`, `SQL`, `API`, `MCP`, `ElevenLabs`, and `Supabase`.

If a caption looks more polished than the spoken sentence, treat it as a defect and re-transcribe or correct from the audio.

## Long Podcast Review Workflow

For long videos, do not jump from ASR candidates straight to final reels. Use a review loop first.

Default division of responsibility:

- HTML review editor = choose and fix cut points.
- Remotion = final render with hook, captions, motion, music, and QA.
- `ffmpeg` preview cuts are allowed for fast review only, but final output goes through the configured project renderer.

Review editor requirements:

- Show context around each candidate, not only the already-cut clip. Default context window: `8s` before proposed start and `8s` after proposed end, unless source constraints require smaller proxies.
- Let the creator play:
  - before context
  - selected range
  - after context
- Let the creator set boundaries from the current playback head:
  - `Set start here`
  - `Set end here`
- Include numeric `Start` and `End` fields in seconds for precise trim changes.
- Include keep/reject buttons and a free-text notes field per clip.
- Persist choices in `localStorage`.
- Export JSON with, at minimum:

```json
{
  "id": "clip-id",
  "choice": "keep",
  "note": "start after breath",
  "sourceStartSec": 175.0,
  "sourceEndSec": 253.0,
  "proposedStartSec": 183.0,
  "proposedEndSec": 245.0,
  "finalStartSec": 183.4,
  "finalEndSec": 244.8
}
```

Cut-boundary rules:

- Avoid cutting inside words or while the creator is mid-sentence.
- Check proposed start/end against ASR segment boundaries and the silence map.
- If a proposed boundary falls inside an ASR caption segment, either expand to the nearest clean boundary or mark it for the creator review in the HTML editor.
- Prefer a little extra leading/trailing breathing room in review. Tighten only after the creator approves the exact boundary.
- Do not rely on speaker classifier alone for the creator-only cuts. Use transcript cues and audio/video review.

Only add a waveform package after the manual loop proves useful. If needed later, use `wavesurfer.js` for waveform selection. Until then, native HTML video controls plus `currentTime` are enough.

## Render

Use `${CLAUDE_PROJECT_DIR}/scripts/daily-reel/caption-video.mjs` when present,
or the renderer configured by the consumer project.

Create job JSON like:

```json
[
  {
    "id": "IMG_0000-v1",
    "input": "IMG_0000.MOV",
    "captions": "IMG_0000.captions.clean.json",
    "output": "processed/v1/IMG_0000-captioned-v1.mp4",
    "base": "processed/base-v1/IMG_0000-base-v1.mp4",
    "layout": "cover",
    "trimStartSec": 0,
    "trimEndSec": 48.9,
    "hook": "בוט בלי דאטה = *ניחוש*",
    "hookDurSec": 5,
    "cuts": [
      { "startSec": 12.3, "endSec": 12.9 }
    ],
    "brand": {
      "hookTop": 260,
      "hookFontSize": 82,
      "captionBottom": 390,
      "captionFontSize": 68
    }
  }
]
```

Render:

```bash
node "${CLAUDE_PROJECT_DIR}/scripts/daily-reel/caption-video.mjs" \
  "${CLAUDE_PROJECT_DIR}/videos-to-caption/caption-jobs-vN.json"
```

## Visual QA

Always inspect frames before calling done:

```bash
mkdir -p videos-to-caption/processed/qa-vN
ffmpeg -v error -y -i <out>.mp4 -frames:v 1 -update 1 -q:v 2 qa-frame-zero.jpg
ffmpeg -v error -y -ss 1 -i <out>.mp4 -frames:v 1 -update 1 -q:v 2 qa-opening.jpg
ffmpeg -v error -y -ss 9 -i <out>.mp4 -frames:v 1 -update 1 -q:v 2 qa-caption.jpg
ffmpeg -v error -y -i <out>.mp4 -vf "fps=1/5,scale=270:-1,tile=3x3" -frames:v 1 -update 1 -q:v 3 qa-contact.jpg
```

Check:

- Frame zero contains readable hook inside safe area.
- Face is visible in opener and contact sheet.
- Hook is big, readable, not on face, and not hidden by Instagram top feed chrome.
- Captions are lower-third and readable.
- No topic/title label.
- No broken Hebrew/LTR token layout.
- Every caption group was sampled at least once, not only t=1s and t=9s.
- Every cut boundary plays without clipped word, duplicated frame, or A/V jump.
- B-roll never collides with hook, captions, face, or platform UI.
- Final duration, dimensions, codecs, audio channels, and frame rate match target.

Probe final media:

```bash
ffprobe -v error -show_entries \
  format=duration:stream=index,codec_type,codec_name,width,height,r_frame_rate,channels \
  -of json <out>.mp4
```

Run:

```bash
node --check "${CLAUDE_PROJECT_DIR}/scripts/daily-reel/caption-video.mjs"
cd "${CLAUDE_PROJECT_DIR}/scripts/daily-reel" && npx tsc --noEmit
```

## Upload

Public upload makes draft reachable outside local machine. Upload only after
creator explicitly approves public exposure and rights review passes. Never
upload private source footage, credentials, hidden client material, or an
unapproved draft. Use configured provider; example below assumes project R2
uploader and required variables are already exported by trusted environment:

```bash
node "${CLAUDE_PROJECT_DIR}/scripts/ops/upload-artifact-r2.mjs" <out>.mp4 \
  --prefix=content/reels/<slug> \
  --out=<manifest>.json
```

Verify public URL returns `200` and `video/mp4`.

R2 uploads can fail transiently with Node/undici errors such as `write EPIPE`,
`UND_ERR_SOCKET`, or `other side closed`. Retry only missing manifest files; do not
re-upload files whose manifest already exists and whose public URL verifies. For URL
checks, prefer `HEAD`/`curl -I` for MIME and status so large MP4s are not downloaded
just to prove `video/mp4`.

## Metricool

Use Metricool app connector if direct MCP needs OAuth.

Call `get_brand_settings` first and use returned brand timezone for create and
refetch. Live provider value wins over local example configuration.

Before creating posts, refetch planner for relevant future window. Do not schedule
into occupied slot unless creator explicitly approves collision. For batches, use
configured cadence and record selection reason.

Schedule only configured and explicitly approved networks:

- `blog_id`: `.content-factory.json.metricool_blog_id`
- `timezone`: live brand setting, falling back to configured `metricool_timezone`
- `content_type`: `REEL`
- `networks`: `.content-factory.json.publishing_networks`
- `media`: `[public_mp4_url]`
- `tiktok_title`: hook without markup, short enough for TikTok
- `youtube_title`: hook without markup, short enough for YouTube
- `youtube_made_for_kids`: `false`
- `draft`: `false`
- time: `.content-factory.json.reel_schedule_time`

If Metricool rejects any approved network, do not silently drop it. Record exact
network and error, then schedule subset only when creator explicitly waives failed
network in current turn.

After create, refetch planner and record:

- Metricool id
- uuid
- date
- timezone
- per-network status for every configured network
- `draft:false`
- `autoPublish:true`
- media count
- exact media URL or Metricool CDN URL when returned
- proof that each Metricool CDN media URL returns `200 video/mp4`
- planner URL when returned

Write back to the asset README or processing record, schedule JSON or `meta.json`
when present, and every configured ledger and timeline. If none exists, retain the
complete handoff packet and do not claim external write-back.

Do not schedule or publish without the creator's explicit current-turn approval.

### Replacement And Duplicate Gate

- Prefer replacing an existing scheduled post only when the Metricool update connector can refetch and prove the old id/uuid now points to the new media.
- If update fails, create a fresh post only after creator explicitly approves scheduling in current turn and all configured approved networks are included.
- Immediately refetch the planner after a fresh create. If the old scheduled post
  still appears, do not describe the replacement as clean. Record
  `scheduled_with_duplicate_cleanup_needed`, both ids/uuids, and exact update
  errors in the asset handoff plus every configured ledger and timeline.
- Metricool may return `youtubeData.type:"video"` even when the upload is vertical and short-form. Record the returned type honestly. Treat it as a Shorts candidate only when YouTube or Metricool confirms Shorts.

## Output Format

```markdown
# Hebrew Reel Handoff

Source:
Final MP4:
Duration / dimensions / codecs:
Hook:
Caption source:
Caption QA:
Cut-boundary QA:
Music source / license:
Audio measurements:
Phone listen test:
Frame-zero proof:
CTA keyword:
Guide URL:
Automation status:
Upload URL / MIME:
Metricool id / uuid:
Networks:
Planner refetch:
Status:
```

## Resources

- `${CLAUDE_PLUGIN_ROOT}/skills/hebrew-captioned-video-reels/references/qa-contract.md` - final media, pixel, audio, CTA, and publish proof.
- `${CLAUDE_PLUGIN_ROOT}/skills/hebrew-captioned-video-reels/scripts/check-reel-media.sh` - executable H.264/AAC/1080x1920/duration gate.
- `${CLAUDE_PLUGIN_ROOT}/skills/hebrew-captioned-video-reels/scripts/check_reel_manifest.py` - required proof-field gate for the handoff.
- Project renderer, transcriber, and uploader only when explicitly selected by the
  user or configured by the project.
- Configured music license, pipeline, ledger, design-system, and design-lessons
  paths when present.
- `carousel-guide` - current named-resource and CTA automation workflow, also
  required for keyword Reels.
- `${CLAUDE_PLUGIN_ROOT}/references/configuration.md` - public configuration contract.

## Key Principles

1. Caption text matches speech exactly.
2. Final pixels and audio prove quality.
3. Keyword CTA never ships to dead route.
4. Exact Metricool target is verified before replacement.
5. Render complete does not mean publish complete.
