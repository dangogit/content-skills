from check_reel_manifest import check_manifest


def test_accepts_handoff_contract():
    text = """Final MP4:\nDuration / dimensions / codecs:\nCaption QA:\nMusic source / license:\nFrame-zero proof:\nStatus:"""
    assert check_manifest(text) == []


def test_rejects_missing_audio_proof():
    errors = check_manifest("Final MP4:\nStatus:")
    assert any("missing Music source / license" in error for error in errors)
