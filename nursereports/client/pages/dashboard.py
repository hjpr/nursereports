from ..components import (
    c2a,
    footer,
    hospital_item_dashboard,
    navbar,
    spacer,
    report_item_dashboard,
    report_protected,
)
from ..components.modals import (
    info_modal,
    my_pay_modal_content,
    my_reports_modal_content,
    remove_report_modal,
    saved_hospitals_modal_content,
)
from ...states import BaseState, DashboardState

import reflex as rx


@rx.page(
    route="/dashboard",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_standard_flow("report"),
        BaseState.event_state_refresh_user_info,
    ],
)
@report_protected
def dashboard_page() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        content(),
        footer(),
        background="linear-gradient(ghostwhite, honeydew)",
        flex_direction="column",
        align_items="center",
        min_height="100vh",
    )


def content() -> rx.Component:
    return rx.flex(
        spacer(height="12px"),
        rx.heading("Dashboard", size="8"),
        spacer(height="24px"),
        saved_hospitals(),
        saved_hospitals_info_modal(),
        my_pay(),
        my_pay_info_modal(),
        my_reports(),
        my_reports_info_modal(),
        my_reports_remove_modal(),
        width="100%",
        max_width="1100px",
        padding="48px",
        align="center",
        spacing="5",
        flex_direction="column",
        flex_basis="auto",
        flex_grow="1",
        flex_shrink="0",
    )


def saved_hospitals() -> rx.Component:
    return rx.card(
        rx.cond(
            BaseState.saved_hospitals,
            rx.vstack(
                rx.flex(
                    rx.icon("hospital"),
                    rx.heading("Saved Hospitals", padding="0px 12px"),
                    rx.spacer(),
                    rx.icon(
                        "info",
                        cursor="pointer",
                        on_click=DashboardState.set_saved_hospitals_info_open(True),
                    ),
                    width="100%",
                    flex_direction="row",
                    align="center",
                ),
                rx.separator(),
                rx.scroll_area(
                    rx.flex(
                        rx.foreach(BaseState.saved_hospitals, hospital_item_dashboard),
                        max_height=["300px", "300px", "400px", "400px", "400px"],
                        width="100%",
                        direction="column",
                        spacing="4",
                    )
                ),
                width="100%",
                spacing="4",
            ),
            rx.flex(
                rx.vstack(
                    rx.heading("My Hospitals"),
                    rx.separator(),
                    rx.flex(
                        rx.button(
                            rx.icon("search"),
                            "Find hospitals to add...",
                            variant="ghost",
                            size="3",
                            cursor="pointer",
                            on_click=rx.redirect("/search/hospital"),
                        ),
                        min_height="100px",
                        width="100%",
                        align="center",
                        justify="center",
                    ),
                    width="100%",
                ),
                width="100%",
            ),
        ),
        height="100%",
        width="100%",
        padding="24px",
    )


def saved_hospitals_info_modal() -> rx.Component:
    return rx.dialog.root(
        info_modal("Saved Hospitals", saved_hospitals_modal_content()),
        open=DashboardState.saved_hospitals_info_open,
    )


def my_pay() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.flex(
                rx.icon("piggy-bank"),
                rx.heading("My Pay", padding="0px 12px"),
                rx.spacer(),
                rx.icon(
                    "info",
                    cursor="pointer",
                    on_click=DashboardState.set_my_pay_info_open(True)
                    ),
                width="100%",
                flex_direction="row",
                align="center",
            ),
            rx.separator(),
            rx.flex(
                rx.flex(bg="snow", height="100%", width="100%"),
                rx.separator(orientation="vertical", margin="0 24px"),
                rx.flex(bg="snow", height="100%", width="100%"),
                height="100%",
                width="100%",
                justify="center",
            ),
            height="100%",
            width="100%",
            spacing="4",
        ),
        height="500px",
        width="100%",
        padding="24px",
    )


def my_pay_info_modal() -> rx.Component:
    return rx.dialog.root(
        info_modal("My Pay", my_pay_modal_content()),
        open=DashboardState.my_pay_info_open,
    )


def my_reports() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.flex(
                rx.icon("file-text"),
                rx.heading("My Reports", padding="0px 12px"),
                rx.spacer(),
                rx.icon(
                    "info",
                    cursor="pointer",
                    on_click=DashboardState.set_my_reports_info_open(True)
                    ),
                width="100%",
                flex_direction="row",
                align="center",
            ),
            rx.separator(),
            rx.scroll_area(
                rx.flex(
                    rx.foreach(BaseState.user_reports, report_item_dashboard),
                    max_height=["300px", "300px", "400px", "400px", "400px"],
                    width="100%",
                    direction="column",
                    spacing="4",
                ),
                width="100%",
            ),
            spacing="4",
        ),
        max_height=["300px", "300px", "400px", "400px", "400px"],
        width="100%",
        padding="24px",
        margin="0px 0px 24px 0px",
    )


def my_reports_info_modal() -> rx.Component:
    return rx.dialog.root(
        info_modal("My Reports", my_reports_modal_content()),
        open=DashboardState.my_reports_info_open,
    )


def my_reports_remove_modal() -> rx.Component:
    return rx.dialog.root(
        remove_report_modal(),
        open=DashboardState.remove_report_confirmation_open
    )
