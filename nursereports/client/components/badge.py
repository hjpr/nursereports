import reflex as rx

# Variant → (light bg, dark bg, light text, dark text)
_VARIANTS: dict[str, str] = {
    "sky": (
        "bg-sky-50 dark:bg-sky-950 "
        "text-sky-700 dark:text-sky-400 "
        "border border-sky-200 dark:border-sky-900"
    ),
    "teal": (
        "bg-teal-50 dark:bg-teal-950 "
        "text-teal-700 dark:text-teal-400 "
        "border border-teal-200 dark:border-teal-900"
    ),
    "neutral": (
        "bg-neutral-100 dark:bg-neutral-800 "
        "text-neutral-600 dark:text-neutral-400 "
        "border border-neutral-200 dark:border-neutral-700"
    ),
    "amber": (
        "bg-amber-50 dark:bg-amber-950 "
        "text-amber-700 dark:text-amber-400 "
        "border border-amber-200 dark:border-amber-900"
    ),
    "rose": (
        "bg-rose-50 dark:bg-rose-950 "
        "text-rose-700 dark:text-rose-400 "
        "border border-rose-200 dark:border-rose-900"
    ),
}

_BASE = (
    "inline-flex items-center gap-1.5 "
    "rounded-full px-3 py-1 "
    "text-xs font-medium tracking-wide"
)


def badge(*children, variant: str = "sky", **props) -> rx.Component:
    """
    Small pill badge / tag.

    variant: "sky" (default) | "neutral" | "amber" | "rose" | "teal" (legacy)
    """
    color_classes = _VARIANTS.get(variant, _VARIANTS["sky"])
    user_classes = props.pop("class_name", "")
    return rx.flex(
        *children,
        class_name=f"{_BASE} {color_classes} {user_classes}".strip(),
        **props,
    )
