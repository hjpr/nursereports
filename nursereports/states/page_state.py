from .user_state import UserState

import reflex as rx

class PageState(UserState):
    context: str = "" # Search param

    @rx.var
    def search_param(self) -> str | None:
        return self.context

    @rx.var
    def comp_is_active(self) -> bool:
        return True if "compensation" in\
            self.router.url else False

    @rx.var
    def staffing_is_active(self) -> bool:
        return True if "staffing" in\
            self.router.url else False

    @rx.var
    def assign_is_active(self) -> bool:
        return True if "assignment" in\
            self.router.url else False
    
