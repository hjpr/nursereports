from ..secrets import api_key, api_url
from ...server.exceptions import CreateUserFailed, LoginCredentialsInvalid, TokenRefreshFailed

from loguru import logger

import httpx
import json

def supabase_login_with_email(email: str, password: str) -> dict:
    """
    Login using email and password. Returns dict of tokens.

    Args:
        email: <-
        password: <-

    Returns:
        dict:
            access_token: str - user JWT object.
    """
    url = f"{api_url}/auth/v1/token"
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
        logger.debug(f"Signed in {email} using email.")
        payload = json.loads(response.content)
        return {
            "access_token": payload.get("access_token"),
        }
    else:
        error = json.loads(response.text)
        raise LoginCredentialsInvalid(error.get("msg"))


def supabase_create_account_with_email(
    email: str,
    password: str,
) -> None:
    """
    Create account using email and password.

    Args:
        email: <-
        password: <-

    Returns:
        None
    """
    url = f"{api_url}/auth/v1/signup"
    headers = {
        "apikey": api_key,
        "Content-Type": "application/json",
    }
    data = {"email": email, "password": password}
    response = httpx.post(
        url=url,
        headers=headers,
        data=json.dumps(data),
    )
    if response.is_success:
        logger.debug("Successfully created account with email.")
    else:
        error_message = json.loads(response.text)["msg"]
        raise CreateUserFailed(error_message)


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

    Exceptions:
        TokenRefreshFailed
    """
    url = f"{api_url}/auth/v1/token"
    params = {"grant_type": "refresh_token"}
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {"refresh_token": refresh_token}
    response = httpx.post(
        url=url, params=params, headers=headers, data=json.dumps(data)
    )
    if response.is_success:
        return {
            "access_token": response.json().get("access_token"),
            "refresh_token": response.json().get("refresh_token"),
        }
    else:
        raise TokenRefreshFailed("Unable to refresh access token.")
    
def supabase_recover_password(email: str) -> None:
    """
    Sends recovery email to a user's email account.

    Args:
        email: str - email of user to recover password for

    Returns:
        None
    """
    url = f"{api_url}/auth/v1/recover"
    headers = {
        "apikey": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "email": email
    }
    response = httpx.post(url=url, headers=headers, data=json.dumps(data))
    if response.is_success:
        logger.debug(f"Sent password recovery email to {email}")
    else:
        error = json.loads(response.text)
        raise Exception(error.get("msg"))
