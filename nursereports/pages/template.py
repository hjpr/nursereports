
from ..components.c2a import c2a_spacer
from ..components.footer import footer
from ..components.navbar import navbar
from ..components.custom import spacer

import reflex as rx

def template_page() -> rx.Component:
    return rx.box(

        navbar(),

        # MAIN CONTENT CONTAINER
        rx.container(

            # SETS TOP OF PAGE FROM UNDERNEATH NAVBAR/C2A    
            c2a_spacer(),

            # REST OF PAGE BELOW

        ),

    )
