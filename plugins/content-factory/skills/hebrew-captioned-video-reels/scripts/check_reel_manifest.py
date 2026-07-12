#!/usr/bin/env python3
"""Validate required proof fields in a Hebrew Reel handoff."""

from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lib"))
from contracts import is_https_url, require_fields, require_one_of, value


REQUIRED = (
    "Source",
    "Final MP4",
    "Duration / dimensions / codecs",
    "Hook",
    "Caption source",
    "Caption QA",
    "Cut-boundary QA",
    "Music source / license",
    "Audio measurements",
    "Phone listen test",
    "Frame-zero proof",
    "CTA keyword",
    "Guide URL",
    "Automation status",
    "Upload URL / MIME",
    "Metricool id / uuid",
    "Networks",
    "Planner refetch",
    "Status",
)


def check_manifest(text: str) -> list[str]:
    fields, errors = require_fields(text, REQUIRED)
    errors += require_one_of(fields, "Caption QA", {"passed", "verified"})
    errors += require_one_of(fields, "Cut-boundary QA", {"passed", "verified"})
    errors += require_one_of(fields, "Phone listen test", {"passed", "verified"})
    errors += require_one_of(fields, "Frame-zero proof", {"passed", "verified"})
    errors += require_one_of(
        fields,
        "Automation status",
        {"active", "not applicable", "not requested", "blocked"},
    )
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
    status = value(fields, "Status").casefold()
    cta_keyword = value(fields, "CTA keyword").casefold()
    if cta_keyword not in {"", "none", "not applicable", "not requested"}:
        if value(fields, "Automation status").casefold() != "active":
            errors.append("keyword CTA requires active Automation status")
        if not is_https_url(value(fields, "Guide URL")):
            errors.append("keyword CTA requires public HTTPS Guide URL")
    if status in {"scheduled-verified", "published-verified"}:
        upload = value(fields, "Upload URL / MIME")
        if not is_https_url(upload.split()[0] if upload else "") or "video/mp4" not in upload.casefold():
            errors.append("verified publication requires HTTPS Upload URL / MIME with video/mp4")
        for label in ("Metricool id / uuid", "Networks"):
            if value(fields, label).casefold() in {"not requested", "not applicable", "none"}:
                errors.append(f"verified publication requires {label}")
        if value(fields, "Planner refetch").casefold() not in {"passed", "verified"}:
            errors.append("verified publication requires passed Planner refetch")
    if "—" in text:
        errors.append("contains an em dash")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("handoff", type=Path)
    args = parser.parse_args()
    errors = check_manifest(args.handoff.read_text(encoding="utf-8"))
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    if errors:
        return 1
    print("PASS: Hebrew Reel handoff contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
