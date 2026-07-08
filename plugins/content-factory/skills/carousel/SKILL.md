---
name: carousel
description: Use when the user wants an Instagram carousel - "carousel", "קרוסלה", "make slides", "post about X on @your-handle", "/carousel" - or wants to iterate on a previous carousel version with feedback.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Skill
  - AskUserQuestion
---

# Instagram Carousel Pipeline (@your-handle)

Produces 10-slide Hebrew RTL carousel PNGs (1080x1350) in the Claude brand: Nano Banana 3D centerpieces with baked Hebrew text by default, plus open-carrusel chrome/fallback layers and Puppeteer export. Validated 2026-06-10 across 3 full decks (fable-5-launch v3.3, fable-5-dos-donts v1.2, fable-5-ai-builds-ai v1.1).

**Sibling skills:** `carousel-with-face` (same pipeline but the user's face on hook/CTA via img2img), `reel` (video -> hook overlay -> Metricool). **Publishing now goes through the Metricool MCP** to **@your-brand** (brand <METRICOOL_BLOG_ID>), not the old Graph-API/browser-use scripts. **Always schedule carousels to Instagram + Facebook + TikTok** (the user, 2026-07-06): `providers:[{network:"instagram"},{network:"facebook"},{network:"tiktok"}]`, `facebookData:{type:"POST"}`, `tiktokData:{photoCoverIndex:0, privacyOption:"PUBLIC_TO_EVERYONE"}` (TikTok photo/slideshow mode accepts the same 10 JPEGs). Not YouTube - YouTube has no image-carousel post type. Media is **JPEG ONLY - Instagram's API cannot fetch PNG ("media could not be fetched", live failure 2026-07-02)**. Convert slides first: `sips -s format jpeg -s formatOptions 90 slide-N.png --out metricool-jpg/slide-N.jpg`, then upload with `scripts/upload-carousel-media.mjs` so MIME is `image/jpeg`. Default provider is tmpfiles; if tmpfiles errors or direct checks fail, use `--provider=litterbox --litterbox-time=72h`; Litterbox may return `https://litter.catbox.moe/...`, which is valid. If 2K JPG uploads time out, create upload-only 1080x1350 JPEG copies and keep review PNGs untouched. Carousels go morning (10:00 Israel). See memory `metricool-publishing.md`. Canonical post-slides templates with R25-R28 layout variety: `content/carousels/2026-06-24-loop-engineering/v1/` (faceless) and `2026-06-24-agentic-engineering/v1/` (face); from 2026-07-02 every deck also needs the R39 blueprint in source.md. Scheduling proof requires Metricool create response plus planner refetch, then write id, uuid, time, timezone, network status, draft state, autoPublish state, and media count into source/copy, version meta, caption, repo ledger, and Obsidian timeline.

## Hub

Everything lives in `<content-repo>/` (its CLAUDE.md = workflow contract):

| What | Path |
|---|---|
| Design system (palette, text budget, anatomy) | `design/DESIGN.md` |
| Learned rules - READ BEFORE EVERY GENERATION | `design/lessons.md` |
| Feedback log (append every iteration) | `design/feedback-log.md` |
| Style references + analysis (peleg.auto) | `design/references/ANALYSIS.md` |
| Image gen script (Nano Banana) | `scripts/generate-image.mjs` |
| Renderer (open-carrusel, dev server :3000) | `tools/open-carrusel/` |
| Canonical slide-code template (newest, full deck) | `carousels/2026-06-10-fable-5-ai-builds-ai/v1/post-slides.mjs` |
| In-place slide-update pattern (PUT) | `carousels/2026-06-10-fable-5-ai-builds-ai/v1/patch-v11.mjs` |
| Output | `carousels/YYYY-MM-DD-slug/vN/` |
| IG auto-poster (browser-use -> real Chrome) | `scripts/instagram/post_browseruse.py` (venv `<content-repo>/.venv-bu`) |
| IG API poster (Graph API, no UI) | `scripts/instagram/post.mjs` + `SETUP.md` (needs Meta app creds; not wired yet) |

The canonical template bakes in the validated style: pills chrome, `padH()` ivory headline backdrop (R19), `darkPill()` callout card, do/don't `tag()` pills, `gradH` gradient headlines, dark/paper rhythm (dark hook -> paper body -> one dark stat mid-deck -> dark CTA -> paper recap).

Gemini key: Keychain `GEMINI_API_KEY_CAROUSEL` (script loads it itself). Never write it to files.

## Copy/Creative Prompt Pack

Before carousel copy or visual planning, read:

- `library/prompts/prompt-pack/README.md`
- `library/prompts/prompt-pack/source/ui-lib-prompts/copy.ts`
- `library/prompts/prompt-pack/source/ui-lib-prompts/creative.ts`
- `library/prompts/prompt-pack/source/ui-lib-prompts/creative-designer.ts`

Use the prompt pack as craft layer:

- Copy pass: hook, pain, desire, objection, CTA.
- Visual pass: one concrete physical scene or object per slide.
- Prompt pass: production-ready NBP / img2img prompt, no placeholders.

Adaptation rules:

- the content niche stays Claude Code, Codex, agents, skills, memory, MCP, operator workflows.
- Hebrew stays spoken Israeli. No translated ad Hebrew.
- Instagram inspiration split: global accounts provide new topic velocity; Israeli/Hebrew accounts provide local pain language, CTA style, and Israel trend signals. Combine both when useful, but never copy source text, screenshots, layout, assets, or exact CTA wording.
- Current experiment: image carries scene plus primary Hebrew text. Prompt the object and Hebrew text as one physical composition, often with subtle 3D/embossed/extruded/glowing material treatment. Best default is one front-facing physical text plane for focal/support copy, plus one separate proof badge only when explicitly needed. Use HTML text only as fallback when generated Hebrew spelling, bidi, or legibility fails.
- the prompt pack sharpens output, `design/DESIGN.md` and `design/lessons.md` still decide final form.

## Workflow

1. **Read `design/lessons.md` + `design/DESIGN.md` first.** Non-negotiable - rules R1-R79+ are accumulated taste. Apply ALL of them.
2. Source content (research report / brief). Save pointer in `carousels/<slug>/source.md` including source lane (`global trend`, `Israeli Hebrew signal`, or `owner proof`) and an "R17 fact basis" section mapping each claim slide to its source line. For Instagram inspiration, run or cite `node scripts/instagram-fetch-carousels.mjs --since-days=1` plus `node scripts/instagram-build-briefs.mjs --limit=100`; use global sources for new ideas and Israeli sources for pain-first Hebrew phrasing. Fact-check claim slides before export.
3. **copy prompt pass:** use `copy.ts` to sharpen hook / pain / desire / objection / CTA before showing copy.
4. **Gemini Pro copy review + improvement gate (R57/R58/R59, REQUIRED before image spend):** after the first Hebrew draft, run `node scripts/sharpen-copy.mjs --model pro --mode both --in <copy.md> --context <source.md> --out <version>/review/gemini-pro-copy-review.md`. Default `pro` = `gemini-3.1-pro-preview`. Use `Improved Copy` as the next draft unless a change is rejected with a clear reason. Resolve every `Flags` item before approving copy. If Pro flags an unsupported number, vague promise, CTA collision, weak hook, repeated cadence, or baked-text renderability issue, rewrite the copy or add a real source and rerun Pro before Nano Banana generation. If visual QA later shows Nano Banana dropped words, misspelled Hebrew, or crowded a baked line, shorten that specific line, record the rejection reason, and rerun Pro in `--mode review`. If Pro changes copy after baked images exist, regenerate the affected slides. Before upload, scheduling, or Metricool replacement, run a fresh current-state audit with `--mode review` on the final copy and current `source.md`; store it as `review/gemini-pro-current-audit-YYYY-MM-DD.md` and point `meta.json.copyReview.path` at it. This catches guide URL, CTA, proof, and stale-context issues after visual work. Do not keep a line just because it will look good visually.
5. **Copy-first checkpoint (validated workflow): write the full 10-slide Hebrew copy as TEXT, show the user, iterate until approved. Zero image spend before copy approval and Gemini Pro flag resolution.** Structure: hook / re-hook / 6 value / CTA / recap-action. Copy voice per R18: spoken Israeli Hebrew, punchy, native idioms, never translated-English. Text budget caps in DESIGN.md section 4. **Hook gate (R40):** slide 1 must pass STAKE (names a cost/loss/consequence) + SYMPTOM (something the viewer experienced this week, R37) + SPECIFIC (a number, named tool, or concrete scene). Abstract thesis hooks are drafts. **User-phrasing (R46):** when the user supplies a brief, reuse their exact expressions instead of copywriter-Hebrew rewrites; CTA speaks first person ("ואני שולח לכם"). **Cadence variety (R41):** the 10 focal lines read aloud must rotate forms (question / command / number-claim / contrast / scene / quote); same syntactic pattern on 3+ slides = rewrite; max 2 "question? answer." slides per deck. CTA keyword: one short English word tied to the topic (used: FABLE, GUIDE, LOOP; shelved deck B uses FACTS). If CTA promises a guide or DM resource, invoke `carousel-guide` before upload/schedule.
6. **Deck blueprint (R39, REQUIRED before any image spend).** Append to `source.md` a table - one row per slide: `archetype` (DESIGN.md section 7 library: hero / big-number / split / object-caption / card-stack / quote / terminal), `base` (image / flat-dark; `paper` is OPT-IN only per R44 - decks are dark end to end, no white cards or ivory pills), `metaphor` (one physical object), `focal line`, `support line`. Verify the deck contract: >= 4 distinct archetypes, no archetype on adjacent slides, full-bleed `hero` base on <= 3 slides (all other slides keep their NBP object per R13/R14 but contained on a flat-dark background - text never fights a full-frame scene), max 2 "question? answer." slides, and the CTA slide is a the user face scene (R45). NEVER render a deck through one template function in a loop - that batch shortcut produced the monotone 2026-06-25 rebuild the user rejected.
7. **creative prompt pass:** use `creative.ts` + `creative-designer.ts` to map each image slide to one concrete scene/object and final image prompt. Prompt the text/object relationship explicitly: object frames, supports, points toward, casts light/shadow on, sits behind, becomes backing texture, or visually echoes the Hebrew text. If object is centered, put Hebrew typography in the foreground over it and let text cover part of the object. Object never covers or strikes glyphs. For baked Hebrew, default to one clean front-facing physical text surface: plaque, sign, stamp, board, engraving. Add a second small proof badge only for sourced proof such as verified GitHub stars. Ban every unrequested label, fake name, fake handle, fake badge, background word, and side signature.
8. One NBP centerpiece per slide, no exceptions (R13/R14). One physical-object metaphor per slide - R15 catalog or extend it. Hero slides = full scene prompts; contained slides = object on flat/paper background per the blueprint base. Generate integrated text-image drafts (batch via a /tmp shell script, run in background):
   `node scripts/generate-image.mjs --aspect 4:5 --size 2K --out carousels/<slug>/vN/img-X.png --prompt "..." --slide-text "..." --support-text "..."` (mkdir vN first). Default text mode is `render`, so Nano Banana renders the slide copy into the image. Default final model for scheduled replacement decks is `--model pro` (`gemini-3-pro-image`), 2K. Use `--model flash` (`gemini-3.1-flash-image`) only for fast proof slides or draft batches. Use `--model lite` (`gemini-3.1-flash-lite-image`) only for fast 1K smoke drafts (validated local smoke: ~3.7s, not final quality). Copy results to `tools/open-carrusel/public/uploads/` (served at `/uploads/<file>`).

   **Validated prompt templates** (one object, center band; R44 = dark by default):
   - Contained object slides: `"Glossy 3D render of <ONE object>, deep near-black background, warm terracotta rim light, soft radial orange glow, cinematic product render. Hebrew typography sits on one straight front-facing physical plaque/sign/stamp/engraving in the middle band, or foreground over the object when the object is centered. Text and object are physically integrated as framed/supported/lit/shadowed/backed by it, subtle 3D or embossed material, fully readable glyphs, no sticker text, no fake labels, no background words, no random names, no unrequested badges, all meaningful text inside phone-safe y280-1070, bottom 240-300px dark and low-detail for chrome."`
   - Hero scenes: photo-real cinematic night scene, deep near-black, warm terracotta accent light, shallow depth of field. Hebrew typography belongs to the scene as light, material, sign plane, engraved/embossed surface, or foreground structure; it must not look pasted on.
   - Proof badge slides: put verified proof on its own small badge close to the main object cluster and still inside y280-1070. Never place proof badges in the top edge or bottom chrome band.
   - Paper prompt (`soft cream paper background...`) only when the user explicitly asked for a paper deck (R44)
   - **CTA slide (R45/R51/R52/R53): the user face scene via img2img** - `node scripts/generate-cover.mjs --image assets/face/<ref>.png --aspect 4:5 --size 2K --out ... --prompt "Keep the EXACT man from the reference photo - same face, beard, likeness... <scene tied to the CTA>, warm terracotta light, low-detail dark lower band for blended chrome, Hebrew typography integrated into the scene but never over the user's face" --slide-text "..." --support-text "..." --wardrobe "scene-matched clothes/accessory" --shirt-text "<optional short exact shirt message>" --hat-text "<optional short exact hat message>"`. Rotate varied refs in `assets/face/`, verify likeness per R33/R51/R53, regenerate if drifted or if Gemini adds wrong text, wrong face, random labels, or visual noise.
   - generate-image.mjs AUTO-APPENDS R20/R49/R50 safe-zone and text-object composition guidelines. With default `--text-mode render`, it asks Nano Banana to place exact Hebrew copy inside the phone-safe zone and combine it with the object. Text may cover a centered object; object may not cover text. Avoid mixed Hebrew + Latin in baked image text; substitute Hebrew or isolate Latin on its own line. Use Pro for final scheduled decks by default; use Flash/Lite only for drafts. Use `--text-mode context` to revert to old no-text image plus HTML overlay only if the user did not explicitly ask for all text and images to be generated with Nano Banana Pro. Judge in review: exact words, bidi, legibility, no extra text, text-object relationship, and no meaningful text in Instagram dead zones.
9. Ensure dev server: `curl -s localhost:3000/api/carousels` else `cd tools/open-carrusel && npm run dev` (background).
10. Build slides: copy the canonical `post-slides.mjs` pattern, but each slide's HTML follows ITS blueprint archetype - distinct markup per archetype, never one shared template function looped over all slides. If image has baked-in text, do not duplicate primary headline/support text in HTML; keep only chrome/fallback layers and notes. Bottom chrome stays renderer overlay, not Gemini text. For generated/photo slides, use `scripts/apply-carousel-chrome.mjs --tone claude|codex|green` or mirror its CSS in open-carrusel: soft bottom scrim, glass handle shell with `assets/face/handle.png`, tone-matched `החליקו ←` pill. Never paste raw handle directly over a full-bleed photo. POST to `/api/carousels` + `/api/carousels/<id>/slides` (`{html, notes}`, body-level HTML). Slide edits: PUT `/api/carousels/<id>/slides/<slideId>` (get ids from GET carousel, slides array is creation-ordered).
11. Export: `curl -X POST localhost:3000/api/carousels/<id>/export -o vN.zip` then unzip to `vN/slides/`.
12. **Arena review yourself before showing**: Read ALL 10 PNGs, zoom-crop suspicious areas via `sips -c`. Per-slide checks: exact generated words, bidi punctuation, headline wraps (orphan words -> smaller font + nowrap), text/object relationship (R42/R49/R50: text may cover object, object must not cover glyphs), straight central baked typography (R54/R67), isolated baked Latin tokens (R55), no background pseudo-text or fake labels (R56/R67), proof badge not in chrome or top dead zone, raw accent text blending into image/background (R35), glyph fallbacks, and phone safe zone y280-1070. If baked Hebrew fails exact rendering, apply R59: shorten that slide's copy, note why part of Pro's `Improved Copy` was rejected, rerun Pro review, and regenerate the slide. If only some slides fail, apply R68: archive bad raw/final files under `review/bad-*`, patch the prompt cause, and rerender only failed slides. Deck-level checks (scroll all 10 as a strip): does layout visibly change slide to slide (R25/R39)? do 10 focal lines read aloud without one repeated sentence pattern (R41)? does slide 1 name a stake (R40)? Fix via PUT patch, re-export.
13. Show via a `view.html` grid (copy from any final deck), `open` it, write `meta.json` (design choices, known issues, open questions) + `caption.md` (caption per R18+R21, hashtags, CTA trigger note). If caption asks viewers to comment for a guide, `caption.md` must include `cta_keyword`, `guide_url`, `automation_status`, and automation proof.
14. On feedback: log verbatim -> distill -> patch. Keep old version dirs unless the user says remove (then move to `<projects>/.trash/`, never rm).
15. **Guide/DM gate before upload or scheduling.** If the carousel promises a guide, checklist, template, prompt pack, or DM resource, run `carousel-guide` and verify: guide URL live on `<your-domain>`, keyword collision checked, `dm-automation.md` written, `tools/instagram-cta-automation/routes.json` updated, route synced to `<host>:~/instagram-cta-automation/routes.json`, local and the remote host `npm run validate:routes` pass, the remote host CTA service health is clean (`dry_run:false`, `poll_enabled:true`, `last_error:null`), synthetic the remote host dry-run returns `status:"sent"` for the exact keyword, asset metadata updated, repo ledger and Obsidian timeline say `automation_status: active`, and caption keyword matches the automation. Do not upload or schedule until this is done unless the user explicitly waives it in the current turn.
16. **Post to Instagram (on request).** Stage the post in the user's real @your-handle tab; they review and click Share (the irreversible step is never automated). Run:
    ```bash
    cd <content-repo>
    osascript -e 'quit app "Google Chrome"'   # browser-use needs the profile lock; tabs restore after
    GOOGLE_API_KEY="$(security find-generic-password -a <macos-user> -s GEMINI_API_KEY_CAROUSEL -w)" \
      .venv-bu/bin/python scripts/instagram/post_browseruse.py \
        --dir carousels/<slug>/vN/slides --caption carousels/<slug>/vN/caption.md \
        --profile "<CHROME_PROFILE>" > /tmp/bu_post.log 2>&1
    ```
    Must run the Bash with the sandbox disabled (the GUI Chrome gets SIGKILLed otherwise). browser-use 0.13.1 drives Chrome **<CHROME_PROFILE>** (already logged into @your-handle), Gemini `gemini-3.5-flash` agent: uploads all 10 slides in order, types the caption, STOPS before Share. Then screenshot via computer-use (`request_access` Google Chrome, read tier) to verify slide order + caption, and hand to the user to click Share. Edit the caption -> re-run (it re-stages from scratch).

## Hook video (HyperFrames, validated 2026-06-10)

Animated hook MP4 for slide 1 (IG mixed image+video carousel) or reels. OSS HyperFrames (`npx -y hyperframes render --output <file>.mp4`), local + free, ~16s/render after first calibration. Project: `tools/hyperframes-hook/` (composition = slide HTML + paused GSAP timeline registered on `window.__timelines["<composition-id>"]`; root needs `data-composition-id/width/height`, timed elements `class="clip"` + `data-start/duration/track-index`). Approved reference cut + rebuild steps: `carousels/2026-06-10-fable-5-launch/v3/hook-video/` (composition-v4.html + README).

- Style: R23 (cinematic, not slide-with-fades) executed per R22 (premium restraint: ONE camera move, masked yPercent type reveals out of overflow:hidden wrappers, expo.out/power2.inOut only, breathing light, slim letterbox, fine static grain; NO RGB-split/shake/flash/fake-particles/bounces). the user rejected trailer-style cut as "looks AI"; picked premium.
- **Renderer DELETES stray files in its project dir** (ate 3 archived mp4s + 2 archived html). All renders (`--output`) and archives live OUTSIDE the project dir. Exactly one root-level composition html (extras = lint error "multiple_root_compositions").
- Vendor gsap.min.js locally in assets/ (no CDN). `<img>` and CSS gradient backgrounds both work in this renderer (unlike open-carrusel).
- 4:5 = data-width 1080 / data-height 1350; reels = 1080x1920. Compare-page pattern: `tools/open-carrusel/public/hooks-compare.html` (videos autoplay muted loop, served on :3000).
- Cloud HyperFrames MCP connector (HeyGen compose/render_video) exists but: paid, 16:9/9:16/1:1 only (no 4:5), zero RTL control. Local OSS route is the pipeline.

## Feedback loop (how taste compounds)

On ANY feedback: append verbatim to `design/feedback-log.md` -> distill into `design/lessons.md` (new R-number; contradiction = replace + note reversal) -> apply ALL rules to vN+1.

## Hard-won gotchas

- **R20 safe zone**: all meaningful text in the y280-1070 band - IG's immersive feed overlays top/bottom ~280px of 4:5 posts. Headlines margin-top ~150px after top chrome; bottom blocks margin-bottom ~190px. Edge chrome pills are sacrificial decoration. Retrofit tool: `scripts/safe-zone-patch.mjs <carouselId...>`. The canonical template already complies.
- **R35 overlay contrast**: never put `color:${O}` / `#d97757` or any accent color on subtitle/support text directly over generated/full-bleed imagery, warm glows, face scenes, or brown/orange props. Use ivory/white or light-gray text on a dark scrim/plate. Keep orange/Codex accent for border, underline, badge background, CTA fill, or one short keyword only after contrast check. If screenshot review shows accent blending, switch to ivory or put it on a solid pill/card before export.
- Bidi (R9): start mixed lines with Hebrew; `&rlm;` after LTR runs before punctuation; code/prices in `<bdi dir="ltr" style="white-space:nowrap">`. "$10/$50" without bdi = flipped.
- **R19**: every paper image slide headline sits on the ivory backdrop pill. CSS trap: `gradH` is a `background` shorthand - it kills any background on the SAME element. Pill bg lives on a wrapper `<span>`, gradH on the inner `<h2>`.
- **✗ (U+2717) renders as a stray alef-like glyph in Assistant** - never use it. Don't-tag pill is text-only ("אל תעשו"); ✓ works fine.
- Long Hebrew headline in padH pill wraps with orphan word -> drop font to ~62px + `white-space:nowrap`.
- `<img>` tag for images, never CSS background-image (headless Puppeteer bug).
- Assistant font only (never Heebo); no letter-spacing on Hebrew; no em dashes.
- Voice (R16): viewer IS the developer - second-person benefit copy; recap = action steps, never "send to a friend" framing.
- Copy voice (R18): would an Israeli dev say it out loud? Contrast lines, curiosity gaps, idioms ("פרארי בפקק", "ידית גז"). Flat-but-accurate = bug.
- **Hook clarity (R37):** do not open with internal architecture jargon like "agent on Opus", "routing", or "execution layer" when the audience pain is visible in the workflow. Start with the symptom the viewer recognizes: "שוב נגמר לך השימוש בקלוד קוד באמצע העבודה?" Then explain the model cause: "זה כי Opus שורף לך טוקנים." Slide 2 can carry the mechanism.
- **News angle (R38):** when the carousel is about a model launch or product update, the launch itself must be visible on slide 1 or slide 2. Do not bury "X יצא" in source, caption, or a mid-deck claim. Keep the human pain hook if it works, but attach the news badge or re-hook immediately.
- Accuracy (R17): plan-included features are "כלול במנוי", never "חינם"; unverifiable comparisons -> invite the math ("תעשו לבד את החשבון") instead of claiming.
- generate-image.mjs writeFileSync fails if out-dir missing - mkdir BEFORE generating (image still billed on failure).
- Lead magnets promised by CTA keywords are part of production. Use `carousel-guide`; do not ship a guide/DM CTA with only a caption note or `dm-automation.md` handoff. The route must be active in the the remote host CTA automation service before Metricool scheduling.
- Vercel guide routes can be overwritten by later dirty local deploys. After the final website deploy, re-check the production guide URL. If it returns 404, redeploy a clean website worktree that includes the guide before calling the carousel shipped.
- **IG posting (step 11)**: browser-use needs Chrome FULLY QUIT first (profile-dir lock) and the Bash run with the sandbox disabled (GUI Chrome is SIGKILLed in the sandbox). The agent stops before Share by design - NEVER auto-click Share (irreversible/outward-facing; the user's call). Re-running re-uploads all 10 slides (~3 min); no in-place caption edit. Gemini key is reused as `GOOGLE_API_KEY` (no extra cost). <CHROME_PROFILE> = @your-handle.
- **Caption (R21)**: max ONE blank line between blocks (hook/body/CTA/footer); body bullets lead with a Hebrew word after any emoji so the line renders RTL not number-first; keep contrast punches + one comment-keyword CTA + save/tag-a-dev + handle + <=6 hashtags. Old caption -> `caption-original.md` before rewrites.
- Other routes that DON'T work for posting: copying Chrome cookies into a headless browser (Keychain blocks v10 decryption), CDP to real Chrome (no debug port by default), computer-use clicks (browsers are read-tier), Claude-in-Chrome ext (loads only at `claude --chrome` launch, not mid-session). The API poster `scripts/instagram/post.mjs` works but is blocked on the user creating a Meta app (`scripts/instagram/SETUP.md`).
