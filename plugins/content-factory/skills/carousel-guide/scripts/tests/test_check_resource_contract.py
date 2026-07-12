from check_resource_contract import check_contract


def test_accepts_complete_contract():
    text = "Named artifact\nGuide URL\nKeyword\nHealth\nSynthetic delivery\nStatus"
    assert check_contract(text) == []


def test_rejects_missing_route_proof():
    assert any("missing Synthetic delivery" in e for e in check_contract("Named artifact"))
