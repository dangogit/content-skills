from check_carousel_packet import check_packet


def test_accepts_complete_packet():
    assert check_packet("Objective\nPromise\nProof\nSlides\nPixel QA") == []


def test_rejects_missing_proof():
    assert any("missing Proof" in e for e in check_packet("Objective\nPromise"))
