from check_reel_handoff import check_handoff


def test_accepts_complete_reel_handoff():
    text = "Source\nFinal MP4\nCaption QA\nAudio\nFrame-zero\nMetricool\nStatus"
    assert check_handoff(text) == []


def test_rejects_missing_audio_proof():
    assert any("missing Audio" in e for e in check_handoff("Source\nFinal MP4"))
