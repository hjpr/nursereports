
from ..server.supabase import supabase_submit_feedback
from .base_state import BaseState

from loguru import logger
from typing import Callable, Iterable

import reflex as rx


class NavbarState(rx.State):
    show_feedback: bool = False
    error_message: str = ""

    def event_state_submit_feedback(self, form_data: dict) -> Iterable[Callable]:
        """
        Submits user feedback entered in feedback modal.
        """
        try:
            user_feedback = form_data.get("feedback")
            if user_feedback:
                data = {
                    "user_feedback": user_feedback,
                    "email": BaseState.get_value("user_claims_email"),
                    "user_id": BaseState.get_value("user_claims_id")
                }
                response = supabase_submit_feedback(BaseState.get_access_token, data)
                if response["success"]:
                    yield rx.toast.success("Your feedback will be reviewed shortly.")
                    self.reset()
                else:
                    self.error_message = response["status"]
            else:
                self.error_message = "No feedback entered."

        except Exception as e:
            logger.critical(e)


