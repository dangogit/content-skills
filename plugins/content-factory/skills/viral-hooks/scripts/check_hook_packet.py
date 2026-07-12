#!/usr/bin/env python3
"""Validate a three-angle hook experiment packet."""

from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lib"))
from contracts import numbered_table_rows, require_fields


REQUIRED = (
    "Objective",
    "Story spine",
    "Recent-hook conflicts",
    "Top pick",
    "Backup",
    "Test variable",
    "Baseline",
    "Truth check",
    "Hebrew read-aloud check",
)


def check_packet(text: str) -> list[str]:
    _, errors = require_fields(text, REQUIRED)
    rows = numbered_table_rows(text, columns=6)
    if len(rows) != 3:
        errors.append("requires exactly three numbered angle rows")
    elif [row[0] for row in rows] != ["1", "2", "3"]:
        errors.append("angle rows must be numbered 1, 2, 3 in order")
    for row in rows:
        if any(not cell for cell in row[1:]):
            errors.append(f"angle {row[0]} has empty visual, verbal, text, proof, or payoff")
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
    print("PASS: hook experiment contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
