#!/usr/bin/env python3
"""Check that a Hebrew Reel handoff records its required proof fields."""

from pathlib import Path
import argparse


REQUIRED = (
    "Final MP4:",
    "Duration / dimensions / codecs:",
    "Caption QA:",
    "Music source / license:",
    "Frame-zero proof:",
    "Status:",
)


def check_manifest(text: str) -> list[str]:
    errors = []
    for label in REQUIRED:
        if label.casefold() not in text.casefold():
            errors.append(f"missing {label}")
    if "—" in text:
        errors.append("contains an em dash")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("handoff", type=Path)
    args = parser.parse_args()
    errors = check_manifest(args.handoff.read_text(encoding="utf-8"))
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: reel handoff manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
