from src.agent import run_recommendation_agent


def test_agent_returns_structure():
    songs = [
        {
            "id": 1,
            "title": "Test Song",
            "artist": "Test Artist",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "tempo_bpm": 120,
            "valence": 0.9,
            "danceability": 0.8,
            "acousticness": 0.2,
        }
    ]

    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "acoustic": False,
        "danceability": 0.8,
    }

    output = run_recommendation_agent(user_prefs, songs, k=1)

    assert "recommendations" in output
    assert "validation" in output
    assert "confidence" in output["validation"]