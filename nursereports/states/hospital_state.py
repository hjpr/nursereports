import numpy as np
import pandas as pd
import polars as pl
import re
import reflex as rx
import rich

from ..states.user_state import UserState
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


class HospitalState(UserState):
    # Full hospital info.
    hospital_info: dict[str, Any]

    # Full list of reports for hospital.
    report_info: list[dict]

    # Full list of reviews pulled from reports.
    review_info: list[dict]

    # Dicts of pay values extrapolated over experience.
    extrapolated_ft_pay_hospital: dict
    extrapolated_pt_pay_hospital: dict
    extrapolated_ft_pay_state: dict
    extrapolated_pt_pay_state: dict

    # Dicts of averaged contract pay.
    averaged_contract_pay_hospital: dict
    averaged_contract_pay_state: dict
    contract_pay: list[dict]

    # Are there less than 10 reports?
    ft_pay_hospital_info_limited: bool
    pt_pay_hospital_info_limited: bool
    ft_pay_state_info_limited: bool
    pt_pay_state_info_limited: bool
    contract_pay_info_hospital_limited: bool
    contract_pay_info_state_limited: bool

    # Units/areas/roles pulled from reports.
    units_areas_roles_for_units: list[str]
    units_areas_roles_hospital_scores: list[dict]
    units_areas_roles_for_reviews: list[str]
    units_areas_roles_for_rankings: pd.DataFrame

    # User selectable fields
    selected_unit: str
    selected_pay_tab: str = "staff"
    selected_experience: int = 4
    selected_hospital_average: str = "Full-time"
    selected_state_average: str = "Full-time"
    review_filter_units_areas_roles: str
    review_sorted: str = "Most Recent"

    @rx.var(cache=True)
    def has_report_info(self) -> bool:
        return True if len(self.report_info) > 0 else False

    @rx.var(cache=True)
    def hosp_id(self) -> str | None:
        """
        Returns hosp_id if page param hosp_id is a valid CMS ID format.
        """
        # Get the CMS ID from the URL.
        hosp_id = self.router.page.params.get("cms_id")
        cms_is_valid = False

        # Check if CMS ID appears to be in valid format.
        if hosp_id:
            cms_is_valid = bool(re.match(r"^[a-zA-Z0-9]{5,6}$", hosp_id))
        return hosp_id if cms_is_valid else None

    @rx.var(cache=True)
    def ft_pay_hospital_formatted(self) -> dict:
        """
        Round and format extrapolated full-time hospital pay data to $XX.XX
        """
        if self.extrapolated_ft_pay_hospital:
            rounded_hourly = round(
                self.extrapolated_ft_pay_hospital.get(self.selected_experience), 2
            )
            formatted_hourly = "{:.2f}".format(rounded_hourly)
            rounded_yearly = round(rounded_hourly * 36 * 52)
            formatted_yearly = "{:,}".format(rounded_yearly)
            return {
                "hourly": f"${formatted_hourly}",
                "yearly": f"${formatted_yearly}",
            }
        else:
            return {}

    @rx.var(cache=True)
    def ft_pay_state_formatted(self) -> dict:
        """
        Round and format extrapolated full-time state hospital pay data to $XX.XX
        """
        if self.extrapolated_ft_pay_state:
            rounded_hourly = round(
                self.extrapolated_ft_pay_state.get(self.selected_experience), 2
            )
            formatted_hourly = "{:.2f}".format(rounded_hourly)
            rounded_yearly = round(rounded_hourly * 36 * 52)
            formatted_yearly = "{:,}".format(rounded_yearly)
            return {
                "hourly": f"${formatted_hourly}",
                "yearly": f"${formatted_yearly}",
            }
        else:
            return {}

    @rx.var(cache=True)
    def pt_pay_hospital_formatted(self) -> dict:
        """
        Round and format extrapolated part-time hospital pay data to $XX.XX
        """
        if self.extrapolated_pt_pay_hospital:
            rounded_hourly = round(
                self.extrapolated_pt_pay_hospital.get(self.selected_experience), 2
            )
            formatted_hourly = "{:.2f}".format(rounded_hourly)
            rounded_yearly = round(rounded_hourly * 36 * 52)
            formatted_yearly = "{:,}".format(rounded_yearly)
            return {
                "hourly": f"${formatted_hourly}",
                "yearly": f"${formatted_yearly}",
            }
        else:
            return {}

    @rx.var(cache=True)
    def pt_pay_state_formatted(self) -> dict:
        """
        Round and format extrapolated part-time state pay data to $XX.XX
        """
        if self.extrapolated_ft_pay_state:
            rounded_hourly = round(
                self.extrapolated_ft_pay_state.get(self.selected_experience), 2
            )
            formatted_hourly = "{:.2f}".format(rounded_hourly)
            rounded_yearly = round(rounded_hourly * 36 * 52)
            formatted_yearly = "{:,}".format(rounded_yearly)
            return {
                "hourly": f"${formatted_hourly}",
                "yearly": f"${formatted_yearly}",
            }
        else:
            return {}


    @rx.var(cache=True)
    def filtered_unit_info(self) -> dict[str, str]:
        """
        Used to display all units if no filters are selected, or filtered units if
        user has selected filters.
        """
        # Iterate to retrieve matched selection.
        for score_dict in self.units_areas_roles_hospital_scores:
            if score_dict["units_areas_roles"] == self.selected_unit:
                return score_dict
            
        # If no match user hasn't filtered so retrieve hospital overall.
        for score_dict in self.units_areas_roles_hospital_scores:
            if score_dict["units_areas_roles"] == "hospital":
                return score_dict

    @rx.var(cache=True)
    def filtered_review_info(self) -> list[dict]:
        """
        Used to display all reviews if no filters are selected, or filtered reviews
        if user has selected filters.
        """
        # Load all reviews to show if no filters selected.
        filtered_review_items = self.review_info

        # Populate filtered_review_items with unit and area_role present.
        if self.review_filter_units_areas_roles and self.review_info:
            filtered_review_items = [
                review
                for review in self.review_info
                if self.review_filter_units_areas_roles == review.get("unit", "")
                or self.review_filter_units_areas_roles == review.get("area_role", "")
            ]

        # Filter for "Most Recent" and/or "Most Helpful" if user has selected filters.
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
        """
        Convert stored letter grades to numbers.
        """
        return {"a": 4, "b": 3, "c": 2, "d": 1, "f": 0}.get(letter)

    @staticmethod
    def number_to_letter(number: int | float) -> str:
        """
        Convert number grades back to formatted letter grades for display.
        """
        return {4: "A", 3: "B", 2: "C", 1: "D", 0: "F"}.get(round(number))

    def set_slider(self, value) -> None:
        self.selected_experience = value[0]

    def event_state_load_hospital_info(self) -> Iterable[Callable]:
        """
        Load hospital data into state from supabase.
        """
        try:
            # Reset all our hospital state variables for a clean slate.
            self.reset()

            # As long as CMS ID appears to be valid, try to get hospital info.
            if self.hosp_id:
                self.hospital_info = supabase_get_hospital_overview_info(
                    self.access_token, self.hosp_id
                )

            # Otherwise send user back to dashboard.
            else:
                yield rx.redirect("/dashboard")

        except RequestFailed as e:
            logger.error(e)
            yield rx.toast.error("Failed to retrieve report data from backend.")
        except Exception as e:
            logger.error(e)
            yield rx.toast.error("Unexpected behavior while loading hospital info.")

    def event_state_load_report_info(self) -> Iterable[Callable]:
        """
        Load report data into state from supabase.
        """
        try:
            self.report_info = supabase_get_hospital_report_data(
                self.access_token, self.hosp_id
            )
        except RequestFailed as e:
            logger.critical(e)
            yield rx.toast.error("Failed to retrieve review data from backend.")
        except Exception as e:
            logger.error(e)
            yield rx.toast.error("Unexpected behavior while loading report info.")
        

    def event_state_load_pay_info(self) -> Iterable[Callable]:
        """
        Pulls pay data out of report_info and processes data to partition into
        user digestible chunks for display.
        """
        try:
            if self.report_info:
                # Copy reports into a dataframe.
                pay_df = pl.DataFrame(self.report_info.copy())

                # Full time hospital pay data and interpolation.
                ft_pay_hospital_df = pay_df.filter(
                    pl.col("comp_select_emp_type") == "Full-time"
                ).select(["comp_input_pay_amount", "comp_select_total_experience"])
                ft_pay_hospital_df = ft_pay_hospital_df.with_columns(
                    pl.col("comp_select_total_experience")
                    .cast(pl.Int8, strict=False)
                    .fill_null(26)
                ).sort(by=pl.col("comp_select_total_experience"))
                ft_pay = ft_pay_hospital_df.to_dicts()

                # Check if more than 10 full-time hospital pay reports.
                self.ft_pay_hospital_info_limited = bool(len(ft_pay) < 10)

                # Extrapolate full-time hospital pay data to dict of values against experience.
                if ft_pay:
                    x = ft_pay_hospital_df["comp_select_total_experience"].to_numpy()
                    y = ft_pay_hospital_df["comp_input_pay_amount"].to_numpy()
                    f = interpolate.interp1d(
                        x, y, kind="quadratic", fill_value="extrapolate"
                    )
                    x_extrapolated = np.arange(0, 27)
                    y_extrapolated = f(x_extrapolated)
                    filtered_ft_pay_hospital_df = pl.DataFrame(
                        {
                            "years_experience": x_extrapolated,
                            "interpolated_pay": y_extrapolated,
                        }
                    )
                    extrapolated_ft_pay_hospital = (
                        filtered_ft_pay_hospital_df.to_dicts()
                    )
                    self.extrapolated_ft_pay_hospital = {
                        item["years_experience"]: item["interpolated_pay"]
                        for item in extrapolated_ft_pay_hospital
                    }

                # Part time pay data and interpolation.
                pt_pay_df = pay_df.filter(
                    pl.col("comp_select_emp_type") == "Part-time"
                ).select(["comp_input_pay_amount", "comp_select_total_experience"])
                pt_pay_df = pt_pay_df.with_columns(
                    pl.col("comp_select_total_experience")
                    .cast(pl.Int8, strict=False)
                    .fill_null(26)
                )
                pt_pay = pt_pay_df.to_dicts()

                # Check if more than 10 part-time hospital pay reports.
                self.pt_pay_hospital_info_limited = bool(len(pt_pay) < 10)

                # Extrapolate part-time hospital pay data to dict of values against experience.
                if pt_pay:
                    x = pt_pay_df["comp_select_total_experience"].to_numpy()
                    y = pt_pay_df["comp_input_pay_amount"].to_numpy()
                    f = interpolate.interp1d(
                        x, y, kind="quadratic", fill_value="extrapolate"
                    )
                    x_extrapolated = np.arange(0, 27)
                    y_extrapolated = f(x_extrapolated)
                    filtered_pt_df = pl.DataFrame(
                        {
                            "years_experience": x_extrapolated,
                            "interpolated_pay": y_extrapolated,
                        }
                    )
                    extrapolated_pt_pay_hospital = filtered_pt_df.to_dict()
                    self.extrapolated_pt_pay_hospital = {
                        item["years_experience"]: item["interpolated_pay"]
                        for item in extrapolated_pt_pay_hospital
                    }

                # Contract pay data and averaged pay.
                contract_pay_df = pay_df.filter(
                    pl.col("comp_select_emp_type") == "Contract"
                ).select(["comp_input_pay_amount", "created_at"])
                contract_pay = contract_pay_df.to_dicts()

                # Check if more than 10 contract pay reports.
                self.contract_pay_info_hospital_limited = bool(len(contract_pay) < 10)

                # Average contract pay data.
                if contract_pay:
                    averaged_contract_pay_df = contract_pay_df.select(
                        pl.col("comp_input_pay_amount")
                        .mean()
                        .alias("average_contract_pay")
                    )
                    self.averaged_contract_pay_hospital = (
                        averaged_contract_pay_df.to_dict()
                    )

        except Exception as e:
            logger.critical(e)

    def event_state_load_unit_info(self) -> Iterable[Callable]:
        try:

            if self.report_info:

                # Create full dataframe and format.
                units_df = (
                    pl.DataFrame(self.report_info.copy())
                    .with_columns(
                        pl.when(
                            pl.col("assign_select_specific_unit").str.contains("Yes")
                        )
                        .then(
                            pl.coalesce(
                                pl.col("assign_select_unit"),
                                pl.col("assign_input_unit_name"),
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
                                pl.col("assign_input_area"),
                            )
                        )
                        .otherwise(None)
                        .alias("area_role"),
                    )
                    .select(
                        [
                            "unit",
                            "area_role",
                            "comp_select_overall",
                            "assign_select_overall",
                            "staffing_select_overall",
                        ]
                    )
                )

                # Get list of units/roles for filters.
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
                self.units_areas_roles_for_units = (
                    units_for_units + areas_roles_for_unit
                )

                # Average scores for respective units.
                unit_score_df = (
                    units_df.with_columns(
                        [
                            pl.col("comp_select_overall")
                            .map_elements(self.letter_to_number, pl.Int8)
                            .alias("comp_numeric"),
                            pl.col("assign_select_overall")
                            .map_elements(self.letter_to_number, pl.Int8)
                            .alias("assign_numeric"),
                            pl.col("staffing_select_overall")
                            .map_elements(self.letter_to_number, pl.Int8)
                            .alias("staffing_numeric"),
                        ]
                    )
                    .with_columns(
                        pl.mean_horizontal("comp_numeric", "assign_numeric", "staffing_numeric")
                        .alias("overall_numeric")
                    )
                    .filter(
                        pl.col("unit").is_not_null()
                    )
                    .group_by("unit")
                    .agg(
                        [
                            pl.col("comp_numeric")
                            .mean()
                            .map_elements(self.number_to_letter, pl.Utf8)
                            .alias("comp_mean"),
                            pl.col("assign_numeric")
                            .mean()
                            .map_elements(self.number_to_letter, pl.Utf8)
                            .alias("assign_mean"),
                            pl.col("staffing_numeric")
                            .mean()
                            .map_elements(self.number_to_letter, pl.Utf8)
                            .alias("staffing_mean"),
                            pl.col("overall_numeric")
                            .mean()
                            .map_elements(self.number_to_letter, pl.Utf8)
                            .alias("overall_mean")
                        ]
                    )
                )

                # Average scores with respect to roles.
                area_role_score_df = (
                    units_df.with_columns(
                        [
                            pl.col("comp_select_overall")
                            .map_elements(self.letter_to_number, pl.Int8)
                            .alias("comp_numeric"),
                            pl.col("assign_select_overall")
                            .map_elements(self.letter_to_number, pl.Int8)
                            .alias("assign_numeric"),
                            pl.col("staffing_select_overall")
                            .map_elements(self.letter_to_number, pl.Int8)
                            .alias("staffing_numeric"),
                        ]
                    )
                    .with_columns(
                        pl.mean_horizontal("comp_numeric", "assign_numeric", "staffing_numeric")
                        .alias("overall_numeric")
                    )
                    .filter(
                        pl.col("area_role").is_not_null()
                    )
                    .group_by("area_role")
                    .agg(
                        [
                            pl.col("comp_numeric")
                            .mean()
                            .map_elements(self.number_to_letter, pl.Utf8)
                            .alias("comp_mean"),
                            pl.col("assign_numeric")
                            .mean()
                            .map_elements(self.number_to_letter, pl.Utf8)
                            .alias("assign_mean"),
                            pl.col("staffing_numeric")
                            .mean()
                            .map_elements(self.number_to_letter, pl.Utf8)
                            .alias("staffing_mean"),
                            pl.col("overall_numeric")
                            .mean()
                            .map_elements(self.number_to_letter, pl.Utf8)
                            .alias("overall_mean")
                        ]
                    )
                )

                # Create an overall hospital score from all units/roles
                hospital_score_df = (
                    units_df.with_columns(
                        [
                            pl.col("comp_select_overall")
                            .map_elements(self.letter_to_number, pl.Int8)
                            .alias("comp_numeric"),
                            pl.col("assign_select_overall")
                            .map_elements(self.letter_to_number, pl.Int8)
                            .alias("assign_numeric"),
                            pl.col("staffing_select_overall")
                            .map_elements(self.letter_to_number, pl.Int8)
                            .alias("staffing_numeric"),
                        ]
                    )
                    .with_columns(
                        pl.mean_horizontal("comp_numeric", "assign_numeric", "staffing_numeric")
                        .alias("overall_numeric")
                    )
                    .select(
                        [
                            pl.lit("hospital").alias("unit"),
                            pl.col("comp_numeric")
                            .mean()
                            .map_elements(self.number_to_letter, pl.Utf8)
                            .alias("comp_mean"),
                            pl.col("assign_numeric")
                            .mean()
                            .map_elements(self.number_to_letter, pl.Utf8)
                            .alias("assign_mean"),
                            pl.col("staffing_numeric")
                            .mean()
                            .map_elements(self.number_to_letter, pl.Utf8)
                            .alias("staffing_mean"),
                            pl.col("overall_numeric")
                            .mean()
                            .map_elements(self.number_to_letter, pl.Utf8)
                            .alias("overall_mean")
                        ]
                    )
                )

                # Combine and save to state
                unit_score_df = unit_score_df.rename({"unit": "units_areas_roles"})
                area_role_score_df = area_role_score_df.rename({"area_role": "units_areas_roles"})
                hospital_score_df = hospital_score_df.rename({"unit": "units_areas_roles"})
                units_areas_roles_df = pl.concat([unit_score_df, area_role_score_df, hospital_score_df], how="vertical")
                self.units_areas_roles_hospital_scores = units_areas_roles_df.to_dicts()

                # Pull dataframe for unit/role rankings.
                rankings_df = pl.concat([unit_score_df, area_role_score_df], how="vertical")
                self.units_areas_roles_for_rankings = rankings_df.to_pandas()

        except Exception as e:
            logger.critical(e)


    def event_state_load_review_info(self) -> Iterable[Callable]:
        try:
            if self.report_info:
                review_df = (
                    pl.DataFrame(self.report_info.copy())
                    .select(
                        [
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
                            "staffing_input_comments",
                        ]
                    )
                    .with_columns(
                        pl.col("likes").list.len().alias("likes_number"),
                        pl.col("likes")
                        .list.contains(self.user_info["user_id"])
                        .alias("user_has_liked"),
                        pl.col("created_at")
                        .str.to_datetime("%Y-%m-%dT%H:%M:%S%.f%z")
                        .dt.strftime("%B %Y")
                        .alias("formatted_created_at"),

                        pl.when(
                            pl.col("assign_select_specific_unit").str.contains("Yes")
                        )
                        .then(
                            pl.coalesce(
                                pl.col("assign_select_unit"),
                                pl.col("assign_input_unit_name"),
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
                                pl.col("assign_input_area"),
                            )
                        )
                        .otherwise(None)
                        .alias("area_role"),

                        pl.when((pl.col("comp_input_comments").str.len_chars() == 0))
                        .then(None)
                        .otherwise(pl.col("comp_input_comments"))
                        .alias("comp_input_comments"),
                        pl.when((pl.col("assign_input_comments").str.len_chars() == 0))
                        .then(None)
                        .otherwise(pl.col("assign_input_comments"))
                        .alias("assign_input_comments"),
                        pl.when(
                            (pl.col("staffing_input_comments").str.len_chars() == 0)
                        )
                        .then(None)
                        .otherwise(pl.col("staffing_input_comments"))
                        .alias("staffing_input_comments"),
                    )
                    .filter(
                        (pl.col("comp_input_comments").is_not_null())
                        | (pl.col("assign_input_comments").is_not_null())
                        | (pl.col("staffing_input_comments").is_not_null())
                    )
                )

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

                self.units_areas_roles_for_reviews = (
                    units_for_reviews + areas_roles_for_reviews
                )

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

    def redirect_to_hospital_overview(self, hosp_id: str) -> Iterable[Callable]:
        return rx.redirect(f"/hospital/{hosp_id}")
