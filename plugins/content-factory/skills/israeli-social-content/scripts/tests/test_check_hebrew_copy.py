from check_hebrew_copy import check_copy


def test_accepts_spoken_hebrew_without_mechanical_traps():
    assert check_copy("בנו סוכן שעובד בשבילכם\nכתבו DESIGN ואשלח את הצ'קליסט") == []


def test_rejects_em_dash_generic_share_cta_and_inline_ai():
    errors = check_copy("זה AI — שתפו עם מישהו שצריך את זה")
    assert any("em dash" in error for error in errors)
    assert any("generic share CTA" in error for error in errors)
    assert any("inline AI" in error for error in errors)
