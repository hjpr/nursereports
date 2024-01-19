
from loguru import logger

import reflex as rx

class NavbarState(rx.State):
    show_c2a: bool = True
    show_feedback: bool = False
    show_sign_in: bool = False
    alert_message: str
    error_sign_in_message: str
    error_create_account_message: str
    error_feedback_message: str

    def toggle_c2a(self):
        self.show_c2a = not self.show_c2a

    def toggle_feedback(self):
        self.show_feedback = not self.show_feedback

    def toggle_login(self):
        self.show_sign_in = not self.show_sign_in
        self.error_sign_in_message = None
        self.error_create_account_message = None

    @rx.var
    def show_alert_message(self) -> bool:
        return True if self.alert_message else False