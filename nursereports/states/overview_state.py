
from ..states import PageState, ReportState
from ..server.supabase.report_requests import supabase_get_hospital_info
from typing import Callable, Iterable

import reflex as rx

class OverviewState(PageState):
    hosp_info: dict

    error_hosp_info: str

    def event_state_get_hospital_info(self) -> None:
        self.hosp_info = {}
        if self.user_is_authenticated and len(self.hosp_id_param) < 7:
            response = supabase_get_hospital_info(
                self.access_token,
                self.hosp_id_param
            )
            if response['success']:
                self.hosp_info = response['payload']
            else:
                self.error_hosp_info = response['status']

    def event_state_goto_report(self) -> Iterable[Callable]:
        if self.hosp_info:
            yield rx.redirect(f"/report/full-report/{self.hosp_id_param}/outline")
            yield ReportState.reset_report