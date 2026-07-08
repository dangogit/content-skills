---
name: hebrew-captioned-video-reels
description: Use when the user gives raw talking-head videos and asks to add Hebrew Instagram-style captions, cut silence, add a first-5s hook, avoid covering their face, and schedule the rendered reels to Facebook, Instagram, TikTok, and YouTube in Metricool.
---

# Hebrew Captioned Video Reels

Turn the user's raw talking-head clips into scheduled Hebrew reels.

## Default Output

- 1080x1920 MP4, H.264/AAC.
- Full-frame video. No split screen.
- Captions overlay video only, lower-third, never over the user's face.
- No topic/title label unless the user explicitly asks.
- First 5 seconds: large scroll-stopping Hebrew hook at top.
- B-roll must be big enough to read on phone. Default near full-width/tall window, not tiny picture-in-picture. Use about `1060x720` at top `112`, and enlarge further for UI/site demos when captions still fit.
- Spoken Israeli Hebrew. Short caption groups. Highlight one key word with `*word*`.
- Cut obvious silence and dead tails. Do not cut meaning.

## Caption CTA And Music Rules

- If a reel uses a CTA keyword or guide/resource route, the social caption must not include the public resource URL. Caption asks for the keyword comment only, for example `כתבו DESIGN ואשלח לכם בפרטי.` The link is delivered by DM automation.
- Do not add music sound names, music credits, or attribution text to the social caption unless the user explicitly approves visible credit in the current turn.
- Do not use CC-BY music for scheduled reels unless the user approves the required visible attribution first. If visible attribution is not approved, use no-attribution licensed music, platform-native audio after upload, or no music.
- If music is expected, verify the final MP4 has an actual mixed music bed. An AAC stream or voice audio is not proof. Do not claim music is included from the filename, notes, or an earlier version.
- Music must be human-audible on phone speakers. Do not rely on sub-bass drones or very low sine tones; include mid-range musical/pulse content and verify the generated bed itself is not buried before mixing. If the user cannot hear the bed, treat the music as missing.
- When the user wants music options, make short preview variants, present them in a local review page, wait for the user's selected option, then render only the selected mix into the final asset. Record the selected option name and source file in the reel README.
- Do not put public resource links, music sound names, or music credits into the social caption unless the user explicitly asks for visible caption text in the current turn.

## Motion Preset

- Default talking-head reel speed is `1.2x` when the user asks for faster delivery.
- Default subtle zoom loop: start at `95%`, zoom in to `105%` over `2s`, hold `105%` for `3s`, zoom out to `95%` over `2s`, hold `95%` for `3s`, then repeat. The low-scale hold is part of the loop, not optional.
- Keep zoom centered and crop-safe: no black edges, no face cut-off, no caption-face collision.
- When the user asks for tension background music and visible attribution is not approved, generate or use no-attribution bed and mix it audibly under voice. QA with `volumedetect`, `silencedetect`, and voice-only-vs-final audio difference before claiming music is present.

## Thumbnail And Cover

- Exact frame `0` of the final MP4 must already include the hook, because Metricool/platform cover selection may use the first frame and the connector may not expose a separate thumbnail field.
- Before upload, export and inspect frame `0` plus a 1-second opener frame. If frame `0` lacks the hook, fix the renderer or prepend a real hook cover before updating Metricool.
- For YouTube, target Shorts. Metricool may show `youtubeData.type:"video"` even for vertical short-form uploads when the connector lacks a Shorts field. Use a vertical `1080x1920` video under 3 minutes and, when update payload supports it, set YouTube type to `short`. Do not claim "Shorts verified" until Metricool/provider returns `short` or YouTube confirms it.

## Targeting And Folder Discipline

- Before trimming or replacing a scheduled video, verify exact target by schedule date, hook/title, Metricool id, uuid, and local filename. If the user says "June" but the active schedule is July, treat it as ambiguous until the planner proves the intended future post.
- If the wrong scheduled post was changed, restore from the last verified good asset first, then apply the requested edit only to the intended date/uuid.
- `videos-to-caption/uploaded/` is for assets that are scheduled or already published. Superseded files go under `videos-to-caption/archive/superseded/`. Rendered corrections that are uploaded to R2 but missed Metricool scheduling go under `videos-to-caption/ready-unscheduled/`.
- If the publish time has passed and the post leaves the pending planner, do not claim the correction is scheduled. Record it as `ready-unscheduled` with the failed update reason and planner proof boundary.

## Required Context

Before production or scheduling, follow repo `AGENTS.md`:

1. Read `content-system/pipeline.md`.
2. State Sync: `content-system/content-ledger.md`, Obsidian `Content Timeline - Metricool`, and Metricool planner when available.
3. Read `design/lessons.md` and `design/DESIGN.md`.
4. For scheduling, use brand `<METRICOOL_BLOG_ID>`, timezone `Asia/Jerusalem`.

