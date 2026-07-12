#!/usr/bin/env python3
"""Validate a carousel handoff contract."""

from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lib"))
from contracts import require_fields, require_one_of


REQUIRED = (
    "Objective",
    "Audience",
    "Promise",
    "Story role",
    "Proof",
    "Slides",
    "Visual blueprint",
    "CTA/resource status",
    "Pixel QA",
    "Planner status",
    "Next action",
)


def check_packet(text: str) -> list[str]:
    fields, errors = require_fields(text, REQUIRED)
    errors += require_one_of(fields, "Pixel QA", {"passed", "verified"})
    errors += require_one_of(fields, "CTA/resource status", {"active", "passed", "not applicable"})
    errors += require_one_of(fields, "Planner status", {"verified", "passed", "not requested"})
    if "—" in text:
        errors.append("contains an em dash")
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
    print("PASS: carousel handoff contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
