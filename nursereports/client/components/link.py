import reflex as rx

_LINK = (
    "text-neutral-600 dark:text-neutral-400 "
    "hover:text-neutral-900 dark:hover:text-neutral-100 "
    "transition-colors duration-150 "
    "cursor-pointer"
)

_LINK_ACCENT = (
    "text-sky-600 dark:text-sky-400 "
    "hover:text-sky-700 dark:hover:text-sky-300 "
    "transition-colors duration-150 "
    "cursor-pointer"
)


def link(*children, accent: bool = False, **props) -> rx.Component:
    """
    Inline text link.

    accent=True  — sky color, for primary in-content links.
    accent=False — neutral muted color (default), for nav/footer links.
    """
    base = _LINK_ACCENT if accent else _LINK
    user_classes = props.pop("class_name", "")
    return rx.link(
        *children,
        class_name=f"{base} {user_classes}".strip(),
        **props,
    )
