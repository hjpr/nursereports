from ..exceptions import RequestFailed, DuplicateReport, DuplicateUUID
from ..secrets import api_key, api_url, admin_key
from datetime import datetime, timedelta, timezone
from loguru import logger

import httpx
import json
import rich


def supabase_check_for_existing_report(access_token: str, report: dict) -> None:
    """
    Checks for an existing report of the same unit within a 30 day window.

    Args:
        access_token: jwt of user
        report: dict of report prepared from state vars

    Exceptions:
        DuplicateReport: a duplicate report was found in database.
        RequestFailed: request to check existing reports failed.
    """
    thirty_days_prior = datetime.now(timezone.utc) - timedelta(days=30)
    date_limit = thirty_days_prior.strftime("%Y-%m-%d %H:%M:%S %z")
    user_id = report["user_id"]

    url = f"{api_url}/rest/v1/reports?user_id=eq.{user_id}&created_at=gte.{date_limit}"
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = httpx.get(url=url, headers=headers)
    if response.is_success:
        existing_reports = json.loads(response.content)
        for existing_report in existing_reports:
            if report["assign_select_specific_unit"] == "Yes":
                if (
                    existing_report["assign_select_unit"]
                    == report["assign_select_unit"]
                    and existing_report["assign_input_unit_name"]
                    == report["assign_input_unit_name"]
                ):
                    raise DuplicateReport(
                        "A report was already submitted for this unit within 30 days."
                    )
            else:
                if (
                    existing_report["assign_select_area"]
                    == report["assign_select_area"]
                    and existing_report["assign_input_area"]
                    == report["assign_input_area"]
                ):
                    raise DuplicateReport(
                        "A report was already submitting for this area/role within 30 days."
                    )
    else:
        rich.inspect(response)
        raise RequestFailed("Request to check for existing report failed.")


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


def supabase_check_report_uuid_conflict(
    access_token: str, user_id: str, report_id: str
) -> None:
    """
    Ensures that uuid is unique for each report in /report.

    Args:
        access_token: jwt object of user
        report_id: report uuid

    Exceptions:
        DuplicateUUID: found a duplicate UUID in database.
        RequestFailed: request to database failed
    """
    url = f"{api_url}/rest/v1/reports?report_id=eq.{report_id}&select=*"
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = httpx.get(url=url, headers=headers)
    if response.is_success:
        report = json.loads(response.content)

        if len(report) == 0:
            logger.debug("No duplicate reports were found.")

        elif len(report) == 1:
            if report[0] and report["user_id"] == user_id:
                logger.debug(
                    "Found report when checking for duplicates but it's because user is attempting to edit."
                )
            else:
                raise DuplicateUUID(
                    f"Found a duplicate UUID in an existing report that isn't from {user_id}"
                )

        elif len(report) > 1:
            logger.critical("Found multiple reports with duplicate UUID's.")
            raise RequestFailed("Internal error - check report UUID assignment. Found multiple duplicates.")

    else:
        rich.inspect(response)
        raise RequestFailed("Request to check for duplicate UUID's in database failed.")


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
    Edits an existing report in /reports via a user

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
        logger.debug(f"Successfully edited {report['report_id']}.")
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
        logger.debug(f"Successfully edited report {report['report_id']}.")
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
