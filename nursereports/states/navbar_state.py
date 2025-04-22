from .base_state import BaseState
from typing import Callable, Iterable

import reflex as rx


class NavbarState(BaseState):
    show_feedback: bool = False

    def event_state_submit_feedback(self, form_data: dict) -> Iterable[Callable]:
        """
        Submits user feedback entered in feedback modal.
        """
        try:
            yield NavbarState.setvar("is_loading", True)
            user_feedback = form_data.get("feedback")
            if not user_feedback:
                raise ValueError("No feedback entered.")
            data = {
                "user_feedback": user_feedback,
                "email": self.user_email,
                "user_id": self.user_id,
            }
            query = self.query.table("feedback").insert(data)
            query.execute()

            yield rx.toast.success("Your feedback will be reviewed shortly.")
            yield NavbarState.setvar("is_loading", True)

        except ValueError as e:
            yield rx.toast.error(str(e))
        except Exception as e:
            yield rx.toast.error(str(e))
