from check_reel_handoff import check_handoff


VALID = """Source: source.mov
Final MP4: final.mp4
Caption QA: verified
Audio measurements: voice clear, -16 LUFS
Frame-zero proof: passed
Planner refetch: not requested
Status: ready-for-review
"""


def test_accepts_complete_reel_handoff():
    assert check_handoff(VALID) == []


def test_rejects_empty_audio_and_unknown_status():
    errors = check_handoff(VALID.replace("Audio measurements: voice clear, -16 LUFS", "Audio measurements:").replace("Status: ready-for-review", "Status: done"))
    assert "empty field: Audio measurements" in errors
    assert "invalid Status: done" in errors
