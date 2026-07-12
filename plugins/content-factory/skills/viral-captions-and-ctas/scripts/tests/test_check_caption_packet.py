from check_caption_packet import check_packet


def test_accepts_complete_packet():
    assert check_packet("Objective: saves\nCaption: שלום\nCTA: שמרו") == []


def test_rejects_missing_fields_and_bait():
    errors = check_packet("share with someone who needs this —")
    assert any("missing Caption" in error for error in errors)
    assert any("generic share CTA" in error for error in errors)
