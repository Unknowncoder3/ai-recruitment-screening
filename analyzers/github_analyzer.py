from utils.github_api import fetch_github_data


def analyze_github(username: str) -> dict:
    if not username:
        return {
            "score": 0,
            "repo_count": 0,
            "languages": [],
            "summary": "No GitHub username provided"
        }

    data = fetch_github_data(username)

    repo_count = data.get("repo_count", 0)
    languages = data.get("languages", [])
    source = data.get("source", "unknown")

    if repo_count == 0:
        return {
            "score": 0,
            "repo_count": 0,
            "languages": [],
            "summary": "No public GitHub data found"
        }

    # Scoring
    repo_score = min(repo_count * 6, 40)
    language_score = min(len(languages) * 10, 40)
    bonus = 10 if repo_count >= 5 else 0

    total_score = repo_score + language_score + bonus

    summary = (
        f"{repo_count} repositories, "
        f"{len(languages)} languages detected "
        f"(source: {source})"
    )

    return {
        "score": min(total_score, 100),
        "repo_count": repo_count,
        "languages": languages,
        "summary": summary
    }
