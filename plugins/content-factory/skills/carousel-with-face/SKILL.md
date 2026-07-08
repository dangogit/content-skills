---
name: carousel-with-face
description: Use when the user wants an Instagram carousel that features their own face/photo on the slides (not only 3D object centerpieces) - "carousel with my face", "קרוסלה עם הפנים שלי", "put me in the carousel", "use my photo in the slides", "/carousel-with-face". For faceless object-centerpiece carousels use the carousel skill instead.
---

# Carousel With Face

A face-forward variant of the carousel pipeline: the user's real likeness appears on the hook / "you" / CTA slides via Gemini Nano Banana image-to-image, while value slides keep the NBP object centerpieces. Everything else (design system, copy-first protocol, render, Metricool scheduling) is identical to the base carousel skill.

**REQUIRED BACKGROUND:** Use the `carousel` skill first - it defines the design system (`content/design/DESIGN.md`, `content/design/lessons.md` rules R1-R68+), the copy-first checkpoint, open-carrusel rendering, NBP prompt templates, blended chrome, and the arena-review step. This skill only adds the FACE step on top of it.

**Copy/Creative Prompt Pack:** after the base `carousel` read, use `content/library/prompts/prompt-pack/source/ui-lib-prompts/creative.ts` and `creative-designer.ts` for face-scene planning. Face slide must match slide copy, not use the face as generic background decoration.

## What changes vs faceless carousel

| Step | Faceless (carousel) | With face (this skill) |
|---|---|---|
| Hook / CTA / "you" slides | NBP 3D object centerpiece | the user's face composited into an AI scene (img2img) |
| Value slides | NBP object per slide | unchanged - NBP object per slide |
| Image script | `generate-image.mjs` (text-to-image) | `generate-cover.mjs` (image-to-image, keeps likeness) for face slides; `generate-image.mjs` for object slides |

**Since R45 (2026-07-02), even faceless `carousel` decks put the user's face on the CTA slide - this skill is for decks where their face also carries the hook/"you" slides.**

**Do NOT put their face on every slide.** Face on ~3 slides max (typically slide 1 hook, one mid "you" slide, slide 9 CTA). A face on all 10 reads repetitive and burns img2img budget. Variety per R25/R28/R53. Face slides count as `hero` archetype in the R39 deck blueprint - the <= 3 full-bleed cap includes them.

## Face reference photo

Quality of the reference drives everything. Use varied refs from `content/assets/face/` when they fit the slide: studio, casual, talking-head frame, outdoor, side angle, different outfits. The output may adapt the user's clothing color/material to the scene palette while preserving face, beard, body type, and likeness. Face scene may be close portrait, half-body, full-body, or a small character of the user inside the environment.

- **Best:** a clean studio headshot - front-facing, even lighting, plain background. Ask the user for one and save to `content/assets/face/me.png`.
- **Fallback:** extract a clean frame from a talking-head clip (front-facing, no motion blur, minimal burned-in subtitle):
  `ffmpeg -ss 20 -i clip.mp4 -frames:v 1 -vf "crop=W:H:0:0" content/assets/face/me.png` (crop off the bottom subtitle strip).
- If the user pastes a photo into chat, it is NOT on disk - ask the user to save it to `~/Downloads` (or give a path); you cannot write what you only see.

## Generate a face slide background (img2img)

`content/scripts/generate-cover.mjs` feeds the reference photo as `inlineData`. Default model is `gemini-3-pro-image` via `--model pro`; use Flash/Lite only for draft speed tests.

```bash
node scripts/generate-cover.mjs --image content/assets/face/me.png --aspect 4:5 --size 2K \
  --out content/carousels/<slug>/v1/face-1.png \
  --prompt "Bold vertical 4:5 social-media slide. Keep the EXACT man from the reference photo - same face, beard, glasses, likeness - as the subject, cinematic confident pose. <SCENE: agents theme tied to this slide>. Dark moody background, warm terracotta orange (#d97757) accent light. Photorealistic, sharp." \
  --slide-text "<HEBREW FOCAL LINE>" \
  --support-text "<HEBREW SUPPORT LINE>" \
  --wardrobe "scene-matched dark hoodie, terracotta rim light" \
  --shirt-text "<OPTIONAL SHORT SHIRT MESSAGE>" \
  --hat-text "<OPTIONAL SHORT HAT MESSAGE>"
```

