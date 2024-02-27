
from . import api_url, api_key
from loguru import logger

import httpx
import json

def supabase_get_user_info(access_token: str) -> dict:
    """Use access token to retrieve a user info from the 
    public users table.

    Args:
        access_token: jwt object containing auth data

    Returns:
        dict:
            success: bool
            status: user-readable reason for failure
            payload: dict of user info
    """
    url = f"{api_url}/rest/v1/users?select=*"
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
        }
    response = httpx.get(
        url=url,
        headers=headers
    )
    if response.is_success:
        content = json.loads(response.content)
        return {
            "success": True,
            "status": None,
            "payload": content
        }
    else:
        return {
            "success": False,
            "status": f"{response.status_code} - {response.reason_phrase}",
            "payload": None
        }
    
def supabase_update_user_info(access_token: str, data: dict) -> dict:
    """Use access token to update info on a user into the public users
    table.
    
    Args:
        access_token: jwt object containing auth data
        data: dict of information to update user with

    Returns:
        dict:
            success: bool
            status: user readable reason for failure
    """
    url = f"{api_url}/rest/v1/users"
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = httpx.patch(
        url=url,
        headers=headers,
        data=json.dumps(data)
    )
    if response.is_success:
        logger.debug("Successfully updated user information.")
        return {
            "success": True,
            "status": None
        }
    else:
        logger.critical(f"{response.status_code} - {response.reason_phrase}")
        return {
            "success": False,
            "status": f"{response.status_code} - {response.reason_phrase}"
        }
