from check_resource_contract import check_contract


VALID = """Asset: carousel/source.md
Named artifact: Agent Reliability Checklist
Guide URL: https://example.com/guides/agents
Keyword: AGENTS
Route collision check: passed
Local validation: passed
Remote validation: passed
Health: healthy
Synthetic delivery: mocked
Consent scope: one requested resource reply
Dedupe/rate limit: verified
Write-back: verified
Status: active
"""


def test_accepts_complete_contract():
    assert check_contract(VALID) == []


def test_rejects_empty_local_url_and_inactive_status():
    text = VALID.replace("Named artifact: Agent Reliability Checklist", "Named artifact:")
    text = text.replace("https://example.com/guides/agents", "http://127.0.0.1:3000/guide")
    text = text.replace("Status: active", "Status: pending")
    errors = check_contract(text)
    assert "empty field: Named artifact" in errors
    assert any("public HTTPS" in error for error in errors)
    assert "invalid Status: pending" in errors


def test_rejects_failed_proof_and_duplicate_fields():
    text = VALID.replace("Remote validation: passed", "Remote validation: failed")
    text += "Health: failed\n"
    errors = check_contract(text)
    assert "invalid Remote validation: failed" in errors
    assert "duplicate field: Health" in errors
