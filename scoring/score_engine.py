def final_score(resume, github, academics):
    return round(
        resume * 0.4 +
        github * 0.4 +
        academics * 0.2,
        2
    )
