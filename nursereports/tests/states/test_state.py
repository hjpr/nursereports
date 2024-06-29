
from ...client.components.lists import leaving_reason, unit_specialties

from ...states import BaseState, ReportState

from loguru import logger
from typing import Callable, Iterable

import random
import reflex as rx
import uuid

class TestState(BaseState):

    def event_state_warn_tests_active(self) -> Iterable[Callable]:
        logger.critical("!!!TEST PAGE IS ACTIVE!!!")
        yield rx.toast.error("TEST PAGE IS ACTIVE", timeout=10000)


class ReportTestState(ReportState):

    is_running: bool

    def event_test_report(self) -> Iterable[Callable]:
        self.is_running = True
        optional = {
            "comp_input_comments": self.comp_input_comments,
            "assign_input_unit_name": self.assign_input_unit_name,
            "assign_input_area": self.assign_input_area,
            "assign_input_comments": self.assign_input_comments,
            "staffing_input_comments": self.staffing_input_comments
        }
        yield ReportState.set_is_test(True)
        yield ReportState.set_report_id(str(uuid.uuid4()))
        yield ReportState.set_comp_select_emp_type(random.choice(['Full-time', 'Part-time', 'Contract']))
        yield ReportState.set_comp_select_pay_type('Weekly')
        yield ReportState.set_comp_input_pay_amount(str(random.randint(500, 1200)))
        yield ReportState.set_comp_select_diff_response(random.choice(['Yes', 'No']))
        yield ReportState.set_comp_input_diff_nights(str(random.randint(1,100)))
        yield ReportState.set_comp_input_diff_weekends(str(random.randint(1, 100)))
        yield ReportState.set_comp_select_incentive_response(random.choice(['Yes', 'No']))
        yield ReportState.set_comp_input_incentive_amount(str(random.randint(1, 100)))
        yield ReportState.set_comp_select_certifications(random.choice(['Yes', 'No']))
        yield ReportState.set_comp_select_shift(random.choice(['Day', 'Night', 'Rotating']))
        yield ReportState.set_comp_select_weekly_shifts(str(random.randint(1,6)))
        yield ReportState.set_comp_select_hospital_experience(str(random.randint(0,5)))
        yield ReportState.set_comp_select_total_experience(str(random.randint(6,10)))
        yield ReportState.set_comp_check_benefit_pto(random.choice([True, False]))
        yield ReportState.set_comp_check_benefit_parental(random.choice([True, False]))
        yield ReportState.set_comp_check_benefit_insurance(random.choice([True, False]))
        yield ReportState.set_comp_check_benefit_retirement(random.choice([True, False]))
        yield ReportState.set_comp_check_benefit_pro_dev(random.choice([True, False]))
        yield ReportState.set_comp_check_benefit_tuition(random.choice([True, False]))
        yield ReportState.set_comp_select_comp_adequate(random.choice(["Yes", "No"]))
        yield ReportState.set_comp_input_comments(optional.get('comp_input_comments', ''))
        yield ReportState.set_comp_select_overall(random.choice(['a', 'b', 'c', 'd', 'f']))
        yield ReportState.set_assign_select_specific_unit(random.choice(['Yes', 'No']))
        yield ReportState.set_assign_select_unit("TEST")
        yield ReportState.set_assign_input_unit_name(optional.get('assign_input_unit_name', ''))
        yield ReportState.set_assign_select_acuity(random.choice(["Intensive", "Intermediate", "Floor", "Mixed", "N/A"]))
        yield ReportState.set_assign_select_area("TEST")
        yield ReportState.set_assign_input_area(optional.get("assign_input_area", ""))
        yield ReportState.set_assign_select_specialty_1(random.choice(unit_specialties))
        yield ReportState.set_assign_select_specialty_2(random.choice(unit_specialties))
        yield ReportState.set_assign_select_specialty_3(random.choice(unit_specialties))
        yield ReportState.set_assign_select_teamwork_rn(random.choice(['Always', 'Usually', 'Sometimes', 'Rarely', 'Never', 'N/A']))
        yield ReportState.set_assign_select_teamwork_na(random.choice(['Always', 'Usually', 'Sometimes', 'Rarely', 'Never', 'N/A']))
        yield ReportState.set_assign_select_providers(random.choice(['Always', 'Usually', 'Sometimes', 'Rarely', 'Never', 'N/A']))
        yield ReportState.set_assign_select_contributions(random.choice(['Always', 'Usually', 'Sometimes', 'Rarely', 'Never', 'N/A']))
        yield ReportState.set_assign_select_impact(random.choice(['Always', 'Usually', 'Sometimes', 'Rarely', 'Never', 'N/A']))
        yield ReportState.set_assign_select_management(random.choice(['Always', 'Usually', 'Sometimes', 'Rarely', 'Never', 'N/A']))
        yield ReportState.set_assign_select_leaving(random.choice(['Yes', 'No']))
        yield ReportState.set_assign_select_leaving_reason(random.choice(leaving_reason))
        yield ReportState.set_assign_select_recommend(random.choice(['Yes', 'No']))
        yield ReportState.set_assign_input_comments(optional.get("assign_input_comments", ""))
        yield ReportState.set_assign_select_overall(random.choice(['a', 'b', 'c', 'd', 'f']))
        yield ReportState.set_staffing_input_ratio(str(random.randint(1,10)))
        yield ReportState.set_staffing_select_ratio_unsafe(random.choice(['Always', 'Usually', 'Sometimes', 'Rarely', 'Never', 'N/A']))
        yield ReportState.set_staffing_select_workload(random.choice(["Overwhelming", "Heavy", "Moderate", "Light"]))
        yield ReportState.set_staffing_select_charge_response(random.choice(['Yes', 'No']))
        yield ReportState.set_staffing_select_charge_assignment(random.choice(['Always', 'Usually', 'Sometimes', 'Rarely', 'Never', 'N/A']))
        yield ReportState.set_staffing_select_nursing_shortages(random.choice(['Always', 'Usually', 'Sometimes', 'Rarely', 'Never', 'N/A']))
        yield ReportState.set_staffing_select_aide_shortages(random.choice(['Always', 'Usually', 'Sometimes', 'Rarely', 'Never', 'N/A']))
        yield ReportState.set_staffing_check_transport(random.choice([True, False]))
        yield ReportState.set_staffing_check_lab(random.choice([True, False]))
        yield ReportState.set_staffing_check_cvad(random.choice([True, False]))
        yield ReportState.set_staffing_check_wocn(random.choice([True, False]))
        yield ReportState.set_staffing_check_chaplain(random.choice([True, False]))
        yield ReportState.set_staffing_check_educator(random.choice([True, False]))
        yield ReportState.set_staffing_select_support_available(random.choice(['Always', 'Usually', 'Sometimes', 'Rarely', 'Never', 'N/A']))
        yield ReportState.set_staffing_input_comments(optional.get("staffing_input_comments", ""))
        yield ReportState.set_staffing_select_overall(random.choice(['a', 'b', 'c', 'd', 'f']))
        yield ReportState.submit_report
        self.is_running = False