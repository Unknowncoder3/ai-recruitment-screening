def candidate_prompt(data):
    return f"""
You are an AI recruitment assistant.

Evaluate the candidate based on:
- Resume skills: {data['resume']}
- GitHub: {data['github']}
- Academics: {data['academics']}

Explain strengths, weaknesses, and hiring recommendation.
"""
