import re
import reflex as rx

from ..server.supabase.hospital_requests import (
    supabase_get_hospital_overview_info,
    supabase_get_hospital_report_data,
)
from .base_state import BaseState

from loguru import logger
from typing import Any, Callable, Iterable


class HospitalState(BaseState):
    hospital_info: dict[str, Any]
    report_info: list[dict]
    unit_area_role_info: list
    review_info: list[dict]

    @rx.var
    def has_report_info(self) -> bool:
        return True if len(self.report_info) > 0 else False

    @rx.var
    def hosp_id(self):
        """Returns hosp_id if page param hosp_id is a valid CMS ID format."""
        hosp_id = self.router.page.params.get("cms_id")
        cms_is_valid = False
        if hosp_id:
            cms_is_valid = bool(re.match(r"^[a-zA-Z0-9]{5,6}$", hosp_id))
        return hosp_id if cms_is_valid else None

    def event_state_load_hospital_info(self) -> Iterable[Callable]:
        """Retrieves and loads the hospital demographic info into the state."""
        try:
            # Retrieve the hospital demographics from database.
            self.hospital_info = supabase_get_hospital_overview_info(
                self.access_token, self.hosp_id
            )
            # Load unit/area/role info into the state.
            units = self.hospital_info.get("hosp_units")
            areas_roles = self.hospital_info.get("hosp_areas_roles")
            self.unit_area_role_info = units + areas_roles
        except Exception as e:
            logger.warning(e)

    def event_state_load_report_info(self) -> Iterable[Callable]:
        """
        Retrieves and loads hospital report info into the state.
        """
        try:
            # Retrieves all the reports for a given CMS ID.
            self.report_info = supabase_get_hospital_report_data(
                self.access_token, self.hosp_id
            )
            # Load reviews into state by user id if user has a review in any category.
            if self.report_info:
                review_info = []
                for report in self.report_info:
                    # Build dict from reports list only if it contains comment(s).
                    if (
                        report.get("comp_input_comments")
                        or report.get("assign_input_comments")
                        or report.get("staffing_input_comments")
                    ):
                        review_dict = {
                                "user_id" : report.get("user_id"),
                                "created_at": report.get("created_at"),
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
        except Exception as e:
            logger.warning(e)
