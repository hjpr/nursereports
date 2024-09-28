from ..exceptions import RequestFailed
from ..secrets import api_key, api_url
from loguru import logger

import httpx
import json
import rich

def supabase_get_hospital_overview_info(access_token: str, hosp_id: str) -> dict[str, any]:
    """
    Retrieves info on single hospital from /hospital via CMS ID #.

    Args:
        access_token: jwt of user
        hosp_id: id of hospital

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
        logger.critical(f"Failed to retrieve {hosp_id} from /hospitals")
        raise RequestFailed("Request failed retrieving hospital.")
    
def supabase_get_hospital_report_data(access_token: str, hosp_id: str) -> dict[str, any]:
    """
    Retrieves all reports for a given hospital via the CMS ID #.

    Args:
        access_token: jwt of user
        hosp_id: CMS ID of hospital

    Returns:
        list:
            dict:
                report_id: str - UUID of report
                user_id: str - UUID of user making report
                license: str - RN - Bachelors / RN - Associates/ LPN / Nursing Student
                trust: int - trust level when user made report (0-4)
                hospital_id: str - CMS ID of hospital
                created_at: str/timestamptz - date/time report was made
                modified_at: str/timestamptz - date/time report was modified
                is_test: bool - if report is a test (exclude report if test)
                comp_select_overall: str - letter grade of compensation (a-f)
                assign_select_overall: str - letter grade of assignment (a-f)
                staffing_select_overall: str - letter grade of staffing (a-f)
                comp_select_emp_type: str - full-time/part-time/prn
                comp_select_pay_type: str - weekly/hourly
                comp_input_pay_amount: int - in dollars/hour|week depending
                comp_input_diff_nights: int - dollars/hr
                comp_input_diff_weekends: int - dollars/hr
                comp_select_total_experience: str - years of nursing experience
                comp_input_comments: str - user entered comments on compensation
                assign_input_comments: str - user entered comments on compensation
                staffing_input_comments: str - user entered comments on compensation
                assign_select_specific_unit: str - "yes" or "no"
                assign_select_unit: str - previously entered units
                assign_input_unit_name: str - if unit not previously entered
                assign_select_area: str - previously entered areas/roles
                assign_input_area: str - if area/role not previously entered
                (...) see Obsidian diagram for rest of rows

    Exceptions:
        RequestFailed: request to pull info failed.
    """
    url = f"{api_url}/rest/v1/reports?hospital_id=eq.{hosp_id}&select=*"
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = httpx.get(url=url, headers=headers)
    if response.is_success:
        content= json.loads(response.content)
        rich.inspect(content)
        return content
    else:
        logger.critical(f"Failed to retrieve {hosp_id} from /reports")
        raise RequestFailed("Request failed retrieving hospital.")
