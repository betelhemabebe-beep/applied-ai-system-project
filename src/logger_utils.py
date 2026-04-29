from datetime import datetime


def log_run(agent_output: dict, log_path: str = "logs/recommendation_log.txt") -> None:
    """Save a simple record of each recommendation run."""
    with open(log_path, "a", encoding="utf-8") as f:
        f.write("=" * 72 + "\n")
        f.write(f"Run time: {datetime.now()}\n")
        f.write(f"Mode: {agent_output['mode']}\n")
        f.write(f"User preferences: {agent_output['user_prefs']}\n")
        f.write(f"Candidate count: {agent_output['candidate_count']}\n")
        f.write(f"Confidence: {agent_output['validation']['confidence']}\n")

        if agent_output["validation"]["warnings"]:
            f.write("Warnings:\n")
            for warning in agent_output["validation"]["warnings"]:
                f.write(f"- {warning}\n")
        else:
            f.write("Warnings: none\n")

        f.write("Recommendations:\n")
        for song, score, explanation in agent_output["recommendations"]:
            f.write(f"- {song['title']} by {song['artist']} | score={score}\n")

        f.write("\n")