import streamlit as st
import re

# -------------------------------
# Imports
# -------------------------------
from analyzers.resume_analyzer import analyze_resume
from analyzers.github_analyzer import analyze_github
from analyzers.academic_analyzer import analyze_academics
from analyzers.project_analyzer import analyze_projects

from scoring.score_engine import final_score
from llm.ollama_client import run_llm
from llm.prompts import candidate_prompt

from utils.pdf_parser import extract_text_from_pdf


# -------------------------------
# Utility: GitHub Username Normalizer
# -------------------------------
def normalize_github_username(input_text: str) -> str:
    """
    Accepts GitHub username or full profile URL
    and extracts the username safely.
    """
    if not input_text:
        return ""

    input_text = input_text.strip()

    # Match full GitHub URL
    match = re.search(r"github\.com/([A-Za-z0-9_-]+)", input_text)
    if match:
        return match.group(1)

    # Otherwise assume it's already a username
    return input_text


# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="AI-Based Candidate Screening System",
    layout="wide"
)

st.title("🤖 AI-Based Candidate Screening System")
st.caption("AI-assisted, privacy-first recruitment screening using local LLMs")


# -------------------------------
# Cached GitHub Analysis
# -------------------------------
@st.cache_data(ttl=3600)
def cached_github_analysis(username: str):
    return analyze_github(username)


# -------------------------------
# Resume Upload Section
# -------------------------------
st.header("📄 Resume")

uploaded_resume = st.file_uploader(
    "Upload Resume (PDF only)",
    type=["pdf"]
)

resume_text = ""

if uploaded_resume:
    try:
        resume_text = extract_text_from_pdf(uploaded_resume)
        st.success("Resume uploaded and parsed successfully.")
        with st.expander("View extracted resume text"):
            st.text(resume_text[:3000])
    except Exception:
        st.error("Failed to parse resume. Please paste text manually.")

# Manual fallback
resume_text_manual = st.text_area(
    "Or paste resume text manually",
    height=200
)

if resume_text_manual.strip():
    resume_text = resume_text_manual


# -------------------------------
# Candidate Inputs
# -------------------------------
st.header("👤 Candidate Information")

raw_github_input = st.text_input(
    "GitHub Username or Profile URL",
    placeholder="Unknowncoder3 or https://github.com/Unknowncoder3"
)

github_username = normalize_github_username(raw_github_input)

st.subheader("🎓 Academic Details")
tenth = st.number_input("10th Percentage", 0.0, 100.0)
twelfth = st.number_input("12th Percentage", 0.0, 100.0)
cgpa = st.number_input("CGPA", 0.0, 10.0)

st.subheader("🧩 Projects")
project_input = st.text_area(
    "Describe projects (one per line)",
    height=150,
    placeholder=(
        "AI-based resume screening system using LLMs\n"
        "Spam SMS detection using Machine Learning\n"
        "Power BI sales dashboard"
    )
)


# -------------------------------
# Evaluate Button
# -------------------------------
if st.button("🚀 Evaluate Candidate"):

    if not resume_text:
        st.warning("Please upload or paste resume text.")
        st.stop()

    if not github_username:
        st.warning("Please enter a GitHub username or profile URL.")
        st.stop()

    with st.spinner("Analyzing candidate profile..."):

        resume_result = analyze_resume(resume_text, "")

        github_result = cached_github_analysis(github_username)

        academic_result = analyze_academics(tenth, twelfth, cgpa)

        project_list = [p.strip() for p in project_input.split("\n") if p.strip()]
        project_result = analyze_projects(project_list)

        score = final_score(
            resume_result["score"],
            github_result["score"],
            academic_result["score"]
        )


    # -------------------------------
    # Results
    # -------------------------------
    st.success("Evaluation Complete")

    st.metric("⭐ Overall Fit Score", score)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Resume Analysis")
        st.write(resume_result)

        st.subheader("🐙 GitHub Analysis")
        st.write(github_result)

        if github_result["score"] == 0:
            st.info(
                "GitHub data may be unavailable due to API rate limits "
                "or no public repositories. This is normal without an API key."
            )

    with col2:
        st.subheader("🎓 Academic Analysis")
        st.write(academic_result)

        st.subheader("🧩 Project Analysis")
        st.write(project_result)


    # -------------------------------
    # AI Recommendation
    # -------------------------------
    st.subheader("🤖 AI Hiring Recommendation")

    prompt = candidate_prompt({
        "resume": resume_result,
        "github": github_result,
        "academics": academic_result,
        "projects": project_result
    })

    with st.spinner("Generating AI recommendation..."):
        recommendation = run_llm(prompt)

    if recommendation.startswith("⚠️"):
        st.warning(recommendation)
        st.info(
            "Fallback Recommendation: Candidate shows strong academic performance "
            "and relevant technical skills. Manual review recommended."
        )
    else:
        st.success("AI Recommendation Generated")
        st.write(recommendation)
