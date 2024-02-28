
from . import BaseState
from typing import Iterable

class OnboardState(BaseState):

    def event_state_submit_onboard(self, form_data: dict) -> Iterable:
        yield