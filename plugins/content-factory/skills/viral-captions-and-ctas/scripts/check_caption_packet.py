#!/usr/bin/env python3
"""Validate caption and CTA packet fields."""

from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lib"))
from contracts import require_fields


REQUIRED = (
    "Objective", "Caption", "CTA", "CTA rationale", "On-screen text",
    "Hashtags", "Pinned comment", "Risk flags",
)


def check_packet(text: str) -> list[str]:
    _, errors = require_fields(text, REQUIRED)
    if "—" in text:
        errors.append("contains an em dash")
    if "share with someone who needs this" in text.casefold():
        errors.append("uses generic share CTA")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    errors = check_packet(args.packet.read_text(encoding="utf-8"))
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    if errors:
        return 1
    print("PASS: caption packet contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