- `--aspect 4:5` for carousel slides (the reel-cover variant uses 9:16). Gemini renders ~1536x2752 for 4:5/2K - fine, open-carrusel/ffmpeg scale to 1080x1350.
- One scene per slide tied to its message (hook = topic visual; "you" = the user supervising/working; CTA = the user + call gesture). Give the user an active role and expression when useful: pointing, holding a verifier board, debugging, teaching, reacting, skeptical, focused, smiling, surprised. Static portrait is allowed only when authority is the point.
- Clothes/accessories are part of scene design: hoodie, jacket, cap, hat, badge, laptop sticker, or shirt message can carry topic. Use only short exact text on clothing/hat, never random labels.
- **Verify every face slide** by Reading the PNG - img2img occasionally drifts the face; regenerate if the likeness is off.

## Generate integrated Hebrew headline

Default flow now bakes the focal/support Hebrew copy into the generated face image with `--slide-text` and `--support-text`. The text must feel native to the face scene: a physical sign plane, light, shadow, subtle 3D/extruded/embossed/engraved/glowing material, clothing message, or object-prop relationship tied to the prompt. Keep main slide text off the user's face, eyes, beard, hands, and body silhouette. Shirt/hat text is allowed when explicitly requested with `--shirt-text` / `--hat-text`. Copy face PNGs to `tools/open-carrusel/public/uploads/face-N.png` and reference `/uploads/face-N.png` as slide `img`. Do not duplicate primary headline/support text in HTML unless generated Hebrew fails. Keep HTML as fallback layer for failed spelling, bidi, or legibility.

## Workflow (delta on top of carousel skill)

