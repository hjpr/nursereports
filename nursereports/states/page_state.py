
from .base_state import BaseState

import reflex as rx

class PageState(BaseState):
    
    @rx.var
    def search_param(self) -> str:
        return self.router.page.params.get('context')

    @rx.var
    def comp_is_active(self) -> bool:
        return True if "compensation" in\
            self.router.page.full_raw_path else False

    @rx.var
    def staffing_is_active(self) -> bool:
        return True if "staffing" in\
            self.router.page.full_raw_path else False

    @rx.var
    def assign_is_active(self) -> bool:
        return True if "assignment" in\
            self.router.page.full_raw_path else False
    
