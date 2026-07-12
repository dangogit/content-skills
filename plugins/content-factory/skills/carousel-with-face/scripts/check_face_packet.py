#!/usr/bin/env python3
"""Validate consent and QA proof for face-mode carousel slides."""

from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lib"))
from contracts import require_fields, require_one_of


REQUIRED = (
    "Mode",
    "Slides",
    "References",
    "Consent",
    "Reference retention",
    "Scene jobs",
    "Likeness QA",
    "Text/pixel QA",
    "Base carousel status",
)


def check_packet(text: str) -> list[str]:
    fields, errors = require_fields(text, REQUIRED)
    errors += require_one_of(fields, "Mode", {"cta-only", "hook-cta", "proof-cta", "custom"})
    errors += require_one_of(fields, "Consent", {"verified"})
    errors += require_one_of(fields, "Reference retention", {"documented", "delete after campaign", "delete after delivery"})
    errors += require_one_of(fields, "Likeness QA", {"passed", "verified"})
    errors += require_one_of(fields, "Text/pixel QA", {"passed", "verified"})
    errors += require_one_of(fields, "Base carousel status", {"passed", "verified"})
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
    print("PASS: face-mode contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
