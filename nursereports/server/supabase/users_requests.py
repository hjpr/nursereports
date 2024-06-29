from ..secrets import api_key, api_url
from ...server.exceptions import (
    DuplicateUserError,
    ReadError,
    RequestFailed,
)
from typing import Any

from datetime import datetime, timezone
from loguru import logger

import httpx
import json
import rich


def supabase_get_user_info(access_token: str) -> dict | None:
    """Use access token to retrieve a user info from the
    public users table.

    Args:
        access_token: jwt object containing auth data

    Returns:
        dict:
            created_at: timestamptz - user creation date, default is nowutc()
            hash: str - hash to compare state -> database
            license: str - user's license type, default is NULL
            license_state: str - user's license type, default is NULL
            membership: str - default value is 'Free'
            modified_at: timestamptz - user modified last date, default is nowutc()
            my_jobs: list[dict] - default value is NULL
            my_reports: list[dict] - default value is NULL
            needs_onboard: bool - default value is True
            reports: int - default value is 0
            saved_hospitals: dict - default value is NULL
            trust: int - default value is 0
            user_id: uuid - jwt provided uuid

    Exceptions:
        DuplicateUserError: retrieved too many user records.
        RequestFailed: request to retrieve user failed.

    """
    url = f"{api_url}/rest/v1/users?select=*"
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = httpx.get(url=url, headers=headers)
    if response.is_success:
        content = json.loads(response.content)
        if len(content) == 1:
            logger.debug("Retrieved user data from public/users.")
            return content[0]
        if len(content) > 1:
            logger.critical("Retrieved multiple user entries from a single user id!")
            raise DuplicateUserError(
                "Retrieved multiple user entries for a single user id."
            )
        else:
            return None
    else:
        logger.critical("Failed to retrieve data from public/users.")
        raise RequestFailed(f"{response.status_code} - {response.reason_phrase}")


def supabase_create_initial_user_info(access_token: str, user_id: str) -> None:
    """
    Creates initial user info in public users table with access_token
    and uuid.

    Args:
        access_token: jwt object of user
        uuid: uuid of user

    Default values set during initial user creation via default
    supabase settings:
        created_at: timestamptz - user creation date, default is nowutc()
        license: str - user's license type, default is NULL
        license_state: str - user's license type, default is NULL
        membership: str - default value is 'Free'
        modified_at: timestamptz - user modified last date, default is nowutc()
        my_jobs: list[dict] - default value is NULL
        my_reports: list[dict] - default value is NULL
        needs_onboard: bool - default value is True
        reports: int - default value is 0
        saved_hospitals: dict - default value is NULL
        trust: int - default value is 0
        user_id: uuid - jwt provided uuid

    Exceptions:
        RequestFailed: request to create user failed.
    """
    url = f"{api_url}/rest/v1/users"
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {"user_id": user_id}
    response = httpx.post(url=url, headers=headers, data=json.dumps(data))
    if response.is_success:
        logger.debug("New user successfully created in public/users.")
    else:
        logger.critical("Failed to create initial user info in public/users!")
        raise RequestFailed(f"{response.status_code} - {response.reason_phrase}")


def supabase_get_user_modified_at_timestamp(access_token: str) -> dict | None:
    """
    Checks if database has updates to user data that are not reflected in the state.

    Args:
        access_token: str - user JWT object

    Returns:
        dict:
            success: bool - if API call successful.
            status: str - user readable errors if any.
            payload: str - timestamp that info was last modified at

    Exceptions:
        RequestFailed: request to pull timestamp from database failed.
    """
    url = f"{api_url}/rest/v1/users?select=modified_at"
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = httpx.get(url=url, headers=headers)
    if response.is_success:
        content = json.loads(response.content)
        logger.debug("Pulled last modified timestamp data from user data.")
        return content[0]
    else:
        raise RequestFailed(
            "Request failed pulling timestamp info to compare stored to state."
        )


