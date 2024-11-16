
from ...states import BaseState

import reflex as rx

@rx.page(route="/roadmap", title="Nurse Reports", on_load=BaseState.event_state_auth_flow)
def roadmap_page() -> rx.Component:
    return rx.flex(
        content(),
        class_name="flex-col bg-gradient-to-b from-teal-100 to-cyan-100 items-center justify-center p-4 min-h-screen w-full",
    )

def content() -> rx.Component:
    return rx.flex(
        header(),
        image(),
        text(),
        class_name="flex-col items-center space-y-12 w-md"
    )

def header() -> rx.Component:
    return rx.flex()

def image() -> rx.Component:
    return rx.flex()

def text() -> rx.Component:
    return rx.flex()