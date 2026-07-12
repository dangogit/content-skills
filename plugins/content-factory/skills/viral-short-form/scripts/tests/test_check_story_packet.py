from check_story_packet import check_packet


def test_accepts_complete_story_packet():
    text = "Objective\nAudience\nStory role\nProof\nSelected spine\nExperiment"
    assert check_packet(text) == []


def test_rejects_missing_audience():
    errors = check_packet("Objective\nStory role\nProof\nSelected spine\nExperiment")
    assert any("missing Audience" in error for error in errors)
