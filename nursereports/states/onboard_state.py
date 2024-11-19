from .user_state import UserState
from ..server.exceptions import InvalidError, RequestFailed

from loguru import logger
from typing import Callable, Iterable

import reflex as rx


class OnboardState(UserState):
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
            # Check if required fields were completed.
            if not self.license or not self.license_state or not self.has_review:
                raise InvalidError("Please complete all fields before continuing.")

            # Update remote database with onboard data.
            user_info = {
                "license": self.license,
                "license_state": self.license_state,
                "needs_onboard": True if self.has_review == "Yes" else False,
            }
            yield from self.update_user_info_and_sync_locally(user_info)

            # Decide if user either needs to submit report, or is okay to proceed.
            if self.user_info["needs_onboard"]:
                logger.debug("User will need to complete a report for site access.")
                yield rx.redirect("/search/hospital")
            else:
                logger.debug("User doesn't have a report to capture.")
                yield rx.redirect("/dashboard")

        except InvalidError as e:
            error_message = str(e)
            self.onboard_error_message = error_message
        except RequestFailed:
            yield rx.redirect("/logout/error")
