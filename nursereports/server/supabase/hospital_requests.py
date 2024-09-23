from ..exceptions import RequestFailed
from ..secrets import api_key, api_url
from loguru import logger

import httpx
import json
import rich

def supabase_get_hospital_overview_info(access_token: str, hosp_id: str) -> dict[str, any]:
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
        content= json.loads(response.content)
        return content[0]
    else:
        rich.inspect(response)
        logger.critical(f"Failed to retrieve {hosp_id} from /hospitals")
        raise RequestFailed("Request failed retrieving hospital.")