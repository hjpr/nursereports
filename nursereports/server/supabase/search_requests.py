
from ..secrets import api_key, api_url
from loguru import logger

import httpx
import json

def supabase_get_hospital_search_results(
    access_token,
    state,
    city
    ) -> dict:
    """
    Pulls hospitals using state abbreviation and city.

    Args:
        access_token: users bearer token
        state: abbreviated user selected state
        city: user selected city

    Returns:
        success: bool
        status: user readable status codes if fail
        payload: returned hospital list
    """
    url = f"{api_url}/rest/v1/hospitals"\
    f"?hosp_state=ilike.{state}"\
    f"&hosp_city=ilike.{city}"\
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
        logger.debug(f"Retrieved search results for {city}, {state} from /hospitals")
        return {
            'success': True,
            'status': None,
            'payload': json.loads(response.content)
            }
    else:
        logger.critical(f"Failed to get results for {city}, {state} from /hospitals")
        return {
            'success': False,
            'status': f"{response.status_code} - {response.reason_phrase}",
            'payload': None
        }
    