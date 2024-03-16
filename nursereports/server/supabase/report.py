
from . import api_key, api_url
from loguru import logger

import httpx
import json
import rich

def supabase_get_hospital_info(access_token, hosp_id) -> dict:
    """
    Retrieves hospital info from /hospital.

    Args:
        access_token: jwt of user
        hospital: id of hospital

    Returns:
        dict:
            success: bool
            status: user-readable error if any
            payload:
                dict:
                    hosp_id: CMS id
                    hosp_name: <-
                    hosp_addr: <-
                    hosp_city: <-
                    hosp_state: state abbreviation
                    hosp_zip: <-
                    hosp_county: <-
    """
    url = f"{api_url}/rest/v1/hospitals"\
    f"?hosp_id=eq.{hosp_id}"\
    "&select=*"
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = httpx.get(
        url=url,
        headers=headers
    )
    if response.is_success:
        logger.debug(f"Got {hosp_id} from /hospitals")
        return {
            "success": True,
            "status": None,
            "payload": json.loads(response.content)[0]
        }
    else:
        logger.critical(f"Failed to retrieve {hosp_id} from /hospitals")
        rich.inspect(response)
        return {
            "success": False,
            "status": f"{response.status_code} - {response.reason_phrase}",
            "payload": None
        }

def supabase_no_report_id_conflict(access_token: str, id: str) -> dict:
    """
    Ensures that uuid is unique for each report in /report.

    Args:
        access_token: jwt object of user
        id: report uuid

    Returns:
        dict:
            success: bool
            status: user readable error if any
    """
    url = f"{api_url}/rest/v1/reports?id=eq.{id}&select=*"
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = httpx.get(
        url=url,
        headers=headers
    )
    if response.is_success:
        id_conflict = json.loads(response.content)
        if not id_conflict:
            logger.debug("No conflicts in /reports with user's report uuid.")
            return {
                "success": True,
                "status": None
            }
        else:
            logger.warning("User's report uuid already exists in /reports.")
            return {
                "success": False,
                "status": "Conflict"
            }
    else:
        logger.critical("Failed to search for uuid conflicts in /reports.")
        rich.inspect(response)
        return {
            "success": False,
            "status": f"{response.status_code} - {response.reason_phrase}"
        }
    
def supabase_submit_full_report(access_token: str, report: dict) -> dict:
        """
        Submits a completed report to /reports.

        Args:
            access_token: jwt object of user
            report: full report dict

        Returns:
            success: bool
            status: user readable error if any 
        """
        url = f"{api_url}/rest/v1/reports"
        data = json.dumps(report)
        headers = {
            "apikey": api_key,
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        response = httpx.post(
            url=url,
            headers=headers,
            data=data
        )
        if response.is_success:
            logger.debug("Successfully submitted report to /reports.")
            return {
                "success": True,
                "status": None
            }
        else:
            logger.critical("Failed to submit report to /reports.")
            rich.inspect(response)
            return {
                "success": False,
                "status": f"{response.status_code} - {response.reason_phrase}"
            }
        
