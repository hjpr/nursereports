
from ..components.footer import footer
from ..components.navbar import navbar, c2a_spacer
from ..components.custom import spacer

import reflex as rx

def onboard_page() -> rx.Component:
    return rx.flex(

        navbar(),

        c2a_spacer(),

        spacer(height='40px'),
        
        # MAIN CONTENT CONTAINER
        rx.flex(
            rx.center(
                rx.vstack(
                    rx.vstack(
                        rx.heading(
                            "Welcome to RN 2.0!"
                        ),
                        rx.divider(),
                        rx.text(
                            """
                            Thanks for joining the newest and best
                            open nursing community in the US. Here you
                            can share information about compensation, 
                            staffing ratios, and overall on-the-unit
                            experience with your peers.
                            """
                        )
                    ),
                    rx.vstack(
                        rx.text(
                            """
                            Before venturing into the site, we'll get a 
                            report from you about your current assignment.
                            This report is your ticket to access our entire
                            database for free. These reports help nurses
                            just like you make career moves, so be helpful
                            and detailed.
                            """
                        )
                    ),
                    rx.button(
                        "I'm ready to submit a report",
                        color_scheme='teal',
                        on_click=rx.redirect('/search/report'),
                        is_loading=~rx.State.is_hydrated,
                    ),
                    width='600px',
                    spacing='1em'
                )
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

        footer(),

        # STYLING FOR BODY CONTAINER
        width='100%',
        flex_direction='column',
        align_items='center',
        min_height='100vh'

    )