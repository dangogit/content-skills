#!/usr/bin/env python3
from pathlib import Path
import argparse


def check_contract(text: str) -> list[str]:
    errors = []
    for label in ("Named artifact", "Guide URL", "Keyword", "Health", "Synthetic delivery", "Status"):
        if label.casefold() not in text.casefold():
            errors.append(f"missing {label}")
    if "generic guide" in text.casefold():
        errors.append("uses generic guide")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    errors = check_contract(args.record.read_text(encoding="utf-8"))
    for error in errors:
        print(f"FAIL: {error}")
    if errors:
        return 1
    print("PASS: resource contract mechanics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
