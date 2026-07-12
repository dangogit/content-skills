from check_hook_packet import check_packet


VALID = """Objective: retention
Story spine: failed agent to verifier
Recent-hook conflicts: none
| Angle | Visual | Verbal | On-screen | Proof | Payoff |
|---|---|---|---|---|---|
| 1 | broken test | הסוכן עבר | בדיקה אחת חסרה | test log | verifier catches bug |
| 2 | red build | זה נראה מוכן | עוד לא | CI screenshot | fix shown |
| 3 | two terminals | סוכן בדק סוכן | ביקורת נפרדת | demo | clean handoff |
Top pick: 1
Backup: 3
Test variable: proof-first opening
Baseline: previous pain-first Reel
Truth check: verified against demo
Hebrew read-aloud check: passed
"""


def test_accepts_three_complete_angle_rows():
    assert check_packet(VALID) == []


def test_rejects_empty_field_and_incomplete_angle():
    text = VALID.replace("Baseline: previous pain-first Reel", "Baseline:")
    text = text.replace("| 3 | two terminals | סוכן בדק סוכן | ביקורת נפרדת | demo | clean handoff |", "| 3 | | | | | |")
    errors = check_packet(text)
    assert "empty field: Baseline" in errors
    assert any("angle 3 has empty" in error for error in errors)


def test_rejects_duplicate_angle_numbers():
    text = VALID.replace("| 2 | red build", "| 1 | red build")
    assert "angle rows must be numbered 1, 2, 3 in order" in check_packet(text)
