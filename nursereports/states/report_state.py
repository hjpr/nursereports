from . import constants_types
from ..states import HospitalState, PageState
from ..server.secrets import groq_key
from ..server.supabase import (
    supabase_user_edit_report,
    supabase_user_patch_report,
    supabase_get_full_report_info,
    supabase_get_hospital_info,
    supabase_submit_full_report,
    supabase_update_hospital_departments,
)
from datetime import datetime, timezone
from loguru import logger
from groq import Groq
from typing import Callable, Iterable, Literal

import copy
import json
import uuid
import pprint
import reflex as rx
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
    uuid_timeout: int

    # Units areas and roles pulled for user selection at report load.
    hospital_units: list[str]
    hospital_areas: list[str]
    hospital_roles: list[str]

    # Full report dictionary.
    report_dict: dict[str, bool | int | str]

    @rx.var
    def mode(self) -> Literal["", "edit", "full-report", "pay-report", "red-flag"]:
        return self.router.page.params.get("report_mode", "")

    def event_state_report_flow(self) -> Iterable[Callable]:
        """
        Ensures that report navigation contains the proper information before proceeding
        """
        if not self.mode or not self.hospital_id or not self.hospital_info:
            if self.hospital_id:
                yield rx.redirect(f"/hospital/{self.hospital_id}")
            else:
                yield rx.redirect("/dashboard")

    def event_state_edit_user_report(self, report_id: str, hospital_id: str) -> Iterable[Callable]:
        """
        Loads report data into state for user to make edits.
        """
        try:
            logger.debug(f"{self.user_claims_id} is attempting to edit {report_id} for {hospital_id}")
            # Reset all report variables.
            self.reset()

            # Populate other report details to state.
            self.report_id = report_id
            self.hospital_id = hospital_id

            # Load report to edit into state.
            report = supabase_get_full_report_info(self.access_token, report_id)

            # Load hospital info into state.
            self.hospital_info = supabase_get_hospital_info(
                self.access_token, self.hospital_id
            )

            # Set available units/areas/roles for user selection to state.
            self.hospital_units = list(self.hospital_info.get("departments", {}).get("units", []))
            self.hospital_units.append("I don't see my unit")
            self.hospital_areas = list(self.hospital_info.get("departments", {}).get("areas", []))
            self.hospital_areas.append("I don't see my area")
            self.hospital_roles = list(self.hospital_info.get("departments", {}).get("roles", []))
            self.hospital_roles.append("I don't see my role")

            # Set up report_dict
            self.report_dict["report_id"] = self.report_id
            self.report_dict["hospital_id"] = self.hospital_id
            self.report_dict["user_id"] = self.user_claims_id
            self.report_dict["user"] = {
                "professional": copy.deepcopy(report["user"]["professional"]),
                "trust": report["user"]["trust"],
                "ip_addr": self.router.session.client_ip,
                "host": self.router.headers.host,
                "user_agent": self.router.headers.user_agent,
            }
            self.report_dict["hospital"] = copy.deepcopy(report["hospital"])
            self.report_dict["moderation"] = copy.deepcopy(report["moderation"])
            self.report_dict["social"] = copy.deepcopy(report["social"])
            self.report_dict["compensation"] = {}
            self.report_dict["assignment"] = {}
            self.report_dict["staffing"] = {}

            self.report_dict["created_at"] = str(datetime.now(timezone.utc).isoformat(timespec="seconds"))
            self.report_dict["submitted_at"] = report["submitted_at"]

            # Set compensation to state.
            self.comp_select_emp_type = report["compensation"]["emp_type"]
            self.comp_select_pay_type = report["compensation"]["pay_type"]
            self.comp_input_pay_hourly = report["compensation"]["pay"]["hourly"]
            self.comp_input_pay_weekly = report["compensation"]["pay"]["weekly"]
            self.comp_input_pay_night = report["compensation"]["pay"]["night"]
            self.comp_input_pay_weekend = report["compensation"]["pay"]["weekend"]
            self.comp_input_pay_weekend_night = report["compensation"]["pay"]["weekend_night"]
            self.comp_select_shift = report["compensation"]["shift"]
            self.comp_select_weekly_shifts = report["compensation"]["weekly_shifts"]
            hospital_experience = str(report["compensation"]["experience"]["hospital"])
            total_experience = str(report["compensation"]["experience"]["total"])
            self.comp_select_hospital_experience = hospital_experience if hospital_experience != "26" else "More than 25 years"
            self.comp_select_total_experience = total_experience if total_experience != "26" else "More than 25 years"

            self.comp_check_benefit_pto = report["compensation"]["benefits"]["pto"]
            self.comp_check_benefit_parental = report["compensation"]["benefits"]["parental_leave"]
            self.comp_check_benefit_insurance = report["compensation"]["benefits"]["insurance"]
            self.comp_check_benefit_retirement = report["compensation"]["benefits"]["retirement"]
            self.comp_check_benefit_reimbursement = report["compensation"]["benefits"]["reimbursement"]
            self.comp_check_benefit_tuition = report["compensation"]["benefits"]["tuition"]
            self.comp_select_overall = report["compensation"]["ratings"]["overall"]
            self.comp_input_comments = report["compensation"]["comments"]

            # Set assignment to state.
            self.assign_select_classify = report["assignment"]["classify"]
            self.assign_select_unit = "I don't see my unit" if report["assignment"]["unit"]["entered_unit"] else report["assignment"]["unit"]["selected_unit"]
            self.assign_input_unit = report["assignment"]["unit"]["entered_unit"]
            self.assign_select_area = "I don't see my area" if report["assignment"]["area"]["entered_area"] else report["assignment"]["area"]["selected_area"]
            self.assign_input_area = report["assignment"]["area"]["entered_area"]
            self.assign_select_role = "I don't see my role" if report["assignment"]["role"]["entered_role"] else report["assignment"]["role"]["selected_role"]
            self.assign_input_role = report["assignment"]["role"]["entered_role"]
            self.assign_select_acuity = report["assignment"]["unit"]["acuity"]
            self.assign_select_specialty_1 = report["assignment"]["specialty"]["specialty_1"]
            self.assign_select_specialty_2 = report["assignment"]["specialty"]["specialty_2"]
            self.assign_select_specialty_3 = report["assignment"]["specialty"]["specialty_3"]
            self.assign_select_rate_nurses = report["assignment"]["ratings"]["nurses"]
            self.assign_select_rate_nurse_aides = report["assignment"]["ratings"]["nurse_aides"]
            self.assign_select_rate_physicians = report["assignment"]["ratings"]["physicians"]
            self.assign_select_rate_management = report["assignment"]["ratings"]["management"]
            self.assign_select_recommend = report["assignment"]["recommend"]
            self.assign_select_overall = report["assignment"]["ratings"]["overall"]
            self.assign_input_comments = report["assignment"]["comments"]

            # Set staffing to state.
            self.staffing_select_ratio = report["staffing"]["ratio"]["has_ratio"]
            self.staffing_input_actual_ratio = report["staffing"]["ratio"]["actual_ratio"]
            self.staffing_select_ratio_appropriate = report["staffing"]["ratio"]["is_appropriate"]
            self.staffing_input_ideal_ratio = report["staffing"]["ratio"]["ideal_ratio"]
            self.staffing_select_workload = report["staffing"]["workload"]["amount"]
            self.staffing_select_rate_workload = report["staffing"]["workload"]["eos_rating"]
            self.staffing_select_charge_present = report["staffing"]["charge"]["has_charge"]
            self.staffing_select_charge_assignment = report["staffing"]["charge"]["takes_patients"]
            self.staffing_check_rapid_response = report["staffing"]["resources"]["rapid_response"]
            self.staffing_check_behavioral_response = report["staffing"]["resources"]["behavioral_response"]
            self.staffing_check_transport = report["staffing"]["resources"]["transport"]
            self.staffing_check_phlebotomy = report["staffing"]["resources"]["phlebotomy"]
            self.staffing_check_cvad = report["staffing"]["resources"]["cvad"]
            self.staffing_check_ivt = report["staffing"]["resources"]["iv_team"]
            self.staffing_check_wocn = report["staffing"]["resources"]["wocn"]
            self.staffing_check_chaplain = report["staffing"]["resources"]["chaplain"]
            self.staffing_check_educator = report["staffing"]["resources"]["educator"]
            self.staffing_select_overall = report["staffing"]["ratings"]["overall"]
            self.staffing_input_comments = report["staffing"]["comments"]

            # Navigate to the first page of report edit page.
            yield rx.redirect("/report/edit/compensation")
            yield ReportState.set_user_is_loading(False)

        except Exception as e:
            logger.critical(str(e))
            yield rx.toast.error("Error while retrieving report details.")
            yield ReportState.set_user_is_loading(False)

    def event_state_create_full_report(self, hospital_id: str) -> Iterable[Callable]:
        """
        Resets and prepares report state for user to make a new report.
        """
        try:
            # Reset all report variables.
            self.reset()

            # Set report UUID to state.
            self.report_id = str(uuid.uuid4())

            # Set CMS ID of report to state.
            self.hospital_id = hospital_id

            # Get hospital info by CMS ID and set to state.
            self.hospital_info = supabase_get_hospital_info(
                self.access_token, self.hospital_id
            )

            # Set available units/areas/roles for user selection to state.
            self.hospital_units = list(self.hospital_info.get("departments", {}).get("units", []))
            self.hospital_units.append("I don't see my unit")
            self.hospital_areas = list(self.hospital_info.get("departments", {}).get("areas", []))
            self.hospital_areas.append("I don't see my area")
            self.hospital_roles = list(self.hospital_info.get("departments", {}).get("roles", []))
            self.hospital_roles.append("I don't see my role")

            # Set user dict data to state.
            self.report_dict["report_id"] = self.report_id
            self.report_dict["hospital_id"] = self.hospital_id
            self.report_dict["user_id"] = self.user_claims_id
            self.report_dict["user"] = {
                "professional": copy.deepcopy(self.user_info["professional"]),
                "trust": self.user_info["account"]["trust"],
                "ip_addr": self.router.session.client_ip,
                "host": self.router.headers.host,
                "user_agent": self.router.headers.user_agent,
            }
            self.report_dict["hospital"] = {
                "name": self.hospital_info.get("hosp_name", ""),
                "address": self.hospital_info.get("hosp_addr", ""),
                "city": self.hospital_info.get("hosp_city", ""),
                "state": self.hospital_info.get("hosp_state", ""),
                "zip": self.hospital_info.get("hosp_zip", ""),
                "county": self.hospital_info.get("hosp_county", "")
            }
            self.report_dict["moderation"] = {"flagged": 0, "reason": ""}
            self.report_dict["compensation"] = {}
            self.report_dict["assignment"] = {}
            self.report_dict["staffing"] = {}
            self.report_dict["social"] = {"likes": {}, "comments": {}, "tags": {}}
            self.report_dict["created_at"] = str(datetime.now(timezone.utc).isoformat(timespec="seconds"))
            self.report_dict["submitted_at"] = None

            # Redirect to first page of full report.
            yield rx.redirect("/report/full-report/overview")
            yield ReportState.set_user_is_loading(False)

        except Exception as e:
            logger.critical(str(e))
            yield rx.toast.error("Error while setting up new report.")
            yield ReportState.set_user_is_loading(False)

    #################################################################
    # COMPENSATION
    #################################################################

    comp_select_emp_type: str = ""
    comp_select_pay_type: str = ""
    comp_input_pay_hourly: int = 0
    comp_input_pay_weekly: int = 0
    comp_input_pay_night: int = 0
    comp_input_pay_weekend: int = 0
    comp_input_pay_weekend_night: int = 0
    input_calculator: str = ""
    calculator_pay_value: str = "0"
    comp_select_shift: str = ""
    comp_select_weekly_shifts: str = ""
    comp_select_hospital_experience: str = ""
    comp_select_total_experience: str = ""
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
        else:
            return 1000

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
                error_messages.append(
                    "Hourly rate entered exceeds normal ranges ($15-$250/hr)."
                )
        if self.comp_input_pay_weekly:
            if not (800 <= self.comp_input_pay_weekly <= 15000):
                error_messages.append(
                    "Weekly rate entered exceeds normal ranges ($800-$15000/wk)."
                )
        if not (0 <= self.comp_input_pay_night <= 50):
            error_messages.append(
                "Night differential entered exceeds normal ranges ($1-$50/hr)."
            )
        if not (0 <= self.comp_input_pay_weekend <= 50):
            error_messages.append(
                "Weekend differential entered exceeds normal ranges ($1-$50/hr)."
            )
        if not (0 <= self.comp_input_pay_weekend_night <= 50):
            error_messages.append(
                "Weekend night differential entered exceeds normal ranges ($1-$50/hr)."
            )
        if len(self.comp_input_comments) > 1000:
            error_messages.append("Length of comment exceeds 1000 characters.")

        for message in error_messages:
            yield rx.toast.error(message, close_button=True)

        # If all checks are complete and everything is groovy.
        if not error_messages:
            # Build compensation section.
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
                    # Gives us the int value 0-26 instead of having to convert to int when parsing.
                    "hospital": self.years_hospital_experience.index(
                        self.comp_select_hospital_experience
                    ),
                    "total": self.years_hospital_experience.index(
                        self.comp_select_total_experience
                    ),
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

            # Professional data at report creation is stale, so update that to reflect current.
            self.report_dict["user"]["professional"]["experience"] = (
                self.years_hospital_experience.index(self.comp_select_total_experience)
            )

            yield rx.redirect(f"/report/{self.mode}/assignment")

    #################################################################
    # ASSIGNMENT
    #################################################################

    assign_select_classify: str = ""
    assign_select_unit: str = ""
    assign_select_area: str = ""
    assign_select_role: str = ""
    assign_input_unit: str = ""
    assign_input_area: str = ""
    assign_input_role: str = ""
    assign_select_acuity: str = ""
    assign_select_specialty_1: str = ""
    assign_select_specialty_2: str = ""
    assign_select_specialty_3: str = ""
    assign_select_rate_nurses: int = 0
    assign_select_rate_nurse_aides: int = 0
    assign_select_rate_physicians: int = 0
    assign_select_rate_management: int = 0
    assign_select_recommend: str = ""
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
        else:
            return 1000

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
                    and self.assign_select_area != "I don't see my area"
                )
                or (
                    self.assign_select_area
                    and self.assign_select_area == "I don't see my area"
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
            # Build assignment section.
            self.report_dict["assignment"] = {
                "classify": self.assign_select_classify,
                "unit": {
                    "selected_unit": self.assign_select_unit
                    if self.assign_select_unit != "I don't see my unit"
                    else "",
                    "entered_unit": self.assign_input_unit.upper(),
                    "acuity": self.assign_select_acuity,
                },
                "area": {
                    "selected_area": self.assign_select_area
                    if self.assign_select_area != "I don't see my area"
                    else "",
                    "entered_area": self.assign_input_area.upper(),
                },
                "role": {
                    "selected_role": self.assign_select_role
                    if self.assign_select_role != "I don't see my role"
                    else "",
                    "entered_role": self.assign_input_role.upper(),
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

            # Professional data at report creation is stale, so update that to reflect current.
            specialty = self.user_info.get("professional", {}).get("specialty", [])
            updated_specialty = list(
                set(specialty)
                | set(
                    filter(
                        None,
                        [
                            self.assign_select_specialty_1,
                            self.assign_select_specialty_2,
                            self.assign_select_specialty_3,
                        ],
                    )
                )
            )
            self.report_dict["user"]["professional"]["specialty"] = updated_specialty
            yield rx.redirect(f"/report/{self.mode}/staffing")

    #################################################################
    # STAFFING
    #################################################################

    staffing_select_ratio: str = ""
    staffing_input_actual_ratio: int = 0
    staffing_select_ratio_appropriate: str = ""
    staffing_input_ideal_ratio: int = 0
    calculator_toggle_ratio: str = ""
    calculator_ratio_value: str = ""
    staffing_select_workload: str = ""
    staffing_select_rate_workload: int = 0
    staffing_select_charge_present: str = ""
    staffing_select_charge_assignment: str = ""
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
        else:
            return 1000

    def handle_submit_staffing(self) -> Callable | Iterable[Callable]:
        # Check our values for completion.
        yield ReportState.set_user_is_loading(True)
        if (
            not (
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
                or (self.staffing_select_ratio == "No")
            )
            or not self.staffing_select_workload
            or not self.staffing_select_rate_workload
            or not (
                (
                    self.staffing_select_charge_present == "Yes"
                    and self.staffing_select_charge_assignment
                )
                or (self.staffing_select_charge_present == "No")
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
                    "educator": self.staffing_check_educator,
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
                    "Data corrupted. Recheck report for completion. If this persists, please contact support.",
                    close_button=True,
                )

            # Ensures that no report UUID's conflict. Submit either full report or update existing report.
            report = supabase_get_full_report_info(self.access_token, self.report_dict["report_id"])

            # If report and report matches user ID, we'll assume user is attempting to edit unless physics suspends and the UUID clashes.
            if report and report["user_id"]:
                self.report_dict["modified_at"] = str(datetime.now(timezone.utc).isoformat(timespec="seconds"))
                supabase_user_edit_report(self.access_token, self.report_dict)

            # If report not present then user is submitting a new report.
            if not report:
                self.report_dict["submitted_at"] = str(datetime.now(timezone.utc).isoformat(timespec="seconds"))
                supabase_submit_full_report(self.access_token, self.report_dict)

            # Update user data with relevant info once report is submitted.
            updated_status: str = "active"

            specialty = self.user_info.get("professional", {}).get("specialty", [])
            updated_specialty = list(
                set(specialty)
                | set(
                    filter(
                        None,
                        [
                            self.assign_select_specialty_1,
                            self.assign_select_specialty_2,
                            self.assign_select_specialty_3,
                        ],
                    )
                )
            )

            updated_experience: int = self.years_hospital_experience.index(
                self.comp_select_total_experience
            )

            ids = self.user_info.get("reports", {}).get("ids", [])
            updated_ids = list(set(ids) | set([self.report_dict["report_id"]]))

            num_full_reports = self.user_info.get("reports", []).get("num_full", 0)
            updated_num = num_full_reports + 1

            hospitals = self.user_info.get("saved", {}).get("hospitals", [])
            updated_hospitals = list(set(hospitals) | set([self.report_dict["hospital_id"]]))

            self.update_user_info_and_sync_locally(
                data={
                    "account": {"status": updated_status},
                    "professional": {
                        "specialty": updated_specialty,
                        "experience": updated_experience,
                    },
                    "reports": {"ids": updated_ids, "num_full": updated_num},
                    "saved" : {"hospitals": updated_hospitals}
                }
            )

            # Moderate our unit/area/role and comment entries
            self.moderate_user_entries()

            # Send update to unit/area/role if moderation ok or unmoderated AND entries present.
            if self.report_dict.get("moderation", {}).get("flagged", 0) in {0, 2} and (
                self.assign_input_unit
                or self.assign_input_area
                or self.assign_input_role
            ):
                units = self.hospital_info.get("departments", {}).get("units", [])
                updated_units = list(
                    set(units) | set(filter(None, [self.assign_input_unit.upper()]))
                )

                areas = self.hospital_info.get("departments", {}).get("areas", [])
                updated_areas = list(
                    set(areas) | set(filter(None, [self.assign_input_area.upper()]))
                )

                roles = self.hospital_info.get("departments", {}).get("roles", [])
                updated_roles = list(
                    set(roles) | set(filter(None, [self.assign_input_role.upper()]))
                )

                hospital_updates = {}
                hospital_updates["departments"] = {
                    "units": updated_units,
                    "areas": updated_areas,
                    "roles": updated_roles,
                }
                supabase_update_hospital_departments(self.hospital_id, hospital_updates)

            # Redirect user to the completed page for fireworks!
            self.reset()
            yield HospitalState.user_completed_report() # In case user navigates back to same hospital as reported. Forces info refresh.
            return rx.redirect(f"/report/{self.mode}/complete")

        except Exception as e:
            logger.warning(e)
            yield rx.toast.error(
                "Failed to submit report to database.", close_button=True
            )
            return ReportState.set_user_is_loading(False)

    def moderate_user_entries(self) -> None:
        """
        Send all user entered fields to AI for moderation.
        """
        try:
            job_location = f"{self.assign_input_unit} {self.assign_input_area} {self.assign_input_role}".strip()
            comments = f"{self.comp_input_comments} {self.assign_input_comments} {self.staffing_input_comments}".strip()
            ai_moderation_model = "llama-3.3-70b-versatile"

            if job_location or comments:
                if not job_location:
                    job_location = "EMPTY"
                if not comments:
                    comments = "EMPTY"
                client = Groq(api_key=groq_key)
                completion = client.chat.completions.create(
                    model=ai_moderation_model,
                    messages=[
                        {
                            "role": "system",
                            "content": textwrap.dedent("""
                                You moderate entries for a nurse review site. Entries may contain location data about where nurse works at hospital.
                                Entries may also contain comments nurses are allowed to share to their peers about pay, staffing, or work environment.
                                Output responses as JSON. Under key 'flagged', output a 1 for invalid entries flagged for containing violence, protected
                                health info, off-topic entries, nonsensical content, spam, advertisements, racism, sexism, or doxxing otherwise if valid
                                output a 0. Profanity and content conveying strong emotions is acceptable given it's on topic. Under key 'reason', if
                                entry is flagged give brief rationale otherwise output ''.
                                """),
                        },
                        {
                            "role": "user",
                            "content": f"User location or role: {job_location}. User comments: {comments}",
                        },
                    ],
                    temperature=0.7,
                    max_completion_tokens=1024,
                    top_p=1,
                    stream=False,
                    response_format={"type": "json_object"},
                    stop=None,
                )
                content = json.loads(completion.choices[0].message.content)

                # If moderation successful assign result, else assign an unmoderated result.
                if "flagged" and "reason" in content:
                    self.report_dict["moderation"] = content
                else:
                    self.report_dict["moderation"] = {
                        "flagged": 2,
                        "reason": "Unmoderated due to incorrectly structured moderation output.",
                    }

                # Send moderation results to report in database.
                if self.report_dict.get("moderation", {}).get("flagged", 0) in {1, 2}:
                    logger.debug(
                        "User entries were either flagged or unmoderated. Sending updates to database."
                    )
                    data = {}
                    data["report_id"] = self.report_id
                    data["moderation"] = self.report_dict.get("moderation").copy()
                    supabase_user_patch_report(self.access_token, data)
                else:
                    logger.debug(
                        f"Entries for report {self.report_id} by {self.user_claims_id} are cleared by {ai_moderation_model}"
                    )

            else:
                logger.debug(
                    f"{self.user_claims_id} hasn't entered any content to be moderated."
                )
        except Exception:
            import traceback
            traceback.print_exc()
            logger.warning(f"Moderation for {self.user_claims_id} failed.")
