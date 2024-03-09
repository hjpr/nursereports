
from . import BaseState, NavbarState
from ..server.supabase.users import supabase_update_user_info
from typing import Iterable

import reflex as rx

class OnboardState(BaseState):

    def event_state_submit_onboard(self, form_data: dict) -> Iterable:
        user_id = self.user_claims['payload']['sub']
        if form_data.get('no_recent_experience') == 'on':
            data = {
                "needs_onboard": False
            }
            response = supabase_update_user_info(
                self.access_token,
                user_id,
                data
            )
            if response['success']:
                self.user_info["needs_onboard"] = False
                yield rx.redirect('/dashboard')
            else:
                yield NavbarState.set_alert_message(response['status'])
        else:
            yield rx.redirect("/search/report")