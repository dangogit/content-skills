from check_face_packet import check_packet


def test_accepts_complete_face_packet():
    text = "Mode\nSlides\nReferences\nScene jobs\nLikeness QA\nText/pixel QA"
    assert check_packet(text) == []


def test_rejects_missing_likeness_proof():
    assert any("missing Likeness QA" in e for e in check_packet("Mode\nSlides"))
