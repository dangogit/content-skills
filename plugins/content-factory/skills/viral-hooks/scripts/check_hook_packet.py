#!/usr/bin/env python3
"""Mechanical gate for a hook experiment packet."""

from pathlib import Path
import argparse


def check_packet(text: str) -> list[str]:
    errors = []
    if "—" in text:
        errors.append("contains an em dash")
    for label in ("Objective", "Proof", "Top pick", "Baseline", "Test variable"):
        if label.casefold() not in text.casefold():
            errors.append(f"missing {label}")
    if text.casefold().count("angle") < 3:
        errors.append("requires three distinct angles")
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
    print("PASS: hook packet mechanics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
