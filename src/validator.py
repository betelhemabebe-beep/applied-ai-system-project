from typing import List, Dict, Tuple


def validate_recommendations(user_prefs: Dict,
                             results: List[Tuple[Dict, float, str]]) -> Dict:
    """
    Validate recommendation quality and return confidence + warnings.
    """
    warnings = []
    confidence = "High"

    if not results:
        return {
            "confidence": "Low",
            "warnings": ["No recommendations were generated."]
        }

    top_song = results[0][0]

    # --- Check 1: Genre match ---
    if user_prefs.get("genre"):
        if top_song["genre"] != user_prefs["genre"]:
            warnings.append("Top result does not match requested genre.")
            confidence = downgrade_confidence(confidence)

    # --- Check 2: Mood match ---
    if user_prefs.get("mood"):
        if top_song["mood"] != user_prefs["mood"]:
            warnings.append("Top result does not match requested mood.")
            confidence = downgrade_confidence(confidence)

    # --- Check 3: Energy mismatch ---
    if "energy" in user_prefs:
        diff = abs(top_song["energy"] - user_prefs["energy"])
        if diff > 0.4:
            warnings.append("Top result energy is far from requested level.")
            confidence = downgrade_confidence(confidence)

    # --- Check 4: Genre missing from catalog ---
    genres_in_results = {r[0]["genre"] for r in results}
    if user_prefs.get("genre") and user_prefs["genre"] not in genres_in_results:
        warnings.append(f"Requested genre '{user_prefs['genre']}' not found in results.")
        confidence = downgrade_confidence(confidence)

    # --- Check 5: Low score overall ---
    avg_score = sum(r[1] for r in results) / len(results)
    if avg_score < 3:
        warnings.append("Overall recommendation scores are low.")
        confidence = downgrade_confidence(confidence)

    return {
        "confidence": confidence,
        "warnings": warnings
    }


def downgrade_confidence(current: str) -> str:
    """
    Reduce confidence level step-by-step.
    """
    if current == "High":
        return "Medium"
    if current == "Medium":
        return "Low"
    return "Low"