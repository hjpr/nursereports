
from ..components.decorators import protected_page
from ..components.footer import footer
from ..components.navbar import navbar, c2a_spacer
from ..components.custom import spacer

import reflex as rx

# Use @protected_page if require user login prior to viewing.
def template_page() -> rx.Component:
    return rx.box(

        navbar(),

        # SETS TOP OF PAGE FROM UNDERNEATH NAVBAR/C2A    
        c2a_spacer(),

        # MAIN CONTENT CONTAINER
        rx.container(

            # REST OF PAGE GOES BELOW

        ),

        footer(),

    )
