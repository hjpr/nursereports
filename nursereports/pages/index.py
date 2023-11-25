
from ..components.footer import footer
from ..components.navbar import navbar, c2a_spacer
from ..components.custom import spacer

import reflex as rx

class Index:

    route: str = '/'

    def page() -> rx.Component:
        return rx.box(

            navbar(),

            c2a_spacer(),

            # MAIN CONTENT CONTAINER
            rx.container(

                # COVER IMAGE WITH TEXT OVERLAY
                rx.center(
                    # rx.text(
                    #     "Placeholder text...",
                    #     font_size=['2em', '3em', '5em', '5em', '5em'],
                    #     text_shadow='0 0 10px white',
                    # ),
                    background_image='/raster/placeholdercropped.webp',
                    background_color='snow',
                    height=['200px', '300px', '500px', '500px', '500px'],
                    background_position='center',
                    background_size='cover',
                ),

                spacer(height='60px', bg='whitesmoke'),

                # PANEL 1 - WELCOME
                rx.vstack(
                    rx.heading(
                        """The first comprehensive hospital report system for nurses,
                        by nurses.""",
                        size='xl',
                        text_align='center',
                        ),
                    spacer(height='20px', bg='snow'),
                    rx.text(
                        """Nursereports.org is a RN-developed, community-provided 
                        repository of hospital reports, to solely benefit nurses
                        by finding the jobs we want with the pay we deserve. 
                        """,
                        font_size='1.2em',
                        text_align='center',
                    ),
                    spacer(height='20px', bg='snow'),
                    rx.button(
                        "Submit a report",
                        size='md',
                        color_scheme='teal',
                    ),
                    max_width='1200px',
                    padding_x=['40px','40px', '100px', '100px', '200px'],
                ),

                spacer(height='60px', bg='whitesmoke'),
                spacer(height='40px', bg='white'),

                # PANEL 2 - MOST IMPORTANT
                rx.flex(

                    # TEXT AREA
                    rx.center(
                        rx.vstack(
                            rx.text(
                                "The most important 5 minutes of your career.",
                                font_size='2em',
                                font_weight='800',
                                text_align=['center', 'center', 'center', 'left', 'left'],
                            ),
                            spacer(height='4px', bg='white'),
                            rx.text(
                                """Share details about pay, benefits, and workplace
                                culture using our short but detailed reporting
                                system.
                                """,
                                font_size='1.2em',
                                text_align=['center', 'center', 'center', 'left', 'left'],
                            ),
                            rx.text(
                                """Access information on hospitals nationwide to find new
                                opportunities, or plan your next career move. 
                                """,
                                font_size='1.2em',
                                text_align=['center', 'center', 'center', 'left', 'left'],
                            ),
                        ),
                        padding_x=['40px','40px', '100px', '80px', '80px'],
                        max_width=['100%', '100%', '100%', '50%', '50%'],
                    ),

                    # IMAGE AREA
                    rx.center(
                            rx.image(
                                src='/raster/dalle1.webp',
                                max_height='400px',
                                min_height='300px'
                            ),
                            width=['100%', '100%', '100%', '50%', '50%'],
                        ),

                    #STYLING FLEX CONTAINER
                    bg='white',
                    flex_direction=['column', 'column', 'column', 'row', 'row'],
                ),


                spacer(height='40px', bg='white'),
                spacer(height='40px', bg='whitesmoke'),

                # PANEL 3 - ALWAYS ANONYMOUS
                rx.flex(
                    # IMAGE AREA
                    rx.center(
                        rx.image(
                            src='/raster/dalle2.webp',
                            max_height='400px',
                            min_height='300px',
                        ),
                        width=['100%', '100%', '100%', '50%', '50%'],
                    ),

                    # TEXT AREA
                    rx.center(
                        rx.vstack(
                            rx.text(
                                """Reports are always anonymous, access is 
                                always free.
                                """,
                                font_size='2em',
                                font_weight='800',
                                text_align=['center', 'center', 'center', 'left', 'left'],
                            ),
                            spacer(height='4px'),
                            rx.text(
                                """Speak freely and without fear of retribution.
                                We don't provide your personal information to 
                                anyone for any reason. The only requirement for 
                                access is submitting a report of your own.
                                """,
                                font_size='1.2em',
                                text_align=['center', 'center', 'center', 'left', 'left'],
                            ),
                        ), 
                        padding_x=['40px','40px', '100px', '80px', '80px'],
                        width=['100%', '100%', '100%', '50%', '50%'],
                    ),

                # STYLING FLEX CONTAINER
                flex_direction=['column-reverse', 'column-reverse', 'column-reverse', 'row', 'row'],
                ),

                spacer(height='40px', bg='whitesmoke'),

                # STYLING FOR CONTENT PANEL
                bg='whitesmoke',
                padding='0 0 0 0',
                max_width='1200px',
            ),

            spacer(height='40px', bg='white'),

            footer(),

        )