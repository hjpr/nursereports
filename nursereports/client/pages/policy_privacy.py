from ...states import BaseState

import reflex as rx


@rx.page(
    route="/policy/privacy",
    title="Nurse Reports",
    on_load=BaseState.event_state_auth_flow,
)
def privacy_policy_page() -> rx.Component:
    return rx.flex(
        content(),
        class_name="flex-col bg-gradient-to-b from-teal-100 to-cyan-100 items-center justify-center p-4 min-h-screen w-full",
    )


def content() -> rx.Component:
    return rx.flex(
        header(),
        introduction(),
        collect_information(),
        use_cookies(),
        use_information(),
        data_security(),
        data_sharing(),
        data_analytics(),
        your_rights(),
        policy_changes(),
        california_privacy_rights(),
        contact_us(),
        class_name="flex-col items-center rounded shadow-lg bg-white p-8 space-y-8 w-full max-w-xl",
    )

def header() -> rx.Component:
    return rx.flex(
        rx.icon("cookie", class_name="h-12 w-12 mt-4 mb-8"),
        rx.text("Privacy Policy", class_name="text-3xl font-bold"),
        rx.text("Last Updated - 10/9/2024", class_name="text-l italic"),
        class_name="flex-col items-center p-4 space-y-2 w-full"
    )


def introduction() -> rx.Component:
    return rx.flex(
        rx.text("1. Introduction", class_name="text-2xl font-bold"),
        rx.divider(),
        rx.text(
            "This Privacy Policy describes how we collect, use, and handle your personal information when you use our website. We are committed to protecting your privacy and ensuring the security of your personal information. This policy applies to users within the United States."
        ),
        class_name="flex-col space-y-2 w-full"
    )


def collect_information() -> rx.Component:
    return rx.flex(
        rx.text("2. Information We Collect", class_name="text-2xl font-bold"),
        rx.divider(),
        rx.text("2.1 Personal Information", class_name="text-lg font-bold"),
        rx.text("We collect the following personal information:"),
        rx.text("- Email address", class_name="ml-8"),
        rx.text("- Password (securely hashed and stored)", class_name="ml-8"),
        rx.text("2.2 Technical Information", class_name="text-lg font-bold"),
        rx.text("We automatically collect:"),
        rx.text(
            "- Authentication tokens via cookies (containing no personally identifiable information)", class_name="ml-8"
        ),
        class_name="flex-col space-y-2 w-full"
    )


def use_cookies() -> rx.Component:
    return rx.flex(
        rx.text("3. How We Use Cookies", class_name="text-2xl font-bold"),
        rx.divider(),
        rx.text("We use only essential cookies that are necessary for the website's basic functionality:"),
        rx.text("- Authentication tokens to keep you logged in", class_name="ml-8"),
        rx.text("- We do not use tracking cookies", class_name="ml-8"),
        rx.text("- We do not use third-party cookies", class_name="ml-8"),
        rx.text(
            "You can configure your browser to refuse cookies, but this may limit your ability to use some features of our website."
        ),
        class_name="flex-col space-y-2 w-full"
    )


def use_information() -> rx.Component:
    return rx.flex(
        rx.text("4. How We Use Your Information", class_name="text-2xl font-bold"),
        rx.divider(),
        rx.text("We use your personal information for:"),
        rx.text("- Account creation and management", class_name="ml-8"),
        rx.text("- Authentication", class_name="ml-8"),
        rx.text("- Providing and improving our services", class_name="ml-8"),
        rx.text("- Analyzing anonymous usage patterns to enhance site functionality/features", class_name="ml-8"),
        rx.text("- Communication regarding your account or our services", class_name="ml-8"),
        class_name="flex-col space-y-2 w-full"
    )


def data_security() -> rx.Component:
    return rx.flex(
        rx.text("5. Data Security", class_name="text-2xl font-bold"),
        rx.divider(),
        rx.text("We implement appropriate security measures to protect your personal information."),
        rx.text("- Passwords are securely stored and hashed", class_name="ml-8"),
        rx.text("- Data is encrypted in transit.", class_name="ml-8"),
        rx.text("- Regular security assessments", class_name="ml-8"),
        rx.text("- Compartmentalized access to personal information via authorized personnel.", class_name="ml-8"),
        class_name="flex-col space-y-2 w-full"
    )


def data_sharing() -> rx.Component:
    return rx.flex(
        rx.text("6. Data Sharing and Third Parties", class_name="text-2xl font-bold"),
        rx.divider(),
        rx.text("We do not:"),
        rx.text("- Sell your personal information to third parties", class_name="ml-8"),
        rx.text("- Share your personal information with third parties", class_name="ml-8"),
        rx.text("- Use third-party tracking tools", class_name="ml-8"),
        class_name="flex-col space-y-2 w-full"
    )


def data_analytics() -> rx.Component:
    return rx.flex(
        rx.text("7. Data Analytics", class_name="text-2xl font-bold"),
        rx.divider(),
        rx.text("We may use anonymous, aggregated data to:"),
        rx.text("- Improve our hospital search algorithms", class_name="ml-8"),
        rx.text("- Enhance user experience and navigation", class_name="ml-8"),
        rx.text("- Analyze website performance", class_name="ml-8"),
        rx.text("- Develop new features to benefit our user base", class_name="ml-8"),
        class_name="flex-col space-y-2 w-full"
    )


def your_rights() -> rx.Component:
    return rx.flex(
        rx.text("8. Your Rights", class_name="text-2xl font-bold"),
        rx.divider(),
        rx.text("You have the right to:"),
        rx.text("- Access your personal information", class_name="ml-8"),
        rx.text("- Correct inaccurate information", class_name="ml-8"),
        rx.text("- Request deletion of your information", class_name="ml-8"),
        class_name="flex-col space-y-2 w-full"
    )


def policy_changes() -> rx.Component:
    return rx.flex(
        rx.text("9. Changes to This Policy", class_name="text-2xl font-bold"),
        rx.divider(),
        rx.text(
            "We may update this Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page and updating the Last Updated date."
        ),
        class_name="flex-col space-y-2 w-full"
    )


def california_privacy_rights() -> rx.Component:
    return rx.flex(
        rx.text("10. California Privacy Rights", class_name="text-2xl font-bold"),
        rx.divider(),
        rx.text(
            "Under California Civil Code Section 1798.83, California residents have the right to request certain information regarding our disclosure of personal information to third parties for their direct marketing purposes. However, we do not share your personal information with third parties for their direct marketing purposes."
        ),
        class_name="flex-col space-y-2 w-full"
    )


def contact_us() -> rx.Component:
    return rx.flex(
        rx.text("11. Contact Us", class_name="text-2xl font-bold"),
        rx.divider(),
        rx.text(
            "If you have any questions about this Privacy Policy, please contact us using the button below."
        ),
        rx.flex(
            rx.button("Contact Us", size="3", on_click=rx.redirect("/contact-us"), class_name="w-full"),
            class_name="pt-8 pb-4 w-full"
        ),
        class_name="flex-col space-y-2 w-full"
    )
