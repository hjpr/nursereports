import re
import reflex as rx
import rich

from .base_state import BaseState
from ..server.supabase.hospital_requests import (
    supabase_get_hospital_overview_info,
    supabase_get_hospital_report_data,
)
from ..server.exceptions import RequestFailed

from datetime import datetime
from loguru import logger
from typing import Any, Callable, Iterable


class HospitalState(BaseState):
    """
    Hospital info loaded in during event_state_load_hospital_info, contains
    a dict of relevant hospital info from /hospitals.
    """
    hospital_info: dict[str, Any]
    """
    Report info loaded in during event_state_load_report_info, contains a
    list of dicts where each dict is a complete report from a user from
    /reports
    """
    report_info: list[dict]
    """
    Unit/area/role info loaded in during event_state_load_hospital_info,
    contains a list of available units from /hospitals from each unit that
    a user adds via a report.
    """
    units_areas_roles_for_units: list
    """
    Review info loaded in during event_state_load_report_info, contains a list
    of dicts where each dict is a user report where that user left a comment in
    any of the three free response sections from /reports.
    """
    review_info: list[dict]
    """
    Units/areas/roles pulled from review_info to allow users to filter the
    reviews by the respective unit/area/role.
    """
    units_areas_roles_for_reviews: list

    @rx.var(cache=True)
    def has_report_info(self) -> bool:
        return True if len(self.report_info) > 0 else False
    
    @rx.var
    def hosp_id(self) -> str:
        """Returns hosp_id if page param hosp_id is a valid CMS ID format."""
        hosp_id = self.router.page.params.get("cms_id")
        cms_is_valid = False
        if hosp_id:
            cms_is_valid = bool(re.match(r"^[a-zA-Z0-9]{5,6}$", hosp_id))
        return hosp_id if cms_is_valid else None
    
    def event_state_load_hospital_info(self) -> Iterable[Callable]:
        """
        Retrieves and loads the hospital demographic info into the state, 
        from /hospitals
        """
        try:
            self.hospital_info = supabase_get_hospital_overview_info(
                self.access_token, self.hosp_id
            )
            units = self.hospital_info.get("hosp_units")
            areas_roles = self.hospital_info.get("hosp_areas_roles")
            self.units_areas_roles_available = units + areas_roles
        except RequestFailed as e:
            logger.error(e)
            yield rx.toast.error("Failed to retrieve report data from backend.")

    def event_state_load_report_info(self) -> Iterable[Callable]:
        """
        Retrieves and loads hospital report info into the state, from
        /reports
        """
        try:
            self.report_info = supabase_get_hospital_report_data(
                self.access_token, self.hosp_id
            )
        except RequestFailed as e:
            logger.critical(e)
            yield rx.toast.error("Failed to retrieve review data from backend.")

    def event_state_load_review_info(self) -> Iterable[Callable]:
        """
        After loading the reports, check through if users left any free responses
        so that we can view those responses in our filterable reviews section.
        """
        if self.report_info:
            review_info = []

            for report in self.report_info:
                if (
                    report.get("comp_input_comments")
                    or report.get("assign_input_comments")
                    or report.get("staffing_input_comments")
                ):
                    review_dict = {
                            "user_id" : report.get("user_id"),
                            "created_at": report.get("created_at"),
                            "formatted_created_at": self.format_datetime_for_overview(report.get("created_at")),
                            "has_comp_comments": bool(report.get("comp_input_comments")),
                            "comp_comments": report.get("comp_input_comments"),
                            "has_assign_comments": bool(report.get("assign_input_comments")),
                            "assign_comments": report.get("assign_input_comments"),
                            "has_staffing_comments": bool(report.get("staffing_input_comments")),
                            "staffing_comments": report.get("staffing_input_comments")
                        }
                    # Build report dicts for units/areas/roles.
                    if report.get("assign_select_specific_unit") == "Yes":
                        review_dict["has_unit"] = True
                        review_dict["has_area_role"] = False
                        if report.get("assign_select_unit") == "I don't see my unit":
                            review_dict["unit"] = report.get("assign_input_unit_name")
                        else:
                            review_dict["unit"] = report.get("assign_select_unit")
                    else:
                        review_dict["has_area_role"] = True
                        review_dict["has_unit"] = False
                        if report.get("assign_select_area") == "I don't see my area or role":
                            review_dict["area_role"] = report.get("assign_input_area")
                        else:
                            review_dict["area_role"] = report.get("assign_select_area")
                    review_info.append(review_dict)
            self.review_info = review_info

        if self.review_info:
            self.units_areas_roles_for_reviews = self.get_unique_units_areas_roles()

    def get_unique_units_areas_roles(self):
        units_areas_roles_reviews = set()

        for review in self.review_info:
            if review["assign_select_specific_unit"] == "Yes":
                if review["assign_input_unit_name"]:
                    item = review["assign_input_unit_name"]
                else:
                    item = review["assign_select_unit"]
            else:
                if review["assign_input_area"]:
                    item = review["assign_input_area"]
                else:
                    item = review["assign_select_area"]
            units_areas_roles_reviews.add(item)

        return list(units_areas_roles_reviews)

    @staticmethod
    def format_datetime_for_overview(time_str) -> str:
        timestamp = datetime.fromisoformat(time_str)
        return timestamp.strftime("%B %Y")