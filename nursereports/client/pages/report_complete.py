
from ..components.c2a import c2a
from ..components.custom import spacer, login_protected
from ..components.footer import footer
from ..components.navbar import navbar
from ...states.base_state import BaseState

import reflex as rx

@rx.page(
    route="/report/submit/[hosp_id]/complete",
    title="Nurse Reports",
    on_load=BaseState.event_state_standard_flow('login')
)
@login_protected
def complete_page() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        spacer(height='48px'),
        content(),
        spacer(height='96px'),
        footer(),
        fireworks(),
        width='100%',
        flex_direction='column',
        align_items='center',
        min_height='100vh',
    )

def content() -> rx.Component:
    return rx.flex(
        header(),
        spacer(height='24px'),
        share(),
        spacer(height='24px'),
        leave(),
        gap='24px',
        padding_x='24px',
        width=['100%', '480px', '480px', '480px', '480px'],
        max_width='1200px',
        flex_direction='column',
        flex_basis='auto',
        flex_grow='1',
        flex_shrink='0',
    )

def header() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.heading(
                "One report closer to full transparency!",
                text_align='center',
                size='7'
            ),
            rx.text(
                """In just a short time you've made a big difference.
                The only bigger difference you can make is to spread
                the word. Share NurseReports.org to your friends and
                colleagues below.
                """,
                text_align='center'
            ),
            width='100%'
        ),
        width='100%'
    )

def share() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.flex(
                rx.text(
                    "Share to:",
                    white_space='nowrap'
                ),
                rx.flex(
                    rx.button(
                        rx.icon('facebook', size=28),
                        size='3',
                        color='#1877F2',
                        variant='ghost',
                        on_click=rx.redirect(
                            'https://www.facebook.com/sharer/sharer.php?u=https://nursereports.org&amp;src=sdkpreparse',
                            external=True
                        )
                    ),
                    rx.button(
                        rx.icon('twitter', size=28),
                        size='3',
                        color='#1DA1F2',
                        variant='ghost',
                        on_click=rx.redirect(
                            'https://twitter.com/intent/post?text=Nationwide hospital reporting built by nurses for nurses.&url=https%3A%2F%2Fnursereports.org',
                            external=True
                        )
                    ),
                    rx.button(
                        rx.icon('linkedin', size=28),
                        size='3',
                        color='#0077B5',
                        variant='ghost',
                        on_click=rx.redirect(
                            'https://www.linkedin.com/sharing/share-offsite/?url=https://nursereports.org',
                            external=True
                        )
                    ),
                    flex_direction='row',
                    align_items='center',
                    justify_content='space-around',
                    width='100%'
                ),
                flex_direction='row',
                align_items='center',
                margin_top='12px'
            ),
            rx.divider(),
            rx.flex(
                rx.text(
                    "Or copy link:",
                    white_space="nowrap"
                ),
                rx.flex(
                    rx.button(
                        rx.icon('clipboard', size=28),
                        size='3',
                        color='teal',
                        variant='ghost',
                        on_click=rx.set_clipboard(
                            'https://nursereports.org'
                        )
                    ),
                    flex_direction='row',
                    align_items='center',
                    justify_content='space-around',
                    width='100%'
                ),
                flex_direction='row',
                align_items='center',
                margin_bottom='12px'
            ),
            flex_direction='column',
            gap='24px'
        )
    )

def leave() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.button(
                "Go to Dashboard",
                rx.icon('arrow-big-right'),
                size='3',
                variant='ghost',
                on_click=rx.redirect('/dashboard')
            ),
            align_items='center',
            justify_content='center',
            width='100%'
        ),
        width='100%'
    )

def fireworks() -> rx.Component:
    return rx.flex(
        rx.script(
            src="https://cdn.jsdelivr.net/npm/@tsparticles/confetti@3.0.3/tsparticles.confetti.bundle.min.js",
            on_ready=rx.call_script(
                """
                const duration = 4 * 1000,
                animationEnd = Date.now() + duration,
                defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

                function randomInRange(min, max) {
                return Math.random() * (max - min) + min;
                }

                const interval = setInterval(function() {
                const timeLeft = animationEnd - Date.now();

                if (timeLeft <= 0) {
                    return clearInterval(interval);
                }

                const particleCount = 50 * (timeLeft / duration);

                // since particles fall down, start a bit higher than random
                confetti(
                    Object.assign({}, defaults, {
                    particleCount,
                    origin: { x: randomInRange(0.1, 0.4), y: Math.random() - 0.2 },
                    startVelocity: 20,
                    gravity: 0.1,
                    decay: 0.8,
                    ticks: 200
                    })
                );
                confetti(
                    Object.assign({}, defaults, {
                    particleCount,
                    origin: { x: randomInRange(0.6, 0.9), y: Math.random() - 0.2 },
                    startVelocity: 40,
                    gravity: 0.1,
                    decay: 0.8,
                    ticks: 200
                    })
                );
                }, 250);
                """
            )
        )
    )