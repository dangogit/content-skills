---
name: reel
description: Use when the user wants to turn a video clip into a published Facebook/Instagram/TikTok/YouTube reel - "make a reel", "add a hook to this video", "post this video", "תעלה את הסרטון", "/reel", or wants a colored Hebrew hook title burned onto a clip and the clip scheduled. For image carousels use the carousel skill instead.
---

# Reel Pipeline (video -> hook -> Metricool)

Take a raw vertical video, burn a 5-second colored Hebrew hook title over the first 5s, downscale, organize, and schedule it to Metricool as a Reel (Facebook + Instagram + TikTok + YouTube Short). Validated 2026-06-24 on 2 reels for @your-brand.

## Hub

| What | Path |
|---|---|
| Working dir | `<content-repo>/` |
| Output (one dir per reel) | `content/reels/YYYY-MM-DD-slug/` |
| Cover img2img generator (optional) | `content/scripts/generate-cover.mjs` |
| Headless Chrome (transparent PNG render) | `~/.cache/puppeteer/chrome-headless-shell/mac_arm-*/chrome-headless-shell-mac-arm64/chrome-headless-shell` |
| Metricool scheduling reference | memory `metricool-publishing.md` |

Brand palette (same as carousel): bg `#141413`, text `#faf9f5`, accent orange `#d97757`, green `#788c5d`. Assistant font, Hebrew RTL, no em dashes.

## Why a PNG overlay (not ffmpeg drawtext)

The local ffmpeg has **NO `drawtext`/freetype** filter, and ffmpeg drawtext cannot shape Hebrew RTL/bidi anyway. So the hook text is rendered as a **transparent PNG by headless Chrome** (correct RTL + web font + brand color) and composited with ffmpeg's `overlay` filter. Never try to burn Hebrew text with ffmpeg directly.

## Workflow

1. **Find the video.** Usually newest in `~/Downloads`:
   `find ~/Downloads -maxdepth 1 -type f \( -iname "*.mp4" -o -iname "*.mov" \) -newermt "-1 day"` then `ls -lt`. Confirm with the user which clip if ambiguous.
2. **Probe specs:** `ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,duration -of default=noprint_wrappers=1 video.mp4`. Talking-head reels are usually 1080x1920 or 2160x3840 (4K), 9:16.
3. **Get the hook text from the user** (a short punchy Hebrew title, 2-4 words). Don't invent it - propose options and let the user pick.
4. **Organize:** `mkdir -p content/reels/<slug>` and `cp` the raw clip to `content/reels/<slug>/video.mp4`. Add `reels/**/*.mp4` to `content/.gitignore` (videos too big for git; md stays tracked).
5. **Write `hook.html`** (transparent, RTL, Assistant font, orange text on a dark scrim panel positioned in the upper area so it clears any existing burned-in subtitles). Sized to the video's exact WxH. Template below.
6. **Render the transparent PNG** with chrome-headless-shell:
   ```bash
   CHS="$HOME/.cache/puppeteer/chrome-headless-shell/mac_arm-147.0.7727.57/chrome-headless-shell-mac-arm64/chrome-headless-shell"
   "$CHS" --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
     --window-size=<W>,<H> --default-background-color=00000000 --virtual-time-budget=4000 \
     --screenshot="content/reels/<slug>/hook.png" "file://$PWD/content/reels/<slug>/hook.html"
   ```
   `--default-background-color=00000000` = transparent. Adjust the chrome-headless-shell version dir to whatever is installed (`ls ~/.cache/puppeteer/chrome-headless-shell/`).
7. **Overlay onto first 5s** (hardware encode for speed, audio copied untouched). Note the `?` in `-map "0:a?"` MUST be quoted in zsh:
   ```bash
   ffmpeg -y -hide_banner -loglevel error \
     -i video.mp4 -i hook.png \
     -filter_complex "[0:v][1:v]overlay=0:0:enable='lte(t,5)'[v]" \
     -map "[v]" -map "0:a?" \
     -c:v h264_videotoolbox -b:v 40M -tag:v avc1 -c:a copy -pix_fmt yuv420p -movflags +faststart \
     video-hooked.mp4
   ```
8. **Verify** the overlay timing: extract a frame at t=2s (hook visible) and t=7s (hook gone) with `ffmpeg -ss N -i video-hooked.mp4 -frames:v 1 -vf scale=720:-1 /tmp/f.png` and Read them.
9. **Downscale for upload** to 1080x1920 (4K is overkill for reels + too big to host):
   ```bash
   ffmpeg -y -hide_banner -loglevel error -i video-hooked.mp4 -vf "scale=1080:1920:flags=lanczos" \
     -c:v h264_videotoolbox -b:v 8M -tag:v avc1 -c:a aac -b:a 128k -pix_fmt yuv420p -movflags +faststart \
     video-1080.mp4
   ```