1. Read `design/lessons.md` + `design/DESIGN.md` (R1-R68+). Get/extract the face reference photo.
2. Source topic, including source lane when Instagram inspiration is used: global trend for new ideas, Israeli Hebrew signal for local pain language, or owner proof for authority. Never copy source text, screenshots, layout, assets, or exact CTA wording. Run copy prompt pass, then run Gemini Pro copy review and improvement via `node scripts/sharpen-copy.mjs --model pro --mode both --in <copy.md> --context <source.md> --out <version>/review/gemini-pro-copy-review.md`. Use `Improved Copy` as the next draft unless rejected with a clear reason. Write 10-slide Hebrew copy, resolve all Pro `Flags`, rerun Pro if score is below 9/10 or cadence/renderability fails, then use the **copy-first checkpoint** with the user. Apply R37: the hook starts from a visible workflow symptom, not internal model/agent jargon. Mark which slides get their face (hook/you/CTA). Zero image spend before approval and Pro flag resolution. If visual QA later shows baked Hebrew dropped words, misspelled text, or crowded a line, shorten that slide, record why the Pro wording was rejected, rerun Pro in `--mode review`, and regenerate the affected face/object slides. Before upload, scheduling, or Metricool replacement, run a fresh current-state audit with `--mode review` on the final copy and current `source.md`; store it as `review/gemini-pro-current-audit-YYYY-MM-DD.md` and point `meta.json.copyReview.path` at it so guide URL, CTA, proof, and stale-context issues are checked after visual work.
3. Write the R39 deck blueprint (base carousel workflow step 5): archetype/base/metaphor per slide, face slides marked `hero`. Then run creative prompt pass for face slides: face ref choice, scale (close/half/full/small character), scene role, facial expression, body language, clothes/accessory, object, lighting, and reason the user belongs in that scene.
4. Generate face slides via `generate-cover.mjs` (img2img + baked text); generate object slides via `generate-image.mjs` (baked text by default). Use varied refs and scene-matched clothing. Default final model for scheduled replacement decks is `--model pro` (`gemini-3-pro-image`). Use Flash/Lite only for draft speed tests. Verify every face slide.
5. Copy all slide images to `tools/open-carrusel/public/uploads/`. Build slides with the canonical `post-slides.mjs` pattern, but do not duplicate baked text. Keep bottom chrome as renderer overlay. For generated/photo slides, use `scripts/apply-carousel-chrome.mjs --tone claude|codex|green` or mirror its CSS in open-carrusel: soft bottom scrim, glass handle shell with `assets/face/handle.png`, tone-matched `החליקו ←` pill. Never paste raw handle directly over a full-bleed face photo. Export PNGs.
6. Arena-review all 10 (exact words, bidi, wraps, face fidelity, collisions, no extra generated text). If the baked text fails, apply R59 before showing: shorten, rerun Pro review, regenerate. Show the user.
7. **Publish:** if the CTA promises a guide or DM resource, run `carousel-guide` first and block upload/scheduling until the production guide URL returns 200, `tools/instagram-cta-automation/routes.json` contains the keyword, the route is synced to `<host>:~/instagram-cta-automation/routes.json`, local and the remote host `npm run validate:routes` pass, the remote host health shows `dry_run:false`, `poll_enabled:true`, and `last_error:null`, and a the remote host synthetic dry-run returns `status:"sent"` for the exact keyword. Then convert slides to JPEG first (`sips -s format jpeg -s formatOptions 90 ...` - Instagram's API cannot fetch PNG, live failure 2026-07-02), upload the 10 JPGs with `scripts/upload-carousel-media.mjs` so MIME is `image/jpeg`, and schedule via Metricool. Default provider is tmpfiles (`/dl/` direct URLs); if tmpfiles errors or direct checks fail, rerun with `--provider=litterbox --litterbox-time=72h`. Schedule via Metricool `createScheduledPost` - **always Instagram + Facebook + TikTok** (the user, 2026-07-06): `providers:[{network:"instagram"},{network:"facebook"},{network:"tiktok"}]`, `instagramData {type:"POST"}`, `facebookData {type:"POST"}`, `tiktokData {photoCoverIndex:0, privacyOption:"PUBLIC_TO_EVERYONE"}`, media = 10 URLs in order, morning slot (10:00 Israel), `autoPublish:true`. Full method in memory `metricool-publishing.md`.

## Validated template (2026-06-24, first face deck)

- **Canonical code:** `content/carousels/2026-06-24-agentic-engineering/v1/post-slides.mjs` - copy this. Face slides 1/5/9 use the `quoteSlide` pattern (dark full-bleed face image + bottom scrim + headline); object slides use `defSlide` / split / `padH`+`card` / list. No two adjacent layouts identical (R25).
- **Default face ref:** `content/assets/face/me.png` = `~/portrait.png` (studio headshot, suit). Likeness held consistently across all 3 face slides - studio headshot is the gold standard.
- **Tonal rhythm (R44 update 2026-07-02):** decks are all-dark by default now - the user rejected white/paper cards. Get rhythm from contained objects on flat-dark vs full-bleed scenes, not from paper slides. Paper prompts only if the user explicitly asks.
- Gemini can add extra labels, brand words, garbled Hebrew, or sticker-looking typography. Regenerate once with stricter R49/R50 prompt or `--model pro`; if still bad, use `--text-mode context` and HTML overlay for that slide.

## Gotchas

- Face on ~3 slides, not all 10 (repetitive + cost). NBP objects carry the value slides. Across those face slides, vary scale/action/expression; do not repeat same static pose.
- Studio headshot is safest for likeness, but do not overuse it. Rotate all usable face refs when scene benefits: casual photo, teaching frame, outdoor, close-up, side angle, different clothes. A photo pasted into chat is NOT a file - get a disk path (`~/Desktop`, `~/Downloads`) or save it there first.
- img2img can drift the face - Read and verify each face slide, regenerate if off.
- Face/full-bleed slides: baked text must be high-contrast ivory/white or light-gray, integrated with scene lighting/material, never pasted across the face. Prefer one clean sign/board/light plane for focal/support copy. Clothes can shift to match slide colors. Shirt/hat/badge messages are allowed only when explicit and short; no random generated labels, fake names, fake handles, or fake badges. Avoid inline Hebrew + Latin in baked text; substitute Hebrew or isolate Latin on its own line.
- Integrated face slides inherit R54-R56: proof a face/text slide before full spend, reject curved typography or top-dead-zone placement, isolate Latin tokens as their own line/headline, and forbid background pseudo-text on blueprints, chat bubbles, labels, and screens.
- Hook clarity follows base carousel R37: start with the viewer's visible pain, then explain the model/system cause. Face hook should show the real situation, not abstract agent architecture.
- News angle follows base carousel R38: if the face deck is about a launch, the launch must appear in slide 1 or slide 2. The face scene should help carry the news, not just decorate the deck.
- Gemini cover gen is image/jpeg output even with a `.png` name; that's fine for `<img>` and ffmpeg.
- 4:5 aspect for carousel slides (not 9:16).
- **tmpfiles uploads occasionally 520** - after uploading N slides, verify N direct URLs came back and retry any that errored before scheduling. If tmpfiles stays flaky, use `--provider=litterbox --litterbox-time=72h` before scheduling. A wrong or missing media URL fails the whole post.
- Same Metricool facts as the `reel` skill: brand <METRICOOL_BLOG_ID> = @your-brand; public media host required; no delete (use draft); carousels go morning, videos evening.
- Same guide/DM facts as the `carousel` skill: comment-keyword CTA means active the remote host CTA automation route before Metricool scheduling, not just `dm-automation.md`.
- **Sourcing topics:** fan out parallel agents (trending web research + blog repurpose + original ideation + a Twitter/X scan) -> shortlist -> the user picks. Then copy-first.
