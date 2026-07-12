# On-screen text

Many viewers encounter social video without useful audio. On-screen text must
carry enough meaning to orient them. Burned-in captions also give production
control and survive cross-posting.

This is the in-video text layer. For the written caption that sits
beside the video, see `caption-craft.md`.

## Burn it in. Do not trust auto-captions

Burned-in captions are hardcoded into the video file. Platform
auto-captions are an overlay that only shows when the viewer has them
toggled on. Default to burned-in for three reasons:

- They survive reposts, screenshots, downloads, and re-uploads.
- You control font, weight, color, size, position, timing.
- They show by default, on mute, to everyone.

Auto-captions remain useful as an accessibility layer. Review platform-generated
captions because accuracy varies by speaker, language, audio quality, and product
version.

## The headline + body pattern

A useful layout to test:

- One **large, static text block** near the hook-safe region: the hook line or the
  topic claim. This gives a viewer immediate context.
- **Body captions** built up word-by-word at the bottom or center as
  the voiceover speaks. These carry the spoken transcript.

The headline orients the viewer. The body carries the spoken argument. Treat
search and retention effects as hypotheses to measure, not guarantees.

## The karaoke pattern

Caption text appears word-by-word or phrase-by-phrase **in sync with
the audio**, not as a static block of the whole sentence. Words
highlight, scale up, or change color as they're spoken.

- Test karaoke, phrase blocks, and static captions against the account baseline.
- Match animation intensity to voice, format, and brand instead of assuming one
  platform style always wins.

Karaoke can support pacing when its timing follows the speech.

## Safe zones

The area the platform UI does **not** cover. Critical text outside
these zones gets eaten by buttons, captions, music tickers, and
profile pictures.

Platform UI changes by device and surface. Use repo renderer safe zones and inspect
actual feed previews. Keep critical text away from top chrome, bottom caption area,
and right action rail. For the creator's Reels, follow `hebrew-captioned-video-reels`.

## Font, color, contrast

- **Weight:** start with a bold weight, then verify readability on a phone.
- **Color:** choose foreground, outline, and background using measured contrast
  and real-frame inspection.
- **Family:** sans-serif geometric fonts dominate. Montserrat Bold,
  TikTok Sans, Futura Bold, Archivo Black are common picks. TikTok Sans
  is open-source and matches the app's native UI if you want the
  in-app feel.
- **Size:** validate on a 1080x1920 phone preview. The creator's current renderer uses
  much larger pixel values than desktop point-size heuristics.
- **Avoid:** thin weights, low-contrast pastels, decorative scripts,
  tight letterspacing. They look fine on a desktop preview and
  disappear on a phone.

## Pace the text the way you'd pace the cuts

- A new word or phrase on screen every beat keeps the eye engaged the
  same way a shot change does.
- If the voiceover pauses for emphasis, the text can hold for a beat
  longer, then resume.
- Avoid dumping a long sentence on screen all at once. The viewer
  reads it faster than the voiceover finishes, then looks away.

## Practical defaults

- Keep the headline as short as meaning allows, in the safe zone.
- Start with high-contrast phrase captions, then validate type size on the target
  phone and feed surface.
- Keep terminology consistent across spoken hook, on-screen text, and written
  caption when that improves clarity.
- Do not repeat the headline as the first line of body captions. The
  body picks up where the headline left off.
