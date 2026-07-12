from check_story_packet import check_packet


VALID = """Objective: authority
Audience: AI builders
Story role: tactical
Content family: agent reliability
Proof: CI log
Relationship to recent posts: new proof angle
1. Pain-first with verifier payoff
2. Proof-first teardown
3. Contrast manual and automated checks
Hook: הסוכן עבר, המוצר נשבר
Context: one-agent workflow
Escalation: hidden regression
Payoff: independent verifier catches it
CTA: save checklist
Variable: proof-first opening
Expected signal: saves per reach
Baseline: previous tactical Reel
"""


def test_accepts_complete_story_packet():
    assert check_packet(VALID) == []


def test_rejects_empty_field_and_duplicate_hypotheses():
    text = VALID.replace("Audience: AI builders", "Audience:")
    text = text.replace("2. Proof-first teardown", "2. Pain-first with verifier payoff")
    errors = check_packet(text)
    assert "empty field: Audience" in errors
    assert "requires three distinct non-empty hypotheses" in errors
