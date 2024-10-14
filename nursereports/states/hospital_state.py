import numpy as np
import polars as pl
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
from scipy import interpolate
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
    Pay info loaded from event_state_load_pay_info derived from report_info.
    """
    interpolated_full_time_pay: dict
    interpolated_part_time_pay: dict
    interpolated_prn_pay: dict
    averaged_contract_pay: dict
    contract_pay: list[dict]
    """
    Sets context for what user is viewing.
    """
    selected_employment_type: str = "Full-time"
    selected_experience: int = 4
    selected_pay_tab: str = "staff"

    """
    If there are less than 10 reports for ft/pt/prn category, then True. Also
    pull from state info to 
      Set during
    event_state_load_pay_info
    """
    ft_hospital_pay_info_limited: bool
    ft_state_pay_info_limited: bool
    pt_hospital_pay_info_limited: bool
    pt_state_pay_info_limited: bool
    prn_hospital_pay_info_limited: bool
    prn_state_pay_info_limited: bool
    contract_hospital_pay_info_limited: bool
    contract_state_pay_info_limited: bool
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
    Units/areas/roles loaded during event_state_load_review_info to allow users to filter the
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
    def has_staff_pay_info_hospital(self) -> bool:
        return (
            True
            if self.interpolated_full_time_pay
            or self.interpolated_part_time_pay
            or self.interpolated_prn_pay
            else False
        )

    @rx.var(cache=True)
    def has_staff_pay_info_state(self) -> bool:
        return False

    @rx.var(cache=True)
    def has_contract_pay_info(self) -> bool:
        return True if self.contract_pay else False

    @rx.var(cache=True)
    def hosp_id(self) -> str:
        """Returns hosp_id if page param hosp_id is a valid CMS ID format."""
        hosp_id = self.router.page.params.get("cms_id")
        cms_is_valid = False
        if hosp_id:
            cms_is_valid = bool(re.match(r"^[a-zA-Z0-9]{5,6}$", hosp_id))
        return hosp_id if cms_is_valid else None

    @rx.var(cache=True)
    def full_time_pay_hospital(self) -> str:
        if self.interpolated_full_time_pay:
            rounded = round(self.interpolated_full_time_pay.get(self.selected_experience), 2)
            formatted = "{:.2f}".format(rounded)
            return f"${formatted}/hr"
        else:
            return False
    
    @rx.var(cache=True)
    def full_time_pay_state(self) -> str:
        pass
    
    @rx.var(cache=True)
    def part_time_pay_hospital(self) -> str:
        return self.interpolated_full_time_pay.get(f"{self.selected_experience}")
    
    @rx.var(cache=True)
    def part_time_pay_state(self) -> str:
        pass
    
    @rx.var(cache=True)
    def prn_pay_hospital(self) -> str:
        return self.interpolated_full_time_pay.get(f"{self.selected_experience}")
    
    @rx.var(cache=True)
    def prn_pay_state(self) -> str:
        pass

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
                    reverse=True,
                )

        return filtered_review_items

    @staticmethod
    def format_datetime_for_overview(time_str) -> str:
        timestamp = datetime.fromisoformat(time_str)
        return timestamp.strftime("%B %Y")

    def set_slider(self, value) -> None:
        self.selected_experience = value[0]

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
            self.units_areas_roles_for_units = units + areas_roles
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

    def event_state_load_pay_info(self) -> Iterable[Callable]:
        """
        Loads and formats...
            interpolated_full_time_pay
            interpolated_part_time_pay
            interpolated_prn_pay
            averaged_contract_pay
            contract_pay

        Casts any non-int value to int for graph use.
        """
        try:
            if self.report_info:
                report_info = supabase_get_hospital_report_data(
                    self.access_token, self.hosp_id
                )
                pay_df = pl.DataFrame(report_info)

                # Full time pay data and interpolation. Also check if enough reports.

                full_time_pay_df = pay_df.filter(
                    pl.col("comp_select_emp_type") == "Full-time"
                ).select(["comp_input_pay_amount", "comp_select_total_experience"])
                full_time_pay_df = full_time_pay_df.with_columns(
                    pl.col("comp_select_total_experience")
                    .cast(pl.Int8, strict=False)
                    .fill_null(26)
                ).sort(by=pl.col("comp_select_total_experience"))
                full_time_pay = full_time_pay_df.to_dicts()
                self.ft_hospital_pay_info_limited = bool(len(full_time_pay) < 10)
                if full_time_pay:
                    x = full_time_pay_df["comp_select_total_experience"].to_numpy()
                    y = full_time_pay_df["comp_input_pay_amount"].to_numpy()
                    f = interpolate.interp1d(
                        x, y, kind="quadratic", fill_value="extrapolate"
                    )
                    x_interpolated = np.arange(0, 27)
                    y_interpolated = f(x_interpolated)
                    full_time_pay_interpolated_df = pl.DataFrame(
                        {
                            "years_experience": x_interpolated,
                            "interpolated_pay": y_interpolated,
                        }
                    )
                    interpolated_full_time_pay = (
                        full_time_pay_interpolated_df.to_dicts()
                    )
                    self.interpolated_full_time_pay = {
                        item["years_experience"]: item["interpolated_pay"]
                        for item in interpolated_full_time_pay
                    }

                # Part time pay data and interpolation. Also check if enough reports.

                part_time_pay_df = pay_df.filter(
                    pl.col("comp_select_emp_type") == "Part-time"
                ).select(["comp_input_pay_amount", "comp_select_total_experience"])
                part_time_pay_df = part_time_pay_df.with_columns(
                    pl.col("comp_select_total_experience")
                    .cast(pl.Int8, strict=False)
                    .fill_null(26)
                )
                part_time_pay = part_time_pay_df.to_dicts()
                self.pt_hospital_pay_info_limited = bool(len(part_time_pay) < 10)
                if part_time_pay:
                    x = part_time_pay_df["comp_select_total_experience"].to_numpy()
                    y = part_time_pay_df["comp_input_pay_amount"].to_numpy()
                    f = interpolate.interp1d(
                        x, y, kind="quadratic", fill_value="extrapolate"
                    )
                    x_interpolated = np.arange(0, 27)
                    y_interpolated = f(x_interpolated)
                    part_time_pay_interpolated_df = pl.DataFrame(
                        {
                            "years_experience": x_interpolated,
                            "interpolated_pay": y_interpolated,
                        }
                    )
                    interpolated_part_time_pay = part_time_pay_interpolated_df.to_dict()
                    self.interpolated_part_time_pay = {
                        item["years_experience"]: item["interpolated_pay"]
                        for item in interpolated_part_time_pay
                    }

                # PRN pay data and interpolation.

                prn_pay_df = pay_df.filter(
                    pl.col("comp_select_emp_type") == "PRN"
                ).select(["comp_input_pay_amount", "comp_select_total_experience"])
                prn_pay_df = (
                    prn_pay_df.with_columns(pl.col("comp_select_total_experience"))
                    .cast(pl.Int8, strict=False)
                    .fill_null(26)
                )
                prn_pay = prn_pay_df.to_dicts()
                self.prn_hospital_pay_info_limited = bool(len(prn_pay) < 10)

                if prn_pay:
                    x = prn_pay_df["comp_select_total_experience"].to_numpy()
                    y = prn_pay_df["comp_input_pay_amount"].to_numpy()
                    f = interpolate.interp1d(
                        x, y, kind="quadratic", fill_value="extrapolate"
                    )
                    x_interpolated = np.arange(0, 27)
                    y_interpolated = f(x_interpolated)
                    prn_pay_interpolated_df = pl.DataFrame(
                        {
                            "years_experience": x_interpolated,
                            "interpolated_pay": y_interpolated,
                        }
                    )
                    interpolated_prn_pay = prn_pay_interpolated_df.to_dicts()
                    self.interpolated_prn_time_pay = {
                        item["years_experience"]: item["interpolated_pay"]
                        for item in interpolated_prn_pay
                    }

                # Contract pay data and averaged pay.

                contract_pay_df = pay_df.filter(
                    pl.col("comp_select_emp_type") == "Contract"
                ).select(["comp_input_pay_amount", "created_at"])
                contract_pay = contract_pay_df.to_dicts()
                self.contract_hospital_pay_info_limited = bool(len(contract_pay) < 10)
                if contract_pay:
                    averaged_contract_pay_df = contract_pay_df.select(
                        pl.col("comp_input_pay_amount")
                        .mean()
                        .alias("average_contract_pay")
                    )
                    self.averaged_contract_pay = averaged_contract_pay_df.to_dict()
        except Exception as e:
            logger.critical(e)

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
                        review_dict["user_has_liked"] = (
                            self.user_info["user_id"] in review_dict["likes"]
                        )
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
                    review["user_has_liked"] = (
                        self.user_info["user_id"] in review_to_edit["likes"]
                    )

        except RequestFailed:
            rx.toast.error("Error providing review feedback.")
