import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from recommender import load_songs
from agent import run_recommendation_agent
from logger_utils import log_run

HEADER = "=" * 72

PROFILES = [
    (
        "High-Energy Pop",
        {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.90,
            "valence": 0.85,
            "acoustic": False,
            "danceability": 0.88,
        },
        "genre-first",
    ),
    (
        "Chill Lofi",
        {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.38,
            "valence": 0.57,
            "acoustic": True,
            "danceability": 0.60,
        },
        "mood-first",
    ),
    (
        "Deep Intense Rock",
        {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.91,
            "valence": 0.45,
            "acoustic": False,
            "danceability": 0.65,
        },
        "energy-focused",
    ),
    (
        "Ghost Genre (blues — not in catalog)",
        {
            "genre": "blues",
            "mood": "sad",
            "energy": 0.45,
            "valence": 0.30,
            "acoustic": True,
            "danceability": 0.50,
        },
        "balanced",
    ),
    (
        "Acoustic Paradox (metal + likes_acoustic=True)",
        {
            "genre": "metal",
            "mood": "aggressive",
            "energy": 0.95,
            "valence": 0.20,
            "acoustic": True,
            "danceability": 0.55,
        },
        "energy-focused",
    ),
    (
        "Contradictory Attributes (acoustic=True + energy=0.95)",
        {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.95,
            "valence": 0.50,
            "acoustic": True,
            "danceability": 0.65,
        },
        "genre-first",
    ),
]


def print_agent_output(label: str, output: dict):
    print(f"\n{HEADER}")
    print(f"  {label}")
    print(f"  Mode: {output['mode']}  |  Candidates: {output['candidate_count']}")
    print(HEADER)

    print(f"  Profile : {output['user_prefs']}\n")

    print("  Recommendations:\n")

    for i, (song, score, explanation) in enumerate(output["recommendations"], 1):
        print(f"  {i}. {song['title']} by {song['artist']}")
        print(f"     Score: {score}")
        for reason in explanation.split(" | "):
            print(f"     {reason}")
        print()

    print("  Validation:")
    print(f"     Confidence: {output['validation']['confidence']}")

    if output["validation"]["warnings"]:
        print("     Warnings:")
        for w in output["validation"]["warnings"]:
            print(f"     - {w}")
    else:
        print("     Warnings: None")

    print(HEADER)
    print()


def main():
    songs = load_songs("data/songs.csv")

    for label, prefs, mode in PROFILES:
        output = run_recommendation_agent(
            user_prefs=prefs,
            songs=songs,
            mode=mode,
            k=3
        )

        print_agent_output(label, output)

        log_run(output)


if __name__ == "__main__":
    main()