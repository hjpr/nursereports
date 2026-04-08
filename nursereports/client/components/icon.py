import reflex as rx

_ICON = "text-neutral-600 dark:text-neutral-400"
_ICON_ACCENT = "text-emerald-600 dark:text-emerald-500"
_ICON_MUTED = "text-neutral-400 dark:text-neutral-600"


def icon(tag: str, accent: bool = False, muted: bool = False, **props) -> rx.Component:
    """
    Icon with default neutral color.

    accent=True  — teal color for decorative/branded icons.
    muted=True   — dimmer neutral for secondary/metadata icons.
    """
    if accent:
        base = _ICON_ACCENT
    elif muted:
        base = _ICON_MUTED
    else:
        base = _ICON

    user_classes = props.pop("class_name", "")
    return rx.icon(
        tag,
        class_name=f"{base} {user_classes}".strip(),
        **props,
    )
