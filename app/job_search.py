import requests
from typing import List, Dict

from app import config, utils

def search_linkedin_jobs(
    token: str,
    keywords: str,
    location: str,
    count: int = 10
) -> List[Dict]:
    """
    Query the LinkedIn Jobs Search endpoint.
    If you lack LinkedIn API access, swap this for Proxycurl or a local JSON fallback.
    """
    url = f"{config.JOB_API_BASE}/jobSearch"
    headers = utils.get_linkedin_headers(token)
    params = {
        "keywords": keywords,
        "location": location,
        "count": count,
    }
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    # LinkedIn returns on key "elements"
    return data.get("elements", [])
