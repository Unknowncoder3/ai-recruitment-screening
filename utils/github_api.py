import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional

GITHUB_API_BASE = "https://api.github.com"


def fetch_repositories_api(username: str) -> List[Dict]:
    """Try GitHub API first"""
    try:
        url = f"{GITHUB_API_BASE}/users/{username}/repos"
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            return []

        data = r.json()
        return data if isinstance(data, list) else []
    except Exception:
        return []


def fetch_repositories_scrape(username: str) -> Dict:
    """Fallback: scrape public GitHub profile"""
    try:
        url = f"https://github.com/{username}"
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            return {}

        soup = BeautifulSoup(r.text, "html.parser")

        # Repo count
        repo_tag = soup.find("span", class_="Counter")
        repo_count = int(repo_tag.text.strip()) if repo_tag else 0

        # Languages (best-effort)
        languages = set()
        for span in soup.find_all("span", itemprop="programmingLanguage"):
            languages.add(span.text.strip())

        return {
            "repo_count": repo_count,
            "languages": list(languages)
        }

    except Exception:
        return {}


def fetch_github_data(username: str) -> Dict:
    """
    Hybrid GitHub data fetcher:
    1. API
    2. Scraping fallback
    """

    repos = fetch_repositories_api(username)

    if repos:
        languages = set()
        for repo in repos:
            if isinstance(repo, dict) and repo.get("language"):
                languages.add(repo["language"])

        return {
            "repo_count": len(repos),
            "languages": list(languages),
            "source": "api"
        }

    # API failed → scrape
    scraped = fetch_repositories_scrape(username)
    scraped["source"] = "scrape"
    return scraped
