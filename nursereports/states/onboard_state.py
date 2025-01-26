from .user_state import UserState
from ..server.exceptions import InvalidError, RequestFailed

from loguru import logger
from typing import Callable, Iterable

import reflex as rx


class OnboardState(UserState):
    has_review: str
    license: str
    license_state: str

    def set_license(self, license: str) -> None:
        self.license = license
        self.license_state = ""
        self.has_review = ""
        if license == "Nursing Student":
            self.has_review = "No"

    def event_state_submit_onboard(self) -> Iterable[Callable]:
        try:
            # Check if required fields were completed.
            if not self.license or not self.license_state or not self.has_review:
                raise InvalidError("Please complete all fields before continuing.")

            # Update remote database with onboard data.
            user_info = {
                "professional": {
                    "license_type": self.license,
                    "license_state": self.license_state,
                    "license_number": "1234567890",
                    "specialty": self.user_info["professional"]["specialty"],
                    "experience": self.user_info["professional"]["experience"]
                }
            }
            logger.critical("About to upload to user data.")
            logger.critical(user_info)
            self.update_user_info_and_sync_locally(user_info)

            # # Decide if user either needs to submit report, or is okay to proceed.
            # if self.user_info["license_type"] !=:
            #     logger.debug("User will need to complete a report for site access.")
            #     yield rx.redirect("/search/hospital")
            # else:
            #     logger.debug("User doesn't have a report to capture.")
            #     yield rx.redirect("/dashboard")

        except InvalidError as e:
            error_message = str(e)
            self.onboard_error_message = error_message
        except RequestFailed:
            yield rx.redirect("/logout/error")
