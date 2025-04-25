import os
from dotenv import load_dotenv

# Load any .env file in project root
load_dotenv()

# LinkedIn OAuth
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
LINKEDIN_REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI", "http://localhost:8501")

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# LinkedIn API base (or swap to Proxycurl if needed)
JOB_API_BASE = os.getenv("JOB_API_BASE", "https://api.linkedin.com/v2")
