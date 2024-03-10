
from . import api_key, api_url

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
        success: if API call successful
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
        return {
            'success': True,
            'status': None,
            'payload': json.loads(response.content)
            }
    else:
        return {
            'success': False,
            'status': f"{response.status_code} - {response.reason_phrase}",
            'payload': None
        }