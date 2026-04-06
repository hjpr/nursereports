from .base_state import BaseState

from datetime import datetime, timezone
from loguru import logger
from typing import Callable, Iterable

import reflex as rx
import time


class NavbarState(BaseState):
    show_feedback: bool = False
    error_message: str = ""

    def event_state_submit_feedback(self, form_data: dict) -> Iterable[Callable]:
        """
        Submits user feedback entered in feedback modal.
        Rate limited to 1 submission per minute per user.
        """
        try:
            user_feedback = form_data.get("feedback")
            if not user_feedback:
                self.error_message = "No feedback entered."
                return

            # Rate limit: check for entries in the last 1 minute.
            exclusion_tz = datetime.fromtimestamp(
                time.time() - 60, tz=timezone.utc
            ).strftime("%Y-%m-%d %H:%M:%S %z")

            recent_entries = self.query().table("feedback").gte(
                "created_at", exclusion_tz
            ).limit(1).select("id").execute()

            if recent_entries:
                self.error_message = "Too many submissions. The limit is 1 submission per 1 minute."
                return

            data = {
                "user_feedback": user_feedback,
                "email": self.user_claims_email,
                "user_id": self.user_claims_id,
            }
            self.query().table("feedback").insert(data, return_="minimal").execute()
            yield rx.toast.success("Your feedback will be reviewed shortly.")
            self.reset()

        except Exception as e:
            logger.critical(e)
