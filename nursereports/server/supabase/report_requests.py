from ..exceptions import RequestFailed
from ..secrets import api_key, api_url, admin_key
from loguru import logger

import httpx
import json
import rich


def supabase_get_hospital_info(access_token: str, hosp_id: str) -> dict[str, any]:
    """
    Retrieves hospital info from /hospital

    Args:
        access_token: jwt of user
        hospital: id of hospital

    Returns:
        dict:
            hosp_id: CMS id
            hosp_name: <-
            hosp_addr: <-
            hosp_city: <-
            hosp_state: state abbreviation
            hosp_zip: <-
            hosp_county: <-
            hosp_units: deduplicated list of units
            hosp_areas_roles: deduplicated list of areas and/or roles

    Exceptions:
        RequestFailed: request to pull info failed.
    """
    url = f"{api_url}/rest/v1/hospitals?hosp_id=eq.{hosp_id}&select=*"
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = httpx.get(url=url, headers=headers)
    if response.is_success:
        content = json.loads(response.content)
        return content[0]
    else:
        rich.inspect(response)
        raise RequestFailed("Request failed retrieving hospital.")


def supabase_submit_full_report(access_token: str, report: dict[str, any]) -> None:
    """
    Submits a completed report to /reports.

    Args:
        access_token: str - jwt object of user
        report: dict - contains full report fields to update in database

    Exceptions:
        RequestFailed: request to database failed
    """
    url = f"{api_url}/rest/v1/reports"
    data = json.dumps(report)
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }
    response = httpx.post(url=url, headers=headers, data=data)
    if response.is_success:
        logger.debug("Successfully submitted report to /reports.")
    else:
        rich.inspect(response)
        raise RequestFailed("Request to submit report to database failed.")


def supabase_user_edit_report(access_token: str, report: dict[str, any]) -> None:
    """
    Edits an existing full report in /reports via a user

    Args:
        access_token: str - jwt object of user
        report: dict - contains fields to update

    Exceptions:
        RequestFailed: request to database failed.
    """
    url = f"{api_url}/rest/v1/reports?report_id=eq.{report['report_id']}"
    data = json.dumps(report)
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }
    response = httpx.put(url=url, headers=headers, data=data)
    if response.is_success:
        logger.debug(f"Successfully edited report {report['report_id']} via user request.")
    else:
        rich.inspect(response)
        raise RequestFailed("Request to submit report to database failed.")
    
def supabase_user_patch_report(access_token: str, report: dict[str, any]) -> None:
    """
    Patches an existing report in /reports via a user

    Args:
        access_token: str - jwt object of user
        report: dict - contains fields to update

    Exceptions:
        RequestFailed: request to database failed.
    """
    url = f"{api_url}/rest/v1/reports?report_id=eq.{report['report_id']}"
    data = json.dumps(report)
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }
    response = httpx.patch(url=url, headers=headers, data=data)
    if response.is_success:
        logger.debug(f"Successfully patched report {report['report_id']} via user request.")
    else:
        rich.inspect(response)
        raise RequestFailed("Request to submit report to database failed.")

def supabase_admin_edit_report(report: dict[str, any]) -> None:
    """
    Edits an existing report in /reports via admin or site feature.

    Args:
        access_token: str - jwt object of user
        report: dict - contains fields to update

    Exceptions:
        RequestFailed: request to database failed.
    """
    url = f"{api_url}/rest/v1/reports?report_id=eq.{report['report_id']}"
    data = json.dumps(report)
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {admin_key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }
    response = httpx.patch(url=url, headers=headers, data=data)
    if response.is_success:
        logger.debug(f"Successfully edited report {report['report_id']} via admin request.")
    else:
        rich.inspect(response)
        raise RequestFailed("Request to submit report to database failed.")


def supabase_update_hospital_departments(hosp_id: str, data: dict) -> None:
    """
    Adds a unit to hospital in /hospitals table.
    """
    url = f"{api_url}/rest/v1/hospitals?hosp_id=eq.{hosp_id}&select=*"
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {admin_key}",
        "Content-Type": "application/json",
    }
    response = httpx.patch(url=url, headers=headers, data=json.dumps(data))
    if response.is_success:
        logger.debug(f"Updated department info for {hosp_id}.")
    else:
        rich.inspect(response)
        raise RequestFailed("Failed to update unit information.")
