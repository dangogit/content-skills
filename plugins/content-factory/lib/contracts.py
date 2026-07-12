"""Shared strict parsers for Content Factory handoff contracts."""

from __future__ import annotations

import re
from collections.abc import Iterable


FIELD_RE = re.compile(r"^\s*(?:[-*]\s*)?([A-Za-z][A-Za-z0-9 /_-]*):\s*(.*?)\s*$")
PLACEHOLDER_RE = re.compile(
    r"^(?:<[^>]+>|tbd|todo|replace me|pending|unknown|unverified)$",
    re.IGNORECASE,
)


def normalize_label(label: str) -> str:
    return " ".join(label.casefold().split())


def parse_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        match = FIELD_RE.match(line)
        if match:
            fields[normalize_label(match.group(1))] = match.group(2).strip()
    return fields


def require_fields(text: str, labels: Iterable[str]) -> tuple[dict[str, str], list[str]]:
    fields = parse_fields(text)
    errors: list[str] = []
    counts: dict[str, int] = {}
    for line in text.splitlines():
        match = FIELD_RE.match(line)
        if match:
            key = normalize_label(match.group(1))
            counts[key] = counts.get(key, 0) + 1
    for label in labels:
        key = normalize_label(label)
        if key not in fields:
            errors.append(f"missing field: {label}")
        elif not fields[key]:
            errors.append(f"empty field: {label}")
        elif PLACEHOLDER_RE.fullmatch(fields[key]):
            errors.append(f"placeholder field: {label}")
        if counts.get(key, 0) > 1:
            errors.append(f"duplicate field: {label}")
    return fields, errors


def value(fields: dict[str, str], label: str) -> str:
    return fields.get(normalize_label(label), "")


def require_one_of(fields: dict[str, str], label: str, allowed: set[str]) -> list[str]:
    raw = value(fields, label)
    if not raw:
        return []
    normalized = raw.casefold().strip()
    if normalized not in {item.casefold() for item in allowed}:
        return [f"invalid {label}: {raw}"]
    return []


def is_https_url(raw: str) -> bool:
    return raw.startswith("https://") and "localhost" not in raw and "127.0.0.1" not in raw


def numbered_table_rows(text: str, columns: int) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in text.splitlines():
        if not re.match(r"^\s*\|\s*\d+\s*\|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == columns:
            rows.append(cells)
    return rows


def numbered_list_items(text: str) -> list[str]:
    return [
        match.group(2).strip()
        for line in text.splitlines()
        if (match := re.match(r"^\s*(\d+)\.\s+(.+?)\s*$", line))
    ]
