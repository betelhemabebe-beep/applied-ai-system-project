from typing import List, Dict
import csv


def load_music_knowledge(path: str) -> List[Dict]:
    """Load music knowledge CSV (genre → typical properties)."""
    knowledge = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            knowledge.append({
                "genre": row["genre"],
                "typical_energy": float(row["typical_energy"]),
                "typical_mood": row["typical_mood"],
                "description": row["description"],
            })
    return knowledge


def retrieve_candidates(user_prefs: Dict, songs: List[Dict]) -> List[Dict]:
    """
    Retrieve a subset of songs that are relevant to the user.
    This is a simple RAG-style filter step.
    """
    candidates = []

    for song in songs:
        score = 0

        # Match genre
        if user_prefs.get("genre") and song["genre"] == user_prefs["genre"]:
            score += 2

        # Match mood
        if user_prefs.get("mood") and song["mood"] == user_prefs["mood"]:
            score += 2

        # Energy proximity (loose filter)
        if "energy" in user_prefs:
            if abs(song["energy"] - user_prefs["energy"]) < 0.3:
                score += 1

        # Acoustic preference
        if "acoustic" in user_prefs:
            if user_prefs["acoustic"] and song["acousticness"] > 0.5:
                score += 1
            if not user_prefs["acoustic"] and song["acousticness"] < 0.5:
                score += 1

        # Keep only somewhat relevant songs
        if score >= 2:
            candidates.append(song)

    # fallback: if nothing matched, return all songs
    if not candidates:
        return songs

    return candidates


def enrich_with_knowledge(song: Dict, knowledge: List[Dict]) -> Dict:
    """
    Attach knowledge-based info to a song (RAG-style enrichment).
    """
    for k in knowledge:
        if song["genre"] == k["genre"]:
            song["typical_energy"] = k["typical_energy"]
            song["typical_mood"] = k["typical_mood"]
            song["genre_description"] = k["description"]
            break
    return song