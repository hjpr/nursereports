import reflex as rx

_LINK = (
    "text-neutral-600 dark:text-neutral-400 "
    "hover:text-neutral-900 dark:hover:text-neutral-100 "
    "transition-colors duration-150 "
    "cursor-pointer"
)

_LINK_ACCENT = (
    "text-teal-600 dark:text-teal-500 "
    "hover:text-teal-700 dark:hover:text-teal-400 "
    "transition-colors duration-150 "
    "cursor-pointer"
)


def link(*children, accent: bool = False, **props) -> rx.Component:
    """
    Inline text link.

    accent=True  — teal color, for primary in-content links.
    accent=False — neutral muted color (default), for nav/footer links.
    """
    base = _LINK_ACCENT if accent else _LINK
    user_classes = props.pop("class_name", "")
    return rx.link(
        *children,
        class_name=f"{base} {user_classes}".strip(),
        **props,
    )
