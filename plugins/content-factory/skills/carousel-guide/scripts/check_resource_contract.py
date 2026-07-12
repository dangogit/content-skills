#!/usr/bin/env python3
"""Validate named-resource delivery proof before release."""

from pathlib import Path
import argparse
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lib"))
from contracts import is_https_url, require_fields, require_one_of, value


REQUIRED = (
    "Asset",
    "Named artifact",
    "Guide URL",
    "Keyword",
    "Route collision check",
    "Local validation",
    "Remote validation",
    "Health",
    "Synthetic delivery",
    "Consent scope",
    "Dedupe/rate limit",
    "Write-back",
    "Status",
)


def check_contract(text: str) -> list[str]:
    fields, errors = require_fields(text, REQUIRED)
    guide_url = value(fields, "Guide URL")
    if guide_url and not is_https_url(guide_url):
        errors.append("Guide URL must be public HTTPS, not local")
    keyword = value(fields, "Keyword")
    if keyword and not re.fullmatch(r"[\w-]{2,32}", keyword, flags=re.UNICODE):
        errors.append("Keyword must be 2-32 letters, numbers, underscores, or hyphens")
    errors += require_one_of(fields, "Health", {"passed", "healthy", "verified"})
    errors += require_one_of(fields, "Synthetic delivery", {"sent", "passed", "mocked"})
    errors += require_one_of(fields, "Route collision check", {"passed", "clear", "verified"})
    errors += require_one_of(fields, "Local validation", {"passed", "verified"})
    errors += require_one_of(fields, "Remote validation", {"passed", "verified"})
    errors += require_one_of(
        fields,
        "Consent scope",
        {"one requested resource reply", "single requested resource", "request-scoped"},
    )
    errors += require_one_of(fields, "Dedupe/rate limit", {"passed", "verified", "enabled"})
    errors += require_one_of(fields, "Write-back", {"passed", "verified"})
    errors += require_one_of(fields, "Status", {"active"})
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    errors = check_contract(args.record.read_text(encoding="utf-8"))
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    if errors:
        return 1
    print("PASS: resource delivery contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
