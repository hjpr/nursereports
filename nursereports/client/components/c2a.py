from ...states import BaseState, NavbarState

import reflex as rx


def c2a() -> rx.Component:
    return rx.cond(
        BaseState.user_claims_authenticated,
        rx.flex(
            rx.button(
                "In Beta. Click here to submit issue or feedback.",
                on_click=NavbarState.set_show_feedback(True),
                class_name="bg-transparent text-zinc-700 cursor-pointer"
            ),
            class_name="flex-col bg-zinc-100 hover:bg-teal-100 p-1 w-full"
        )
    )
