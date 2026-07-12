from check_caption_packet import check_packet


VALID = """Objective: saves
Caption: הנה הצ'קליסט שביקשתם
CTA: שמרו לפעם הבאה
CTA rationale: reference value
On-screen text: שורה אחת באזור הבטוח
Hashtags: none
Pinned comment: none
Risk flags: none
"""


def test_accepts_complete_packet():
    assert check_packet(VALID) == []


def test_rejects_empty_fields_and_bait():
    errors = check_packet(VALID.replace("Caption: הנה הצ'קליסט שביקשתם", "Caption:") + "share with someone who needs this —")
    assert "empty field: Caption" in errors
    assert "uses generic share CTA" in errors
    assert "contains an em dash" in errors
