def analyze_academics(tenth, twelfth, cgpa):
    score = (tenth * 0.3) + (twelfth * 0.3) + (cgpa * 10 * 0.4)
    return {
        "score": round(score, 2),
        "summary": "Academic consistency evaluated"
    }
