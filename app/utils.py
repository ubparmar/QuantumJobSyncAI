import secrets
from urllib.parse import urlencode

import requests
import streamlit as st

from app import config

def generate_state() -> str:
    """Create a CSRF token for OAuth flow."""
    return secrets.token_urlsafe(16)

def build_linkedin_auth_url(state: str) -> str:
    """Construct the LinkedIn OAuth2 authorization URL."""
    params = {
        "response_type": "code",
        "client_id": config.LINKEDIN_CLIENT_ID,
        "redirect_uri": config.LINKEDIN_REDIRECT_URI,
        "scope": "r_liteprofile r_emailaddress",
        "state": state,
    }
    return f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(params)}"

def exchange_code_for_token(code: str) -> str:
    """Swap LinkedIn 'code' for an access token."""
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config.LINKEDIN_REDIRECT_URI,
        "client_id": config.LINKEDIN_CLIENT_ID,
        "client_secret": config.LINKEDIN_CLIENT_SECRET,
    }
    r = requests.post(token_url, data=payload)
    r.raise_for_status()
    return r.json()["access_token"]

def get_linkedin_headers(token: str) -> dict:
    """Standard headers for LinkedIn API calls."""
    return {
        "Authorization": f"Bearer {token}",
        "X-Restli-Protocol-Version": "2.0.0",
    }