## Transcribe

Use local Hebrew ASR:

```bash
python3 scripts/transcribe-hebrew-captions.py videos-to-caption/<file>.MOV
```

Preferred model: `ivrit-ai/whisper-large-v3-turbo-ct2` through `faster-whisper`.

Write:

- `<file>.captions.auto.json`
- `<file>.captions.auto.srt`
- `<file>.transcript.auto.txt`
- `<file>.captions.clean.json`

Clean captions manually before render. Keep each group short enough for one or two lines.

Hard rule: caption text must match what the user says. Do not rewrite captions into marketing copy, summaries, or improved phrasing. Only fix ASR mistakes, punctuation, obvious names, and bidi-safe Latin tokens such as `Claude Code`, `DESIGN.md`, `SQL`, `API`, `MCP`, `ElevenLabs`, and `Supabase`.

If a caption looks more polished than the spoken sentence, treat it as a defect and re-transcribe or correct from the audio.

## Render

Use `scripts/daily-reel/caption-video.mjs`.

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
      "captionBottom": 390,
      "captionFontSize": 68
    }
  }
]
```

Render:

```bash
node scripts/daily-reel/caption-video.mjs videos-to-caption/caption-jobs-vN.json
```

## Visual QA

Always inspect frames before calling done:

```bash
mkdir -p videos-to-caption/processed/qa-vN
ffmpeg -v error -y -ss 1 -i <out>.mp4 -frames:v 1 -update 1 -q:v 2 qa-opening.jpg
ffmpeg -v error -y -ss 9 -i <out>.mp4 -frames:v 1 -update 1 -q:v 2 qa-caption.jpg
ffmpeg -v error -y -i <out>.mp4 -vf "fps=1/5,scale=270:-1,tile=3x3" -frames:v 1 -update 1 -q:v 3 qa-contact.jpg
```

Check:

- Face is visible in opener and contact sheet.
- Hook is big, top, readable, not on face.
- Captions are lower-third and readable.
- No topic/title label.
- No broken Hebrew/LTR token layout.

Run:

```bash
node --check scripts/daily-reel/caption-video.mjs
cd scripts/daily-reel && npx tsc --noEmit
```

## Upload

Prefer Cloudflare R2 when `.env` has `CONTENT_R2_*`:

```bash
set -a; source .env; set +a
node scripts/ops/upload-artifact-r2.mjs <out>.mp4 \
  --prefix=content/reels/<slug> \
  --out=<manifest>.json
```

Verify public URL returns `200` and `video/mp4`.

## Metricool

Use Metricool app connector if direct MCP needs OAuth.

Default schedule target is Facebook + Instagram + TikTok + YouTube unless the user explicitly overrides:

- `blog_id`: `<METRICOOL_BLOG_ID>`
- `timezone`: `Asia/Jerusalem`
- `content_type`: `REEL`
- `networks`: `["facebook", "instagram", "tiktok", "youtube"]`
- `media`: `[public_mp4_url]`
- `tiktok_title`: hook without markup, short enough for TikTok
- `youtube_title`: hook without markup, short enough for YouTube
- `youtube_made_for_kids`: `false`
- `draft`: `false`
- time: 18:00 Israel for evening reels

If Metricool rejects any network, do not silently drop that network. Record the exact network and error, then schedule a subset only when the user explicitly waives the failed network in the current turn.

After create, refetch planner and record:

- Metricool id
- uuid
- date
- timezone
- per-network status for Facebook, Instagram, TikTok, and YouTube
- `draft:false`
- media count
- planner URL when returned

Write back to:

- `videos-to-caption/processing-notes.md`
- `content-system/content-ledger.md`
- `~/Obsidian/agent-memory/20-Projects/Content Timeline - Metricool.md`

Do not schedule or publish without the user's explicit current-turn approval.

### Replacement And Duplicate Gate

- Prefer replacing an existing scheduled post only when the Metricool update connector can refetch and prove the old id/uuid now points to the new media.
- If update fails, create a fresh post only after the user has explicitly approved scheduling in the current turn and all default networks are included.
- Immediately refetch the planner after a fresh create. If the old scheduled post still appears, do not describe the replacement as clean. Record `scheduled_with_duplicate_cleanup_needed`, the old id/uuid, the new id/uuid, and the exact update errors in the asset README, schedule JSON, `content-system/content-ledger.md`, and Obsidian timeline.
- Metricool may return `youtubeData.type:"video"` even when the upload is vertical and short-form. Record the returned type honestly. Treat it as a Shorts candidate only when YouTube or Metricool confirms Shorts.
