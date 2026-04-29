from src.retriever import retrieve_candidates


def test_retrieve_candidates_filters_songs():
    songs = [
        {"genre": "pop", "mood": "happy", "energy": 0.8, "acousticness": 0.2},
        {"genre": "rock", "mood": "intense", "energy": 0.9, "acousticness": 0.1},
    ]

    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "acoustic": False,
    }

    results = retrieve_candidates(user_prefs, songs)

    assert len(results) >= 1
    assert results[0]["genre"] == "pop"