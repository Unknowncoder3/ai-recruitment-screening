from typing import List, Dict

# ---------------------------------------------
# CONFIG: Keywords for core knowledge detection
# ---------------------------------------------

CORE_KNOWLEDGE_KEYWORDS = {
    "machine_learning": [
        "machine learning", "classification", "regression",
        "model", "training", "accuracy", "scikit", "tensorflow"
    ],
    "data_structures": [
        "array", "linked list", "stack", "queue", "tree",
        "graph", "hash", "algorithm"
    ],
    "web_development": [
        "react", "flask", "fastapi", "django",
        "frontend", "backend", "api", "rest"
    ],
    "databases": [
        "sql", "mysql", "postgres", "mongodb", "database"
    ],
    "ai_llm": [
        "llm", "langchain", "ollama", "openai",
        "embedding", "faiss", "vector"
    ]
}

REAL_WORLD_TERMS = [
    "real-world", "production", "scalable",
    "dashboard", "automation", "system", "application"
]


# ---------------------------------------------
# MAIN ANALYZER FUNCTION
# ---------------------------------------------

def analyze_projects(project_descriptions: List[str]) -> Dict:
    """
    Analyze candidate projects to infer:
    - Core CS knowledge
    - Practical / real-world exposure
    - Technical depth
    """

    if not project_descriptions:
        return {
            "score": 0,
            "strengths": [],
            "weaknesses": ["No projects provided"],
            "summary": "No projects available for evaluation"
        }

    core_areas_covered = set()
    real_world_projects = 0

    for project in project_descriptions:
        text = project.lower()

        # Detect core knowledge areas
        for area, keywords in CORE_KNOWLEDGE_KEYWORDS.items():
            if any(k in text for k in keywords):
                core_areas_covered.add(area)

        # Detect real-world orientation
        if any(term in text for term in REAL_WORLD_TERMS):
            real_world_projects += 1

    # -----------------------------
    # Scoring Logic
    # -----------------------------
    core_score = min(len(core_areas_covered) * 15, 60)
    real_world_score = min(real_world_projects * 20, 40)

    total_score = core_score + real_world_score

    # -----------------------------
    # Strengths & Weaknesses
    # -----------------------------
    strengths = []
    weaknesses = []

    if core_areas_covered:
        strengths.append(
            f"Covers core areas: {', '.join(core_areas_covered)}"
        )
    else:
        weaknesses.append(
            "Projects do not clearly demonstrate core CS concepts"
        )

    if real_world_projects > 0:
        strengths.append(
            f"{real_world_projects} real-world oriented project(s)"
        )
    else:
        weaknesses.append(
            "Projects lack clear real-world application focus"
        )

    # -----------------------------
    # Summary
    # -----------------------------
    summary = (
        f"Analyzed {len(project_descriptions)} projects. "
        f"Core knowledge areas covered: {len(core_areas_covered)}. "
        f"Real-world projects detected: {real_world_projects}."
    )

    return {
        "score": round(total_score, 2),
        "strengths": strengths,
        "weaknesses": weaknesses,
        "summary": summary
    }
