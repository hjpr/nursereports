
from dotenv import load_dotenv
from loguru import logger

import httpx
import json
import os

load_dotenv()
api_url = os.getenv("SUPABASE_URL")
api_key = os.getenv("SUPABASE_ANON_KEY")
jwt_key = os.getenv("SUPABASE_JWT_KEY")

def event_supabase_submit_feedback(
        access_token,
        feedback
    ) -> dict:
    """Submits feedback to /rest/v1/feedback."""
    url = f"{api_url}/rest/v1/feedback"
    data = json.dumps(feedback)
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = httpx.post(
        url=url,
        headers=headers,
        data=data
    )
    if response.is_success:
        logger.debug(f"Feedback submitted successfully to {url}.")
        return {"success": True, "status": None}
    else:
        logger.critical(f"{response.status_code} - {response.reason_phrase}")
        return {
            "success": False,
            "status": f"{response.status_code} - {response.reason_phrase}"
        }