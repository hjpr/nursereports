
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