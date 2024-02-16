
from loguru import logger
from ..states.cookie import CookieState
from typing import Callable, Iterable

import httpx
import json
import os
import uuid
import re
import reflex as rx
import rich

from dotenv import load_dotenv
load_dotenv()

api_url = os.getenv("SUPABASE_URL")
api_key = os.getenv("SUPABASE_ANON_KEY")
anyscale_url = os.getenv("ANYSCALE_URL")
anyscale_api_key = os.getenv("ANYSCALE_API_KEY")

class ReportState(CookieState):
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

    comp_check_benefit_pto: bool

    comp_check_benefit_parental: bool

    comp_check_benefit_insurance: bool

    comp_check_benefit_retirement: bool

    comp_check_benefit_pro_dev: bool

    comp_check_benefit_tuition: bool

    comp_select_comp_adequate: str

    comp_input_comments: str

    comp_select_overall: str

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
        if self.comp_input_pay_amount:
            if self.comp_input_pay_amount < 1 or\
                self.comp_input_pay_amount > 125 and self.is_hourly:
                return True
            if self.comp_input_pay_amount < 1 or\
                self.comp_input_pay_amount > 12000 and not self.is_hourly:
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
            return 500 - len(self.comp_input_comments)
        
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

    assign_select_teamwork: str

    assign_select_providers: str

    assign_select_contributions: str

    assign_select_impact: str

    assign_select_management: str

    assign_select_leaving: str

    assign_select_leaving_reason: str

    assign_select_recommend: str

    assign_input_comments: str

    assign_select_overall: str

    def set_assign_select_specific_unit(self, unit: str) -> None:
        self.assign_select_acuity = ""
        self.assign_input_unit_abbr = ""
        self.assign_input_unit_name = ""
        self.assign_select_unit = ""
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
            if len(self.assign_input_unit_name) > 45:
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
            return 500 - len(self.assign_input_comments)
        
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

        if self.assign_select_teamwork:
            progress = progress + 10
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
    


    #################################################################
    #
    # STAFFING VARIABLES
    #
    #################################################################

    staffing_input_ratio: int

    staffing_select_ratio_unsafe: str

    staffing_select_workload: str

    staffing_select_float: str

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
            return 500 - len(self.staffing_input_comments)
        
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

    #################################################################
    #
    # UNCATEGORIZED REPORT VARIABLES
    #
    #################################################################
           
    id: str = str(uuid.uuid4())

    @rx.var
    def comp_is_active(self) -> bool:
        return True if "compensation" in self.router.page.full_raw_path else False

    @rx.var
    def staffing_is_active(self) -> bool:
        return True if "staffing" in self.router.page.full_raw_path else False

    @rx.var
    def assign_is_active(self) -> bool:
        return True if "assignment" in self.router.page.full_raw_path else False

    @rx.var
    def completed_report(self) -> bool:
        if self.comp_progress == 100 and\
        self.staffing_progress == 100 and\
        self.assign_progress == 100:
            return True
        else:
            return False
        
    @rx.cached_var
    def hosp_info(self) -> dict:
        if self.summary_id:
            url = f"{api_url}/rest/v1/hospitals"\
            f"?hosp_id=eq.{self.summary_id}"\
            "&select=*"
            headers = {
                "apikey": api_key,
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }
            response = httpx.get(
                url=url,
                headers=headers
            )
            if response.is_success:
                logger.debug("Response from Supabase.")
                hospital = json.loads(response.content)
                return hospital[0]
            else:
                logger.critical("Getting search results failed!")
    
    #################################################################
    #
    # REPORT SUBMISSION & HANDLERS
    #
    #################################################################
        
    def handle_submit_comp(self, form_data: dict) -> Iterable[Callable]:
        from ..states.navbar import NavbarState

        if len(self.comp_input_comments) > 500:
            return NavbarState.set_alert_message(
                """Text input field contains too many characters! Please limit
                your response to less than 500 characters."""
                )
        elif self.is_pay_invalid or self.is_experience_invalid:
            return NavbarState.set_alert_message(
                """Some fields contain invalid information. Please fix
                before attempting to proceed."""
                )
        else:
            return rx.redirect(f"/report/submit/{self.report_id}/assignment/summary")

    def handle_submit_assign(self, form_data: dict) -> Iterable[Callable]:
        from ..states.navbar import NavbarState

        if len(self.assign_input_comments) > 500:
            return NavbarState.set_alert_message(
                """Text input field contains too many characters! Please limit
                your response to less than 500 characters."""
                )
        else:
            return rx.redirect(f"/report/submit/{self.report_id}/staffing/summary")

    def handle_submit_staffing(self, form_data: dict) -> Iterable[Callable] | Callable:
        from ..states.navbar import NavbarState

        if len(self.staffing_input_comments) > 500:
            return NavbarState.set_alert_message(
                """Text input field contains too many characters! Please limit
                your response to less than 500 characters."""
                )
        elif self.has_ratios and not self.ratio_is_valid:
            return NavbarState.set_alert_message(
                """Some fields contain invalid information. Please fix
                before attempting to proceed."""
                )
        elif self.comp_can_progress and self.staffing_can_progress and self.assign_can_progress:
            if self.if_report_id_exists():
                logger.debug("Found a duplicate uuid! Hell froze over! Buy a lottery ticket!")
                self.id = str(uuid.uuid4())
            yield ReportState.submit_full_report
            yield ReportState.moderate_user_entries
        else:
            yield NavbarState.set_alert_message(
                "Unable to submit report. Server-side error."
            )

    def submit_full_report(self) -> Iterable[Callable]:
        from ..states.navbar import NavbarState

        url = f"{api_url}/rest/v1/reports"
        data = json.dumps(self.prepare_report_dict())
        headers = {
            "apikey": api_key,
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        response = httpx.post(
            url=url,
            headers=headers,
            data=data
        )
        
        if response.is_success:
            logger.debug("Report submitted successfully.")
            yield rx.redirect(f"/report/submit/{self.report_id}/complete")
        else:
            logger.critical("Error while submitting report!")
            yield rx.call_script("window.location.reload")
            yield NavbarState.set_alert_message(f"{response.reason_phrase} - {response.text}")

    def prepare_report_dict(self) -> dict[str, str | int | None]:
        report = {
            "id": self.id,
            "user_id": self.claims['sub'],
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
            "assign_select_teamwork": self.assign_select_teamwork,
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
            "staffing_select_float": self.staffing_select_float,
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
    
    def if_report_id_exists(self) -> bool:
        """Check if generated uuid exists in report database."""
        url = f"{api_url}/rest/v1/reports?id=eq.{self.id}&select=*"
        headers = {
            "apikey": api_key,
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        response = httpx.get(
            url=url,
            headers=headers
        )

        if response.is_success:
            logger.debug("Successfully checked for duplicate report id's.")
            rich.inspect(response)
            return True if json.loads(response.content) else False
        else:
            logger.critical("Unable to check for duplicate report id's.")
            rich.inspect(response)

    #################################################################
    #
    # NAVIGATION EVENTS & PAGE PARAMETERS
    #
    #################################################################

    @rx.var
    def summary_id(self) -> str:
        """
        Pulls params from /report/summary/{summary_id}
        """
        return self.router.page.params.get('summary_id')

    @rx.var
    def report_id(self) -> str:
        """
        Pulls params from /report/submit/{report_id}/report_page
        """
        return self.router.page.params.get('report_id')

    def report_nav(self, target_url: str) -> Callable:
        """
        Takes a target_url and determines if on summary page or report
        page to route with medicare ID appropriately.
        """
        from ..states.navbar import NavbarState

        if target_url == 'summary':
            return rx.redirect(f"/report/summary/{self.report_id}/")
        else:
            if self.report_id:
                return rx.redirect(f"/report/submit/{self.report_id}/{target_url}")
            elif self.summary_id:
                return rx.redirect(f"/report/submit/{self.summary_id}/{target_url}")
            else:
                return NavbarState.set_alert_message(
                    f"Invalid URL target - {target_url}"
            )
                
    def clear_and_nav_to_compensation(self) -> Iterable[Callable]:
        """
        Reset all vars in ReportState to prep for a new report. Do it
        using the button nav between summary and compensation so that
        user accidentally hitting back can still go forward back to
        their report stored in state.
        """
        yield rx.redirect(f"/report/submit/{self.summary_id}/compensation/summary")
        self.reset()

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

        system_prompt = """You moderate user entries for a hospital
        review site, outputting responses in JSON"""
        user_prompt = f"""Flag user entries for abusive/racist language, links
        to other sites, or spam. User entries = {json.dumps(user_entry_dict)}"""
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

        async with httpx.AsyncClient(timeout=15.0) as client:
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
                logger.debug("Successfully flagged entries for moderation in database.")
                return None
            else:
                logger.critical("Error calling API for moderation.")
                rich.inspect(response)
                return None
        else:
            logger.debug("No entries found requiring moderation.")
            return None

