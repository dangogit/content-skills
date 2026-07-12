from check_carousel_packet import check_packet


VALID = """Objective: saves
Audience: AI builders
Promise: reliable agents
Story role: tactical
Proof: demo recording
Slides: 9 slides in v2/
Visual blueprint: visual-plan.md
CTA/resource status: not applicable
Pixel QA: verified
Planner status: not requested
Next action: creator review
"""


def test_accepts_complete_packet():
    assert check_packet(VALID) == []


def test_rejects_empty_fields_and_unverified_qa():
    errors = check_packet(VALID.replace("Proof: demo recording", "Proof:").replace("Pixel QA: verified", "Pixel QA: pending"))
    assert "empty field: Proof" in errors
    assert "invalid Pixel QA: pending" in errors
