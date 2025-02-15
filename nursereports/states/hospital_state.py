import numpy as np
import polars as pl
import re
import reflex as rx

from ..client.components.dicts import abbr_to_state_dict
from ..states.user_state import UserState
from ..server.supabase.hospital_requests import (
    supabase_get_hospital_overview_info,
    supabase_get_hospital_report_data,
)
from ..server.supabase.report_requests import supabase_admin_edit_report
from ..server.exceptions import RequestFailed

from datetime import datetime
from loguru import logger
from typing import Any, Callable, Iterable

import copy
import humanize
import math
import rich
import pprint
import traceback


class HospitalState(UserState):

    MAX_REVIEWS_DISPLAYED = 10

    # Full info for each section.
    hospital_info: dict[str, Any]
    report_info: list[dict]
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
    overall_hospital_scores: dict

    # User selectable fields.
    selected_unit: str = "Hospital Overall"
    selected_experience: int = 4
    selected_hospital_average: str = "Full-time"
    selected_state_average: str = "Full-time"

    # Pagination for sections.
    current_review_page: int = 1

    @rx.var
    def has_report_info(self) -> bool:
        return True if len(self.report_info) > 0 else False

    @rx.var
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

    @rx.var
    def ft_pay_hospital_formatted(self) -> dict:
        """
        Round and format extrapolated full-time hospital pay data to $XX.XX
        """
        if self.extrapolated_ft_pay_hospital:
            hourly = self.extrapolated_ft_pay_hospital.get(self.selected_experience)
            formatted_hourly = "{:.2f}".format(hourly)
            rounded_yearly = round(hourly * 36 * 52)
            formatted_yearly = "{:,}".format(rounded_yearly)
            return {
                "hourly": f"${formatted_hourly}",
                "yearly": f"${formatted_yearly}",
            }
        else:
            return {}

    @rx.var
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

    @rx.var
    def pt_pay_hospital_formatted(self) -> dict:
        """
        Round and format extrapolated part-time hospital pay data to $XX.XX
        """
        if self.extrapolated_pt_pay_hospital:
            hourly = self.extrapolated_pt_pay_hospital.get(self.selected_experience)
            formatted_hourly = "{:.2f}".format(hourly)
            rounded_yearly = round(hourly * 36 * 52)
            formatted_yearly = "{:,}".format(rounded_yearly)
            return {
                "hourly": f"${formatted_hourly}",
                "yearly": f"${formatted_yearly}",
            }
        else:
            return {}

    @rx.var
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

    @rx.var
    def selected_unit_info(self) -> dict[str, str]:
        """
        If user has a unit selected in the unit grades section, show scores
        for that unit. Hospital scores are stored as list of dicts, overall score
        is simply a dict that we can return.
        """
        # Iterate to retrieve matched selection.
        matched_dict = next(
            (
                d
                for d in self.units_areas_roles_hospital_scores
                if d.get("units_areas_roles") == self.selected_unit
            ),
            None
        )

        # Otherwise if no matches, user hasn't selected anything and we return hospital overall.
        return matched_dict if matched_dict else self.overall_hospital_scores

    @rx.var
    def filtered_review_info(self) -> list[dict]:
        """
        Used to display all reviews if no filters are selected, or filtered reviews
        if user has selected filters.
        """
        matched_list = [review for review in self.review_info if review.get("units_areas_roles", "") == self.selected_unit]

        # If reviews, sort by time submitted.
        if matched_list:
            matched_list = sorted(
                matched_list,
                key=lambda review: datetime.fromisoformat(review["timestamp"]),
                reverse=True,
            )

        return matched_list if matched_list else self.review_info

    @rx.var
    def paginated_review_info(self) -> list[dict]:
        """
        Takes the filtered review info and paginates into a dict where user can
        flip between sets of reviews. If there aren't enough reviews to paginate,
        then return a dict with reviews under page 1.
        """
        if len(self.filtered_review_info) > self.MAX_REVIEWS_DISPLAYED:
            # Determine number of pages.
            num_pages = math.ceil(len(self.filtered_review_info) / self.MAX_REVIEWS_DISPLAYED)
            num_pages_list = [page for page in range(1, (num_pages + 1))]

            # Build dict.
            paginated_reports = { number: [] for number in num_pages_list}

            # Fill dict.
            current_page = 1
            for review in self.filtered_review_info:
                if len(paginated_reports[current_page]) >= self.MAX_REVIEWS_DISPLAYED:
                    current_page += 1
                paginated_reports[current_page].append(review)

            return paginated_reports.get(self.current_review_page)

        else:
            return self.filtered_review_info

    @rx.var
    def num_review_pages(self) -> int:
        num_pages = math.ceil(len(self.filtered_review_info) / self.MAX_REVIEWS_DISPLAYED)
        return num_pages

    def next_review_page(self) -> None:
        num_pages = math.ceil(len(self.filtered_review_info) / self.MAX_REVIEWS_DISPLAYED)
        if self.current_review_page < num_pages:
            self.current_review_page += 1

    def previous_review_page(self) -> None:
        if self.current_review_page > 1:
            self.current_review_page -= 1

    def set_slider(self, value) -> None:
        self.selected_experience = value[0]

    def event_state_load_hospital_info(self) -> Callable | None:
        """
        Load hospital data into state from supabase.
        """
        try:
            # If user is opening hospital info already loaded, skip load.
            if self.hospital_info:
                if self.hospital_info["hosp_id"] != self.hosp_id:
                    self.reset()
                else:
                    self.selected_hospital_average = "Full-time"
                    self.selected_state_average = "Full-time"
                    self.selected_experience = 4
                    self.selected_unit = "Hospital Overall"
                    return

            # As long as CMS ID appears to be valid, try to get hospital info.
            if self.hosp_id:
                self.hospital_info = supabase_get_hospital_overview_info(
                    self.access_token, self.hosp_id
                )
                self.hospital_info["hosp_state_abbr"] = self.hospital_info["hosp_state"]
                self.hospital_info["hosp_state"] = abbr_to_state_dict.get(
                    self.hospital_info["hosp_state_abbr"]
                )
                self.load_report_info()
                self.load_pay_info()
                self.load_unit_info()
                self.load_review_info()

            # Otherwise send user back to dashboard.
            else:
                return rx.redirect("/dashboard")

        except RequestFailed as e:
            logger.error(e)
            return rx.toast.error("Failed to retrieve data from backend.")
        except Exception as e:
            logger.error(e)
            return rx.toast.error("Error while loading hospital info.")

    def load_report_info(self) -> None:
        """
        Load report data into state from supabase.
        """
        self.report_info = supabase_get_hospital_report_data(
            self.access_token, self.hosp_id
        )

    def load_pay_info(self) -> None:
        """
        Pulls pay data out of report_info and processes data to partition into
        user digestible chunks for display.
        """
        try:
            if self.report_info:
                # Copy reports into a dataframe.
                pay_df = pl.DataFrame(copy.deepcopy(self.report_info))

                # Create our full time pay dictionary with columns hourly and total.
                ft_pay_hospital_df = (
                    pay_df.filter(
                        pl.col("compensation").struct.field("emp_type") == "Full-time"
                    )
                    .select(
                        [
                            pl.col("compensation")
                            .struct.field("pay")
                            .struct.field("hourly"),
                            pl.col("compensation")
                            .struct.field("experience")
                            .struct.field("total"),
                        ]
                    )
                    .sort(by=pl.col("total"))
                )

                # Remove outliers.
                ft_pay_hospital_df = self.remove_pay_outliers(
                    ft_pay_hospital_df, "hourly"
                )

                # Flatten entries for years into an average.
                ft_pay_hospital_df = self.flatten_pay(
                    ft_pay_hospital_df, "total", "hourly"
                )

                # Set full time pay limited flag if less than 10 reports.
                self.ft_pay_hospital_info_limited = bool(len(ft_pay_hospital_df) < 10)

                # Quadratic interpolation as long as we have more than 2 reports.
                self.extrapolated_ft_pay_hospital = self.linear_regression_pay(
                    ft_pay_hospital_df, "total", "hourly"
                )
                logger.debug(f"Pulled {len(ft_pay_hospital_df)} full time report(s).")

                # Part time pay data and interpolation.
                pt_pay_hospital_df = (
                    pay_df.filter(
                        pl.col("compensation").struct.field("emp_type") == "Part-time"
                    )
                    .select(
                        [
                            pl.col("compensation")
                            .struct.field("pay")
                            .struct.field("hourly"),
                            pl.col("compensation")
                            .struct.field("experience")
                            .struct.field("total"),
                        ]
                    )
                    .sort(by=pl.col("total"))
                )

                # Remove outliers.
                pt_pay_hospital_df = self.remove_pay_outliers(
                    pt_pay_hospital_df, "hourly"
                )

                # Flatten entries for years into an average.
                pt_pay_hospital_df = self.flatten_pay(
                    pt_pay_hospital_df, "total", "hourly"
                )

                # Set part time pay limited flag if less than 10 reports.
                self.pt_pay_hospital_info_limited = bool(len(pt_pay_hospital_df) < 10)

                # Perform our linear regression.
                self.extrapolated_pt_pay_hospital = self.linear_regression_pay(
                    pt_pay_hospital_df, "total", "hourly"
                )
                logger.debug(f"Pulled {len(pt_pay_hospital_df)} part time report(s).")

                # Contract pay data and averaged pay.
                contract_pay_df = (
                    pay_df.filter(
                        pl.col("compensation").struct.field("emp_type") == "Contract"
                    )
                    .select(
                        [
                            pl.col("compensation")
                            .struct.field("pay")
                            .struct.field("weekly"),
                            pl.col("created_at"),
                        ]
                    )
                    .sort(by=pl.col("created_at"))
                )

                # Check if more than 10 contract pay reports.
                self.contract_pay_info_hospital_limited = bool(
                    len(contract_pay_df) < 10
                )

                # Average contract pay data.
                if len(contract_pay_df) > 0:
                    self.simple_average_pay(contract_pay_df, "weekly")
                    logger.debug(
                        f"Pulled {len(contract_pay_df)} contract report(s) and averaged them."
                    )
                else:
                    logger.debug(
                        "No contract pay data present to be loaded to state..."
                    )

        except Exception as e:
            traceback.print_exc()
            logger.critical(e)

    @staticmethod
    def remove_pay_outliers(
        df_to_clean: pl.DataFrame, y_name: str, multiplier: float = 2
    ) -> pl.DataFrame:
        """
        Removes outliers from DataFrame. Requires at least 4 entries.
        """
        if len(df_to_clean) < 4:
            logger.debug("Not enough entries to remove outliers.")
            return df_to_clean

        y_values = df_to_clean[y_name].to_numpy()

        # Calc Q1 and Q3 (25th % and 75th %).
        Q1 = np.percentile(y_values, 25)
        Q3 = np.percentile(y_values, 75)

        # Calc IQR.
        IQR = Q3 - Q1

        # Calc outlier thresholds.
        lower_bound = Q1 - (multiplier * IQR)
        upper_bound = Q3 + (multiplier * IQR)

        # Filter rows outside of our lower and upper bounds.
        filtered_df = df_to_clean.filter(
            (df_to_clean[y_name] >= lower_bound) & (df_to_clean[y_name] <= upper_bound)
        )
        logger.debug(
            f"Dropped {len(df_to_clean) - len(filtered_df)} report(s) as outliers."
        )
        return filtered_df

    @staticmethod
    def flatten_pay(
        df_to_flatten: pl.DataFrame, x_name: str, y_name: str
    ) -> pl.DataFrame:
        """
        Can't interpolate duplicate years ex. [{4, 5, 5}, {41, 37, 87}]. Averages duplicate
        entries eg. [{4, 5}{41, 80.5}]
        """
        x = df_to_flatten[x_name].to_numpy()
        y = df_to_flatten[y_name].to_numpy()

        unique_x = np.unique(x)
        averaged_y = [np.mean(y[x == val]) for val in unique_x]

        flattened_df = pl.DataFrame({x_name: unique_x, y_name: averaged_y})
        logger.debug(
            f"Flattened by {df_to_flatten.height - flattened_df.height} report(s)."
        )
        return flattened_df

    @staticmethod
    def simple_average_pay(pay_df: pl.DataFrame, y_name: str) -> dict:
        """
        Takes a pay dataframe with years on x-axis and pay on y-axis and computes
        the average of those values. Returns a dict where the key is averaged_y_name
        e.g. averaged_hourly / averaged_weekly etc.
        """
        averaged_pay = pay_df.select(
            pl.col(f"{y_name}").mean().alias(f"averaged_{y_name}")
        )
        return averaged_pay.to_dict()

    @staticmethod
    def linear_regression_pay(pay_df: pl.DataFrame, x_name: str, y_name: str) -> dict:
        """
        Returns a dict of values where the key is a range from 0-26 representing
        the years of experience, and the value is the pay as a float rounded to 2
        decimal points. This function can handle dataframes with 1 or 2 pay entries.

        Clamps values to sanity if regression has negative slope or unrealistic
        y-intercept. Mainly should only happen with limited data. Once the dataset for
        pay gets larger, removing outliers should help with sanity.
        """
        MIN_NEW_RN_PAY = 20
        MAX_NEW_RN_PAY = 55
        MIN_PAY_PROGRESSION_SLOPE = 0.5
        MAX_PAY_PROGRESSION_SLOPE = 4

        # Set our axes.
        years = pay_df[f"{x_name}"].to_numpy()  # Years experience.
        pay = pay_df[f"{y_name}"].to_numpy()  # Pay value at each year experience

        # Array to calc for 0-26 years.
        x_range = np.arange(0, 27)

        # Return empty dict for no entries.
        if len(pay_df) == 0:
            return {}

        # If there's only one pay entry, same pay across all experiences.
        if len(pay_df) == 1:
            y_range = np.full_like(x_range, pay[0], dtype=float)

        # If there are two pay entries, compute linear regression.
        elif len(pay_df) > 1:
            m, b = np.polyfit(years, pay, 1)

            # With limited reports, clamp values to avoid really wild regressions.
            if len(pay_df) < 10:
                b = max(MIN_NEW_RN_PAY, min(b, MAX_NEW_RN_PAY))
                m = max(MIN_PAY_PROGRESSION_SLOPE, min(m, MAX_PAY_PROGRESSION_SLOPE))

            # Calc the y from the line function.
            y_range = m * x_range + b

        pay_dict = dict(zip(x_range, y_range))
        final_pay_dict = {
            int(experience): round(float(pay), 2)
            for experience, pay in pay_dict.items()
        }
        return final_pay_dict

    def load_unit_info(self) -> None:
        try:
            if self.report_info:
                # Create full dataframe and format.
                full_df = pl.DataFrame(copy.deepcopy(self.report_info))

                # Create our units dictionary with units/areas/roles extracted.
                refined_df = full_df.select(
                    # Flatten unit/area/role structs to unit/area/role columns as strings.
                    pl.coalesce(
                        [
                            pl.col("assignment").struct.field("unit").struct.field("entered_unit").replace("", None),
                            pl.col("assignment").struct.field("unit").struct.field("selected_unit").replace("", None),
                        ]
                    ).alias("unit"),
                    pl.coalesce(
                        [
                            pl.col("assignment").struct.field("area").struct.field("entered_area").replace("", None),
                            pl.col("assignment").struct.field("area").struct.field("selected_area").replace("", None),
                        ]
                    ).alias("area"),
                    pl.coalesce(
                        [
                            pl.col("assignment").struct.field("role").struct.field("entered_role").replace("", None),
                            pl.col("assignment").struct.field("role").struct.field("selected_role").replace("", None),
                        ]
                    ).alias("role"),
                    pl.col("compensation")
                    .struct.field("ratings")
                    .struct.field("overall")
                    .cast(pl.Int8)
                    .alias("comp_overall"),
                    pl.col("assignment")
                    .struct.field("ratings")
                    .struct.field("overall")
                    .cast(pl.Int8)
                    .alias("assign_overall"),
                    pl.col("staffing")
                    .struct.field("ratings")
                    .struct.field("overall")
                    .cast(pl.Int8)
                    .alias("staff_overall"),
                ).with_columns(
                    pl.mean_horizontal(
                        "comp_overall", "assign_overall", "staff_overall"
                    )
                    .round(0)
                    .cast(pl.Int8)
                    .alias("overall")
                )

                sorted_units = refined_df.select(pl.col("unit")).to_dict()
                sorted_units = sorted(
                    list(unit for unit in set(sorted_units["unit"]) if unit)
                )

                sorted_areas = refined_df.select(pl.col("area")).to_dict()
                sorted_areas = sorted(
                    list(area for area in set(sorted_areas["area"]) if area)
                )

                sorted_roles = refined_df.select(pl.col("role")).to_dict()
                sorted_roles = sorted(
                    list(role for role in set(sorted_roles["role"]) if role)
                )

                self.units_areas_roles_for_units = (
                    ["Hospital Overall"] + sorted_units + sorted_areas + sorted_roles
                )

                # Calc average scores for entire hospital.
                hospital_score_df = full_df.select(
                    pl.lit("HOSPITAL").alias("units_areas_roles"),
                    pl.col("compensation")
                    .struct.field("ratings")
                    .struct.field("overall")
                    .mean()
                    .round()
                    .cast(pl.Int8)
                    .alias("comp_overall"),
                    pl.col("assignment")
                    .struct.field("ratings")
                    .struct.field("overall")
                    .mean()
                    .round()
                    .cast(pl.Int8)
                    .alias("assign_overall"),
                    pl.col("staffing")
                    .struct.field("ratings")
                    .struct.field("overall")
                    .mean()
                    .round()
                    .cast(pl.Int8)
                    .alias("staff_overall"),
                ).with_columns(
                    pl.mean_horizontal(
                        "comp_overall", "assign_overall", "staff_overall"
                    )
                    .round(0)
                    .cast(pl.Int8)
                    .alias("overall")
                )

                unit_score_df = (
                    #
                    refined_df.with_columns(pl.col("unit").replace("", None))
                    .group_by("unit")
                    .agg(
                        pl.col("comp_overall")
                        .mean()
                        .round(0)
                        .cast(pl.Int8)
                        .alias("comp_overall"),
                        pl.col("assign_overall")
                        .mean()
                        .round(0)
                        .cast(pl.Int8)
                        .alias("assign_overall"),
                        pl.col("staff_overall")
                        .mean()
                        .round(0)
                        .cast(pl.Int8)
                        .alias("staff_overall"),
                    )
                    .with_columns(
                        pl.mean_horizontal(
                            "comp_overall", "assign_overall", "staff_overall"
                        )
                        .round(0)
                        .cast(pl.Int8)
                        .alias("overall")
                    )
                    .drop_nulls("unit")
                    .rename({"unit": "units_areas_roles"})
                )

                area_score_df = (
                    refined_df.with_columns(pl.col("area").replace("", None))
                    .group_by("area")
                    .agg(
                        pl.col("comp_overall")
                        .mean()
                        .round(0)
                        .cast(pl.Int8)
                        .alias("comp_overall"),
                        pl.col("assign_overall")
                        .mean()
                        .round(0)
                        .cast(pl.Int8)
                        .alias("assign_overall"),
                        pl.col("staff_overall")
                        .mean()
                        .round(0)
                        .cast(pl.Int8)
                        .alias("staff_overall"),
                    )
                    .with_columns(
                        pl.mean_horizontal(
                            "comp_overall", "assign_overall", "staff_overall"
                        )
                        .round(0)
                        .cast(pl.Int8)
                        .alias("overall")
                    )
                    .drop_nulls("area")
                    .rename({"area": "units_areas_roles"})
                )

                role_score_df = (
                    refined_df.with_columns(pl.col("role").replace("", None))
                    .group_by("role")
                    .agg(
                        pl.col("comp_overall")
                        .mean()
                        .round(0)
                        .cast(pl.Int8)
                        .alias("comp_overall"),
                        pl.col("assign_overall")
                        .mean()
                        .round(0)
                        .cast(pl.Int8)
                        .alias("assign_overall"),
                        pl.col("staff_overall")
                        .mean()
                        .round(0)
                        .cast(pl.Int8)
                        .alias("staff_overall"),
                    )
                    .with_columns(
                        pl.mean_horizontal(
                            "comp_overall", "assign_overall", "staff_overall"
                        )
                        .round(0)
                        .cast(pl.Int8)
                        .alias("overall")
                    )
                    .drop_nulls("role")
                    .rename({"role": "units_areas_roles"})
                )
                units_areas_roles_scores_df = pl.concat(
                    [unit_score_df, area_score_df, role_score_df], how="vertical"
                )

                # Set scores to state.
                self.overall_hospital_scores = hospital_score_df.to_dicts()[0]
                self.units_areas_roles_hospital_scores = (
                    units_areas_roles_scores_df.to_dicts()
                )

        except Exception as e:
            traceback.print_exc()
            logger.critical(e)

    def load_review_info(self) -> None:
        try:
            if self.report_info:
                review_df = (
                    pl.DataFrame(copy.deepcopy(self.report_info))
                )

                refined_df = (
                    review_df
                    .select(
                        pl.coalesce(
                            [
                                pl.col("assignment").struct.field("unit").struct.field("entered_unit").replace("", None),
                                pl.col("assignment").struct.field("unit").struct.field("selected_unit").replace("", None),
                            ]
                        ).alias("unit"),
                        pl.coalesce(
                            [
                                pl.col("assignment").struct.field("area").struct.field("entered_area").replace("", None),
                                pl.col("assignment").struct.field("area").struct.field("selected_area").replace("", None),
                            ]
                        ).alias("area"),
                        pl.coalesce(
                            [
                                pl.col("assignment").struct.field("role").struct.field("entered_role").replace("", None),
                                pl.col("assignment").struct.field("role").struct.field("selected_role").replace("", None),
                            ]
                        ).alias("role"),

                        pl.col("compensation").struct.field("comments").alias("comp_comments").replace("", None),
                        pl.col("assignment").struct.field("comments").alias("assign_comments").replace("", None),
                        pl.col("staffing").struct.field("comments").alias("staff_comments").replace("", None),
                        pl.col("social").struct.field("likes").alias("likes"),
                        pl.col("social").struct.field("tags").alias("tags"),

                        pl.when(
                            pl.col("modified_at").is_not_null()
                        )
                        .then(
                            pl.col("modified_at").alias("timestamp")
                        )
                        .otherwise(
                            pl.col("submitted_at").alias("timestamp")
                        )
                    )
                    .filter(
                        pl.any_horizontal(
                            [
                                pl.col("comp_comments").is_not_null(),
                                pl.col("assign_comments").is_not_null(),
                                pl.col("staff_comments").is_not_null(),
                            ]
                        )
                    )
                    .with_columns(
                        pl.col("timestamp").map_elements(lambda ts: humanize.naturaltime(datetime.fromisoformat(ts)), return_dtype=pl.String).alias("time_ago")
                    )
                )

                refined_df = (
                    refined_df.select(
                        pl.coalesce(
                            [
                                pl.col("unit"),
                                pl.col("area"),
                                pl.col("role")
                            ]
                        ).alias("units_areas_roles"),
                        pl.col("comp_comments"),
                        pl.col("assign_comments"),
                        pl.col("staff_comments"),
                        pl.col("likes"),
                        pl.col("tags"),
                        pl.col("timestamp"),
                        pl.col("time_ago")
                    )
                )

                # Add all to units_areas_roles list for user select.
                self.review_info = refined_df.to_dicts()

        except Exception as e:
            logger.critical(e)

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
