from ..components import (
    flex,
    text,
    solid_button
)
from ...states import BaseState

import reflex as rx


@rx.page(
    route="/policy/ai", title="Nurse Reports", on_load=BaseState.event_state_auth_flow
)
def ai_policy_page() -> rx.Component:
    return flex(
        content(),
        class_name="flex-col bg-gradient-to-b from-teal-100 to-cyan-100 dark:from-zinc-800 dark:to-zinc-950 items-center justify-center p-4 min-h-screen w-full",
    )


def content() -> rx.Component:
    return flex(
        header(),
        introduction(),
        ai_usage(),
        data_usage(),
        ai_oversight(),
        transparency(),
        user_rights(),
        future_developments(),
        policy_changes(),
        contact_us(),
        class_name="flex-col items-center rounded shadow-lg bg-white p-8 space-y-8 w-full max-w-xl",
    )


def header() -> rx.Component:
    return flex(
        rx.icon("bot", class_name="h-12 w-12 mt-4 mb-8"),
        text("AI Policy", class_name="text-3xl font-bold"),
        text("Last Updated - 10/9/2024", class_name="text-l italic"),
        class_name="flex-col items-center text-zinc-700 p-4 space-y-2 w-full",
    )


def introduction() -> rx.Component:
    return flex(
        text("1. Introduction", class_name="text-2xl font-bold"),
        rx.divider(),
        text(
            "This AI Policy explains how we use artificial intelligence (AI) technologies on our website to provide and improve our services. We are committed to the responsible and transparent use of AI while protecting your privacy and ensuring the quality of our services."
        ),
        class_name="flex-col space-y-2 w-full",
    )


def ai_usage() -> rx.Component:
    return flex(
        text("2. AI Features and Usage", class_name="text-2xl font-bold"),
        rx.divider(),
        text("2.1 Content Generation", class_name="text-lg font-bold"),
        text("We use AI to:"),
        text("- Generate summaries of hospital report data", class_name="ml-8"),
        text(
            "- Build personalized suggestions based on data comparisons",
            class_name="ml-8",
        ),
        text(
            "- Convert complicated datasets into accessible reports", class_name="ml-8"
        ),
        text("2.2 Content Moderation", class_name="text-lg font-bold"),
        text("We employ AI systems to:"),
        text("- Detect and prevent spam", class_name="ml-8"),
        text("- Identify inappropriate and/or abusive content", class_name="ml-8"),
        text("- Maintain a professionally focused report pool", class_name="ml-8"),
        class_name="flex-col space-y-2 w-full",
    )


def data_usage() -> rx.Component:
    return flex(
        text("3. Data Usage in AI Systems", class_name="text-2xl font-bold"),
        rx.divider(),
        text("3.1 Data Protection", class_name="text-lg font-bold"),
        text("We maintain strict data protection standards:"),
        text(
            "- No personal data is transmitted to third-party inference servers",
            class_name="ml-8",
        ),
        text("- All data processed by AI systems is anonymized", class_name="ml-8"),
        text(
            "- Moderation systems operate only on report content, not user data",
            class_name="ml-8",
        ),
        text("3.2 Training Data", class_name="text-lg font-bold"),
        text("While training internal AI models:"),
        text(
            "- We do not use user identifiable data in datasets", class_name="ml-8"
        ),
        text(
            "- We will not license or sell training data to third parties",
            class_name="ml-8",
        ),
        class_name="flex-col space-y-2 w-full",
    )


def ai_oversight() -> rx.Component:
    return flex(
        text("4. AI System Oversight", class_name="text-2xl font-bold"),
        rx.divider(),
        text(
            "We maintain oversight of our AI systems through a combination of human review, and periodic system audits. We also provide the ability for our users to provide direct feedback to our developers."
        ),
        class_name="flex-col space-y-2 w-full",
    )


def transparency() -> rx.Component:
    return flex(
        text("5. Transparency", class_name="text-2xl font-bold"),
        rx.divider(),
        text("We are committed to transparency to accomplish:"),
        text(
            "- Protecting the sensitive identities of our user base", class_name="ml-8"
        ),
        text(
            "- Enhancing trust by revealing certain processes of our system components",
            class_name="ml-8",
        ),
        class_name="flex-col space-y-2 w-full",
    )


def user_rights() -> rx.Component:
    return flex(
        text("6. User Rights", class_name="text-2xl font-bold"),
        rx.divider(),
        text("You have the right:"),
        text(
            "- To know when you are interacting with an AI system.", class_name="ml-8"
        ),
        text(
            "- To request human review of AI-moderated decisions", class_name="ml-8"
        ),
        text(
            "- Opt out of AI features where technically feasible", class_name="ml-8"
        ),
        text("- Submit feedback about AI system performance", class_name="ml-8"),
        class_name="flex-col space-y-2 w-full",
    )


def future_developments() -> rx.Component:
    return flex(
        text("7. Future developments", class_name="text-2xl font-bold"),
        rx.divider(),
        text(
            "We reserve the right to develop features and capabilities based off of your contributed data that benefit our user base and the national nursing profession."
        ),
        text("We may in the future:"),
        text("- Improve our AI using contributed data", class_name="ml-8"),
        text(
            "- Modify this policy as technology and opportunity evolves",
            class_name="ml-8",
        ),
        class_name="flex-col space-y-2 w-full",
    )


def policy_changes() -> rx.Component:
    return flex(
        text("8. Changes to This Policy", class_name="text-2xl font-bold"),
        rx.divider(),
        text(
            "We may update this AI Policy from time to time. We will notify you of any changes by posting the new AI Policy on this page and updating the Last Updated date."
        ),
        class_name="flex-col space-y-2 w-full",
    )


def contact_us() -> rx.Component:
    return flex(
        text("9. Contact Us", class_name="text-2xl font-bold"),
        rx.divider(),
        text(
            "If you have any questions about this AI Policy, please contact us using the button below."
        ),
        flex(
            solid_button(
                "Contact Us",
                size="3",
                on_click=rx.redirect("/contact-us"),
                class_name="w-full",
            ),
            class_name="pt-8 pb-4 w-full",
        ),
        class_name="flex-col space-y-2 w-full",
    )
