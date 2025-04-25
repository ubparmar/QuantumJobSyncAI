import streamlit as st

def render_search_form() -> dict:
    """
    Sidebar form for user inputs:
    - keywords, location, experience, job type filters
    """
    st.sidebar.header("🔍 Job Search Filters")
    keywords   = st.sidebar.text_input("Keywords", value="Software Engineer")
    location   = st.sidebar.text_input("Location", value="Remote")
    experience = st.sidebar.selectbox(
        "Experience Level",
        ["Internship", "Entry level", "Associate", "Mid-Senior", "Director"],
        index=1,
    )
    job_type   = st.sidebar.multiselect(
        "Job Type",
        ["Full-time", "Part-time", "Contract", "Temporary", "Volunteer", "Internship"],
        default=["Full-time"],
    )
    return {
        "keywords": keywords,
        "location": location,
        "experience": experience,
        "job_type": job_type,
    }
