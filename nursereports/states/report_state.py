from ..states import PageState
from ..server.exceptions import RequestFailed, DuplicateReport, DuplicateUUID
from ..server.secrets import anyscale_api_key, anyscale_url, api_url, api_key
from ..server.supabase import (
    supabase_check_for_existing_report,
    supabase_user_edit_report,
    supabase_get_full_report_info,
    supabase_get_hospital_info,
    supabase_no_report_id_conflict,
    supabase_submit_full_report,
    supabase_update_user_info,
    supabase_update_hospital_units,
    supabase_update_hospital_area_role,
)
from loguru import logger
from typing import Callable, Iterable, Literal

import httpx
import inspect
import json
import uuid
import re
import reflex as rx
import rich
import textwrap


class ReportState(PageState):
    """
    State for the report, variables grouped into the three major
    groups of the report; compensation, staffing, and assignment.
    """

    # CMS ID pulled from URL parameters.
    hospital_id: str

    # Dict of hospital data pulled from /hospital.
    hospital_info: dict[str, str | int | list]

    # Generated uuid for the current report.
    report_id: str

    @rx.var
    def mode(self) -> Literal["edit", "full-report", "pay-report", "red-flag"]:
        return self.router.page.params.get("report_mode")

    def event_state_report_flow(self) -> Iterable[Callable]:
        """
        Ensures that report navigation contains the proper information before proceeding
        """
        if not self.mode or not self.hospital_id or not self.hospital_info:
            if self.hospital_id:
                yield rx.redirect(f"/hospital/{self.hospital_id}")
            else:
                yield rx.redirect("/dashboard")
        logger.critical(self.hospital_id)
        logger.critical(self.hospital_info)
        logger.critical(self.report_id)
        logger.critical(self.mode)

    def event_state_edit_user_report(self, report_id: str) -> Iterable[Callable]:
        """
        Loads report data into state for user to make edits.
        """
        try:
            # Reset all report variables.
            self.reset()

            # Load report to edit into the state.
            report = supabase_get_full_report_info(self.access_token, report_id)
            self.save_report_dict_to_state(report)

            # Populate other report details to state.
            self.report_id = report["report_id"]
            self.hospital_id = report["hospital_id"]
            self.hospital_info = supabase_get_hospital_info(
                self.access_token, self.hospital_id
            )

            # Navigate to the first page of report edit page.
            yield rx.redirect("/report/edit/compensation")

        except Exception as e:
            logger.critical(str(e))
            yield rx.redirect("/dashboard")
            yield rx.toast.error("Error while retrieving report details.")

    def event_state_create_full_report(self, hospital_id: str) -> Iterable[Callable]:
        """
        Resets and prepares report state for user to make a new report.
        """
        try:
            # Reset all report variables.
            self.reset()

            # Set necessary info for report.
            self.report_id = str(uuid.uuid4())
            self.hospital_id = hospital_id
            self.hospital_info = supabase_get_hospital_info(
                self.access_token, self.hospital_id
            )

            # Redirect to first page of full report.
            yield rx.redirect("/report/full-report/overview")

        except Exception as e:
            yield rx.redirect("/dashboard")
            logger.critical(str(e))
            raise Exception("Error while setting up new report.")

    def event_state_get_hospital_info(self) -> Iterable[Callable]:
        """
        Retrieves hospital info using hospital_id from state.
        """
        try:
            self.hospital_info = supabase_get_hospital_info(
                self.access_token, self.hospital_id
            )

        except Exception as e:
            yield rx.redirect("/dashboard")
            logger.critical(str(e))
            raise Exception("Error while pulling hospital details.")

    #################################################################
    #
    # COMPENSATION
    #
    #################################################################

    comp_select_emp_type: Literal["Full-time", "Part-time", "Contract"] = ""
    comp_select_pay_type: Literal["Hourly", "Weekly"] = ""
    comp_input_pay_hourly: int = 0
    comp_input_pay_weekly: int = 0
    comp_input_pay_night: int = 0
    comp_input_pay_weekend: int = 0
    comp_input_pay_weekend_night: int = 0
    input_calculator: Literal[
        "hourly", "weekly", "night", "weekend", "weekend_night"
    ] = ""
    calculator_value: str = "0"
    comp_select_shift: Literal["Day", "Night", "Rotating"] = ""
    comp_select_weekly_shifts: Literal[
        "Less than 1",
        "1",
        "2",
        "3",
        "4",
        "5",
    ] = ""
    comp_select_hospital_experience: Literal[
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "More than 25 years",
    ] = ""
    comp_select_total_experience: Literal[
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "More than 25 years",
    ] = ""
    comp_check_benefit_pto: bool = False
    comp_check_benefit_parental: bool = False
    comp_check_benefit_insurance: bool = False
    comp_check_benefit_retirement: bool = False
    comp_check_benefit_pro_dev: bool = False
    comp_check_benefit_tuition: bool = False
    comp_select_overall: int = 0
    comp_input_comments: str = ""

    def set_comp_select_pay_type(self, type: str) -> None:
        self.comp_select_pay_type = type
        self.comp_input_pay_hourly = 0
        self.comp_input_pay_weekly = 0

    def set_comp_select_hospital_experience(self, experience: str) -> None:
        self.comp_select_hospital_experience = experience
        self.comp_select_total_experience = ""

    def set_calculator_value(self, input: str) -> None:
        """
        Set calculator based on context from self.input_calculator. Restricts length
        of input based on if user is entering hourly/weekly/etc rates.
        """
        if input == "clear":
            self.calculator_value = "0"
            return
        if input == "enter":
            setattr(
                self,
                f"comp_input_pay_{self.input_calculator}",
                int(self.calculator_value),
            )
            self.calculator_value = "0"
            return
        if self.calculator_value == "0":
            self.calculator_value = input
            return
        else:
            if (
                self.input_calculator in ("weekend", "night")
                and len(self.calculator_value) >= 2
            ):
                return
            elif self.input_calculator == "hourly" and len(self.calculator_value) >= 3:
                return
            elif self.input_calculator == "weekly" and len(self.calculator_value) >= 5:
                return
            else:
                self.calculator_value += input

    @rx.var
    def comp_comments_chars_left(self) -> int:
        if self.comp_input_comments:
            return 1000 - len(self.comp_input_comments)

    @rx.var
    def years_hospital_experience(self) -> list[str]:
        from ..client.components import years_experience

        return years_experience

    @rx.var
    def years_total_experience(self) -> list[str]:
        """
        Uses years_hospital_experience to ensure that RN can't select a number of years
        less than the number worked at hospital as RN.
        """
        index = 0
        if self.comp_select_hospital_experience:
            index = self.years_hospital_experience.index(
                self.comp_select_hospital_experience
            )
        return self.years_hospital_experience[index:]

    def handle_submit_compensation(self) -> Callable | Iterable[Callable]:
        """
        Ensure validity of all entries in the compensation section before advancing to the
        assignment section.
        """
        # Check all our required values for completion.
        if (
            not self.comp_select_emp_type
            or not self.comp_select_pay_type
            or not (self.comp_input_pay_hourly or self.comp_input_pay_weekly)
            or not self.comp_select_shift
            or not self.comp_select_weekly_shifts
            or not self.comp_select_hospital_experience
            or not self.comp_select_total_experience
            or not self.comp_select_overall
        ):
            return rx.toast.error(
                "Missing information. Please check form and complete required questions.",
                close_button=True,
            )

        # Check all our values for validity.
        if (
            self.comp_select_emp_type not in ("Full-time", "Part-time", "Contract")
            or self.comp_select_pay_type not in ("Hourly", "Weekly")
            or not isinstance(self.comp_input_pay_hourly, int)
            or self.comp_input_pay_hourly > 999
            or not isinstance(self.comp_input_pay_weekly, int)
            or self.comp_input_pay_weekly > 9999
            or not isinstance(self.comp_input_pay_night, int)
            or self.comp_input_pay_night > 99
            or not isinstance(self.comp_input_pay_weekend, int)
            or self.comp_input_pay_weekend > 99
            or self.comp_select_shift not in ("Day", "Night", "Rotating")
            or self.comp_select_weekly_shifts
            not in ("Less than 1", "1", "2", "3", "4", "5")
            or self.comp_select_hospital_experience
            not in tuple(str(i) for i in range(26)) + tuple("More than 25 years")
            or self.comp_select_total_experience
            not in tuple(str(i) for i in range(26)) + tuple("More than 25 years")
            or not isinstance(self.comp_check_benefit_pto, bool)
            or not isinstance(self.comp_check_benefit_parental, bool)
            or not isinstance(self.comp_check_benefit_insurance, bool)
            or not isinstance(self.comp_check_benefit_retirement, bool)
            or not isinstance(self.comp_check_benefit_pro_dev, bool)
            or not isinstance(self.comp_check_benefit_tuition, bool)
            or not isinstance(self.comp_select_overall, int)
            or (5 < self.comp_select_overall < 1)
            or not isinstance(self.comp_input_comments, str)
        ):
            return rx.toast.error(
                "Validity check failed. Contact support if problem persists.",
                close_button=True,
            )

        # Check all our values for sanity.
        error_messages = []
        if self.comp_input_pay_hourly:
            if not (15 <= self.comp_input_pay_hourly <= 250):
                error_messages.append("Hourly rate entered exceeds normal ranges.")
        if self.comp_input_pay_weekly:
            if not (800 <= self.comp_input_pay_weekly <= 15000):
                error_messages.append("Weekly rate entered exceeds normal ranges.")
        if not (0 <= self.comp_input_pay_night <= 50):
            error_messages.append("Night differential entered exceeds normal ranges.")
        if not (0 <= self.comp_input_pay_weekend <= 50):
            error_messages.append("Weekend differential entered exceeds normal ranges.")
        if not (0 <= self.comp_input_pay_weekend_night <= 50):
            error_messages.append(
                "Weekend night differential entered exceeds normal ranges."
            )
        if len(self.comp_input_comments) > 1000:
            error_messages.append("Length of comment exceeds 1000 characters.")

        for message in error_messages:
            yield rx.toast.error(message, close_button=True)

        # If all checks are complete and everything is groovy.
        if not error_messages:
            return rx.redirect(f"/report/{self.mode}/assignment")

    #################################################################
    #
    # ASSIGNMENT VARIABLES
    #
    #################################################################

    assign_select_specific_unit: str
    assign_select_unit: str
    assign_input_unit_name: str
    assign_select_acuity: str
    assign_select_area: str
    assign_input_area: str
    assign_select_specialty_1: str
    assign_select_specialty_2: str
    assign_select_specialty_3: str
    assign_select_teamwork_rn: str
    assign_select_teamwork_na: str
    assign_select_providers: str
    assign_select_contributions: str
    assign_select_impact: str
    assign_select_management: str
    assign_select_leaving: str
    assign_select_leaving_reason: str
    assign_select_recommend: str
    assign_input_comments: str
    assign_select_overall: str
    assign_error_message: str

    def set_assign_select_specific_unit(self, unit: str) -> None:
        self.assign_select_acuity = ""
        self.assign_select_unit = ""
        self.assign_select_area = ""
        self.assign_input_area = ""
        self.assign_input_unit_name = ""
        self.assign_select_specific_unit = unit

    def set_assign_select_specialty_1(self, specialty: str) -> None:
        self.assign_select_specialty_3 = ""
        self.assign_select_specialty_2 = ""
        self.assign_select_specialty_1 = specialty

    def set_assign_select_specialty_2(self, specialty: str) -> None:
        self.assign_select_specialty_3 = ""
        self.assign_select_specialty_2 = specialty

    @rx.var
    def name_too_long(self) -> bool:
        if self.assign_input_unit_name:
            if len(self.assign_input_unit_name) > 30:
                return True
            else:
                return False
        else:
            return False

    @rx.var
    def area_too_long(self) -> bool:
        if self.assign_input_area:
            if len(self.assign_input_area) > 50:
                return True
            else:
                return False
        else:
            return False

    @rx.var(cache=True)
    def hospital_units(self) -> list[str]:
        if self.hospital_info:
            units = self.hospital_info["hosp_units"]
            units.sort()
            units.append("I don't see my unit")
            return units
        else:
            return ["I don't see my unit"]

    @rx.var(cache=True)
    def hospital_areas(self) -> list[str]:
        if self.hospital_info:
            areas = self.hospital_info["hosp_areas_roles"]
            areas.sort()
            areas.append("I don't see my area or role")
            return areas
        else:
            return ["I don't see my area or role"]

    @rx.var
    def has_unit(self) -> bool:
        return True if self.assign_select_specific_unit else False

    @rx.var
    def is_unit(self) -> bool:
        return True if self.assign_select_specific_unit == "Yes" else False

    @rx.var
    def unit_not_present(self) -> bool:
        return True if self.assign_select_unit == "I don't see my unit" else False

    @rx.var
    def area_not_present(self) -> bool:
        return (
            True if self.assign_select_area == "I don't see my area or role" else False
        )

    @rx.var
    def has_specialty_1(self) -> bool:
        return True if self.assign_select_specialty_1 else False

    @rx.var
    def has_specialty_2(self) -> bool:
        return True if self.assign_select_specialty_2 else False

    @rx.var
    def is_leaving(self) -> bool:
        return True if self.assign_select_leaving == "Yes" else False

    @rx.var
    def assign_input_comments_chars_over(self) -> bool:
        if self.assign_input_comments_chars_left:
            if self.assign_input_comments_chars_left < 0:
                return True
            else:
                return False

    @rx.var
    def assign_input_comments_chars_left(self) -> int:
        if self.assign_input_comments:
            return 1000 - len(self.assign_input_comments)

    @rx.var
    def assign_select_overall_description(self) -> str:
        if self.assign_select_overall == "a":
            return "Great"
        if self.assign_select_overall == "b":
            return "Good"
        if self.assign_select_overall == "c":
            return "So-so"
        if self.assign_select_overall == "d":
            return "Bad"
        if self.assign_select_overall == "f":
            return "Terrible"

    @rx.var
    def assign_select_overall_background(self) -> str:
        if self.assign_select_overall == "a":
            return "rgb(95, 163, 217)"
        if self.assign_select_overall == "b":
            return "rgb(95, 154, 100)"
        if self.assign_select_overall == "c":
            return "rgb(237, 234, 95)"
        if self.assign_select_overall == "d":
            return "rgb(197, 116, 57)"
        if self.assign_select_overall == "f":
            return "rgb(185, 65, 55)"

    @rx.var
    def assign_progress(self) -> int:
        progress = 0
        if self.assign_select_specific_unit == "Yes":
            progress = progress + 10
            if self.assign_select_unit:
                if self.assign_select_unit != "I don't see my unit":
                    progress = progress + 10
                if self.assign_select_unit == "I don't see my unit":
                    progress = progress + 5
                    if self.assign_input_unit_name:
                        progress = progress + 5
                if self.assign_select_acuity:
                    progress = progress + 10

        if self.assign_select_specific_unit == "No":
            progress = progress + 10
            if self.assign_select_area:
                if self.assign_select_area != "I don't see my area or role":
                    progress = progress + 20
                if self.assign_select_area == "I don't see my area or role":
                    progress = progress + 10
                    if self.assign_input_area:
                        progress = progress + 10

        if self.assign_select_teamwork_rn:
            progress = progress + 5
        if self.assign_select_teamwork_na:
            progress = progress + 5
        if self.assign_select_providers:
            progress = progress + 10
        if self.assign_select_contributions:
            progress = progress + 10
        if self.assign_select_impact:
            progress = progress + 5
        if self.assign_select_management:
            progress = progress + 5
        if self.assign_select_leaving:
            if self.is_leaving:
                progress = progress + 5
                if self.assign_select_leaving_reason:
                    progress = progress + 5
            else:
                progress = progress + 10
        if self.assign_select_recommend:
            progress = progress + 10

        if self.assign_select_overall:
            progress = progress + 10

        return progress

    @rx.var
    def assign_can_progress(self) -> bool:
        if self.assign_progress == 100:
            return True
        else:
            return False

    @rx.var
    def assign_has_error(self) -> bool:
        return True if self.assign_error_message else False

    #################################################################
    #
    # STAFFING VARIABLES
    #
    #################################################################

    staffing_input_ratio: int
    staffing_select_ratio_unsafe: str
    staffing_select_workload: str
    staffing_select_charge_response: str
    staffing_select_charge_assignment: str
    staffing_select_nursing_shortages: str
    staffing_select_aide_shortages: str
    staffing_check_transport: bool
    staffing_check_lab: bool
    staffing_check_cvad: bool
    staffing_check_wocn: bool
    staffing_check_chaplain: bool
    staffing_check_educator: bool
    staffing_select_support_available: str
    staffing_input_comments: str
    staffing_select_overall: str
    staffing_error_message: str

    def set_staffing_input_ratio(self, ratio: str) -> None:
        if bool(re.match(r"^[0-9]+$", ratio)):
            self.staffing_input_ratio = int(ratio)
        if ratio == "":
            self.staffing_input_ratio = 0

    def set_staffing_select_ratio_response(self, response: str) -> None:
        self.staffing_input_ratio = 0
        self.staffing_select_ratio_unsafe = ""
        self.staffing_select_ratio_response = response

    def set_staffing_select_charge_response(self, response: str) -> None:
        self.staffing_select_charge_assignment = ""
        self.staffing_select_charge_response = response

    @rx.var
    def has_ratios(self) -> bool:
        if (
            self.assign_select_acuity == "Intensive"
            or self.assign_select_acuity == "Intermediate"
            or self.assign_select_acuity == "Floor"
        ):
            return True
        else:
            return False

    @rx.var
    def ratio_is_valid(self) -> bool:
        return True if 0 < self.staffing_input_ratio < 30 else False

    @rx.var
    def has_charge(self) -> bool:
        return True if self.staffing_select_charge_response == "Yes" else False

    @rx.var
    def ratios_unsafe(self) -> bool:
        if (
            self.staffing_select_ratio_unsafe == "Always"
            or self.staffing_select_ratio_unsafe == "Usually"
            or self.staffing_select_ratio_unsafe == "Sometimes"
        ):
            return True
        else:
            return False

    @rx.var
    def staffing_input_comments_chars_over(self) -> bool:
        if self.staffing_input_comments_chars_left:
            if self.staffing_input_comments_chars_left < 0:
                return True
            else:
                return False

    @rx.var
    def staffing_input_comments_chars_left(self) -> int:
        if self.staffing_input_comments:
            return 1000 - len(self.staffing_input_comments)

    @rx.var
    def staffing_select_overall_description(self) -> str:
        if self.staffing_select_overall == "a":
            return "Great"
        if self.staffing_select_overall == "b":
            return "Good"
        if self.staffing_select_overall == "c":
            return "So-so"
        if self.staffing_select_overall == "d":
            return "Bad"
        if self.staffing_select_overall == "f":
            return "Terrible"

    @rx.var
    def staffing_select_overall_background(self) -> str:
        if self.staffing_select_overall == "a":
            return "rgb(95, 163, 217)"
        if self.staffing_select_overall == "b":
            return "rgb(95, 154, 100)"
        if self.staffing_select_overall == "c":
            return "rgb(237, 234, 95)"
        if self.staffing_select_overall == "d":
            return "rgb(197, 116, 57)"
        if self.staffing_select_overall == "f":
            return "rgb(185, 65, 55)"

    @rx.var
    def staffing_progress(self) -> int:
        progress = 0
        if self.has_ratios:
            if self.staffing_input_ratio and self.ratio_is_valid:
                progress = progress + 10
            if self.staffing_select_ratio_unsafe:
                progress = progress + 10
        if not self.has_ratios and self.staffing_select_workload:
            progress = progress + 20
        if self.staffing_select_workload:
            progress = progress + 10
        if self.staffing_select_charge_response == "Yes":
            progress = progress + 5
            if self.staffing_select_charge_assignment:
                progress = progress + 5
        if self.staffing_select_charge_response == "No":
            progress = progress + 10
        if self.staffing_select_nursing_shortages:
            progress = progress + 15
        if self.staffing_select_aide_shortages:
            progress = progress + 15
        if self.staffing_select_support_available:
            progress = progress + 15
        if self.staffing_select_overall:
            progress = progress + 15
        return progress

    @rx.var
    def staffing_can_progress(self) -> bool:
        return True if self.staffing_progress == 100 else False

    @rx.var
    def staffing_has_error(self) -> bool:
        return True if self.staffing_error_message else False

    #################################################################
    #
    # REPORT SUBMISSION \ HANDLERS
    #
    #################################################################

    def handle_edit_staffing(self) -> Callable | None:
        return ReportState.edit_report

    def handle_submit_assignment(self) -> Callable:
        if not self.assign_can_progress:
            self.assign_error_message = "Some fields incomplete or invalid."
            return
        if len(self.assign_input_comments) > 1000:
            self.assign_error_message = "Comments contain too many characters."
            return
        self.assign_error_message = ""
        return rx.redirect("/report/full-report/staffing")

    def handle_submit_staffing(self) -> Callable:
        if not self.staffing_can_progress:
            self.staffing_error_message = "Some fields incomplete or invalid."
            return
        if self.has_ratios and not self.ratio_is_valid:
            self.staffing_error_message = "Some fields incomplete or invalid."
            return
        if len(self.staffing_input_comments) > 1000:
            self.staffing_error_message = "Comments contain too many characters."
            return
        self.staffing_error_message = ""
        return ReportState.submit_full_report

    def edit_report(self) -> Iterable[Callable]:
        """
        Prepare and submit edits to database for a previously completed report.
        """
        try:
            # Build report from state data.
            report = self.prepare_report_dict()

            # Check if all fields are complete.
            if not self.comp_can_progress:
                self.comp_error_message = "Some fields incomplete or invalid."
                return rx.redirect("/report/edit/compensation")
            if not self.assign_can_progress:
                self.assign_error_message = "Some fields incomplete or invalid."
                return rx.redirect("/report/edit/assignment")
            if not self.staffing_can_progress:
                self.staffing_can_progress = "Some fields incomplete or invalid."
                return rx.redirect("/report/edit/staffing")

            # Upload changes to supabase.
            supabase_user_edit_report(self.access_token, report)

            # Moderate new entries via AI.
            yield ReportState.moderate_user_entries(report)

            # Redirect to complete page.
            yield rx.redirect("/report/edit/complete")

            # Set report complete to prevent back navigation
            # INSERT HERE

        except Exception as e:
            rich.inspect(e)
            yield rx.toast.error("Unable to submit edits. Check logs.")

    def submit_full_report(self) -> Iterable[Callable]:
        """
        Prepare and submit full report to database.
        """
        try:
            # Build report from state data.
            report = self.prepare_report_dict()

            # Check if all fields are complete.
            if not self.comp_can_progress:
                self.comp_error_message = "Some fields incomplete or invalid."
                return rx.redirect("/report/full-report/compensation")
            if not self.assign_can_progress:
                self.assign_error_message = "Some fields incomplete or invalid."
                return rx.redirect("/report/full-report/assignment")
            if not self.staffing_can_progress:
                self.staffing_can_progress = "Some fields incomplete or invalid."
                return rx.redirect("/report/full-report/staffing")

            # Ensure that no report UUID's conflict.
            supabase_no_report_id_conflict(self.access_token, self.report_id)

            # SHIT IS BROKEN AS HECK
            # supabase_check_for_existing_report(self.access_token, report)

            # Submit report to supabase.
            supabase_submit_full_report(self.access_token, report)

            updated_data = supabase_update_user_info(
                self.access_token,
                self.user_id,
                data={
                    "needs_onboard": False,
                },
            )

            self.user_info.update(updated_data)
            yield ReportState.moderate_user_entries(report)
            yield rx.redirect("/report/full-report/complete")

        except DuplicateReport:
            self.is_loading = False
            yield ReportState.edit_report
        except DuplicateUUID:
            self.is_loading = False
            self.generate_report_id()
            yield ReportState.submit_full_report
        except RequestFailed as e:
            yield rx.toast.error(str(e))
            self.is_loading = False
        except Exception as e:
            logger.critical(e)
            yield rx.toast.error(
                "Uncaught exception. If this persists contact support@nursereports.org"
            )
            self.is_loading = False

    def prepare_report_dict(self) -> dict:
        report = {
            "report_id": self.report_id,
            "hospital_id": self.hospital_id,
            "user_id": self.user_claims_id,
            "license": self.user_info["license"],
            "license_state": self.user_info["license_state"],
            "trust": self.user_info["trust"],
            "comp_select_emp_type": self.comp_select_emp_type,
            "comp_select_pay_type": self.comp_select_pay_type,
            "comp_input_pay_amount": self.comp_input_pay_amount,
            "comp_select_diff_response": self.comp_select_diff_response,
            "comp_input_diff_nights": self.comp_input_diff_nights,
            "comp_input_diff_weekends": self.comp_input_diff_weekends,
            "comp_select_incentive_response": self.comp_select_incentive_response,
            "comp_input_incentive_amount": self.comp_input_incentive_amount,
            "comp_select_certifications": self.comp_select_certifications,
            "comp_select_shift": self.comp_select_shift,
            "comp_select_weekly_shifts": self.comp_select_weekly_shifts,
            "comp_select_hospital_experience": self.comp_select_hospital_experience,
            "comp_select_total_experience": self.comp_select_total_experience,
            "comp_check_benefit_pto": self.comp_check_benefit_pto,
            "comp_check_benefit_parental": self.comp_check_benefit_parental,
            "comp_check_benefit_insurance": self.comp_check_benefit_insurance,
            "comp_check_benefit_retirement": self.comp_check_benefit_retirement,
            "comp_check_benefit_pro_dev": self.comp_check_benefit_pro_dev,
            "comp_check_benefit_tuition": self.comp_check_benefit_tuition,
            "comp_select_comp_adequate": self.comp_select_comp_adequate,
            "comp_input_comments": self.comp_input_comments,
            "comp_select_overall": self.comp_select_overall,
            "assign_select_specific_unit": self.assign_select_specific_unit,
            "assign_select_unit": (
                self.assign_select_unit
                if self.assign_select_unit != "I don't see my unit"
                else None
            ),
            "assign_input_unit_name": self.assign_input_unit_name,
            "assign_select_acuity": self.assign_select_acuity,
            "assign_select_area": (
                self.assign_select_area
                if self.assign_select_area != "I dont see my area or role"
                else None
            ),
            "assign_input_area": self.assign_input_area,
            "assign_select_specialty_1": self.assign_select_specialty_1,
            "assign_select_specialty_2": self.assign_select_specialty_2,
            "assign_select_specialty_3": self.assign_select_specialty_3,
            "assign_select_teamwork_rn": self.assign_select_teamwork_rn,
            "assign_select_teamwork_na": self.assign_select_teamwork_na,
            "assign_select_providers": self.assign_select_providers,
            "assign_select_contributions": self.assign_select_contributions,
            "assign_select_impact": self.assign_select_impact,
            "assign_select_management": self.assign_select_management,
            "assign_select_leaving": self.assign_select_leaving,
            "assign_select_leaving_reason": self.assign_select_leaving_reason,
            "assign_select_recommend": self.assign_select_recommend,
            "assign_input_comments": self.assign_input_comments,
            "assign_select_overall": self.assign_select_overall,
            "staffing_input_ratio": self.staffing_input_ratio,
            "staffing_select_ratio_unsafe": self.staffing_select_ratio_unsafe,
            "staffing_select_workload": self.staffing_select_workload,
            "staffing_select_charge_response": self.staffing_select_charge_response,
            "staffing_select_charge_assignment": self.staffing_select_charge_assignment,
            "staffing_select_nursing_shortages": self.staffing_select_nursing_shortages,
            "staffing_select_aide_shortages": self.staffing_select_aide_shortages,
            "staffing_check_transport": self.staffing_check_transport,
            "staffing_check_lab": self.staffing_check_lab,
            "staffing_check_cvad": self.staffing_check_cvad,
            "staffing_check_wocn": self.staffing_check_wocn,
            "staffing_check_chaplain": self.staffing_check_chaplain,
            "staffing_check_educator": self.staffing_check_educator,
            "staffing_select_support_available": self.staffing_select_support_available,
            "staffing_input_comments": self.staffing_input_comments,
            "staffing_select_overall": self.staffing_select_overall,
        }
        return report

    def save_report_dict_to_state(self, report: dict) -> None:
        """
        Pop the following values out of the report as erroneous to report state.
        """
        # Pop keys out of the report.
        report.pop("user_id")
        report.pop("license")
        report.pop("license_state")
        report.pop("trust")
        report.pop("created_at")
        report.pop("modified_at")
        report.pop("comp_input_comments_flag")
        report.pop("assign_input_comments_flag")
        report.pop("staffing_input_comments_flag")
        report.pop("assign_input_unit_name_flag")
        report.pop("assign_input_area_flag")
        report.pop("is_test")
        report.pop("likes")

        # Set the rest of the keys to the state.
        for key, value in report.items():
            setattr(self, f"{key}", value)

    @rx.background
    async def moderate_user_entries(self, report: dict) -> None:
        """
        Send all user entered fields to AI for moderation. AI will send
        response flagging entries
        """
        user_entry_dict = {}
        if report["comp_input_comments"]:
            user_entry_dict["comp_input_comments"] = self.comp_input_comments
        if report["staffing_input_comments"]:
            user_entry_dict["staffing_input_comments"] = self.staffing_input_comments
        if report["assign_input_unit_name"]:
            user_entry_dict["assign_input_unit_name"] = self.assign_input_unit_name
        if report["assign_input_area"]:
            user_entry_dict["assign_input_area"] = self.assign_input_area
        if report["assign_input_comments"]:
            user_entry_dict["assign_input_comments"] = self.assign_input_comments

        system_prompt = inspect.cleandoc(
            """You moderate user entries by nurses for a hospital
        review site. Output responses in JSON"""
        )
        user_prompt = f"""Moderate user entries for racism, slurs,
        threats, web links, spam, personally identifiable
        information, or names of specific people. An example of a
        JSON output could be...
        'comp_input_comments_flag': 'Slur',
        'assign_input_unit_name_flag': 'Spam'
        if comp_input_comments contained a slur, and
        assign_input_unit_name contained nonsensical words not
        relevant to a hospital review.
        
        Entry name with user entries are as follows. {json.dumps(user_entry_dict)}"""
        url = f"{anyscale_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {anyscale_api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "mistralai/Mixtral-8x22B-Instruct-v0.1",
            "messages": [
                {"role": "system", "content": textwrap.dedent(system_prompt)},
                {"role": "user", "content": textwrap.dedent(user_prompt)},
            ],
            "response_format": {
                "type": "json_object",
                "schema": {
                    "type": "object",
                    "properties": {
                        "entries": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "entry_name": {"type": "string"},
                                    "flag": {"type": "boolean"},
                                    "flag_reason": {"type": "string"},
                                },
                                "required": ["entry_name", "flag", "flag_reason"],
                            },
                        }
                    },
                    "required": ["entries"],
                },
            },
            "temperature": 0.5,
        }
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    url=url, headers=headers, data=json.dumps(data)
                )
                if response.is_success:
                    logger.debug("Retrieved moderation suggestions from Anyscale.")
                    content = json.loads(response.content)
                    rich.inspect(content)
                    self.parse_moderation_suggestions(content, report)
                    return None
                else:
                    logger.warning("User entry moderation to Anyscale unsuccessful.")
                    return None
        except Exception as e:
            logger.critical(f"Exception while moderating report - {e}")

    def parse_moderation_suggestions(self, content: list, report: dict) -> None:
        """
        flags['entries'] contains a list of dicts with keys
        'entry_name', 'flag', and 'flag_reason'. If the flag
        is true, add entry to moderation data so that we can
        upload the flag_reason to our field _flag column to
        prevent other users from accessing and having the
        capability to manually review that before releasing.
        """
        moderation_data = {}
        flags = json.loads(content["choices"][0]["message"]["content"])
        for entry in flags["entries"]:
            """
            Add entry. For example if assign_input_comments has
            issue, add assign_input_comments_flag with the reason
            so we can manually check it later.
            """
            if entry["flag"] is True:
                flag_name = f"{entry['entry_name']}_flag".replace(" ", "_")
                moderation_data[flag_name] = entry["flag_reason"]

        if moderation_data:
            logger.warning(
                f"""Found some entries requiring moderation - {moderation_data}"""
            )
            url = f"{api_url}/rest/v1/reports?report_id=eq.{report['report_id']}"
            data = json.dumps(moderation_data)
            headers = {
                "apikey": api_key,
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal",
            }
            response = httpx.patch(url=url, headers=headers, data=data)
            if response.is_success:
                logger.debug(
                    f"Successfully flagged entries in {report['report_id']}\
                    for moderation in database."
                )
                return
            else:
                logger.critical(f"Error calling API to moderate {report['report_id']}.")
                rich.inspect(response)
                return
        else:
            logger.debug(
                f"""User report {report["report_id"]} seems ok. No entries found requiring moderation."""
            )
            return

    def redirect_to_red_flag_report(self, hosp_id: str) -> Iterable[Callable]:
        return rx.redirect(f"/report/red-flag-report/{hosp_id}/overview")
