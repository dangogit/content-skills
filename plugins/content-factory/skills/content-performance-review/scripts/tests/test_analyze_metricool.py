import pytest

from analyze_metricool import analyze, derive, ratio


def test_ratio_handles_missing_and_zero_denominator():
    assert ratio(5, 10) == 0.5
    assert ratio(5, 0) is None
    assert ratio(None, 10) is None


def test_derive_calculates_objective_rates():
    item = derive({
        "id": "design",
        "reach": 100,
        "comments": 20,
        "likes": 10,
        "saves": 5,
        "shares": 5,
        "average_watch_time": 15,
        "duration_seconds": 30,
        "qualified_keyword_comments": 18,
        "dm_deliveries": 15,
    })
    assert item["interaction_rate"] == 0.4
    assert item["authority_rate"] == 0.1
    assert item["watch_time_ratio"] == 0.5
    assert item["keyword_comment_rate"] == 0.18
    assert item["dm_delivery_rate"] == pytest.approx(15 / 18)


def test_analyze_keeps_objectives_separate():
    report = analyze({
        "content_type": "reels",
        "window": "24h",
        "items": [
            {"id": "reach", "reach": 1000, "views": 1200, "three_second_view_rate": 60},
            {"id": "conversion", "reach": 100, "qualified_keyword_comments": 20, "dm_deliveries": 18},
        ],
    })
    assert report["leaders"]["reach"] == "reach"
    assert report["leaders"]["conversion"] == "conversion"
    assert report["overall_score"] is None


def test_negative_metric_is_rejected():
    with pytest.raises(ValueError, match="reach"):
        derive({"id": "bad", "reach": -1})


def test_retention_leader_does_not_add_unlike_units():
    report = analyze({
        "content_type": "reels",
        "items": [
            {"id": "watch-ratio", "reach": 10, "average_watch_time": 8, "duration_seconds": 10},
            {"id": "three-second-only", "reach": 10, "three_second_view_rate": 99},
        ],
    })
    assert report["leaders"]["retention"] == "watch-ratio"
