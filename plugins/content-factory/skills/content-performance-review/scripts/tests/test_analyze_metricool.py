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


def test_missing_components_stay_missing_instead_of_becoming_zero():
    item = derive({"id": "partial", "reach": 100, "likes": 10})
    assert item["interaction_rate"] is None
    assert item["authority_rate"] is None


def test_analyze_keeps_objectives_separate():
    report = analyze({
        "content_type": "reels",
        "window": "24h",
        "items": [
            {"id": "reach", "reach": 1000, "views": 1200, "three_second_view_rate": 60},
            {"id": "conversion", "reach": 100, "qualified_keyword_comments": 20, "dm_deliveries": 18},
        ],
    })
    assert report["leaders"]["reach"]["reach"] == "reach"
    assert report["leaders"]["conversion"]["keyword_comment_rate"] == "conversion"
    assert report["overall_score"] is None


def test_negative_metric_is_rejected():
    with pytest.raises(ValueError, match="reach"):
        derive({"id": "bad", "reach": -1})


def test_retention_reports_each_metric_leader_separately():
    report = analyze({
        "content_type": "reels",
        "items": [
            {"id": "watch-ratio", "reach": 10, "average_watch_time": 8, "duration_seconds": 10},
            {"id": "three-second-only", "reach": 10, "three_second_view_rate": 99},
        ],
    })
    assert report["leaders"]["retention"]["watch_time_ratio"] == "watch-ratio"
    assert report["leaders"]["retention"]["three_second_view_rate"] == "three-second-only"


def test_impossible_funnel_counts_are_rejected():
    with pytest.raises(ValueError, match="dm_deliveries"):
        derive({
            "id": "bad-funnel",
            "comments": 10,
            "qualified_keyword_comments": 5,
            "dm_deliveries": 6,
        })


def test_qualified_comments_cannot_exceed_comments():
    with pytest.raises(ValueError, match="qualified_keyword_comments"):
        derive({"id": "bad-qualified", "comments": 3, "qualified_keyword_comments": 4})


def test_percentage_over_100_is_rejected():
    with pytest.raises(ValueError, match="three_second_view_rate"):
        derive({"id": "bad-rate", "three_second_view_rate": 101})


def test_duplicate_item_ids_are_rejected():
    with pytest.raises(ValueError, match="unique"):
        analyze({"content_type": "posts", "items": [{"id": "same"}, {"id": "same"}]})
