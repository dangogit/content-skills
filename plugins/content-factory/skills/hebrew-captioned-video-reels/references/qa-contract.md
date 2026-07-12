# Reel QA contract

Run this contract on the final MP4 before upload. A render is not publishable
until every required proof is recorded in the asset handoff.

| Area | Required proof | Reject when |
| --- | --- | --- |
| Media | 1080x1920, H.264 video, AAC audio, duration under 180 seconds | wrong orientation, missing stream, or unexpected codec |
| Frame zero | Hook is visible in frame 0 and remains inside the readable safe band | opener starts without the hook |
| Captions | Hebrew text matches speech, no dropped words, readable on a phone | paraphrase, bidi corruption, face collision, or overflow |
| Cuts | Start and end boundaries preserve words and meaning | mid-word cut, clipped breath, or dead tail remains |
| Audio | Voice is clear; music bed is audible but subordinate when requested | clipping, buried bed, masking, or unintended silence |
| CTA | Named artifact, live URL, active route, synthetic delivery proof | generic guide, dead URL, or unverified route |
| Publish | Metricool create response and planner refetch agree | missing id/uuid, network, media, timezone, or auto-publish proof |

Use the repository checker for the media row:

```bash
scripts/check-reel-media.sh <final.mp4>
```

The checker is a fast machine gate. It does not replace frame inspection,
phone listening, caption review, or Metricool planner refetch.
