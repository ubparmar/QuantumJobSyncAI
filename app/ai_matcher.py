import json
from typing import List, Dict

import groq

from app import config

# Initialize Groq client
_client = groq.Client(api_key=config.GROQ_API_KEY)

def rank_jobs_with_groq(
    user_query: str,
    jobs: List[Dict]
) -> List[Dict]:
    """
    Send user query + raw jobs list to Groq for semantic ranking.
    Expects a JSON-encoded array of {id, match_score}.
    """
    messages = [
        {"role": "system", "content": "You are a job matching assistant."},
        {
            "role": "user",
            "content": json.dumps({
                "query": user_query,
                "jobs": jobs
            }),
        }
    ]
    response = _client.chat.completions.create(
        model="mixtral-8x7b",
        messages=messages,
        temperature=0.0
    )
    # Assume the assistant returns a JSON list of {"id":..., "match":...}
    ranked = json.loads(response.choices[0].message.content)
    # Merge match scores back into original job dicts
    job_map = {job["id"]: job for job in jobs}
    for item in ranked:
        job = job_map.get(item["id"])
        if job:
            job["match_score"] = item["match"]
    # Sort descending
    return sorted(job_map.values(), key=lambda j: j.get("match_score", 0), reverse=True)
