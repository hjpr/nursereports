
import reflex as rx


def footer() -> rx.Component:
    """Footer component for page."""

    return rx.flex(
        rx.vstack(
            rx.text("Hospital"),
        ),
        rx.vstack(
            rx.text("Reports"),
        ),
        rx.vstack(
            rx.text("Our Mission"),
        ),
        rx.vstack(
            rx.text("Support"),
        ),

        # STYLING FOR FLEX CONTAINER
        bg='teal',
        color='white',
        flex_direction=['column', 'column', 'row', 'row', 'row'],
        content_align='center',
        justify_content='center',
    )
