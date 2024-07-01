
import reflex as rx

class DashboardState(rx.State):
    saved_hospitals_info_open: bool = False
    my_pay_info_open: bool = False
    my_reports_info_open: bool = False

    def close_all_modals(self) -> None:
        self.saved_hospitals_info_open = False
        self.my_pay_info_open = False
        self.my_reports_info_open = False