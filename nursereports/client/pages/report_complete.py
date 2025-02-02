from ..components import (
    flex,
    footer,
    login_protected,
    navbar,
    text
)
from ...states import BaseState

import reflex as rx


@rx.page(
    route="/report/full-report/complete",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_auth_flow,
        BaseState.event_state_access_flow("login"),
    ],
)
@login_protected
def complete_page() -> rx.Component:
    return rx.flex(
        navbar(),
        content(),
        footer(),
        fireworks(),
        class_name="flex-col items-center min-h-svh",
    )


def content() -> rx.Component:
    return rx.flex(
        header(),
        share(),
        leave(),
        class_name="flex-col items-center space-y-10 px-4 py-24 w-full md:max-w-screen-sm",
    )


def header() -> rx.Component:
    return rx.flex(
        rx.text(
            "Like saving a few slices of pepperoni for night shift.",
            class_name="font-bold text-center text-4xl text-zinc-700",

        ),
        rx.text(
            """You're a team player! Every report adds to transparency and
            accountability across the US. Don't forget to share this site
            with your friends and colleagues by using the social links below.
            """,
            class_name="text-zinc-700"
        ),
        class_name="flex-col space-y-10 pb-4 w-full max-w-screen-sm",
    )


def share() -> rx.Component:
    return flex(
        rx.flex(
            text("Share to...", class_name="text-xl font-bold"),
            class_name="flex-col items-center bg-zinc-100 dark:bg-zinc-800 p-4 w-full",
        ),
        flex(
            rx.flex(
                rx.flex(
                    rx.icon("facebook", class_name= "stroke-zinc-700"),
                    text("Facebook", class_name="font-bold select-none"),
                    on_click=rx.redirect(
                        "https://www.facebook.com/sharer/sharer.php?u=https://nursereports.org&amp;src=sdkpreparse",
                        external=True,
                    ),
                    class_name="flex-row items-center justify-center space-x-4 p-4 cursor-pointer",
                ),
                class_name="flex-col w-full active:bg-zinc-200 transition-colors duration-75",
            ),
            rx.flex(
                rx.flex(
                    rx.icon("twitter", class_name= "stroke-zinc-700"),
                    text("Twitter", class_name="font-bold select-none"),
                    on_click=rx.redirect(
                        "https://twitter.com/intent/post?text=Nationwide hospital reporting built by nurses for nurses.&url=https%3A%2F%2Fnursereports.org",
                        external=True,
                    ),
                    class_name="flex-row items-center justify-center space-x-4 p-4 cursor-pointer",
                ),
                class_name="flex-col w-full active:bg-zinc-200 transition-colors duration-75",
            ),
            rx.flex(
                rx.flex(
                    rx.icon("linkedin", class_name= "stroke-zinc-700"),
                    text("LinkedIn", class_name="font-bold select-none"),
                    on_click=rx.redirect(
                        "https://www.linkedin.com/sharing/share-offsite/?url=https://nursereports.org",
                        external=True,
                    ),
                    class_name="flex-row items-center justify-center space-x-4 p-4 cursor-pointer",
                ),
                class_name="flex-col w-full active:bg-zinc-200 transition-colors duration-75",
            ),
            class_name="flex-col dark:divide-zinc-500 divide-y w-full",
        ),
        class_name="flex-col border rounded shadow-lg dark:border-zinc-500 bg-zinc-100 dark:bg-zinc-800 divide-y w-full",
    )


def leave() -> rx.Component:
    return flex(
        rx.flex(
            rx.flex(
                text("Go to Dashboard", class_name="font-bold select-none"),
                rx.icon("arrow-right", class_name= "stroke-zinc-700"),
                on_click=rx.redirect("/dashboard"),
                class_name="flex-row items-center justify-center space-x-2 p-4 cursor-pointer",
            ),
            class_name="flex-col w-full active:bg-zinc-200 transition-colors duration-75",
        ),
        class_name="flex-col border rounded shadow-lg dark:border-zinc-500 bg-zinc-100 dark:bg-zinc-800 divide-y w-full",
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

                const particleCount = 60 * (timeLeft / duration);

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
            ),
        )
    )
