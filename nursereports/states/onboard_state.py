from . import BaseState
from ..server.exceptions import InvalidError, RequestFailed
from ..server.supabase import supabase_update_user_info
from loguru import logger
from typing import Callable, Iterable

import reflex as rx


class OnboardState(BaseState):
    has_review: str
    license: str
    license_state: str
    onboard_error_message: str

    @rx.var(cache=True)
    def onboard_has_error(self) -> bool:
        return True if self.onboard_error_message else False

    @rx.var(cache=True)
    def is_student(self) -> bool:
        if self.license == "Nursing Student":
            return True
        else:
            return False

    @rx.var(cache=True)
    def can_give_review(self) -> bool:
        if self.has_review == "No":
            return False
        else:
            return True
        
    def set_license(self, license: str) -> None:
        if license == "Nursing Student":
            self.license_state = "Student"
            self.has_review = "No"
        else:
            self.has_review = ""
            self.license_state = ""
        self.license = license

    def event_state_submit_onboard(self) -> Iterable[Callable]:
        try:
            if not self.license or not self.license_state or not self.has_review:
                raise InvalidError("Please complete all fields before continuing.")
            data = {
                "license": self.license,
                "license_state": self.license_state,
                "needs_onboard": True if self.has_review == "Yes" else False,
            }
            updated_info = supabase_update_user_info(
                self.access_token, self.user_claims["payload"]["sub"], data
            )
            self.user_info.update(updated_info)
            if self.user_info["needs_onboard"]:
                logger.debug("User will need to complete a report for site access.")
                yield rx.redirect("/search/report")
            else:
                logger.debug("User doesn't have a report to capture.")
                yield rx.redirect("/dashboard")
        except InvalidError as e:
            error_message = str(e)
            self.onboard_error_message = error_message
        except RequestFailed:
            yield rx.redirect("/logout/error")