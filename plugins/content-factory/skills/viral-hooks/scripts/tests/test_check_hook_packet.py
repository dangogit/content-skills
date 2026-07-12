from check_hook_packet import check_packet


def test_accepts_three_angle_packet():
    text = "Objective: reach\nProof: demo\nAngle 1\nAngle 2\nAngle 3\nTop pick\nBaseline\nTest variable"
    assert check_packet(text) == []


def test_rejects_missing_proof():
    errors = check_packet("Objective: reach\nAngle 1\nAngle 2\nAngle 3")
    assert any("missing Proof" in error for error in errors)