def supabase_update_user_info(
    access_token: str,
    user_id: str,
    data: Any,
) -> dict:
    """
    Updates public users table with users access_token and dict of
    info to change. Returns updated values so user can save to state.

    Args:
        access_token: jwt object of user
        user_id: claims id of user
        data: columns to update

    Returns:
        dict: updated data to save to state

    Exceptions:
        RequestFailed: Request failed to update info in /users.
    """
    data["modified_at"] = get_current_utc_timestamp_as_str()
    url = f"{api_url}/rest/v1/users?user_id=eq.{user_id}"
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }
    response = httpx.patch(url=url, headers=headers, data=json.dumps(data))
    if response.is_success:
        logger.debug("Updated user info in public/users.")
        return data
    else:
        raise RequestFailed("Failed to update user information.")


def supabase_get_user_reports(access_token, user_id) -> list[dict] | None:
    """
    Retrieves the user reports formatted for the dashboard page for
    display, editing, and removal.

    Args:
        access_token: jwt object of user
        user_id: claims id of user

    Returns:
        list[dict]: - list of reports as dicts
            assign_select_unit: str - user selected unit
            assign_input_unit_name: str - if unit not present, user entered unit
            assign_select_area: str - user selected area
            assign_input_area: str - if area not present, user entered area
            created_at: str - time report was created
            hospital_id: str - medicare id
            modified_at: str - time report was modified
            report_id: str - uuid of report

    Exceptions
        RequestFailed: request to database failed
    """
    columns = "report_id,hospital_id,assign_select_unit,assign_input_unit_name,assign_select_area,assign_input_area,created_at,modified_at"
    url = f"{api_url}/rest/v1/reports?user_id=eq.{user_id}&select={columns}"
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = httpx.get(url=url, headers=headers)
    if response.is_success:
        content = json.loads(response.content)
        logger.debug(f"Pulled {len(content)} user report(s) successfully.")
        return content
    else:
        raise RequestFailed("Unable to retrieve user reports from database.")


def supabase_get_saved_hospitals(access_token: str, user_id: str) -> list | None:
    """
    Retrieves any hospitals that user has saved for use in the dashboard.

    Args:
        access_token: str - user JWT object.
        user_id: str - uuid of user

    Returns:
        list[str]: list of hospitals as str (medicare ID #'s)

    Exceptions:
        RequestFailed: request to database failed.

    """
    url = f"{api_url}/rest/v1/users?user_id=eq.{user_id}&select=saved_hospitals"
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = httpx.get(url=url, headers=headers)
    if response.is_success:
        content = json.loads(response.content)
        saved_hospitals = content[0]["saved_hospitals"]
        if saved_hospitals:
            rich.inspect(saved_hospitals)
            logger.debug("Retrieved information from user's saved hospitals list.")
            return saved_hospitals
        else:
            logger.debug("User doesn't have any saved hospitals to retrieve.")
    else:
        raise RequestFailed("Request failed retrieving saved hospitals.")


def supabase_populate_saved_hospital_details(
    access_token: str, hosp_id: list
) -> list[dict] | None:
    """
    Pulls hospital information for use in the "My Hospitals" dashboard section.

    Args:
        access_token: str - user JWT object
        hospital_id

    Returns:
        list[dict]: list of hospital dicts populated with information
            dict:
                hosp_id: str - hospitals Medicare ID
                hosp_name: str - hospital's full name
                hosp_state: str - hospital's state as abbr
                hosp_city: str - hospital's city

    Exceptions:
        ReadError: expected information but response was empty.
        RequestFailed: request to database failed.
    """
    columns = "hosp_name,hosp_state,hosp_city,hosp_id"
    hosp_id_str = ','.join(map(str, hosp_id))
    url = f"{api_url}/rest/v1/hospitals?hosp_id=in.({hosp_id_str})&select={columns}"
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = httpx.get(url=url, headers=headers)
    if response.is_success:
        content = json.loads(response.content)
        if content:
            logger.debug("Retrieved full hospital details on user's saved hospitals.")
            return content
        else:
            raise ReadError(
                "Expected to retrieve saved hospital details but response was empty."
            )
    else:
        raise RequestFailed("Request failed retrieving saved hospital details.")


def get_current_utc_timestamp_as_str() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d %H:%M:%S.%f%z")
