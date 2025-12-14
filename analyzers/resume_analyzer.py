import re
from typing import Dict, List

# -------------------------------------------------
# Skill patterns (robust + realistic)
# -------------------------------------------------

SKILL_PATTERNS = {
    "Python": [r"\bpython\b"],
    "Machine Learning": [
        r"\bmachine learning\b",
        r"\bml\b"
    ],
    "Data Science": [
        r"\bdata science\b",
        r"\bdata analysis\b",
        r"\bpandas\b",
        r"\bnumpy\b"
    ],
    "Web Development": [
        r"\breact\b",
        r"\bhtml\b",
        r"\bcss\b",
        r"\bjavascript\b"
    ],
    "Backend Development": [
        r"\bflask\b",
        r"\bdjango\b",
        r"\bfastapi\b",
        r"\bapi\b"
    ],
    "Databases": [
        r"\bsql\b",
        r"\bmysql\b",
        r"\bpostgres\b",
        r"\bmongodb\b"
    ],
    "Power BI": [
        r"\bpower bi\b",
        r"\bdax\b"
    ],
    "Core CS": [
        r"\boperating systems\b",
        r"\bcomputer networks\b",
        r"\boop\b",
        r"\bobject oriented\b"
    ]
}

# -------------------------------------------------
# TEXT NORMALIZATION (CRITICAL FIX)
# -------------------------------------------------

def normalize_text(text: str) -> str:
    """
    Fix PDF extraction issues where characters are space-separated.
    Example: 'P y t h o n' -> 'python'
    """
    # Remove spaces between single characters
    text = re.sub(r'(?<=\b[A-Za-z])\s+(?=[A-Za-z]\b)', '', text)

    # Normalize multiple spaces
    text = re.sub(r'\s+', ' ', text)

    return text.lower()


# -------------------------------------------------
# Resume Analyzer
# -------------------------------------------------

def analyze_resume(text: str, job_desc: str = "") -> Dict:

    if not text or not isinstance(text, str):
        return {
            "skills": [],
            "score": 0,
            "summary": "No resume text provided"
        }

    clean_text = normalize_text(text)

    matched_skills: List[str] = []

    for skill, patterns in SKILL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, clean_text):
                matched_skills.append(skill)
                break

    matched_skills = sorted(set(matched_skills))

    # -----------------------------
    # Scoring (realistic ATS-style)
    # -----------------------------
    score = min(len(matched_skills) * 12, 100)

    summary = (
        f"Detected {len(matched_skills)} skill areas: "
        f"{', '.join(matched_skills)}"
        if matched_skills
        else "No recognizable technical skills detected"
    )

    return {
        "skills": matched_skills,
        "score": score,
        "summary": summary
    }
