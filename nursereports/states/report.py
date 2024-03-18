from ..server.supabase.report import (
    supabase_no_report_id_conflict,
    supabase_submit_full_report
)
from ..states.page import PageState
from loguru import logger
from typing import Callable, Iterable

import httpx
import json
import os
import uuid
import re
import reflex as rx
import rich
import time

from dotenv import load_dotenv
load_dotenv()

api_url = os.getenv("SUPABASE_URL")
api_key = os.getenv("SUPABASE_ANON_KEY")
anyscale_url = os.getenv("ANYSCALE_URL")
anyscale_api_key = os.getenv("ANYSCALE_API_KEY")

class ReportState(PageState):
    """
    State for the report, variables grouped into the three major
    groups of the report; compensation, staffing, and assignment.
    """

    #################################################################
    #
    # COMPENSATION VARIABLES
    #
    #################################################################

    comp_select_emp_type: str

    comp_select_pay_type: str

    comp_input_pay_amount: int

    comp_select_diff_response: str

    comp_input_diff_nights: int

    comp_input_diff_weekends: int

    comp_select_incentive_response: str

    comp_input_incentive_amount: int

    comp_select_certifications: str

    comp_select_shift: str

    comp_select_weekly_shifts: str

    comp_select_hospital_experience: str

    comp_select_total_experience: str

    comp_check_benefit_pto: bool = False

    comp_check_benefit_parental: bool = False

    comp_check_benefit_insurance: bool = False

    comp_check_benefit_retirement: bool = False

    comp_check_benefit_pro_dev: bool = False

    comp_check_benefit_tuition: bool = False

    comp_select_comp_adequate: str

    comp_input_comments: str

    comp_select_overall: str

    comp_error_message: str

    def set_comp_input_pay_amount(self, pay: str) -> None:
        if bool(re.match(r"^[0-9]+$", pay)):
            self.comp_input_pay_amount = int(pay)
        if pay == "":
            self.comp_input_pay_amount = 0

    def set_comp_select_pay_type(self, type: str) -> None:
        self.comp_select_pay_type = type
        self.comp_input_pay_amount = 0

    def set_comp_select_diff_response(self, response: str) -> None:
        self.comp_input_diff_nights = 0
        self.comp_input_diff_weekends = 0
        self.comp_select_diff_response = response

    def set_comp_input_diff_nights(self, pay: str) -> None:
        if bool(re.match(r"^[0-9]+$", pay)):
            self.comp_input_diff_nights = int(pay)
        if pay == "":
            self.comp_input_diff_nights = 0

    def set_comp_input_diff_weekends(self, pay: str) -> None:
        if bool(re.match(r"^[0-9]+$", pay)):
            self.comp_input_diff_weekends = int(pay)
        if pay == "":
            self.comp_input_diff_weekends = 0

    def set_comp_select_incentive_response(self, response: str) -> None:
        self.comp_select_incentive_response = response
        self.comp_input_incentive_amount = 0

    def set_comp_input_incentive_amount(self, pay: str) -> None:
        if bool(re.match(r"^[0-9]+$", pay)):
            self.comp_input_incentive_amount = int(pay)
        if pay == "":
            self.comp_input_incentive_amount = 0

    @rx.var
    def is_hourly(self) -> bool:
        if self.comp_select_pay_type:
            return True if self.comp_select_pay_type == "Hourly" else False

    @rx.var
    def is_pay_invalid(self) -> bool:
        if self.comp_input_pay_amount or self.comp_input_pay_amount == 0:
            if (self.comp_input_pay_amount < 20 or
                self.comp_input_pay_amount > 200) and self.is_hourly:
                return True
            if (self.comp_input_pay_amount < 500 or
                self.comp_input_pay_amount > 12000) and not self.is_hourly:
                return True
        else:
            return False
        
    @rx.var
    def is_experience_invalid(self) -> bool:
        if self.comp_select_hospital_experience and\
            self.comp_select_total_experience:
            if self.comp_select_hospital_experience == 'More than 25 years':
                hospital_experience = 26
            elif self.comp_select_hospital_experience == 'Less than a year':
                hospital_experience = 0
            else:
                hospital_experience = int(self.comp_select_hospital_experience)

            if self.comp_select_total_experience == 'More than 25 years':
                total_experience = 26
            elif self.comp_select_total_experience == 'Less than a year':
                total_experience = 0
            else:
                total_experience = int(self.comp_select_total_experience)
            
            if (total_experience - hospital_experience) < 0:
                return True
            else:
                return False
        else:
            return False

    @rx.var
    def gets_differential(self) -> bool:
        return True if self.comp_select_diff_response == "Yes" else False

    @rx.var
    def gets_incentive(self) -> bool:
        return True if self.comp_select_incentive_response == "Yes" else False

    @rx.var
    def is_weekly(self) -> bool:
        return True if self.comp_select_pay_type == "Weekly" else False
    
    @rx.var
    def compensation_is_inadequate(self) -> bool:
        return True if self.comp_select_comp_adequate == "No" else False
        
    @rx.var
    def comp_comments_chars_left(self) -> int:
        if self.comp_input_comments:
            return 1000 - len(self.comp_input_comments)
        
    @rx.var
    def comp_comments_chars_over(self) -> bool:
        if self.comp_comments_chars_left:
            if self.comp_comments_chars_left < 0:
                return True
            else:
                return False
    
    @rx.var
    def comp_overall_description(self) -> str:
        if self.comp_select_overall == "a":
            return "Great"
        if self.comp_select_overall == "b":
            return "Good"
        if self.comp_select_overall == "c":
            return "So-so"
        if self.comp_select_overall == "d":
            return "Bad"
        if self.comp_select_overall == "f":
            return "Terrible"
        
    @rx.var
    def comp_overall_background(self) -> str:
        if self.comp_select_overall == "a":
            return "rgb(95, 163, 217)"
        if self.comp_select_overall == "b":
            return "rgb(95, 154, 100)"
        if self.comp_select_overall == "c":
            return "rgb(237, 234, 95)"
        if self.comp_select_overall == "d":
            return "rgb(197, 116, 57)"
        if self.comp_select_overall == "f":
            return "rgb(185, 65, 55)"
        
    @rx.var
    def comp_progress(self) -> int:
        progress = 0
        if self.comp_select_emp_type:
            progress = progress + 5
        if self.comp_select_pay_type:
            progress = progress + 5
        if self.comp_input_pay_amount and not\
            self.is_pay_invalid:
            progress = progress + 10
        if self.comp_select_diff_response:
            progress = progress + 10
        if self.comp_select_incentive_response:
            progress = progress + 5
        if self.comp_select_certifications:
            progress = progress + 5
        if self.comp_select_shift:
            progress = progress + 10
        if self.comp_select_weekly_shifts:
            progress = progress + 10
        if self.comp_select_hospital_experience and\
            self.comp_select_total_experience\
            and not self.is_experience_invalid:
            progress = progress + 20
        if self.comp_select_comp_adequate:
            progress = progress + 10
        if self.comp_select_overall:
            progress = progress + 10
        return progress
    
    @rx.var
    def comp_can_progress(self) -> bool:
        return True if self.comp_progress == 100 else False
    
    @rx.var
    def comp_has_error(self) -> bool:
        return True if self.comp_error_message else False

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

    @rx.cached_var
    def hospital_units(self) -> list[str]:
        units = []
        units.append("I don't see my unit")
        return units
    
    @rx.cached_var
    def hospital_areas(self) -> list[str]:
        areas = []
        areas.append("I don't see my area or role")
        return areas
    
    @rx.var
    def has_unit(self) -> bool:
        return True if self.assign_select_specific_unit else False

    @rx.var
    def is_unit(self) -> bool:
        return True if self.assign_select_specific_unit == "Yes" else False
    
    @rx.var
    def unit_not_present(self) -> bool:
        return True if self.assign_select_unit == "I don't see my unit"\
            else False
    
    @rx.var
    def area_not_present(self) -> bool:
        return True if self.assign_select_area == "I don't see my area or role"\
            else False
            
    @ rx.var
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
        if self.assign_select_acuity == "Intensive" or\
            self.assign_select_acuity == "Intermediate" or\
            self.assign_select_acuity == "Floor":
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
        if self.staffing_select_ratio_unsafe == "Always" or\
        self.staffing_select_ratio_unsafe == "Usually" or\
        self.staffing_select_ratio_unsafe == "Sometimes":
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
        return

    #################################################################
    #
    # UNCATEGORIZED REPORT VARIABLES
    #
    #################################################################
           
    id: str = str(uuid.uuid4())
    
    #################################################################
    #
    # REPORT SUBMISSION \ HANDLERS
    #
    #################################################################
        
    def handle_submit_compensation(self) -> Callable:
        if not self.comp_can_progress:
            self.comp_error_message = \
                "Some fields incomplete or invalid."
        if len(self.comp_input_comments) > 1000:
            self.comp_error_message = \
                "Comments contain too many characters."
            return
        self.comp_error_message = ""
        return rx.redirect(
            f"/report/submit/{self.hosp_id_param}/assignment"
        )

    def handle_submit_assignment(self) -> Callable:
        if not self.assign_can_progress:
            self.assign_error_message = \
                "Some fields incomplete or invalid."
            return
        if len(self.assign_input_comments) > 1000:
            self.assign_error_message = \
                "Comments contain too many characters."
            return
        self.assign_error_message = ""
        return rx.redirect(
            f"/report/submit/{self.hosp_id_param}/staffing"
            )

    def handle_submit_staffing(self) -> Callable:
        if not self.staffing_can_progress:
            self.staffing_error_message = \
                "Some fields incomplete or invalid."
            return
        if self.has_ratios and not self.ratio_is_valid:
            self.staffing_error_message = \
                "Some fields incomplete or invalid."
        if len(self.staffing_input_comments) > 1000:
            self.staffing_error_message = \
                "Comments contain too many characters."
            return
        self.staffing_error_message = ""
        return ReportState.submit_report
    
    def submit_report(self) -> Iterable[Callable]:
        """
        Final checkpoint for submitting report.

        1. Check that all sections are completed to 100%, if not then
        redirect to those sections and add warning message.

        2. Ensure that no duplicated report ID's exist. If so,
        attempts to regen code 5 times before fails to server error.

        3. Submits report to /report

        4. Submits user entries to AI moderation.
        """
        if not self.comp_can_progress:
            self.comp_error_message = \
                "Some fields incomplete or invalid."
            return rx.redirect(
                f"/report/submit/{self.hosp_id_param}/compensation"
            )
        if not self.assign_can_progress:
            self.assign_error_message = \
                "Some fields incomplete or invalid."
            return rx.redirect(
                f"/report/submit/{self.hosp_id_param}/assignment"
            )
        if not self.staffing_can_progress:
            self.staffing_can_progress = \
                "Some fields incomplete or invalid."
            return rx.redirect(
                f"/report/submit/{self.hosp_id_param}/staffing"
            )
        if not self.ensure_no_duplicate_report_id():
            self.staffing_error_message = \
                "Server error - UUID conflict check failed."
            return
        response = supabase_submit_full_report(
            self.access_token, self.prepare_report_dict()
        )
        if response['success']:
            yield ReportState.moderate_user_entries
            yield rx.redirect(
                f"/report/submit/{self.hosp_id_param}/complete"
            )
        else:
            self.staffing_error_message = \
                "Server error - Failed to upload report to database."

    def prepare_report_dict(self) -> dict:
        report = {
            "id": self.id,
            "user_id": self.user_claims['payload']['sub'],
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
            "assign_select_unit": self.assign_select_unit,
            "assign_input_unit_name": self.assign_input_unit_name,
            "assign_select_acuity": self.assign_select_acuity,
            "assign_select_area": self.assign_select_area,
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
    
    def ensure_no_duplicate_report_id(self) -> bool:
        response = supabase_no_report_id_conflict(
            self.access_token, self.id
            )
        if response['success']:
            return True
        if not response['success'] and response['status'] == "Conflict":
            for x in range(4):
                logger.warning(
                    f"""
                    Found a uuid conflict in /report with {self.id}.
                    Trying {4-x} more times to generate new uuid.
                    """
                    )
                self.id = uuid.uuid4()
                response = supabase_no_report_id_conflict(
                    self.access_token, self.id
                )
                if response['success']:
                    return True
                else:
                    time.sleep(1)
            return False
        return False

    def reset_report(self) -> None:
        self.reset()

    #################################################################
    #
    # NAVIGATION EVENTS & PAGE PARAMETERS
    #
    #################################################################

    def report_nav(self, target_url: str) -> Callable:
        return rx.redirect(f"/report/submit/{self.hosp_id_param}/{target_url}")

    #################################################################
    #
    # REPORT MODERATION
    #
    #################################################################

    @rx.background
    async def moderate_user_entries(self) -> None:
        """
        Send all user entered fields to AI for moderation. AI will send
        response flagging entries
        """
        user_entry_dict = {}
        if self.comp_input_comments:
            user_entry_dict['comp_input_comments'] = self.comp_input_comments
        if self.staffing_input_comments:
            user_entry_dict['staffing_input_comments'] = self.staffing_input_comments
        if self.assign_input_unit_name:
            user_entry_dict['assign_input_unit_name'] = self.assign_input_unit_name
        if self.assign_input_area:
            user_entry_dict['assign_input_area'] = self.assign_input_area
        if self.assign_input_comments:
            user_entry_dict['assign_input_comments'] = self.assign_input_comments

        system_prompt = """You moderate user entries by nurses for a hospital
        review site. Output responses in JSON"""
        user_prompt = f"""Flag user entries for racism, threats, links
        to other sites, spam, or personally identifiable information.
        User entries = {json.dumps(user_entry_dict)}"""
        url = f"{anyscale_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {anyscale_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
                 
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
                                "required": ["entry_name", "flag", "flag_reason"]
                            }
                        }
                    },
                    "required": ["entries"]
                }
            },
            "temperature": 0.5

        }

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                url=url,
                headers=headers,
                data=json.dumps(data)
            )
            if response.is_success:
                logger.debug("Retrieved moderation suggestions from Anyscale.")
                self.parse_moderation_suggestions(json.loads(response.content))
                return None
            else:
                logger.warning("User entry moderation to Anyscale unsuccessful.")
                return None

    def parse_moderation_suggestions(self, content) -> None:
        """
        flags['entries'] contains a list of dicts with keys 'entry_name', 'flag',
        and 'flag_reason'. If the flag is true, add entry to moderation data
        so that we can upload the flag_reason to our field _flag column to
        prevent other users from accessing and having the capability to 
        manually review that before releasing.
        """
        moderation_data = {}
        flags = json.loads(content['choices'][0]['message']['content'])
        for entry in flags['entries']:
            """
            Add entry. For example if assign_input_comments has issue, add
            assign_input_comments_flag with the reason so we can manually
            check it later.
            """
            if entry['flag'] is True:
                flag_name = f"{entry['entry_name']}_flag".replace(" ", "_")
                moderation_data[flag_name] = entry['flag_reason']

        if moderation_data:
            logger.warning(f"Found some entries requiring moderation. {moderation_data}")
            url = f"{api_url}/rest/v1/reports?id=eq.{self.id}"
            data = json.dumps(moderation_data)
            headers = {
                "apikey": api_key,
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal",
            }
            response = httpx.patch(
                url=url,
                headers=headers,
                data=data
            )
            if response.is_success:
                logger.debug(
                    f"Successfully flagged entries in {self.id}\
                    for moderation in database."
                    )
                return
            else:
                logger.critical(
                    f"Error calling API to moderate {self.id}."
                    )
                rich.inspect(response)
                return
        else:
            logger.debug(
                f"User report {self.id} seems ok. No entries found\
                requiring moderation."
                )
            return
