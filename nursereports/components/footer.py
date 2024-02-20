
from .custom import spacer

import reflex as rx

def footer() -> rx.Component:
    """
    Main footer component.
    """
    return rx.flex(
        spacer(height='40px'),
        # CENTERED FOOTER CONTAINER
        rx.flex(
            # LEFT FOOTER SECTION
            rx.flex(
                # LEFT FOOTER HEADER W IMAGE  
                rx.flex(
                    rx.image(
                        src='/vector/icon_web_footer.svg',
                        height='32px',
                        width='32px',
                        margin_right='6px',
                        align_self='center'
                    ),
                    rx.heading(
                        "Nurse Reports",
                        align_self='flex-end',
                    ),
                    flex_direction='row',
                ),
                spacer(height='8px'),
                rx.text(
                    "© 2023 Nursereports.org. All rights reserved.",
                    font_size='0.8em',
                ),
                spacer(height='8px'),
                rx.text(
                    "Nursereports.org is a nurse developed site built on\
                    principles of trust and community. Please check our\
                    policies for details on how we handle your information\
                    and how nurses are our primary beneficiaries.",
                    font_size='0.6em',
                    text_align='left',
                ),
                # LEFT FOOTER STYLING
                display=['none', 'none', 'none', 'block', 'block'],
                width='360px',
                height='100%',
                flex_direction='column',
                justify_content='left',
            ),

            # RIGHT FOOTER SECTION
            rx.flex(
                # REPORTS
                rx.flex(
                    rx.text("REPORTS", font_size='0.9em', font_weight='700'),
                    spacer(height='12px'),
                    rx.link(
                        "By Hospital",
                        color='white',
                        text_decoration_color='white',
                        font_size='0.9em'
                    ),
                    rx.link(
                        "By State",
                        color='white',
                        text_decoration_color='white',
                        font_size='0.9em'
                    ),
                    text_align='left',
                    flex_direction='column',
                ),
                # SUPPORT US
                rx.flex(
                    rx.text("SUPPORT US",font_size='0.9em', font_weight='700'),
                    spacer(height='12px'),
                    rx.link(
                        "Membership",
                        color='white',
                        text_decoration_color='white',
                        font_size='0.9em'
                    ),
                    rx.link(
                        "Donate",
                        color='white',
                        text_decoration_color='white',
                        font_size='0.9em'
                    ),
                    rx.link(
                        "Store",
                        color='white',
                        text_decoration_color='white',
                        font_size='0.9em'
                    ),
                    text_align='left',
                    flex_direction='column',
                ),
                # INFO
                rx.flex(
                    rx.text("INFO", font_size='0.9em', font_weight='700'),
                    spacer(height='12px'),
                    rx.link(
                        "About Us",
                        color='white',
                        text_decoration_color='white',
                        font_size='0.9em'
                    ),
                    rx.link(
                        "Contact",
                        color='white',
                        text_decoration_color='white',
                        font_size='0.9em'
                    ),
                    rx.link(
                        "Privacy Policy",
                        color='white',
                        text_decoration_color='white',
                        font_size='0.9em'
                    ),
                    rx.link(
                        "AI Policy",
                        color='white',
                        text_decoration_color='white',
                        font_size='0.9em'
                    ),
                    text_align='left',
                    flex_direction='column',
                ),
                # RIGHT FOOTER STYLING
                width='360px',
                flex_direction='row',
                justify_content='space-between',
            ),
            # ON MOBILE - COPYRIGHT
            rx.flex(
                spacer(height='40px'),
                rx.text(
                    "© 2023 Nursereports.org. All rights reserved.",
                    color='white',
                    font_size='0.8em',
                    text_align='center',
                    ),
                spacer(height='20px'),
                rx.text(
                    "Nursereports.org is a nurse developed site built on\
                    principles of trust and community. Please check our\
                    policies for details on how we handle your information\
                    and how nurses are our primary beneficiaries.",
                    color='white',
                    font_size='0.6em',
                    text_align='left',
                ),
                display=['block', 'block', 'block', 'none', 'none'],
                width='100%',
                padding_x='40px',
            ),
            # STYLING FOR CENTERED FOOTER CONTAINER
            flex_direction=['column', 'column', 'column', 'row', 'row'],
            align_items='center',
            justify_content='space-around',
            width='100%',
            max_width='1200px',
        ),
        spacer(height='40px'),
        # STYLING FOR FOOTER CONTAINER
        bg='#12A594',
        color='white',
        box_shadow='inset 0px 4px 5px -5px rgba(0, 0, 0, 0.5)',
        min_height='260px',
        flex_direction='column',
        flex_basis='auto',
        flex_grow='0',
        flex_shrink='0',
        width='100%',
        justify_content='center',
        align_items='center'
    )
