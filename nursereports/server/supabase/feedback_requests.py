
from ..secrets import api_key, api_url
from .rate_limit_requests import rate_limit_supabase
from loguru import logger

import httpx
import json

@rate_limit_supabase('feedback', 1, 1)
def supabase_submit_feedback(
        access_token,
        data
    ) -> dict:
    """
    Submits feedback to /rest/v1/feedback. Returns a dict with
    explanation of failure if occurs.

    Args:
        access_token: user jwt
        data: dict of values to upload

    Returns:
        success: bool
        status: user-readable reason for failure
    """
    url = f"{api_url}/rest/v1/feedback"
    data = json.dumps(data)
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
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