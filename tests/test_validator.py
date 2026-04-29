from src.validator import validate_recommendations


def test_validator_high_confidence():
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
    }

    results = [
        ({"genre": "pop", "mood": "happy", "energy": 0.8}, 5.0, "ok")
    ]

    output = validate_recommendations(user_prefs, results)

    assert output["confidence"] == "High"
    assert output["warnings"] == []


def test_validator_low_confidence_when_mismatch():
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
    }

    results = [
        ({"genre": "rock", "mood": "sad", "energy": 0.2}, 2.0, "bad match")
    ]

    output = validate_recommendations(user_prefs, results)

    assert output["confidence"] in ["Medium", "Low"]
    assert len(output["warnings"]) > 0