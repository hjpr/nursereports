import re
import reflex as rx

_TEXT_SIZES: dict[str, str] = {
    "xs": "text-xs",
    "sm": "text-sm",
    "md": "text-base",
    "lg": "text-lg",
    "xl": "text-xl",
}

_HEADING_SIZES: dict[str, str] = {
    "sm":  "text-lg",
    "md":  "text-xl",
    "lg":  "text-2xl",
    "xl":  "text-3xl",
    "2xl": "text-4xl md:text-5xl",
    "3xl": "text-5xl md:text-6xl",
}

_WEIGHTS: dict[str, str] = {
    "thin":      "font-thin",
    "light":     "font-light",
    "normal":    "font-normal",
    "medium":    "font-medium",
    "semibold":  "font-semibold",
    "bold":      "font-bold",
    "extrabold": "font-extrabold",
}

_DEFAULT_TEXT_COLOR = "text-neutral-700 dark:text-neutral-300"
_DEFAULT_HEADING_COLOR = "text-neutral-950 dark:text-neutral-50"


_STRIP_RE = re.compile(
    r"^(?:[a-z]+:)?"
    r"(?:"
    r"text-(?:xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl)"           # size
    r"|text-(?:[a-z]+-\d+|white|black|transparent|current|inherit)"          # color
    r"|font-(?:thin|light|normal|medium|semibold|bold|extrabold|black)"      # weight
    r")$"
)


def _strip_conflicting(class_name: str) -> str:
    """Remove size, color, and weight text/font classes that conflict with our params."""
    return " ".join(t for t in class_name.split() if not _STRIP_RE.match(t))


def text(
    *children,
    size: str = "md",
    weight: str = "normal",
    color: str | None = None,
    style: dict | None = None,
    **props,
) -> rx.Component:
    """
    Body text.
      size:   xs | sm | md | lg | xl  (default: md)
      weight: thin | light | normal | medium | semibold | bold | extrabold  (default: normal)
      color:  Tailwind color token without the 'text-' prefix, e.g. 'blue-600'  (default: neutral)
      style:  inline style dict for one-off overrides
    """
    user_classes = _strip_conflicting(props.pop("class_name", ""))
    size_cls = _TEXT_SIZES.get(size, _TEXT_SIZES["md"])
    weight_cls = _WEIGHTS.get(weight, _WEIGHTS["normal"])
    color_cls = f"text-{color}" if color else _DEFAULT_TEXT_COLOR
    class_name = " ".join(filter(None, [size_cls, weight_cls, color_cls, user_classes]))
    return rx.text(*children, class_name=class_name, style=style, **props)


def heading(
    *children,
    size: str = "lg",
    weight: str = "bold",
    color: str | None = None,
    style: dict | None = None,
    **props,
) -> rx.Component:
    """
    Heading text.
      size:   sm | md | lg | xl | 2xl | 3xl  (default: lg)
      weight: thin | light | normal | medium | semibold | bold | extrabold  (default: bold)
      color:  Tailwind color token without the 'text-' prefix, e.g. 'blue-600'  (default: neutral)
      style:  inline style dict for one-off overrides
    """
    user_classes = _strip_conflicting(props.pop("class_name", ""))
    size_cls = _HEADING_SIZES.get(size, _HEADING_SIZES["lg"])
    weight_cls = _WEIGHTS.get(weight, _WEIGHTS["bold"])
    color_cls = f"text-{color}" if color else _DEFAULT_HEADING_COLOR
    class_name = " ".join(filter(None, ["tracking-tight", size_cls, weight_cls, color_cls, user_classes]))
    return rx.text(*children, class_name=class_name, style=style, **props)
