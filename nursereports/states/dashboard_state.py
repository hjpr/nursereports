import reflex as rx


class DashboardState(rx.State):
    my_pay_info_open: bool = False
    my_reports_info_open: bool = False
    remove_report_confirmation_open: bool = False
    report_to_remove: str = ""
    saved_hospitals_info_open: bool = False

    def close_all_modals(self) -> None:
        self.saved_hospitals_info_open = False
        self.my_pay_info_open = False
        self.my_reports_info_open = False
