
from loguru import logger
from ..states.cookie import CookieState
from typing import Callable, Iterable

import httpx
import json
import os
import reflex as rx
import rich

from dotenv import load_dotenv
load_dotenv()

api_url = os.getenv("SUPABASE_URL")
api_key = os.getenv("SUPABASE_ANON_KEY")

class ReportState(CookieState):
    """
    State for the report, variables grouped into the three major
    groups of the report; compensation, staffing, and assignment.
    """

    """
    Compensation fields and logic. ----------------------------------
    """

    pay_emp_type: str

    pay_amount: int

    pay_differential_response: str

    pay_differential_nights: int

    pay_differential_weekends: int

    pay_incentive_response: str

    pay_incentive_amount: int

    pay_shift: str

    pay_weekly_shifts: str

    pay_hospital_experience: str

    pay_total_experience: str

    pay_benefit_pto: bool

    pay_benefit_parental: bool

    pay_benefit_insurance: bool

    pay_benefit_retirement: bool

    pay_benefit_pro_dev: bool

    pay_benefit_tuition: bool

    pay_compensation: str

    pay_desired_changes: str

    pay_comments: str

    pay_overall: str

    def set_pay_amount(self, pay: int | str) -> None:
        if pay == '' or pay == '00':
            self.pay_amount = 0
        else:
            self.pay_amount = int(pay)

    def set_pay_emp_type(self, type: str) -> None:
        self.pay_emp_type = type
        self.pay_amount = 0

    def set_pay_differential(self, pay: str) -> None:
        self.pay_differential = pay
        self.pay_differential_nights = 0
        self.pay_differential_weekends = 0

    def set_pay_differential_nights(self, pay: str) -> None:
        if pay == '' or pay == '00':
            self.pay_differential_nights = 0
        else:
            self.pay_differential_nights = int(pay)

    def set_pay_differential_weekends(self, pay: str) -> None:
        if pay == '' or pay == '00':
            self.pay_differential_weekends = 0
        else:
            self.pay_differential_weekends = int(pay)

    def set_pay_incentive_response(self, response: str) -> None:
        self.pay_incentive_amount = 0
        self.pay_incentive_response = response


    def set_pay_compensation(self, response: str) -> None:
        self.pay_compensation = response
        self.pay_compensation_changes = ""

    @rx.var
    def is_pay_invalid(self) -> bool:
        if self.pay_amount < 1 or self.pay_amount > 125 and not self.is_contract:
            return True
        elif self.pay_amount < 1 or self.pay_amount > 12000 and self.is_contract:
            return True
        else:
            return False
        
    @rx.var
    def is_experience_invalid(self) -> bool:
        if self.pay_hospital_experience and self.pay_total_experience:
            if self.pay_hospital_experience == 'More than 25 years':
                hospital_experience = 26
            elif self.pay_hospital_experience == 'Less than a year':
                hospital_experience = 0
            else:
                hospital_experience = int(self.pay_hospital_experience)

            if self.pay_total_experience == 'More than 25 years':
                total_experience = 26
            elif self.pay_total_experience == 'Less than a year':
                total_experience = 0
            else:
                total_experience = int(self.pay_total_experience)
            
            if (total_experience - hospital_experience) < 0:
                return True
            else:
                return False
        else:
            return False

    @rx.var
    def gets_differential(self) -> bool:
        return True if self.pay_differential_response == "Yes" else False

    @rx.var
    def gets_incentive(self) -> bool:
        return True if self.pay_incentive_response == "Yes" else False

    @rx.var
    def is_contract(self) -> bool:
        return True if self.pay_emp_type == "Contract" else False
    
    @rx.var
    def compensation_is_inadequate(self) -> bool:
        return True if self.pay_compensation == "No" else False
    
    @rx.var
    def pay_compensation_changes_chars_left(self) -> int:
        if self.pay_desired_changes:
            return 500 - len(self.pay_desired_changes)
        
    @rx.var
    def pay_compensation_comments_chars_left(self) -> int:
        if self.pay_comments:
            return 500 - len(self.pay_comments)
        
    @rx.var
    def pay_compensation_changes_chars_over(self) -> bool:
        if self.pay_compensation_changes_chars_left:
            if self.pay_compensation_changes_chars_left < 0:
                return True
            else:
                return False
        
    @rx.var
    def pay_compensation_comments_chars_over(self) -> bool:
        if self.pay_compensation_comments_chars_left:
            if self.pay_compensation_comments_chars_left < 0:
                return True
            else:
                return False
    
    @rx.var
    def pay_overall_description(self) -> str:
        if self.pay_overall == "a":
            return "Great"
        if self.pay_overall == "b":
            return "Good"
        if self.pay_overall == "c":
            return "So-so"
        if self.pay_overall == "d":
            return "Bad"
        if self.pay_overall == "f":
            return "Terrible"
        
    @rx.var
    def pay_overall_background(self) -> str:
        if self.pay_overall == "a":
            return "rgb(95, 163, 217)"
        if self.pay_overall == "b":
            return "rgb(95, 154, 100)"
        if self.pay_overall == "c":
            return "rgb(237, 234, 95)"
        if self.pay_overall == "d":
            return "rgb(197, 116, 57)"
        if self.pay_overall == "f":
            return "rgb(185, 65, 55)"
        
    @rx.var
    def pay_progress(self) -> int:
        progress = 0
        if self.pay_emp_type:
            progress = progress + 10
        if self.pay_amount and not\
            self.is_pay_invalid:
            progress = progress + 10
        if self.pay_differential_response:
            progress = progress + 10
        if self.pay_incentive_response:
            progress = progress + 10
        if self.pay_shift:
            progress = progress + 10
        if self.pay_weekly_shifts:
            progress = progress + 10
        if self.pay_hospital_experience and self.pay_total_experience\
            and not self.is_experience_invalid:
            progress = progress + 20
        if self.pay_compensation:
            progress = progress + 10
        if self.pay_overall:
            progress = progress + 10
        return progress
    
    @rx.var
    def pay_can_progress(self) -> bool:
        if self.pay_progress == 100:
            return True
        else:
            return False

    """
    Staffing fields and logic. --------------------------------------
    """

    staffing_ratio_response: str

    staffing_ratio: int

    staffing_ratio_variable: str

    staffing_ratio_unsafe: str

    staffing_workload: str

    staffing_float: str

    staffing_charge_response: str

    staffing_charge_assignment: str

    staffing_nursing_shortages: str

    staffing_aide_shortages: str

    staffing_select_transport: bool

    staffing_select_lab: bool

    staffing_select_cvad: bool

    staffing_select_wocn: bool

    staffing_select_chaplain: bool

    staffing_select_educator: bool

    staffing_support_available: str

    staffing_comments: str

    staffing_overall: str

    @rx.var
    def has_ratios(self) -> bool:
        return True if self.staffing_ratio_response == "Yes" else False
    
    @rx.var
    def same_ratio(self) -> bool:
        return True if self.staffing_ratio_variable == "Staff" else False
        
    @rx.var
    def ratio_is_valid(self) -> bool:
        return True if 0 < self.staffing_ratio < 30 else False
        
    @rx.var
    def has_charge(self) -> bool:
        return True if self.staffing_charge_response == "Yes" else False
    
    @rx.var
    def ratios_unsafe(self) -> bool:
        if self.staffing_ratio_unsafe == "Always" or\
        self.staffing_ratio_unsafe == "Usually" or\
        self.staffing_ratio_unsafe == "Sometimes":
            return True
        else:
            return False
        
    @rx.var
    def staffing_comments_chars_over(self) -> bool:
        if self.staffing_comments_chars_left:
            if self.staffing_comments_chars_left < 0:
                return True
            else:
                return False
        
    @rx.var
    def staffing_comments_chars_left(self) -> int:
        if self.staffing_comments:
            return 500 - len(self.staffing_comments)
        
    @rx.var
    def staffing_overall_description(self) -> str:
        if self.staffing_overall == "a":
            return "Great"
        if self.staffing_overall == "b":
            return "Good"
        if self.staffing_overall == "c":
            return "So-so"
        if self.staffing_overall == "d":
            return "Bad"
        if self.staffing_overall == "f":
            return "Terrible"

    @rx.var
    def staffing_overall_background(self) -> str:
        if self.staffing_overall == "a":
            return "rgb(95, 163, 217)"
        if self.staffing_overall == "b":
            return "rgb(95, 154, 100)"
        if self.staffing_overall == "c":
            return "rgb(237, 234, 95)"
        if self.staffing_overall == "d":
            return "rgb(197, 116, 57)"
        if self.staffing_overall == "f":
            return "rgb(185, 65, 55)"

    @rx.var
    def staffing_progress(self) -> int:
        progress = 0
        if self.staffing_ratio_response == "Yes":
            progress = progress + 5
            if self.staffing_ratio_variable == "Same acuity":
                progress = progress + 5
                if self.staffing_ratio and self.ratio_is_valid:
                    progress = progress + 5
                if self.staffing_ratio_unsafe:
                    progress = progress + 5
            if self.staffing_ratio_variable == "Variable acuity":
                progress = progress + 15
        if self.staffing_ratio_response == "No":
            progress = progress + 20
        if self.staffing_workload:
            progress = progress + 10
        if self.staffing_charge_response == "Yes":
            progress = progress + 5
            if self.staffing_charge_assignment:
                progress = progress + 5
        if self.staffing_charge_response == "No":
            progress = progress + 10
        if self.staffing_nursing_shortages:
            progress = progress + 15
        if self.staffing_aide_shortages:
            progress = progress + 15
        if self.staffing_support_available:
            progress = progress + 15
        if self.staffing_overall:
            progress = progress + 15
        return progress
    
    @rx.var
    def staffing_can_progress(self) -> bool:
        return True if self.staffing_progress == 100 else False
        
    def set_staffing_ratio_response(self, response: str) -> None:
        self.staffing_ratio = 0
        self.staffing_ratio_variable = ""
        self.staffing_ratio_unsafe = ""
        self.staffing_ratio_response = response

    def set_staffing_ratio(self, ratio: int | str) -> None:
        if ratio == '' or ratio == '00':
            self.staffing_ratio = 0
        else:
            self.staffing_ratio = int(ratio)

    def set_staffing_charge_response(self, response: str) -> None:
        self.staffing_charge_assignment = ""
        self.staffing_charge_response = response
    
    """
    Unit fields and logic. ------------------------------------------
    """

    assign_specific_unit: str

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

    assign_select_tools: str

    assign_select_leaving: str

    assign_select_leaving_reason: str

    assign_select_recommend: str

    assign_input_comments: str

    assign_overall: str

    def set_assign_specific_unit(self, unit: str) -> None:
        self.assign_select_acuity = ""
        self.assign_input_unit_abbr = ""
        self.assign_input_unit_name = ""
        self.assign_select_unit = ""
        self.assign_specific_unit = unit

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
        return True if self.assign_specific_unit else False

    @rx.var
    def is_unit(self) -> bool:
        return True if self.assign_specific_unit == "Yes" else False
    
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
    def assign_overall_description(self) -> str:
        if self.assign_overall == "a":
            return "Great"
        if self.assign_overall == "b":
            return "Good"
        if self.assign_overall == "c":
            return "So-so"
        if self.assign_overall == "d":
            return "Bad"
        if self.assign_overall == "f":
            return "Terrible"

    @rx.var
    def assign_overall_background(self) -> str:
        if self.assign_overall == "a":
            return "rgb(95, 163, 217)"
        if self.assign_overall == "b":
            return "rgb(95, 154, 100)"
        if self.assign_overall == "c":
            return "rgb(237, 234, 95)"
        if self.assign_overall == "d":
            return "rgb(197, 116, 57)"
        if self.assign_overall == "f":
            return "rgb(185, 65, 55)"

    @rx.var
    def assign_progress(self) -> int:
        progress = 0
        if self.assign_specific_unit == "Yes":
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

        if self.assign_specific_unit == "No":
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
        if self.assign_select_tools:
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

        if self.assign_overall:
            progress = progress + 10

        return progress
    
    @rx.var
    def assign_can_progress(self) -> bool:
        if self.assign_progress == 100:
            return True
        else:
            return False
    
    """
    Handle form submissions and validate. ---------------------------
    """

    @rx.var
    def completed_report(self) -> bool:
        if self.pay_progress == 100 and\
        self.staffing_progress == 100 and\
        self.unit_progress == 100:
            return True
        else:
            return False
        
    def handle_submit_pay(self, form_data: dict) -> Iterable[Callable]:
        yield rx.redirect(f"/report/submit/{self.report_id}/staffing")

    def handle_submit_staffing(self, form_data: dict) -> Iterable[Callable]:
        yield rx.redirect(f"/report/submit/{self.report_id}/assignment")

    def handle_submit_unit(self, form_data: dict) -> Iterable[Callable]:
        yield ReportState.submit_full_report
    
    """
    API calls. ------------------------------------------------------
    """

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

    def submit_full_report(self) -> Iterable[Callable]:
        yield rx.redirect(f"/report/submit/{self.report_id}/complete")

    """
    Navigation events. ----------------------------------------------
    """

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

    def report_nav(self, target_url: str) -> Iterable[Callable]:
        """
        Takes a target_url and determines if on summary page or report
        page to route with medicare ID appropriately.
        """
        from ..states.navbar import NavbarState

        if target_url == 'summary':
            yield rx.redirect(f"/report/summary/{self.report_id}/")
        else:
            if self.report_id:
                yield rx.redirect(f"/report/submit/{self.report_id}/{target_url}")
            elif self.summary_id:
                yield rx.redirect(f"/report/submit/{self.summary_id}/{target_url}")
            else:
                yield NavbarState.set_alert_message(
                    f"Invalid URL target - {target_url}"
            )
                
    def clear_and_nav_to_compensation(self) -> Iterable[Callable]:
        """
        Reset all vars in ReportState to prep for a new report. Do it
        using the button nav between summary and compensation so that
        user accidentally hitting back can still go forward back to
        their report stored in state.
        """
        yield rx.redirect(f"/report/submit/{self.summary_id}/compensation")
        self.reset()