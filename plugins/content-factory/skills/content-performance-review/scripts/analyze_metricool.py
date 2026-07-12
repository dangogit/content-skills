#!/usr/bin/env python3
"""Normalize Metricool content metrics without blending objectives."""

from __future__ import annotations

import argparse
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


COUNT_FIELDS = (
    "reach",
    "views",
    "comments",
    "likes",
    "saves",
    "shares",
    "qualified_keyword_comments",
    "dm_deliveries",
)


def ratio(numerator: float | int | None, denominator: float | int | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return float(numerator) / float(denominator)


def validate_item(item: dict[str, Any]) -> None:
    if not item.get("id"):
        raise ValueError("Each item requires non-empty 'id'")
    for field in COUNT_FIELDS + ("average_watch_time", "duration_seconds", "three_second_view_rate"):
        value = item.get(field)
        if value is not None and (
            isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0
        ):
            raise ValueError(f"{item['id']}: {field} must be a non-negative number or null")
    three_second_rate = item.get("three_second_view_rate")
    if three_second_rate is not None and three_second_rate > 100:
        raise ValueError(f"{item['id']}: three_second_view_rate must be between 0 and 100")
    comments = item.get("comments")
    qualified = item.get("qualified_keyword_comments")
    deliveries = item.get("dm_deliveries")
    if comments is not None and qualified is not None and qualified > comments:
        raise ValueError(f"{item['id']}: qualified_keyword_comments cannot exceed comments")
    if qualified is not None and deliveries is not None and deliveries > qualified:
        raise ValueError(f"{item['id']}: dm_deliveries cannot exceed qualified_keyword_comments")


def derive(item: dict[str, Any]) -> dict[str, Any]:
    validate_item(item)
    reach = item.get("reach")
    interaction_values = [item.get(field) for field in ("comments", "likes", "saves", "shares")]
    interactions = sum(interaction_values) if all(value is not None for value in interaction_values) else None
    derived = dict(item)
    derived["interaction_rate"] = ratio(interactions, reach)
    derived["comment_rate"] = ratio(item.get("comments"), reach)
    derived["save_rate"] = ratio(item.get("saves"), reach)
    derived["share_rate"] = ratio(item.get("shares"), reach)
    saves = item.get("saves")
    shares = item.get("shares")
    derived["authority_rate"] = ratio(saves + shares, reach) if saves is not None and shares is not None else None
    derived["watch_time_ratio"] = ratio(item.get("average_watch_time"), item.get("duration_seconds"))
    derived["keyword_comment_rate"] = ratio(item.get("qualified_keyword_comments"), reach)
    derived["dm_delivery_rate"] = ratio(item.get("dm_deliveries"), item.get("qualified_keyword_comments"))
    return derived


def median(items: list[dict[str, Any]], field: str) -> float | None:
    values = [float(item[field]) for item in items if item.get(field) is not None]
    return statistics.median(values) if values else None


def leader(items: list[dict[str, Any]], field: str) -> str | None:
    """Pick one metric leader without blending unlike units."""
    scored = [
        (float(item[field]), str(item["id"]))
        for item in items
        if item.get(field) is not None
    ]
    return max(scored)[1] if scored else None


def metric_leaders(items: list[dict[str, Any]], fields: tuple[str, ...]) -> dict[str, str | None]:
    return {field: leader(items, field) for field in fields}


def analyze(payload: dict[str, Any]) -> dict[str, Any]:
    content_type = payload.get("content_type")
    if content_type not in {"posts", "reels"}:
        raise ValueError("content_type must be 'posts' or 'reels'")
    raw_items = payload.get("items")
    if not isinstance(raw_items, list) or not raw_items:
        raise ValueError("items must be a non-empty list")
    items = [derive(item) for item in raw_items]
    item_ids = [str(item["id"]) for item in items]
    if len(item_ids) != len(set(item_ids)):
        raise ValueError("item ids must be unique")
    metric_fields = (
        "reach",
        "views",
        "interaction_rate",
        "comment_rate",
        "save_rate",
        "share_rate",
        "authority_rate",
        "watch_time_ratio",
        "three_second_view_rate",
        "keyword_comment_rate",
        "dm_delivery_rate",
    )
    baselines = {field: median(items, field) for field in metric_fields}
    leaders = {
        "reach": metric_leaders(items, ("reach", "views")),
        "retention": metric_leaders(items, ("watch_time_ratio", "three_second_view_rate")),
        "authority": metric_leaders(items, ("save_rate", "share_rate", "authority_rate")),
        "conversion": metric_leaders(items, ("keyword_comment_rate", "dm_delivery_rate")),
    }
    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "content_type": content_type,
        "window": payload.get("window", "unspecified"),
        "items": items,
        "baselines": baselines,
        "leaders": leaders,
        "overall_score": None,
    }


def markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Content Performance Review",
        "",
        f"- Content type: `{report['content_type']}`",
        f"- Window: `{report['window']}`",
        f"- Generated: `{report['generated_at']}`",
        "",
        "## Objective Leaders",
        "",
    ]
    for objective, metrics in report["leaders"].items():
        lines.append(f"- {objective}:")
        for metric, item_id in metrics.items():
            lines.append(f"  - {metric}: `{item_id or 'unavailable'}`")
    lines.extend(["", "## Items", "", "| ID | Reach | Interaction rate | Authority rate | Watch ratio | Keyword rate | DM delivery |", "|---|---:|---:|---:|---:|---:|---:|"])
    for item in report["items"]:
        def fmt(field: str) -> str:
            value = item.get(field)
            return "-" if value is None else f"{value:.4f}"
        item_id = str(item["id"]).replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {item_id} | {item.get('reach', '-')} | {fmt('interaction_rate')} | "
            f"{fmt('authority_rate')} | {fmt('watch_time_ratio')} | "
            f"{fmt('keyword_comment_rate')} | {fmt('dm_delivery_rate')} |"
        )
    lines.extend(["", "No overall score. Interpret each objective separately.", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        report = analyze(payload)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    json_path = args.output_dir / f"content_performance_{stamp}.json"
    md_path = args.output_dir / f"content_performance_{stamp}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(markdown(report), encoding="utf-8")
    print(json_path)
    print(md_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
