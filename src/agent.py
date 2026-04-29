from typing import Dict, List

from src.recommender import recommend_songs, max_score_for_mode
from src.retriever import retrieve_candidates, enrich_with_knowledge, load_music_knowledge
from src.validator import validate_recommendations

def run_recommendation_agent(user_prefs: Dict,
                             songs: List[Dict],
                             mode: str = "balanced",
                             k: int = 3) -> Dict:
    """
    Run the full applied AI workflow:
    1. Retrieve relevant candidates
    2. Enrich candidates with music knowledge
    3. Recommend songs
    4. Validate recommendations
    5. Return final structured response
    """
    knowledge = load_music_knowledge("data/music_knowledge.csv")

    candidates = retrieve_candidates(user_prefs, songs)
    enriched_candidates = [
        enrich_with_knowledge(song.copy(), knowledge)
        for song in candidates
    ]

    results = recommend_songs(
        user_prefs=user_prefs,
        songs=enriched_candidates,
        k=k,
        mode=mode,
        diverse=True
    )

    validation = validate_recommendations(user_prefs, results)

    return {
        "user_prefs": user_prefs,
        "mode": mode,
        "max_score": max_score_for_mode(user_prefs, mode),
        "candidate_count": len(enriched_candidates),
        "recommendations": results,
        "validation": validation
    }