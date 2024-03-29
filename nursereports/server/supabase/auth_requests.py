
from ..secrets import api_key, api_url

from loguru import logger

import httpx
import json
import rich

def supabase_login_with_email(
        email: str,
        password: str
        ) -> dict:
    """
    Login using email and password. Returns dict of values.

    Args:
        email: <-
        password: <-

    Returns:
        success: If API call successful.
        status: Status codes if any.refle
        payload: Important data to return.
    """
    url = f'{api_url}/auth/v1/token'
    params = {
        "grant_type": "password",
        }
    headers = {
        "apikey": api_key,
        "Content-Type": "application/json",
        }
    data = {
        "email": email,
        "password": password,
        }
    response = httpx.post(
        url=url,
        params=params,
        headers=headers,
        data=json.dumps(data),
        )
    if response.is_success:
        logger.debug("Successfully signed in using email.")
        return {
            "success": True,
            "status": None,
            "payload": {
                "access_token": response.cookies.get(
                    'sb-access-token'
                    ),
                "refresh_token": response.cookies.get(
                    'sb-refresh-token'
                    )
                }
            }
    else:
        logger.critical("Failed to login using email.")
        error = json.loads(response.text)
        return {
            "success": False,
            "status": f"{error['error_description']}",
            "payload": None
            }
    
def supabase_create_account_with_email(
        email: str,
        password: str,
        ) -> dict:
    """
    Create account using email and password. Returns dict of values.

    Args:
        email: <-
        password: <-

    Returns:
        success: If API call successful.
        status: Status codes if any.
    """
    url = f'{api_url}/auth/v1/signup'
    headers = {
        "apikey": api_key,
        "Content-Type": "application/json",
        }
    data = {
        "email": email,
        "password": password
        }
    response = httpx.post(
        url=url,
        headers=headers,
        data=json.dumps(data),
        )
    if response.is_success:
        logger.debug("Successfully created account with email.")
        return {
            "success": True,
            "status": None,
            }
    else:
        logger.critical("Unable to create account using email.")
        rich.inspect(response)
        error = json.loads(response.text)
        return {
            "success": False,
            "status": f"{error['msg']}"
        }
    


def supabase_get_new_access_token(
        access_token: str,
        refresh_token: str,
        ) -> dict:
    """
    Get new access token using refresh token. Returns dict of values.

    Args:
        access_token: jwt object of user
        refresh_token: refresh token to be used to refresh expiration

    Returns:
        success: If API call successful.
        status: Status codes if any.
        payload: Important data to return.
    """
    url = f"{api_url}/auth/v1/token"
    params = {
        "grant_type": "refresh_token"
    }
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "refresh_token": refresh_token
    }
    response = httpx.post(
        url=url,
        params=params,
        headers=headers,
        data=json.dumps(data)
    )
    if response.is_success:
        logger.debug("Refreshed access token.")
        return {
            "success": True,
            "status": None,
            "payload": {
                "access_token": response.json().get('access_token'),
                "refresh_token": response.json().get('refresh_token')
            }
        }
    else:
        logger.warning("Unable to refresh access token.")
        rich.inspect(response)
        return {
            "success": False,
            "status": f"{response.status_code} - \
                        {response.reason_phrase}",
            "payload": None
        }