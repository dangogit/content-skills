#!/usr/bin/env python3
"""Validate canonical Reel handoff fields for legacy alias users."""

from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lib"))
from contracts import require_fields, require_one_of


REQUIRED = (
    "Source",
    "Final MP4",
    "Caption QA",
    "Audio measurements",
    "Frame-zero proof",
    "Planner refetch",
    "Status",
)


def check_handoff(text: str) -> list[str]:
    fields, errors = require_fields(text, REQUIRED)
    errors += require_one_of(fields, "Caption QA", {"passed", "verified"})
    errors += require_one_of(fields, "Frame-zero proof", {"passed", "verified"})
    errors += require_one_of(
        fields,
        "Planner refetch",
        {"passed", "verified", "not requested", "blocked"},
    )
    errors += require_one_of(
        fields,
        "Status",
        {"ready-for-review", "ready-unscheduled", "scheduled-verified", "published-verified"},
    )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("handoff", type=Path)
    args = parser.parse_args()
    errors = check_handoff(args.handoff.read_text(encoding="utf-8"))
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    if errors:
        return 1
    print("PASS: Reel handoff contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
