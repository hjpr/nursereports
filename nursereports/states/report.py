
from loguru import logger
from typing import Callable, Iterable

import httpx
import json
import os
import reflex as rx

from dotenv import load_dotenv
load_dotenv()

api_url = os.getenv("SUPABASE_URL")
api_key = os.getenv("SUPABASE_ANON_KEY")

class ReportState(rx.State):
    completed_summary: bool = False
    completed_pay: bool = False
    completed_staffing: bool = False
    completed_unit: bool = False
    completed_report: bool = False
    unit_or_area_name: str = None
    
    @rx.var
    def summary_id(self) -> str:
        """
        /report/summary/{summary_id}
        """
        return self.router.page.params.get('summary_id')

    @rx.var
    def report_id(self) -> str:
        """
        /report/submit/{report_id}/report_page
        """
        return self.router.page.params.get('report_id')
        
    @rx.cached_var
    def progress(self) -> int:
        if self.completed_report:
            return 100
        if self.completed_staffing:
            return 70
        if self.completed_pay:
            return 40
        if self.completed_summary:
            return 10
        return 0
    
    @rx.cached_var
    def completed_report(self) -> bool:
        if self.completed_summary and self.completed_pay and self.completed_staffing and self.completed_unit:
            return True
        else:
            return False
    
    @rx.cached_var
    def hosp_info(self) -> dict:
        if self.summary_id:
            access_token = rx.State.get_cookies(self).get("access_token")
            url = f"{api_url}/rest/v1/hospitals"\
            f"?hosp_id=eq.{self.summary_id}"\
            "&select=*"
            headers = {
                "apikey": api_key,
                "Authorization": f"Bearer {access_token}",
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

    '''
    Doing this redirect scheme to keep the summary API call from
    firing when navigating report pages.
    '''
    def nav_summary_to_pay(self) -> Iterable[Callable]:
        yield ReportState.set_completed_summary(True)
        yield rx.redirect(f"/report/submit/{self.summary_id}/pay")

    def nav_pay_to_staffing(self) -> Iterable[Callable]:
        # Check validity
        # Stop if errors
        # Set pay complete
        yield ReportState.set_completed_pay(True)
        yield rx.redirect(f"/report/submit/{self.report_id}/staffing")

    def nav_staffing_to_unit(self) -> Iterable[Callable]:
        # Check validity
        # Stop if errors
        # Set staffing complete
        yield ReportState.set_completed_staffing(True)
        yield rx.redirect(f"/report/submit/{self.report_id}/unit")

    def nav_unit_to_staffing(self) -> Iterable[Callable]:
        yield rx.redirect(f"/report/submit/{self.report_id}/staffing")

    def nav_staffing_to_pay(self) -> Iterable[Callable]:
        yield rx.redirect(f"/report/submit/{self.report_id}/pay")

    def nav_pay_to_summary(self) -> Iterable[Callable]:
        yield rx.redirect(f"/report/summary/{self.report_id}")

    def submit_report(self) -> Iterable[Callable]:
        # Submit report to Supabase
        # Confirm that report has been uploaded
        response = True
        if response:
            yield rx.redirect(f"/report/submit/{self.report_id}/complete")