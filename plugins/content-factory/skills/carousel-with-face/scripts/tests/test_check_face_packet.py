from check_face_packet import check_packet


VALID = """Mode: hook-cta
Slides: 1 and 9
References: assets/face/approved.png
Consent: verified
Reference retention: delete after campaign
Scene jobs: hook reaction and CTA invitation
Likeness QA: passed
Text/pixel QA: passed
Base carousel status: verified
"""


def test_accepts_complete_face_packet():
    assert check_packet(VALID) == []


def test_rejects_empty_consent_and_invalid_mode():
    errors = check_packet(VALID.replace("Consent: verified", "Consent:").replace("Mode: hook-cta", "Mode: every-slide"))
    assert "empty field: Consent" in errors
    assert "invalid Mode: every-slide" in errors
