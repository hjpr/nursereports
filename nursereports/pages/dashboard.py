
from ..components.decorators import protected_page
from ..components.footer import footer
from ..components.navbar import navbar, c2a_spacer
from ..components.custom import spacer

import reflex as rx

@protected_page
def dashboard() -> rx.Component:
    return rx.box(

        navbar(),

        c2a_spacer(),
        
        # MAIN CONTENT CONTAINER
        rx.container(


            # REST OF PAGE BELOW
            

        # STYLING FOR MAIN CONTAINER
        height='300px',
        ),

        footer(),
    )
