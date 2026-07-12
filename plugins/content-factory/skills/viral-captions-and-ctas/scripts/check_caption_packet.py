#!/usr/bin/env python3
"""Mechanical gate for a caption/CTA packet."""

from pathlib import Path
import argparse


def check_packet(text: str) -> list[str]:
    errors = []
    if "—" in text:
        errors.append("contains an em dash")
    for label in ("Caption", "CTA", "Objective"):
        if label.casefold() not in text.casefold():
            errors.append(f"missing {label}")
    if "share with someone who needs this" in text.casefold():
        errors.append("uses generic share CTA")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    errors = check_packet(args.packet.read_text(encoding="utf-8"))
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: caption packet mechanics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
