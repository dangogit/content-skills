#!/usr/bin/env python3
from pathlib import Path
import argparse


def check_packet(text: str) -> list[str]:
    errors = []
    for label in ("Mode", "Slides", "References", "Scene jobs", "Likeness QA", "Text/pixel QA"):
        if label.casefold() not in text.casefold():
            errors.append(f"missing {label}")
    for forbidden in ("random shirt", "random hat", "random label"):
        if forbidden in text.casefold():
            errors.append(f"contains {forbidden}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    errors = check_packet(args.packet.read_text(encoding="utf-8"))
    for error in errors:
        print(f"FAIL: {error}")
    if errors:
        return 1
    print("PASS: face packet mechanics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
