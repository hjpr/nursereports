from ..exceptions import RequestFailed
from ..secrets import api_key, api_url
from loguru import logger

import httpx
import json
import rich


def supabase_get_hospital_info(access_token: str, hosp_id: str) -> dict[str, any]:
    """
    Retrieves hospital info from /hospital.

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
        content= json.loads(response.content)
        return content[0]
    else:
        logger.critical(f"Failed to retrieve {hosp_id} from /hospitals")
        raise RequestFailed("Request failed retrieving hospital ")

def supabase_no_report_id_conflict(access_token: str, report_id: str) -> dict:
    """
    Ensures that uuid is unique for each report in /report.

    Args:
        access_token: jwt object of user
        report_id: report uuid

    Returns:
        dict:
            success: bool
            status: user readable error if any
    """
    url = f"{api_url}/rest/v1/reports?report_id=eq.{report_id}&select=*"
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = httpx.get(url=url, headers=headers)
    if response.is_success:
        id_conflict = json.loads(response.content)
        if not id_conflict:
            logger.debug("No conflicts in /reports with user's report uuid.")
            return {"success": True, "status": None}
        else:
            logger.warning("User's report uuid already exists in /reports.")
            return {"success": False, "status": "Conflict"}
    else:
        logger.critical("Failed to search for uuid conflicts in /reports.")
        rich.inspect(response)
        return {
            "success": False,
            "status": f"{response.status_code} - {response.reason_phrase}",
        }


def supabase_submit_full_report(access_token: str, report: dict[str, any]) -> None:
    """
    Submits a completed report to /reports.

    Args:
        access_token: jwt object of user
        report: full report dict

    Exceptions:
        RequestFailed: Request to database failed.
    """
    url = f"{api_url}/rest/v1/reports"
    data = json.dumps(report)
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = httpx.post(url=url, headers=headers, data=data)
    if response.is_success:
        logger.debug("Successfully submitted report to /reports.")
    else:
        rich.inspect(response)
        raise RequestFailed("Request to submit report to database failed.")
