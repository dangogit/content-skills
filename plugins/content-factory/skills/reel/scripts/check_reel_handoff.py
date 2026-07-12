#!/usr/bin/env python3
from pathlib import Path
import argparse


def check_handoff(text: str) -> list[str]:
    errors = []
    for label in ("Source", "Final MP4", "Caption QA", "Audio", "Frame-zero", "Metricool", "Status"):
        if label.casefold() not in text.casefold():
            errors.append(f"missing {label}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("handoff", type=Path)
    args = parser.parse_args()
    errors = check_handoff(args.handoff.read_text(encoding="utf-8"))
    for error in errors:
        print(f"FAIL: {error}")
    if errors:
        return 1
    print("PASS: Reel handoff mechanics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
