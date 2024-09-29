import re
import reflex as rx
import rich

from .base_state import BaseState
from ..server.supabase.hospital_requests import (
    supabase_get_hospital_overview_info,
    supabase_get_hospital_report_data,
)
from ..server.supabase.report_requests import supabase_admin_edit_report
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
    units_areas_roles_for_units: list[str]
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
    units_areas_roles_for_reviews: list[str]
    """User selectable filter by unit/area/role"""
    review_filter_units_areas_roles: str
    """User selectable filter by most liked/helpful etc."""
    review_sorted: str = "Most Recent"
    """Which page of reviews that user is on"""

    @rx.var(cache=True)
    def has_report_info(self) -> bool:
        return True if len(self.report_info) > 0 else False

    @rx.var(cache=True)
    def hosp_id(self) -> str:
        """Returns hosp_id if page param hosp_id is a valid CMS ID format."""
        hosp_id = self.router.page.params.get("cms_id")
        cms_is_valid = False
        if hosp_id:
            cms_is_valid = bool(re.match(r"^[a-zA-Z0-9]{5,6}$", hosp_id))
        return hosp_id if cms_is_valid else None

    @rx.var(cache=True)
    def filtered_review_info(self) -> list[dict]:
        """
        If user has selected filters, return list of dicts containing only
        reports from review_info
        """
        filtered_review_items = self.review_info

        if self.review_filter_units_areas_roles and self.review_info:
            filtered_review_items = [
                review
                for review in filtered_review_items
                if self.review_filter_units_areas_roles in review.get("unit", "")
                or self.review_filter_units_areas_roles in review.get("area_role", "")
            ]

        if self.review_sorted and self.review_info:
            if self.review_sorted == "Most Recent":
                filtered_review_items = sorted(
                    filtered_review_items,
                    key=lambda review: datetime.fromisoformat(review["created_at"]),
                    reverse=True,
                )
            if self.review_sorted == "Most Helpful":
                filtered_review_items = sorted(
                    filtered_review_items,
                    key=lambda review: review["likes_number"],
                    reverse=True
                )

        return filtered_review_items

    @staticmethod
    def format_datetime_for_overview(time_str) -> str:
        timestamp = datetime.fromisoformat(time_str)
        return timestamp.strftime("%B %Y")

    def event_state_load_hospital_info(self) -> Iterable[Callable]:
        """
        Retrieves and loads the hospital demographic info into the state,
        from /hospitals
        """
        try:
            self.reset()
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
        Build and store self.review_info to state to access info, and handle
        pulling out the units/areas/roles for filters.

        All reviews have the following...

        user_id: str
        report_id: str
        created_at: str
        formatted_created_at: str
        has_comp_comments: bool
        comp_comments: str
        has_assign_comments: bool
        assign_comments: str
        has_staffing_comments: bool
        staffing_comments: str

        Reviews with comments additionally have...

        has_unit
        has_area_role
        unit
        area_role
        likes
        likes_number
        user_has_liked
        """
        try:
            if self.report_info:
                review_info = []

                # Only do this process if there are comments in report.

                for report in self.report_info:
                    if (
                        report.get("comp_input_comments")
                        or report.get("assign_input_comments")
                        or report.get("staffing_input_comments")
                    ):
                        review_dict = {
                            "user_id": report.get("user_id"),
                            "report_id": report.get("report_id"),
                            "created_at": report.get("created_at"),
                            "formatted_created_at": self.format_datetime_for_overview(
                                report.get("created_at")
                            ),
                            "has_comp_comments": bool(
                                report.get("comp_input_comments")
                            ),
                            "comp_comments": report.get("comp_input_comments"),
                            "has_assign_comments": bool(
                                report.get("assign_input_comments")
                            ),
                            "assign_comments": report.get("assign_input_comments"),
                            "has_staffing_comments": bool(
                                report.get("staffing_input_comments")
                            ),
                            "staffing_comments": report.get("staffing_input_comments"),
                            "likes": report.get("likes"),
                        }

                        # Pull out units for unit/area/role filtering.

                        if report.get("assign_select_specific_unit") == "Yes":
                            review_dict["has_unit"] = True
                            review_dict["has_area_role"] = False
                            if (
                                report.get("assign_select_unit")
                                == "I don't see my unit"
                            ):
                                review_dict["unit"] = report.get(
                                    "assign_input_unit_name"
                                )
                            else:
                                review_dict["unit"] = report.get("assign_select_unit")
                        else:
                            review_dict["has_area_role"] = True
                            review_dict["has_unit"] = False
                            if (
                                report.get("assign_select_area")
                                == "I don't see my area or role"
                            ):
                                review_dict["area_role"] = report.get(
                                    "assign_input_area"
                                )
                            else:
                                review_dict["area_role"] = report.get(
                                    "assign_select_area"
                                )

                        # Format likes for the frontend so the user can see if they liked comment

                        review_dict["likes_number"] = len(review_dict["likes"])
                        review_dict["user_has_liked"] = self.user_info["user_id"] in review_dict["likes"]
                        review_info.append(review_dict)

                self.review_info = review_info

            # Make sure that units/areas/roles available to filter are unique

            if self.review_info:
                units_areas_roles = set()

                for review in self.review_info:
                    if review["has_unit"]:
                        units_areas_roles.add(review["unit"])
                    if review["has_area_role"]:
                        units_areas_roles.add(review["area_role"])
                self.units_areas_roles_for_reviews = sorted(list(units_areas_roles))

        except Exception as e:
            logger.critical(e)
            yield rx.toast.error("Whoops! Couldn't save reviews to state.")

    def event_state_like_unlike_review(
        self, review_to_edit: dict[str, str | list | bool]
    ) -> Iterable[Callable]:
        """
        Edits the report in the database at /report and then saves the changes
        to the state to reflect those changes in the review section of hospital
        overview.
        """
        try:
            rich.inspect(review_to_edit)
            if self.user_info["user_id"] in review_to_edit["likes"]:
                review_to_edit["likes"].remove(self.user_info["user_id"])
            else:
                review_to_edit["likes"].append(self.user_info["user_id"])
            review_to_edit = {
                "report_id": review_to_edit["report_id"],
                "likes": review_to_edit["likes"],
            }
            supabase_admin_edit_report(review_to_edit)

            for review in self.review_info:
                if review["report_id"] == review_to_edit["report_id"]:
                    review["likes"] = review_to_edit["likes"]
                    review["likes_number"] = len(review_to_edit["likes"])
                    review["user_has_liked"] = self.user_info["user_id"] in review_to_edit["likes"]

        except RequestFailed:
            rx.toast.error("Error providing review feedback.")