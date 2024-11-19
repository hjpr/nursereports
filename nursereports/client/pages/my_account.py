from ..components.footer import footer
from ..components.navbar import navbar
from ...states import BaseState

import reflex as rx


@rx.page(
    route="/my-account",
    title="Nurse Reports",
    on_load=BaseState.event_state_auth_flow,
)
def my_account_page() -> rx.Component:
    return rx.flex(
        navbar(),
        content(),
        footer(),
        class_name="flex-col items-center bg-gradient-to-b from-white to-teal-200 min-h-svh",
    )


def content() -> rx.Component:
    return rx.flex(class_name="flex-col items-center w-full")
