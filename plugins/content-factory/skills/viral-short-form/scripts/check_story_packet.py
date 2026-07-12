#!/usr/bin/env python3
"""Validate a short-form story and experiment packet."""

from pathlib import Path
import argparse
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lib"))
from contracts import require_fields


REQUIRED = (
    "Objective",
    "Audience",
    "Story role",
    "Content family",
    "Proof",
    "Relationship to recent posts",
    "Hook",
    "Context",
    "Escalation",
    "Payoff",
    "CTA",
    "Variable",
    "Expected signal",
    "Baseline",
)


def check_packet(text: str) -> list[str]:
    _, errors = require_fields(text, REQUIRED)
    hypotheses = [
        (match.group(1), match.group(2).strip())
        for line in text.splitlines()
        if (match := re.match(r"^\s*([123])\.\s+(.+?)\s*$", line))
    ]
    if (
        len(hypotheses) != 3
        or [number for number, _ in hypotheses] != ["1", "2", "3"]
        or len({text for _, text in hypotheses}) != 3
    ):
        errors.append("requires three distinct non-empty hypotheses")
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
    print("PASS: short-form story contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
