
import reflex as rx

def sidebar():
    return rx.box(
        rx.vstack(
            rx.image(
                src='/favicon.ico',
                margin='0 auto',
            ),
            rx.heading(
                'Sidebar',
                text_align='center',
                margin_bottom='1em',
            ),
        ),
        position='fixed',
        height='100%',
        left='0px',
        top='72px',
        z_index='500',
    )