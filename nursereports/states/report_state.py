from . import constants_types
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
from rich.pretty import pprint

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

    # Units areas and roles pulled for user selection at report load.
    hospital_units: list[str]
    hospital_areas: list[str]
    hospital_roles: list[str]

    # Full report dictionary.
    report_dict: dict[str, bool | int | str] = {}

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

            self.hospital_units = self.hospital_info.get("hosp_units", [])
            self.hospital_units.append("I don't see my unit")
            self.hospital_areas = self.hospital_info.get("hosp_areas", [])
            self.hospital_areas.append("I don't see my area")
            self.hospital_roles = self.hospital_info.get("hosp_roles", [])
            self.hospital_roles.append("I don't see my role")

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

    comp_select_emp_type: constants_types.ValidEmploymentType
    comp_select_pay_type: constants_types.ValidPayType
    comp_input_pay_hourly: int = 0
    comp_input_pay_weekly: int = 0
    comp_input_pay_night: int = 0
    comp_input_pay_weekend: int = 0
    comp_input_pay_weekend_night: int = 0
    input_calculator: constants_types.ValidCalculatorInputType
    calculator_pay_value: str = "0"
    comp_select_shift: constants_types.ValidShiftType
    comp_select_weekly_shifts: constants_types.ValidWeeklyShiftsType
    comp_select_hospital_experience: constants_types.ValidHospitalExperienceType
    comp_select_total_experience: constants_types.ValidHospitalExperienceType
    comp_check_benefit_pto: bool = False
    comp_check_benefit_parental: bool = False
    comp_check_benefit_insurance: bool = False
    comp_check_benefit_retirement: bool = False
    comp_check_benefit_reimbursement: bool = False
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

    def set_calculator_pay_value(self, input: str) -> None:
        """
        Set calculator based on context from self.input_calculator. Restricts length
        of input based on if user is entering hourly/weekly/etc rates.
        """
        if input == "clear":
            self.calculator_pay_value = "0"
            return
        if input == "enter":
            setattr(
                self,
                f"comp_input_pay_{self.input_calculator}",
                int(self.calculator_pay_value),
            )
            self.calculator_pay_value = "0"
            return
        if self.calculator_pay_value == "0":
            self.calculator_pay_value = input
            return
        else:
            if (
                self.input_calculator in ("weekend", "night")
                and len(self.calculator_pay_value) >= 2
            ):
                return
            elif self.input_calculator == "hourly" and len(self.calculator_pay_value) >= 3:
                return
            elif self.input_calculator == "weekly" and len(self.calculator_pay_value) >= 5:
                return
            else:
                self.calculator_pay_value += input

    @rx.var
    def comp_comments_chars_left(self) -> int:
        if self.comp_input_comments:
            return 1000 - len(self.comp_input_comments)

    @rx.var(cache=True)
    def years_hospital_experience(self) -> list[str]:
        return constants_types.COMP_SELECT_HOSPITAL_EXPERIENCE

    @rx.var(cache=True)
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
            self.comp_select_emp_type
            not in constants_types.COMP_SELECT_EMP_TYPE_SELECTIONS
            or self.comp_select_pay_type
            not in constants_types.COMP_SELECT_PAY_TYPE_SELECTIONS
            or not isinstance(self.comp_input_pay_hourly, int)
            or self.comp_input_pay_hourly > 999
            or not isinstance(self.comp_input_pay_weekly, int)
            or self.comp_input_pay_weekly > 9999
            or (self.comp_input_pay_hourly and self.comp_input_pay_weekly)
            or not isinstance(self.comp_input_pay_night, int)
            or self.comp_input_pay_night > 99
            or not isinstance(self.comp_input_pay_weekend, int)
            or self.comp_input_pay_weekend > 99
            or self.comp_select_shift
            not in constants_types.COMP_SELECT_SHIFT_SELECTIONS
            or self.comp_select_weekly_shifts
            not in constants_types.COMP_SELECT_WEEKLY_SHIFTS_SELECTIONS
            or self.comp_select_hospital_experience
            not in constants_types.COMP_SELECT_HOSPITAL_EXPERIENCE
            or self.comp_select_total_experience
            not in constants_types.COMP_SELECT_HOSPITAL_EXPERIENCE
            or not isinstance(self.comp_check_benefit_pto, bool)
            or not isinstance(self.comp_check_benefit_parental, bool)
            or not isinstance(self.comp_check_benefit_insurance, bool)
            or not isinstance(self.comp_check_benefit_retirement, bool)
            or not isinstance(self.comp_check_benefit_reimbursement, bool)
            or not isinstance(self.comp_check_benefit_tuition, bool)
            or not isinstance(self.comp_select_overall, int)
            or (5 < self.comp_select_overall < 1)
            or not isinstance(self.comp_input_comments, str)
        ):
            # Grab all relevant fields by key so we can see whats going wrong.
            keys = [key for key in ReportState.__fields__.keys() if "comp" in key]
            debug_dict = {}
            for key in keys:
                value = self.get_value(key)
                debug_dict[key] = value
                logger.warning(f"{key} - {value} - {type(value)}")

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
            self.report_dict = {
                "compensation": {
                    "emp_type": self.comp_select_emp_type,
                    "pay_type": self.comp_select_pay_type,
                    "pay": {
                        "hourly": self.comp_input_pay_hourly,
                        "weekly": self.comp_input_pay_weekly,
                        "night": self.comp_input_pay_night,
                        "weekend": self.comp_input_pay_weekend,
                        "weekend_night": self.comp_input_pay_weekend_night,
                    },
                    "shift": self.comp_select_shift,
                    "weekly_shifts": self.comp_select_weekly_shifts,
                    "experience": {
                        "hospital": self.comp_select_hospital_experience,
                        "total": self.comp_select_total_experience,
                    },
                    "benefits": {
                        "pto": self.comp_check_benefit_pto,
                        "parental_leave": self.comp_check_benefit_parental,
                        "insurance": self.comp_check_benefit_insurance,
                        "retirement": self.comp_check_benefit_retirement,
                        "reimbursement": self.comp_check_benefit_reimbursement,
                        "tuition": self.comp_check_benefit_tuition,
                    },
                    "ratings": {
                        "overall": self.comp_select_overall,
                    },
                    "comments": self.comp_input_comments,
                }
            }
            return rx.redirect(f"/report/{self.mode}/assignment")

    #################################################################
    #
    # ASSIGNMENT VARIABLES
    #
    #################################################################

    assign_select_classify: constants_types.ValidClassifyType
    assign_select_unit: str
    assign_select_area: str
    assign_select_role: str
    assign_input_unit: str
    assign_input_area: str
    assign_input_role: str
    assign_select_acuity: constants_types.ValidAcuityType
    assign_select_specialty_1: constants_types.ValidSpecialtyType
    assign_select_specialty_2: constants_types.ValidSpecialtyType
    assign_select_specialty_3: constants_types.ValidSpecialtyType
    assign_select_rate_nurses: int = 0
    assign_select_rate_nurse_aides: int = 0
    assign_select_rate_physicians: int = 0
    assign_select_rate_management: int = 0
    assign_select_recommend: constants_types.ValidYesNoType
    assign_select_overall: int = 0
    assign_input_comments: str
    assign_error_message: str

    def set_assign_select_classify(self, classification: str) -> None:
        self.assign_select_classify = classification
        self.assign_select_unit = ""
        self.assign_select_area = ""
        self.assign_select_role = ""
        self.assign_input_unit = ""
        self.assign_input_area = ""
        self.assign_input_role = ""
        self.assign_select_acuity = ""

    def set_assign_select_unit(self, unit: str) -> None:
        self.assign_select_unit = unit
        self.assign_input_unit = ""
        self.assign_select_acuity = ""

    def set_assign_select_area(self, area: str) -> None:
        self.assign_select_area = area
        self.assign_input_area = ""

    def set_assign_select_role(self, role: str) -> None:
        self.assign_select_role = role
        self.assign_input_role = ""

    @rx.var(cache=True)
    def assign_specialty_1(self) -> list[str]:
        return constants_types.ASSIGN_SELECT_SPECIALTY_SELECTIONS

    @rx.var(cache=True)
    def assign_specialty_2(self) -> list[str]:
        return [
            unit
            for unit in self.assign_specialty_1
            if unit not in self.assign_select_specialty_1
        ]

    @rx.var(cache=True)
    def assign_specialty_3(self) -> list[str]:
        return [
            unit
            for unit in self.assign_specialty_2
            if unit not in self.assign_select_specialty_2
        ]

    @rx.var
    def assign_input_comments_chars_left(self) -> int:
        if self.assign_input_comments:
            return 1000 - len(self.assign_input_comments)

    def handle_submit_assignment(self) -> Callable | Iterable[Callable]:
        # Check all our values for completion.
        if (
            not self.assign_select_classify
            or not (
                (
                    self.assign_select_unit
                    and self.assign_select_unit != "I don't see my unit"
                    and self.assign_select_acuity
                )
                or (
                    self.assign_select_unit
                    and self.assign_select_unit == "I don't see my unit"
                    and self.assign_input_unit
                    and self.assign_select_acuity
                )
                or (
                    self.assign_select_area
                    and self.assign_select_area != "I don't see my unit"
                )
                or (
                    self.assign_select_area
                    and self.assign_select_area == "I don't see my unit"
                    and self.assign_input_area
                )
                or (
                    self.assign_select_role
                    and self.assign_select_role != "I don't see my role"
                )
                or (
                    self.assign_select_role
                    and self.assign_select_role == "I don't see my role"
                    and self.assign_input_role
                )
            )
            or not self.assign_select_rate_nurses
            or not self.assign_select_rate_nurse_aides
            or not self.assign_select_rate_physicians
            or not self.assign_select_rate_management
            or not self.assign_select_recommend
            or not self.assign_select_overall
        ):
            return rx.toast.error(
                "Missing information. Please check form and complete required questions.",
                close_button=True,
            )

        # Check all our values for validity.
        if (
            self.assign_select_classify == "Unit" and (self.assign_select_acuity
            not in constants_types.ASSIGN_SELECT_ACUITY_SELECTIONS)
            or not isinstance(self.assign_input_unit, str)
            or len(self.assign_input_unit) > 50
            or not isinstance(self.assign_input_area, str)
            or len(self.assign_input_area) > 50
            or not isinstance(self.assign_input_role, str)
            or len(self.assign_input_role) > 50
            or self.assign_select_classify
            not in constants_types.ASSIGN_SELECT_CLASSIFY_SELECTIONS
            or (
                self.assign_select_specialty_1 != "" 
                and self.assign_select_specialty_1 not in constants_types.ASSIGN_SELECT_SPECIALTY_SELECTIONS
            )
            or (
                self.assign_select_specialty_2 != "" 
                and self.assign_select_specialty_2 not in constants_types.ASSIGN_SELECT_SPECIALTY_SELECTIONS
            )
            or (
                self.assign_select_specialty_3 != "" 
                and self.assign_select_specialty_3 not in constants_types.ASSIGN_SELECT_SPECIALTY_SELECTIONS
            )
            or not isinstance(self.assign_select_rate_nurses, int)
            or (5 < self.assign_select_rate_nurses < 1)
            or not isinstance(self.assign_select_rate_nurse_aides, int)
            or (5 < self.assign_select_rate_nurse_aides < 1)
            or not isinstance(self.assign_select_rate_physicians, int)
            or (5 < self.assign_select_rate_physicians < 1)
            or not isinstance(self.assign_select_rate_management, int)
            or (5 < self.assign_select_rate_management < 1)
            or self.assign_select_recommend
            not in constants_types.ASSIGN_SELECT_RECOMMEND_SELECTIONS
            or not isinstance(self.assign_input_comments, str)
        ):
            # Grab all relevant fields by key to see what is going wrong.
            keys = [key for key in ReportState.__fields__.keys() if "assign" in key]
            debug_dict = {}
            for key in keys:
                value = self.get_value(key)
                debug_dict[key] = value
                logger.warning(f"{key} - {value} - {type(value)}")

            return rx.toast.error(
                "Validity check failed. Contact support if problem persists.",
                close_button=True,
            )

        # Check all our values for sanity.
        error_messages = []
        if (
            self.assign_select_specialty_1 and (self.assign_select_specialty_1 in self.assign_select_specialty_2)
            or self.assign_select_specialty_2 and (self.assign_select_specialty_2 in self.assign_select_specialty_3)
            or self.assign_select_specialty_3 and (self.assign_select_specialty_3 in self.assign_select_specialty_1)
        ):
            error_messages.append("Can't have duplicate specialty entries.")
        if len(self.assign_input_comments) > 1000:
            error_messages.append("Length of comment exceeds 1000 characters")

        for message in error_messages:
            yield rx.toast.error(message, close_button=True)

        # If all checks complete and everything is groovy.
        if not error_messages:
            self.report_dict = {
                "assignment": {
                    "classify": self.assign_select_classify,
                    "unit": {
                        "selected_unit": self.assign_select_unit
                        if self.assign_select_unit != "I don't see my unit"
                        else "",
                        "entered_unit": self.assign_input_unit,
                        "acuity": self.assign_select_acuity,
                    },
                    "area": {
                        "selected_area": self.assign_select_area
                        if self.assign_select_area != "I don't see my area"
                        else "",
                        "entered_area": self.assign_input_area,
                    },
                    "role": {
                        "selected_role": self.assign_select_role
                        if self.assign_select_role != "I don't see my role"
                        else "",
                        "entered_role": self.assign_input_role,
                    },
                    "specialty": {
                        "specialty_1": self.assign_select_specialty_1,
                        "specialty_2": self.assign_select_specialty_2,
                        "specialty_3": self.assign_select_specialty_3,
                    },
                    "ratings": {
                        "nurses": self.assign_select_rate_nurses,
                        "nurse_aides": self.assign_select_rate_nurse_aides,
                        "physicians": self.assign_select_rate_physicians,
                        "management": self.assign_select_rate_management,
                        "overall": self.assign_select_overall,
                    },
                    "recommend": self.assign_select_recommend,
                    "comments": self.assign_input_comments,
                }
            }
            return rx.redirect(f"/report/{self.mode}/staffing")

    #################################################################
    #
    # STAFFING VARIABLES
    #
    #################################################################

    staffing_input_actual_ratio: int
    staffing_input_ideal_ratio: int
    calculator_select_ratio: str
    calculator_ratio_value: str
    staffing_select_workload: str
    staffing_select_charge_response: str
    staffing_select_charge_assignment: str
    staffing_select_nursing_shortages: str
    staffing_select_aide_shortages: str
    staffing_check_transport: bool = False
    staffing_check_lab: bool = False
    staffing_check_cvad: bool = False
    staffing_check_wocn: bool = False
    staffing_check_chaplain: bool = False
    staffing_check_educator: bool = False
    staffing_select_overall: int = 0
    staffing_input_comments: str

    def set_calculator_ratio_value(self, input: str) -> None:
            """
            Set calculator based on context from self.input_calculator. Restricts length
            of input to 2 digits.
            """
            if input == "clear":
                self.calculator_ratio_value = "0"
                return
            if input == "enter":
                setattr(
                    self,
                    f"staffing_input_{self.calculator_select_ratio}",
                    int(self.calculator_ratio_value),
                )
                self.calculator_ratio_value = "0"
                return
            if self.calculator_ratio_value == "0":
                self.calculator_ratio_value = input
                return
            else:
                if (
                    self.input_calculator in ("weekend", "night")
                    and len(self.calculator_ratio_value) >= 2
                ):
                    return
                elif self.input_calculator == "hourly" and len(self.calculator_ratio_value) >= 3:
                    return
                elif self.input_calculator == "weekly" and len(self.calculator_ratio_value) >= 5:
                    return
                else:
                    self.calculator_ratio_value += input

    def set_staffing_select_ratio_response(self, response: str) -> None:
        self.staffing_input_ratio = 0
        self.staffing_select_ratio_unsafe = ""
        self.staffing_select_ratio_response = response

    def set_staffing_select_charge_response(self, response: str) -> None:
        self.staffing_select_charge_assignment = ""
        self.staffing_select_charge_response = response

    @rx.var
    def staffing_input_comments_chars_left(self) -> int:
        if self.staffing_input_comments:
            return 1000 - len(self.staffing_input_comments)


    #################################################################
    #
    # REPORT SUBMISSION \ HANDLERS
    #
    #################################################################

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
