from check_reel_manifest import check_manifest


VALID = """Source: source.mov
Final MP4: final.mp4
Duration / dimensions / codecs: 42s, 1080x1920, H.264/AAC
Hook: אתם בודקים את הסוכן הלא נכון
Caption source: captions.clean.json
Caption QA: verified
Cut-boundary QA: passed
Music source / license: none, voice only
Audio measurements: voice clear, no clipping
Phone listen test: passed
Frame-zero proof: verified
CTA keyword: none
Guide URL: not applicable
Automation status: not applicable
Upload URL / MIME: not requested
Metricool id / uuid: not requested
Networks: not requested
Planner refetch: not requested
Status: ready-for-review
"""


def test_accepts_handoff_contract():
    assert check_manifest(VALID) == []


def test_rejects_empty_license_and_unknown_status():
    errors = check_manifest(VALID.replace("Music source / license: none, voice only", "Music source / license:").replace("Status: ready-for-review", "Status: done"))
    assert "empty field: Music source / license" in errors
    assert "invalid Status: done" in errors


def test_verified_schedule_requires_real_publish_proof():
    text = VALID.replace("Status: ready-for-review", "Status: scheduled-verified")
    errors = check_manifest(text)
    assert any("Upload URL" in error for error in errors)
    assert "verified publication requires Metricool id / uuid" in errors
    assert "verified publication requires Networks" in errors
    assert "verified publication requires passed Planner refetch" in errors


def test_keyword_cta_requires_active_route_and_https_guide():
    text = VALID.replace("CTA keyword: none", "CTA keyword: DESIGN")
    errors = check_manifest(text)
    assert "keyword CTA requires active Automation status" in errors
    assert "keyword CTA requires public HTTPS Guide URL" in errors
