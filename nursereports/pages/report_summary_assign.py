
from ..components.footer import footer
from ..components.navbar import navbar, c2a_spacer
from ..components.custom import spacer
from ..states.report import ReportState

import reflex as rx

def assign_summary_page() -> rx.Component:
    return rx.flex(

        navbar(),

        c2a_spacer(),

        spacer(height='40px'),

        # MAIN CONTENT CONTAINER
        rx.flex(
            rx.vstack(

                assignment_summary(),

                spacer(height='40px'),

                buttons(),

                spacing='1em'

            ),

            # STYLING FOR CONTENT CONTAINER
            padding_x='20px',
            width=['100%', '100%', '600px', '600px', '600px'],
            max_width='1200px',
            flex_direction='column',
            flex_basis='auto',
            flex_grow='1',
            flex_shrink='0',

        ),

        spacer(height='80px'),

        footer(),

        # STYLING FOR BODY CONTAINER
        width='100%',
        flex_direction='column',
        align_items='center',
        min_height='100vh',
    )

def assignment_summary() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading(
                "Assignment"
            ),
            rx.divider(),
            rx.text(
                """Next, we'll ask questions in a category called assignment.
                This covers details about the area or unit you are assigned
                to like culture, environment, and management.

                We'll ask about ratios and workload in the section after 
                this one.
                """,
                text_align='center'
            )
        )
    )

def buttons() -> rx.Component:
    return rx.center(
        rx.button_group(
            rx.button("Back",
                    width='100%',
                    on_click=ReportState.report_nav('compensation'),
                    is_loading=~rx.State.is_hydrated,
                    color_scheme='teal'
            ),
            rx.button("Next",
                    width='100%',
                    on_click=ReportState.report_nav('assignment'),
                    is_loading=~rx.State.is_hydrated,
                    color_scheme='teal'
            ),
            width='50%',
        ),
        width='100%'
    )

