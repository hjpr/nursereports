import numpy as np
import pandas as pd
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
    report_scores: list[dict]
    report_dataframe: pd.DataFrame

    """
    Pay info loaded from event_state_load_pay_info derived from report_info.
    """
    interpolated_ft_pay_hospital: dict
    interpolated_pt_pay_hospital: dict
    interpolated_prn_pay_hospital: dict
    interpolated_ft_pay_state: dict
    interpolated_pt_pay_state: dict
    interpolated_prn_pay_state: dict
    averaged_contract_pay_hospital: dict
    averaged_contract_pay_state: dict
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
    ft_pay_hospital_info_limited: bool
    pt_pay_hospital_info_limited: bool
    prn_pay_hospital_info_limited: bool
    ft_pay_state_info_limited: bool
    pt_pay_state_info_limited: bool
    prn_pay_state_info_limited: bool
    contract_pay_info_hospital_limited: bool
    contract_pay_info_state_limited: bool

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
    def ft_pay_hospital_formatted(self) -> dict:
        if self.interpolated_ft_pay_hospital:
            rounded_hourly = round(self.interpolated_ft_pay_hospital.get(self.selected_experience), 2)
            formatted_hourly = "{:.2f}".format(rounded_hourly)
            rounded_yearly = round(rounded_hourly * 36 * 52)
            formatted_yearly = "{:,}".format(rounded_yearly)
            return {
                "hourly": f"${formatted_hourly} /hr",
                "yearly": f"(${formatted_yearly} /yr)"
            }
        else:
            return False
    
    @rx.var(cache=True)
    def ft_pay_state_formatted(self) -> str:
        if self.interpolated_ft_pay_state:
            rounded = round(self.interpolated_ft_pay_state.get(self.selected_experience), 2)
            formatted = "{:.2f}".format(rounded)
            return f"${formatted}/hr"
        else:
            return False
    
    @rx.var(cache=True)
    def pt_pay_hospital_formatted(self) -> str:
        if self.interpolated_pt_pay_hospital:
            rounded = round(self.interpolated_pt_pay_hospital.get(self.selected_experience), 2)
            formatted = "{:.2f}".format(rounded)
            return f"${formatted}/hr"
        else:
            return False
    
    
    @rx.var(cache=True)
    def pt_pay_state_formatted(self) -> str:
        if self.interpolated_ft_pay_state:
            rounded = round(self.interpolated_ft_pay_state.get(self.selected_experience), 2)
            formatted = "{:.2f}".format(rounded)
            return f"${formatted}/hr"
        else:
            return False
    
    
    @rx.var(cache=True)
    def prn_pay_hospital_formatted(self) -> str:
        if self.interpolated_prn_pay_hospital:
            rounded = round(self.interpolated_prn_pay_hospital.get(self.selected_experience), 2)
            formatted = "{:.2f}".format(rounded)
            return f"${formatted}/hr"
        else:
            return False
    
    
    @rx.var(cache=True)
    def prn_pay_state_formatted(self) -> str:
        if self.interpolated_prn_pay_state:
            rounded = round(self.interpolated_prn_pay_state.get(self.selected_experience), 2)
            formatted = "{:.2f}".format(rounded)
            return f"${formatted}/hr"
        else:
            return False

    @rx.var(cache=True)
    def filtered_review_info(self) -> list[dict]:
        """
        If no filters are selected, returns all reviews. Otherwise applies filters
        so that user can filter down to desired reviews.
        """
        filtered_review_items = self.review_info

        if self.review_filter_units_areas_roles and filtered_review_items:
            filtered_review_items = [
                review for review in filtered_review_items
                if self.review_filter_units_areas_roles == review.get("unit", "")
                or self.review_filter_units_areas_roles == review.get("area_role", "")
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
    def letter_to_number(letter: str) -> int:
        return {'a': 4, 'b': 3, 'c': 2, 'd': 1, 'f': 0}.get(letter)

    @staticmethod
    def number_to_letter(number: int | float) -> str:
        return {4: 'a', 3: 'b', 2: 'c', 1: 'd', 0: 'f'}.get(round(number))

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
                pay_df = pl.DataFrame(self.report_info.copy())

                # Full time pay data and interpolation. Also check if enough reports.

                ft_pay_hospital_df = pay_df.filter(
                    pl.col("comp_select_emp_type") == "Full-time"
                ).select(["comp_input_pay_amount", "comp_select_total_experience"])
                ft_pay_hospital_df = ft_pay_hospital_df.with_columns(
                    pl.col("comp_select_total_experience")
                    .cast(pl.Int8, strict=False)
                    .fill_null(26)
                ).sort(by=pl.col("comp_select_total_experience"))
                ft_pay = ft_pay_hospital_df.to_dicts()
                self.ft_pay_hospital_info_limited = bool(len(ft_pay) < 10)
                if ft_pay:
                    x = ft_pay_hospital_df["comp_select_total_experience"].to_numpy()
                    y = ft_pay_hospital_df["comp_input_pay_amount"].to_numpy()
                    f = interpolate.interp1d(
                        x, y, kind="quadratic", fill_value="extrapolate"
                    )
                    x_interpolated = np.arange(0, 27)
                    y_interpolated = f(x_interpolated)
                    filtered_ft_pay_hospital_df = pl.DataFrame(
                        {
                            "years_experience": x_interpolated,
                            "interpolated_pay": y_interpolated,
                        }
                    )
                    interpolated_ft_pay_hospital = (
                        filtered_ft_pay_hospital_df.to_dicts()
                    )
                    self.interpolated_ft_pay_hospital = {
                        item["years_experience"]: item["interpolated_pay"]
                        for item in interpolated_ft_pay_hospital
                    }

                # Part time pay data and interpolation. Also check if enough reports.

                pt_pay_df = pay_df.filter(
                    pl.col("comp_select_emp_type") == "Part-time"
                ).select(["comp_input_pay_amount", "comp_select_total_experience"])
                pt_pay_df = pt_pay_df.with_columns(
                    pl.col("comp_select_total_experience")
                    .cast(pl.Int8, strict=False)
                    .fill_null(26)
                )
                pt_pay = pt_pay_df.to_dicts()
                self.pt_pay_hospital_info_limited = bool(len(pt_pay) < 10)
                if pt_pay:
                    x = pt_pay_df["comp_select_total_experience"].to_numpy()
                    y = pt_pay_df["comp_input_pay_amount"].to_numpy()
                    f = interpolate.interp1d(
                        x, y, kind="quadratic", fill_value="extrapolate"
                    )
                    x_interpolated = np.arange(0, 27)
                    y_interpolated = f(x_interpolated)
                    filtered_pt_df = pl.DataFrame(
                        {
                            "years_experience": x_interpolated,
                            "interpolated_pay": y_interpolated,
                        }
                    )
                    interpolated_pt_pay_hospital = filtered_pt_df.to_dict()
                    self.interpolated_pt_pay_hospital = {
                        item["years_experience"]: item["interpolated_pay"]
                        for item in interpolated_pt_pay_hospital
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
                self.prn_pay_hospital_info_limited = bool(len(prn_pay) < 10)

                if prn_pay:
                    x = prn_pay_df["comp_select_total_experience"].to_numpy()
                    y = prn_pay_df["comp_input_pay_amount"].to_numpy()
                    f = interpolate.interp1d(
                        x, y, kind="quadratic", fill_value="extrapolate"
                    )
                    x_interpolated = np.arange(0, 27)
                    y_interpolated = f(x_interpolated)
                    interpolated_prn_pay_hospital_df = pl.DataFrame(
                        {
                            "years_experience": x_interpolated,
                            "interpolated_pay": y_interpolated,
                        }
                    )
                    interpolated_prn_pay_hospital = interpolated_prn_pay_hospital_df.to_dicts()
                    self.interpolated_prn_pay_hospital = {
                        item["years_experience"]: item["interpolated_pay"]
                        for item in interpolated_prn_pay_hospital
                    }

                # Contract pay data and averaged pay.

                contract_pay_df = pay_df.filter(
                    pl.col("comp_select_emp_type") == "Contract"
                ).select(["comp_input_pay_amount", "created_at"])
                contract_pay = contract_pay_df.to_dicts()
                self.contract_pay_info_hospital_limited = bool(len(contract_pay) < 10)
                if contract_pay:
                    averaged_contract_pay_df = contract_pay_df.select(
                        pl.col("comp_input_pay_amount")
                        .mean()
                        .alias("average_contract_pay")
                    )
                    self.averaged_contract_pay_hospital = averaged_contract_pay_df.to_dict()
        except Exception as e:
            logger.critical(e)

    def event_state_load_unit_info(self) -> Iterable[Callable]:
        """
        From reports data, pull out info pertinent to unit classification
        and scoring and perform dataframe operations to average and organize
        scoring.
        """
        try:
            if self.report_info:
                units_df = (
                    pl.DataFrame(self.report_info.copy())
                    .with_columns(
                        pl.when(
                            pl.col("assign_select_specific_unit").str.contains("Yes")
                        )
                        .then(
                            pl.coalesce(
                                pl.col("assign_select_unit"),
                                pl.col("assign_input_unit_name")
                            )
                        )
                        .otherwise(None)
                        .alias("unit"),

                        pl.when(
                            pl.col("assign_select_specific_unit").str.contains("No")
                        )
                        .then(
                            pl.coalesce(
                                pl.col("assign_select_area"),
                                pl.col("assign_input_area")
                            )
                        )
                        .otherwise(None)
                        .alias("area_role")
                    )
                    .select([
                        "unit",
                        "area_role",
                        "comp_select_overall",
                        "assign_select_overall",
                        "staffing_select_overall"
                    ])
                )

                """
                Pull out units/areas/roles for filtering/selection
                """

                units_for_units = sorted(
                    units_df.select("unit")
                    .filter(pl.col("unit").is_not_null())
                    .unique()
                    .to_series()
                    .to_list()
                )

                areas_roles_for_unit = sorted(
                    units_df.select("area_role")
                    .filter(pl.col("area_role").is_not_null())
                    .unique()
                    .to_series()
                    .to_list()
                )

                self.units_areas_roles_for_units = units_for_units + areas_roles_for_unit

                # logger.debug("Units Dataframe")
                # logger.debug(units_df.head())
                # logger.debug(units_df.to_dicts())

                """
                Averages scores by unit for view in the units section.
                """

                scored_unit_df = (
                    units_df
                    .with_columns([
                        pl.col("comp_select_overall").map_elements(self.letter_to_number, pl.Int8).alias("comp_numeric"),
                        pl.col("assign_select_overall").map_elements(self.letter_to_number, pl.Int8).alias("assign_numeric"),
                        pl.col("staffing_select_overall").map_elements(self.letter_to_number, pl.Int8).alias("staffing_numeric")
                    ])
                    .filter(pl.col("unit").is_not_null())
                    .group_by("unit")
                    .agg([
                        pl.col("comp_numeric").mean().map_elements(self.number_to_letter, pl.Utf8).alias("comp_mean"),
                        pl.col("assign_numeric").mean().map_elements(self.number_to_letter, pl.Utf8).alias("assign_mean"),
                        pl.col("staffing_numeric").mean().map_elements(self.number_to_letter, pl.Utf8).alias("staffing_mean")
                    ])
                )

                # logger.debug("Scored Unit Averages")
                # logger.debug(scored_unit_df.head())
                # logger.debug(scored_unit_df.to_dicts())

                scored_area_role_df = (
                    units_df
                    .with_columns([
                        pl.col("comp_select_overall").map_elements(self.letter_to_number, pl.Int8).alias("comp_numeric"),
                        pl.col("assign_select_overall").map_elements(self.letter_to_number, pl.Int8).alias("assign_numeric"),
                        pl.col("staffing_select_overall").map_elements(self.letter_to_number, pl.Int8).alias("staffing_numeric")
                    ])
                    .filter(pl.col("area_role").is_not_null())
                    .group_by("area_role")
                    .agg([
                        pl.col("comp_numeric").mean().map_elements(self.number_to_letter, pl.Utf8).alias("comp_mean"),
                        pl.col("assign_numeric").mean().map_elements(self.number_to_letter, pl.Utf8).alias("assign_mean"),
                        pl.col("staffing_select_overall").mean().map_elements(self.number_to_letter, pl.Utf8).alias("staffing_mean")
                    ])
                )
                # logger.debug("Scored Area/Role Averages")
                # logger.debug(scored_area_role_df.head())
                # logger.debug(scored_area_role_df.to_dicts())

                scored_hospital_df = (
                    units_df
                    .with_columns([
                        pl.col("comp_select_overall").map_elements(self.letter_to_number, pl.Int8).alias("comp_numeric"),
                        pl.col("assign_select_overall").map_elements(self.letter_to_number, pl.Int8).alias("assign_numeric"),
                        pl.col("staffing_select_overall").map_elements(self.letter_to_number, pl.Int8).alias("staffing_numeric"),
                    ])
                    .select([
                        pl.lit("Hospital").alias("unit"),
                        pl.col("comp_numeric").mean().map_elements(self.number_to_letter, pl.Utf8).alias("hospital_comp_mean"),
                        pl.col("assign_numeric").mean().map_elements(self.number_to_letter, pl.Utf8).alias("hospital_assign_mean"),
                        pl.col("staffing_numeric").mean().map_elements(self.number_to_letter, pl.Utf8).alias("hospital_staffing_mean"),
                        (
                            ((pl.col("comp_numeric").mean() + pl.col("assign_numeric").mean() + pl.col("staffing_numeric").mean()) / 3)
                            .map_elements(self.number_to_letter, pl.Utf8).alias("hospital_overall_mean")
                        )
                    ])
                )
                
                # logger.debug("Hospital Averages")
                # logger.debug(scored_hospital_df.head())
                # logger.debug(scored_hospital_df.to_dicts())

                # scored_df = pl.concat([
                #     scored_unit_df, scored_area_role_df
                # ])
                # self.scored_units_areas_roles = scored_df.to_dicts
                # logger.debug(self.scored_units_areas_roles)

        except Exception as e:
            logger.critical(e)

    def event_state_load_review_info(self) -> Iterable[Callable]:
        """
        If reports are present, load a dataframe for relevant values. Perform
        dataframe methods to populate and add columns we need for various review
        features. Also strip out reports that don't contain review info.
        """
        try:
            if self.report_info:

                review_df = (
                    pl.DataFrame(self.report_info.copy())
                    .select([
                        "user_id",
                        "report_id",
                        "created_at",
                        "likes",
                        "assign_select_specific_unit",
                        "assign_select_unit",
                        "assign_input_unit_name",
                        "assign_select_area",
                        "assign_input_area",
                        "comp_input_comments",
                        "assign_input_comments",
                        "staffing_input_comments"
                    ])
                    .with_columns(
                        # "Number of likes a post has"
                        pl.col("likes").list.len().alias("likes_number"),

                        # "If current user has liked the review"
                        pl.col("likes").list.contains(self.user_info["user_id"]).alias("user_has_liked"),

                        # "Formatted date from timestamp string"
                        pl.col("created_at").str.to_datetime("%Y-%m-%dT%H:%M:%S%.f%z")
                            .dt.strftime("%B %Y")
                            .alias("formatted_created_at"),

                        # "Coalese unit down to single column"
                        pl.when(
                            pl.col("assign_select_specific_unit").str.contains("Yes")
                        )
                        .then(
                            pl.coalesce(
                                pl.col("assign_select_unit"),
                                pl.col("assign_input_unit_name")
                            )
                        )
                        .otherwise(None)
                        .alias("unit"),

                        # "Coalesce area_role down to single column"
                        pl.when(
                            pl.col("assign_select_specific_unit").str.contains("No")
                        )
                        .then(
                            pl.coalesce(
                                pl.col("assign_select_area"),
                                pl.col("assign_input_area")
                            )
                        )
                        .otherwise(None)
                        .alias("area_role"),

                        # Replace empty strings with None
                        pl.when(
                            (pl.col("comp_input_comments").str.len_chars() == 0)
                        )
                        .then(None)
                        .otherwise(pl.col("comp_input_comments"))
                        .alias("comp_input_comments"),

                        pl.when(
                            (pl.col("assign_input_comments").str.len_chars() == 0)
                        )
                        .then(None)
                        .otherwise(pl.col("assign_input_comments"))
                        .alias("assign_input_comments"),

                        pl.when(
                            (pl.col("staffing_input_comments").str.len_chars() == 0)
                        )
                        .then(None)
                        .otherwise(pl.col("staffing_input_comments"))
                        .alias("staffing_input_comments")

                    )
                    .filter(
                        (pl.col("comp_input_comments").is_not_null()) |
                        (pl.col("assign_input_comments").is_not_null()) |
                        (pl.col("staffing_input_comments").is_not_null())
                    )
                )

                """
                Set the state units/areas/roles to use for dropdowns in review section.
                """

                units_for_reviews = sorted(
                    review_df.select("unit")
                    .filter(pl.col("unit").is_not_null())
                    .unique()
                    .to_series()
                    .to_list()
                )

                areas_roles_for_reviews = sorted(
                    review_df.select("area_role")
                    .filter(pl.col("area_role").is_not_null())
                    .unique()
                    .to_series()
                    .to_list()
                )

                self.units_areas_roles_for_reviews = units_for_reviews + areas_roles_for_reviews

                """
                Set reviews to state.
                """

                self.review_info = review_df.to_dicts()

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


