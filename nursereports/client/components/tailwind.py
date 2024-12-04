from loguru import logger

import reflex as rx


FLEX_CLASSES = "flex bg-zinc-50 dark:bg-zinc-900 dark:border-zinc-500"
ICON_CLASSES = "text-zinc-700 dark:text-zinc-50"
INPUT_CLASSES = "border border-solid border-zinc-300 dark:border-zinc-500 ring-0 bg-zinc-100 dark:bg-zinc-800"
LINK_CLASSES = "text-zinc-700 dark:text-zinc-50 hover:text-zinc-700 dark:hover:text-zinc-50 cursor-pointer"
OUTLINE_BUTTON_CLASSES = "bg-zinc-50 border border-solid border-zinc-300 text-zinc-700 dark:bg-zinc-800 dark:border-zinc-500 dark:text-zinc-50 cursor-pointer"
SOLID_BUTTON_CLASSES = "bg-teal-600 dark:bg-teal-700 cursor-pointer"
TEXT_CLASSES = "text-zinc-700 dark:text-zinc-300"


def merged_class_name(default_classes: str, user_defined_classes: str) -> str:
    return f"{default_classes} {user_defined_classes}".strip()


def flex(*children, **props) -> rx.Component:
    default_classes = FLEX_CLASSES
    user_defined_classes = props.pop("class_name", "")
    return rx.flex(*children, class_name=merged_class_name(default_classes, user_defined_classes), **props)


def icon(*children, **props) -> rx.Component:
    default_classes = ICON_CLASSES
    user_defined_classes = props.pop("class_name", "")
    return rx.icon(*children, class_name=merged_class_name(default_classes, user_defined_classes), **props)

def input(*children, **props) -> rx.Component:
    default_classes = INPUT_CLASSES
    user_defined_classes = props.pop("class_name", "")
    return rx.input(*children, class_name=merged_class_name(default_classes, user_defined_classes), **props)

def link(*children, **props) -> rx.Component:
    default_classes = LINK_CLASSES
    user_defined_classes = props.pop("class_name", "")
    return rx.link(*children, class_name=merged_class_name(default_classes, user_defined_classes), **props)


def outline_button(*children, **props) -> rx.Component:
    default_classes = OUTLINE_BUTTON_CLASSES
    user_defined_classes = props.pop("class_name", "")
    return rx.button(*children, class_name=merged_class_name(default_classes, user_defined_classes), **props)


def solid_button(*children, **props) -> rx.Component:
    default_classes = SOLID_BUTTON_CLASSES
    user_defined_classes = props.pop("class_name", "")
    return rx.button(*children, class_name=merged_class_name(default_classes, user_defined_classes), **props)


def text(*children, **props) -> rx.Component:
    default_classes = TEXT_CLASSES
    user_defined_classes = props.pop("class_name", "")
    return rx.text(*children, class_name=merged_class_name(default_classes, user_defined_classes), **props)
