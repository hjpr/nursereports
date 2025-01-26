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
from datetime import datetime, timezone
from loguru import logger
from typing import Callable, Iterable, Literal

import httpx
import inspect
import json
import uuid
import pprint
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
    report_dict: dict[str, bool | int | str]

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

            # Set report UUID
            self.report_id = str(uuid.uuid4())

            # Set CMS ID of report.
            self.hospital_id = hospital_id

            # Get hospital info by CMS ID
            self.hospital_info = supabase_get_hospital_info(
                self.access_token, self.hospital_id
            )

            # Set available units/areas/roles for user selection.
            self.hospital_units = self.hospital_info.get("hosp_units", [])
            self.hospital_units.append("I don't see my unit")
            self.hospital_areas = self.hospital_info.get("hosp_areas", [])
            self.hospital_areas.append("I don't see my area")
            self.hospital_roles = self.hospital_info.get("hosp_roles", [])
            self.hospital_roles.append("I don't see my role")

            # Set user dict data.
            self.report_dict["report_id"] = self.report_id
            self.report_dict["hospital_id"] = self.hospital_id
            self.report_dict["user"] = {
                "user_id": self.user_claims_id,
                "professional": self.user_info.get("professional"),
                "ip_addr": self.router.session.client_ip,
                "host": self.router.headers.host,
                "user_agent": self.router.headers.user_agent,
            }
            self.report_dict["compensation"] = {}
            self.report_dict["assignment"] = {}
            self.report_dict["staffing"] = {}
            self.report_dict["social"] = {"likes": {}, "comments": {}, "tags": {}}
            self.report_dict["created_at"] = str(datetime.now(timezone.utc))
            self.report_dict["modified_at"] = str(datetime.now(timezone.utc))

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
    # COMPENSATION
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
            elif (
                self.input_calculator == "hourly"
                and len(self.calculator_pay_value) >= 3
            ):
                return
            elif (
                self.input_calculator == "weekly"
                and len(self.calculator_pay_value) >= 5
            ):
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
        Ensure completion, validity, and sanity of all entries in the compensation
        section before advancing to the assignment section.
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
            self.report_dict["compensation"] = {
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
            return rx.redirect(f"/report/{self.mode}/assignment")

    #################################################################
    # ASSIGNMENT
    #################################################################

    assign_select_classify: constants_types.ValidClassifyType
    assign_select_unit: str = ""
    assign_select_area: str = ""
    assign_select_role: str = ""
    assign_input_unit: str = ""
    assign_input_area: str = ""
    assign_input_role: str = ""
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
    assign_input_comments: str = ""

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
            self.assign_select_classify == "Unit"
            and (
                self.assign_select_acuity
                not in constants_types.ASSIGN_SELECT_ACUITY_SELECTIONS
            )
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
                and self.assign_select_specialty_1
                not in constants_types.ASSIGN_SELECT_SPECIALTY_SELECTIONS
            )
            or (
                self.assign_select_specialty_2 != ""
                and self.assign_select_specialty_2
                not in constants_types.ASSIGN_SELECT_SPECIALTY_SELECTIONS
            )
            or (
                self.assign_select_specialty_3 != ""
                and self.assign_select_specialty_3
                not in constants_types.ASSIGN_SELECT_SPECIALTY_SELECTIONS
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
            self.assign_select_specialty_1
            and (self.assign_select_specialty_1 in self.assign_select_specialty_2)
            or self.assign_select_specialty_2
            and (self.assign_select_specialty_2 in self.assign_select_specialty_3)
            or self.assign_select_specialty_3
            and (self.assign_select_specialty_3 in self.assign_select_specialty_1)
        ):
            error_messages.append("Can't have duplicate specialty entries.")
        if len(self.assign_input_comments) > 1000:
            error_messages.append("Length of comment exceeds 1000 characters")

        for message in error_messages:
            yield rx.toast.error(message, close_button=True)

        # If all checks complete and everything is groovy.
        if not error_messages:
            self.report_dict["assignment"] = {
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
            return rx.redirect(f"/report/{self.mode}/staffing")

    #################################################################
    # STAFFING
    #################################################################

    staffing_select_ratio: constants_types.ValidYesNoType
    staffing_input_actual_ratio: int = 0
    staffing_select_ratio_appropriate: constants_types.ValidRatioType
    staffing_input_ideal_ratio: int = 0
    calculator_toggle_ratio: constants_types.ValidCalculatorToggleRatioType
    calculator_ratio_value: str = ""
    staffing_select_workload: constants_types.ValidWorkloadType
    staffing_select_rate_workload: int = 0
    staffing_select_charge_present: constants_types.ValidYesNoType
    staffing_select_charge_assignment: constants_types.ValidChargeAssignmentType
    staffing_check_rapid_response: bool = False
    staffing_check_behavioral_response: bool = False
    staffing_check_transport: bool = False
    staffing_check_phlebotomy: bool = False
    staffing_check_cvad: bool = False
    staffing_check_ivt: bool = False
    staffing_check_wocn: bool = False
    staffing_check_chaplain: bool = False
    staffing_check_educator: bool = False
    staffing_select_overall: int = 0
    staffing_input_comments: str = ""

    def set_staffing_select_ratio(self, ratio: str) -> None:
        self.staffing_select_ratio = ratio
        self.staffing_input_actual_ratio = 0
        self.staffing_select_ratio_appropriate = ""
        self.staffing_input_ideal_ratio = 0

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
                f"staffing_input_{self.calculator_toggle_ratio}",
                int(self.calculator_ratio_value),
            )
            self.calculator_ratio_value = "0"
            return
        if self.calculator_ratio_value == "0":
            self.calculator_ratio_value = input
            return
        else:
            if len(self.calculator_ratio_value) >= 2:
                return
            else:
                self.calculator_ratio_value += input

    def set_staffing_select_charge_present(self, response: str) -> None:
        self.staffing_select_charge_present = response
        self.staffing_select_charge_assignment = ""

    @rx.var
    def staffing_input_comments_chars_left(self) -> int:
        if self.staffing_input_comments:
            return 1000 - len(self.staffing_input_comments)

    def handle_submit_staffing(self) -> Callable | Iterable[Callable]:
        # Check our values for completion.
        yield ReportState.set_user_is_loading(True)
        if (
            not self.staffing_select_ratio
            or not (
                (
                    self.staffing_select_ratio == "Yes"
                    and self.staffing_input_actual_ratio
                    and self.staffing_select_ratio_appropriate == "Yes"
                )
                or (
                    self.staffing_select_ratio == "Yes"
                    and self.staffing_input_actual_ratio
                    and self.staffing_select_ratio_appropriate == "No"
                    and self.staffing_input_ideal_ratio
                )
            )
            or not self.staffing_select_workload
            or not self.staffing_select_rate_workload
            or not self.staffing_select_charge_present
            or not (
                self.staffing_select_charge_present == "Yes"
                and self.staffing_select_charge_assignment
            )
            or not self.staffing_select_overall
        ):
            yield ReportState.set_user_is_loading(False)
            return rx.toast.error(
                "Missing information. Please check form and complete required questions.",
                close_button=True,
            )

        # Check all our values for validity.
        if (
            self.staffing_select_ratio
            not in constants_types.STAFFING_SELECT_RATIO_SELECTIONS
            or not isinstance(self.staffing_input_actual_ratio, int)
            or (
                self.staffing_select_ratio == "Yes"
                and self.staffing_select_ratio_appropriate
                not in constants_types.STAFFING_SELECT_RATIO_APPROPRIATE
            )
            or not isinstance(self.staffing_input_ideal_ratio, int)
            or self.staffing_select_workload
            not in constants_types.STAFFING_SELECT_WORKLOAD_SELECTIONS
            or not isinstance(self.staffing_select_rate_workload, int)
            or (5 < self.staffing_select_rate_workload < 1)
            or self.staffing_select_charge_present
            not in constants_types.STAFFING_SELECT_CHARGE_PRESENT_SELECTIONS
            or (
                self.staffing_select_charge_present == "Yes"
                and self.staffing_select_charge_assignment
                not in constants_types.STAFFING_SELECT_CHARGE_ASSIGNMENT_SELECTIONS
            )
            or not isinstance(self.staffing_check_rapid_response, bool)
            or not isinstance(self.staffing_check_behavioral_response, bool)
            or not isinstance(self.staffing_check_transport, bool)
            or not isinstance(self.staffing_check_phlebotomy, bool)
            or not isinstance(self.staffing_check_cvad, bool)
            or not isinstance(self.staffing_check_ivt, bool)
            or not isinstance(self.staffing_check_wocn, bool)
            or not isinstance(self.staffing_check_chaplain, bool)
            or not isinstance(self.staffing_check_educator, bool)
            or not isinstance(self.staffing_select_overall, int)
            or not isinstance(self.staffing_input_comments, str)
        ):
            # Grab all relevant fields by key to see what is going wrong.
            keys = [key for key in ReportState.__fields__.keys() if "staffing" in key]
            debug_dict = {}
            for key in keys:
                value = self.get_value(key)
                debug_dict[key] = value
                logger.warning(f"{key} - {value} - {type(value)}")

            yield ReportState.user_is_loading(False)
            return rx.toast.error(
                "Validity check failed. Contact support if problem persists.",
                close_button=True,
            )

        # Check all our values for sanity.
        error_messages = []
        if self.staffing_input_actual_ratio and self.staffing_input_actual_ratio > 15:
            error_messages.append(
                "Ratio can't be higher than 1:15. Please contact site admin if a higher ratio applies to you."
            )
        if self.staffing_input_ideal_ratio and self.staffing_input_ideal_ratio > 15:
            error_messages.append(
                "Ratio can't be higher than 1:15. Please contact site admin if a higher ratio applies to you."
            )
        for message in error_messages:
            yield rx.toast.error(message, close_button=True)

        # If all checks complete and everything is groovy.
        if not error_messages:
            self.report_dict["staffing"] = {
                "ratio": {
                    "has_ratio": self.staffing_select_ratio,
                    "actual_ratio": self.staffing_input_actual_ratio,
                    "is_appropriate": self.staffing_select_ratio_appropriate,
                    "ideal_ratio": self.staffing_input_ideal_ratio,
                },
                "workload": {
                    "amount": self.staffing_select_workload,
                    "eos_rating": self.staffing_select_rate_workload,
                },
                "charge": {
                    "has_charge": self.staffing_select_charge_present,
                    "takes_patients": self.staffing_select_charge_assignment,
                },
                "resources": {
                    "rapid_response": self.staffing_check_rapid_response,
                    "behavioral_response": self.staffing_check_behavioral_response,
                    "transport": self.staffing_check_transport,
                    "phlebotomy": self.staffing_check_phlebotomy,
                    "cvad": self.staffing_check_cvad,
                    "iv_team": self.staffing_check_ivt,
                    "wocn": self.staffing_check_wocn,
                    "chaplain": self.staffing_check_chaplain,
                },
                "ratings": {"overall": self.staffing_select_overall},
                "comments": self.staffing_input_comments,
            }
            yield ReportState.submit_full_report()

    #################################################################
    # REPORT SUBMISSION \ HANDLERS
    #################################################################

    def submit_full_report(self) -> Iterable[Callable]:
        """
        Prepare and submit full report to database.
        """
        try:
            if not (
                self.report_dict["report_id"]
                and self.report_dict["hospital_id"]
                and self.report_dict["user"]
                and self.report_dict["compensation"]
                and self.report_dict["assignment"]
                and self.report_dict["staffing"]
            ):
                return rx.toast.error(
                    "Data corrupted. Recheck report for completion.", close_button=True
                )

            # # Ensure that no report UUID's conflict.
            # supabase_no_report_id_conflict(self.access_token, self.report_dict["report_id"])

            # # Submit report to supabase.
            # supabase_submit_full_report(self.access_token, self.report_dict)

            # updated_data = supabase_update_user_info(
            #     self.access_token,
            #     self.user_id,
            #     data={
            #         "needs_onboard": False,
            #     },
            # )

            # self.user_info.update(updated_data)
            # yield ReportState.moderate_user_entries(self.report_dict)
            # yield rx.redirect("/report/full-report/complete")

        except Exception:
            yield rx.toast.error("Something went wrong", close_button=True)

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
