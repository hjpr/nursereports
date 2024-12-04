from .tailwind import (
    flex
)

from ...states import NavbarState, UserState

import reflex as rx


def c2a() -> rx.Component:
    return rx.cond(
        UserState.user_claims_authenticated,
        flex(
            rx.button(
                "In Beta. Click here to submit issue or feedback.",
                on_click=NavbarState.set_show_feedback(True),
                class_name="bg-zinc-200 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-700 cursor-pointer"
            ),
            class_name="flex-col p-1 w-full"
        )
    )