10. **Write `copy.md`** in the reel dir: caption, hashtags, hook text, source-clip timing, status. (Caption voice = spoken Israeli Hebrew, no em dashes. **No inline "AI" in Hebrew lines** - it scrambles bidi in plain IG captions; write "סוכן"/"בינה מלאכותית"/"המודל" or isolate the Latin token on its own line.)
11. **Host + schedule** - see Publishing below.

## Hook HTML template

Sized to the video (replace `1080`/`1920` with the actual WxH, scale font ~`180px` for 1080-wide, ~`210px` for 2160-wide). Panel sits in the upper third.

```html
<!doctype html>
<html lang="he" dir="rtl"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@800&display=swap" rel="stylesheet">
<style>
  html,body{margin:0;padding:0;width:1080px;height:1920px;background:transparent;overflow:hidden;}
  .stage{width:1080px;height:1920px;display:flex;justify-content:center;align-items:flex-start;}
  .panel{margin-top:280px;max-width:860px;padding:30px 50px;background:rgba(0,0,0,0.42);border-radius:36px;text-align:center;}
  .hook{font-family:'Assistant','Arial Hebrew',sans-serif;font-weight:800;font-size:120px;line-height:1.12;
        color:#d97757;text-shadow:0 6px 30px rgba(0,0,0,0.9),0 2px 6px rgba(0,0,0,1);margin:0;direction:rtl;}
</style></head>
<body><div class="stage"><div class="panel"><p class="hook">HOOK TEXT HERE</p></div></div></body></html>
```

## Publishing (Metricool)

Host the `video-1080.mp4` on a public URL, then schedule. Full method + gotchas in memory `metricool-publishing.md`. Short version:

- **Host:** `curl -s -F "file=@video-1080.mp4" https://tmpfiles.org/api/v1/upload` -> returns a viewer URL; the direct URL is the same with `/dl/` inserted: `https://tmpfiles.org/dl/<id>/<name>`. (litterbox.catbox.moe also works but rate-limits after ~a dozen uploads.) tmpfiles throws an occasional `520` - verify the URL came back, retry if not.
- **Schedule** with the Metricool MCP `createScheduledPost`: blogId `<METRICOOL_BLOG_ID>`, `date` ISO+03:00, `info.media=[<direct url>]`, `providers=[{facebook},{instagram},{tiktok},{youtube}]`, `facebookData {type:"REEL"}`, `instagramData {type:"REEL"}`, `tiktokData {title, privacyOption:"PUBLIC_TO_EVERYONE"}`, `youtubeData {title, type:"short", privacy:"public", madeForKids:false}`, `publicationDate {dateTime, timezone:"Asia/Jerusalem"}`, `autoPublish:true`.
- When using the Metricool app connector, use `networks:["facebook","instagram","tiktok","youtube"]`, `content_type:"REEL"`, one public MP4 URL, `tiktok_title`, `youtube_title`, and `youtube_made_for_kids:false`.
- Never silently drop a default network. If Metricool rejects Facebook, Instagram, TikTok, or YouTube, record the exact network and error, then schedule a subset only when the user explicitly waives the failed network in the current turn.
- Metricool ingests the video into its own CDN at schedule time, so the temp URL only needs to live during the call.
- **Cadence:** the user posts videos in the **evening (18:00 Israel)**, carousels in the morning. Best-time per network via `getBestTimeToPostByNetwork`.

## Gotchas

- ffmpeg has no `drawtext` here - Hebrew hook MUST be a Chrome-rendered PNG overlay. Don't fight it.
- Position the hook panel in the UPPER area - talking-head clips often have burned-in subtitles at the bottom; overlapping looks broken.
- `-map "0:a?"` - quote it in zsh or the `?` globs and the command fails.
- Use `h264_videotoolbox` (Apple HW encoder) for speed; `libx264` is slow on 4K60.
- Keep the 4K original `video.mp4` and the hooked `video-hooked.mp4`; upload the `video-1080.mp4`.
- Metricool has no delete tool - to unschedule, `updateScheduledPost` with `draft:true, autoPublish:false`.
- TikTok auto-publish may force private/draft if the account's API access isn't fully audited - flag this to the user.
- YouTube or Facebook may reject vertical videos or missing account/title requirements in some Metricool flows - verify planner status per network before calling scheduled.
- @your-handle is NOT connected to Metricool; only @your-brand (brand <METRICOOL_BLOG_ID>).
