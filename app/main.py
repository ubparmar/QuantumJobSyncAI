import os
import sys

# Insert project root (parent of this file) into sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import streamlit as st

from app import utils
from app.inputs import render_search_form
from app.job_search import search_linkedin_jobs
from app.ai_matcher import rank_jobs_with_groq


def main():
    st.set_page_config(
        page_title="QuantumJobSyncAI",
        page_icon="⚛️",
        layout="wide"
    )
    st.title("QuantumJobSyncAI ⚛️")

    # — OAuth flow —
    if "access_token" not in st.session_state:
        params = st.query_params  # <- replaced experimental_get_query_params
        code  = params.get("code", [None])[0]
        state = params.get("state", [None])[0]

        if code:
            try:
                token = utils.exchange_code_for_token(code)
                st.session_state.access_token = token
                st.set_query_params()    # <- replaced experimental_set_query_params
            except Exception as e:
                st.error(f"OAuth error: {e}")
            return

        # first‐time: no code, so build & show the LinkedIn login link
        if "oauth_state" not in st.session_state:
            st.session_state.oauth_state = utils.generate_state()
        auth_url = utils.build_linkedin_auth_url(st.session_state.oauth_state)
        st.markdown(f"[👉 Login with LinkedIn]({auth_url})")
        return

    # — After login —
    token = st.session_state.access_token

    # Render filters + input form
    criteria = render_search_form()
    if st.sidebar.button("🔎 Search Jobs"):
        with st.spinner("Fetching jobs…"):
            try:
                jobs = search_linkedin_jobs(
                    token,
                    criteria["keywords"],
                    criteria["location"],
                )
                if not jobs:
                    st.warning("No jobs found. Try changing filters.")
                    return

                # AI‐powered ranking
                ranked = rank_jobs_with_groq(criteria["keywords"], jobs)

                # Display results
                for job in ranked:
                    title   = job.get("title", "Untitled")
                    company = job.get("companyName", "")
                    loc     = job.get("location", "")
                    score   = job.get("match_score", 0.0)

                    st.markdown(f"### [{title}]({job.get('applyUrl','')})")
                    st.write(f"**Company:** {company} • **Location:** {loc}")
                    st.progress(score)  # visual match‐bar
                    st.write("---")

            except Exception as e:
                st.error(f"Error during search: {e}")


if __name__ == "__main__":
    main()
