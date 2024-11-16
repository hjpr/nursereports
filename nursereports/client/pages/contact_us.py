
from ...states import BaseState

import reflex as rx

@rx.page(route="/contact-us", title="Nurse Reports", on_load=BaseState.event_state_auth_flow)
def contact_page() -> rx.Component:
    return rx.flex(
        content(),
        class_name="flex-col bg-gradient-to-b from-teal-100 to-cyan-100 items-center justify-center p-4 min-h-screen w-full",
    )

def content() -> rx.Component:
    return rx.flex(
        header(),
        form(),
        class_name="flex-col md:flex-row items-center rounded shadow-lg bg-white w-full max-w-4xl",
    )

def header() -> rx.Component:
    return rx.flex(
        rx.icon("mail", class_name="h-12 w-12"),
        rx.text("Contact Us", class_name="text-3xl font-bold"),
        rx.flex(
            rx.divider(),
            class_name="py-6 md:display-none w-full"
        ),
        rx.flex(
            rx.icon("instagram", class_name="h-10 md:h-8 w-10 md:w-8 cursor-pointer"),
            rx.icon("facebook", class_name="h-10 md:h-8 w-10 md:w-8 cursor-pointer"),
            rx.icon("linkedin", class_name="h-10 md:h-8 w-10 md:w-8 cursor-pointer"),
            class_name="flex-row items-center justify-center space-x-12 w-full"
        ),
        class_name="flex-col items-center p-8 mb-4 space-y-4 w-full"
    )

def form() -> rx.Component:
    return rx.form(
        rx.flex(
            rx.flex(
                rx.text("Subject:", class_name="text-md"),
                rx.input(
                    max_length=50,
                    name="subject"
                ),
                class_name="flex-col space-y-1 w-full"
            ),
            rx.flex(
                rx.text("Message:", class_name="text-md"),
                rx.text_area(
                    max_length=1000,
                    name="text",
                    class_name="h-36"
                ),
                class_name="flex-col space-y-1 w-full"
            ),
            rx.flex(
                rx.button("Submit", type="submit", class_name="w-full"),
                class_name="pt-4 w-full"
            ),
            class_name="flex-col items-center p-8 mb-4 space-y-4 w-full"
        ),
        on_submit=BaseState.event_state_contact_us_submit,
        reset_on_submit=True
    )