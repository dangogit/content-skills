#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <final.mp4>" >&2
  exit 2
fi

file="$1"
if [[ ! -f "$file" ]]; then
  echo "missing file: $file" >&2
  exit 2
fi

if ! command -v ffprobe >/dev/null 2>&1; then
  echo "missing dependency: ffprobe" >&2
  exit 2
fi

probe="$(ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,channels:format=duration -of default=nw=1 "$file")"
printf '%s\n' "$probe"

grep -q '^codec_type=video$' <<<"$probe" || { echo "FAIL: no video stream" >&2; exit 1; }
grep -q '^codec_name=h264$' <<<"$probe" || { echo "FAIL: video is not H.264" >&2; exit 1; }
grep -q '^width=1080$' <<<"$probe" || { echo "FAIL: width is not 1080" >&2; exit 1; }
grep -q '^height=1920$' <<<"$probe" || { echo "FAIL: height is not 1920" >&2; exit 1; }
grep -q '^codec_type=audio$' <<<"$probe" || { echo "FAIL: no audio stream" >&2; exit 1; }
grep -q '^codec_name=aac$' <<<"$probe" || { echo "FAIL: audio is not AAC" >&2; exit 1; }

duration="$(awk -F= '/^duration=/{print $2}' <<<"$probe")"
awk -v d="${duration:-0}" 'BEGIN { if (d <= 0 || d > 180) exit 1 }' || {
  echo "FAIL: duration must be greater than 0 and at most 180 seconds" >&2
  exit 1
}

echo "PASS: reel media contract"
