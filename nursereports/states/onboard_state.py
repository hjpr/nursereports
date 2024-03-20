
from . import BaseState
from ..server.supabase import *
from loguru import logger
from typing import Callable, Iterable

import reflex as rx

class OnboardState(BaseState):

    license: str

    license_state: str

    has_review: str
    
    onboard_error_message: str

    def set_license(self, license: str) -> None:
        self.has_review = ""
        self.license_state = ""
        self.license = license

    @rx.cached_var
    def onboard_has_error(self) -> bool :
        return True if self.onboard_error_message else False

    @rx.cached_var
    def is_student(self) -> bool:
        if self.license == "Nursing Student":
            return True
        else:
            return False
        
    @rx.cached_var
    def can_give_review(self) -> bool:
        if self.has_review == "No" or self.license == "Nursing Student":
            return False
        else:
            return True
                
    def event_state_submit_onboard(self) -> Iterable[Callable]:
        if self.onboard_entries_valid():
            needs_onboard = True if self.has_review == "Yes" else False
            data = {
                "license": self.license,
                "license_state": self.license_state,
                "needs_onboard": needs_onboard
            }
            response = supabase_update_user_info(
                self.access_token,
                self.user_claims['payload']['sub'],
                data
            )
            if response['success']:
                self.user_info["needs_onboard"] = needs_onboard
                self.user_info["license"] = self.license
                self.user_info["license_state"] = self.license_state
                if needs_onboard:
                    yield rx.redirect('/search/report')
                else:
                    yield rx.redirect('/dashboard')
            else:
                self.onboard_error_message = response['status']
        else:
            self.onboard_error_message = "Some fields incomplete or invalid."

    def onboard_entries_valid(self) -> bool:
        """
        User OK if nursing student, otherwise must have
        filled out license state and if they've recently
        worked a hospital.
        """
        if self.license:
            if self.license == "Nursing Student":
                return True
            else:
                if self.license_state and self.has_review:
                    return True
                else:
                    False
        else:
            return False