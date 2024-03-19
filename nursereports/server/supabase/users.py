
from . import api_url, api_key
from datetime import datetime, timezone
from loguru import logger

import httpx
import json
import rich

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

    Payload contains:
        dict:
            uuid: str - users id as uuid
            license: str - user license type
            license_state: str user license state
            membership: str - membership level
            my_hospitals: dict - list of saved hospitals by id
            my_jobs: dict - list of saved jobs by id
            needs_onboard: bool - has user completed a report
            trust: int - trust level
            reports: int - how many successful reports submitted
            created_at: unix timestamp when user profile created
            modified_at: unix timestamp when user last changed info
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
        if content:
            logger.debug("Retrieved user data from public/users.")
            return {
                "success": True,
                "status": None,
                "payload": content[0]
            }
        else:
            logger.warning("No user data present in public/users.")
            return {
                "success": False,
                "status": "No user info present",
                "payload": None
            }
    else:
        logger.critical("Failed to retrieve data from public/users.")
        return {
            "success": False,
            "status": f"{response.status_code} - {response.reason_phrase}",
            "payload": None
        }
    
def supabase_create_initial_user_info(
        access_token: str,
        user_id: str,
    ) -> dict:
    """
    Creates initial user info in public users table with access_token
    and uuid.

    Args:
        access_token: jwt object of user
        uuid: uuid of user

    Returns:
        success: If API call successful.
        status: Status codes if any.

    Default values set during initial user creation via default
    supabase settings:
        user_id: user provided uuid
        created_at: user creation date
        modified_at: user modified last date
        membership: 'free'
        needs_onboard: True
        my_hospitals: {}
        my_jobs: {}
        trust: 0
    """
    url = f'{api_url}/rest/v1/users'
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "user_id": user_id,
    }
    response = httpx.post(
        url=url,
        headers=headers,
        data=json.dumps(data)
    )
    if response.is_success:
        logger.debug("New user successfully created in public/users.")
        return {
            "success": True,
            "status": None
        }
    else:
        logger.critical("Failed to create initial user info in public/users!")
        return {
            "success": False,
            "status": f"{response.status_code} - \
                {response.reason_phrase}"
        }
        
def supabase_update_user_info(
        access_token: str,
        user_id: str,
        data: list,
    ) -> dict:
    """
    Updates public users table with users access_token and dict of
    info to change.

    Args:
        access_token: jwt object of user
        user_id: claims id of user
        data: list of columns to update

    Returns:
        success: if API call successful
        status: user readable errors if any
    """
    data['modified_at'] = get_current_utc_timestamp_as_str()
    url = f'{api_url}/rest/v1/users?user_id=eq.{user_id}'
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    response = httpx.patch(
        url=url,
        headers=headers,
        data=json.dumps(data)
    )
    if response.is_success:
        logger.debug("Updated user info in public/users.")
        return {
            "success": True,
            "status": None
        }
    else:
        logger.critical("Failed to update user info in public/users!")
        rich.inspect(response)
        return {
            "success": False,
            "status": f"{response.status_code} - \
                {response.reason_phrase}"
        }
    
def get_current_utc_timestamp_as_str() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime('%Y-%m-%d %H:%M:%S.%f%z')
