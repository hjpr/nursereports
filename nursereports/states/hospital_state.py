
import re
import reflex as rx

from ..server.supabase.hospital_requests import supabase_get_hospital_overview_info
from .base_state import BaseState

from loguru import logger
from typing import Callable, Iterable

class HospitalState(BaseState):

    hospital_info: dict[str, str | int | list]

    @rx.var
    def cms_id(self):
        return self.router.page.params.get("hosp_id")
    
    def event_state_load_hospital_info(self) -> Iterable[Callable]:
        try:
            cms_is_valid = bool(re.match(r'^[a-zA-Z0-9]{5,6}$', self.cms_id))
            if cms_is_valid:
                self.hospital_info = supabase_get_hospital_overview_info(
                    self.access_token, self.cms_id
                )
            else:
                raise Exception("CMS ID is not in a valid format.")
        except Exception as e:
            logger.warning(e)