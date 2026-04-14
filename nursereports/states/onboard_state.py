from .user_state import UserState

from typing import Callable, Iterable

import random
import reflex as rx


FIRST_ADJECTIVES = [
    "Antsy", "Artful", "Bold", "Brazen", "Brave", "Bright", "Calm",
    "Clever", "Crisp", "Daring", "Deft", "Dynamic", "Eager", "Earnest",
    "Edgy", "Feisty", "Fierce", "Frank", "Grounded", "Gritty", "Hardy",
    "Humble", "Icy", "Inquisitive", "Jazzy", "Jaunty", "Jolly", "Keen",
    "Kinetic", "Kooky", "Lively", "Loyal", "Merry", "Nimble", "Noble",
    "Peppy", "Plucky", "Quick", "Radiant", "Savvy", "Steely", "Swift",
    "Tender", "Upbeat", "Vibrant", "Witty", "Wily", "Wry", "Zesty",
    "Zippy", "Snappy", "Sturdy", "Sprightly", "Steady", "Sharp", "Rugged",
    "Spirited", "Spunky", "Sunny", "Sassy", "Serene", "Sleek", "Smooth",
]

SECOND_ADJECTIVES = [
    "Abundant", "Amazing", "Balanced", "Brilliant", "Capable", "Cheerful",
    "Dedicated", "Dynamic", "Earnest", "Energetic", "Essential", "Fabulous",
    "Faithful", "Glowing", "Graceful", "Harmonious", "Hopeful", "Inspired",
    "Innovative", "Joyful", "Jubilant", "Knowing", "Knowledgeable", "Limitless",
    "Luminous", "Magnetic", "Mindful", "Natural", "Noble", "Optimal",
    "Persistent", "Powerful", "Quirky", "Radiant", "Resilient", "Serene",
    "Steadfast", "Tenacious", "Thoughtful", "Unwavering", "Uplifting",
    "Valiant", "Versatile", "Vibrational", "Watchful", "Wholesome",
    "Wonderful", "Yearning", "Zealous", "Extraordinary", "Phenomenal",
    "Remarkable", "Stellar", "Triumphant", "Vivacious", "Whimsical",
    "Electrifying", "Formidable", "Galvanizing", "Illuminated", "Magnificent",
]

DOER_NOUNS = [
    "Achiever", "Advocate", "Believer", "Builder", "Carer", "Champion",
    "Climber", "Connector", "Creator", "Doer", "Dreamer", "Explorer",
    "Enthusiast", "Expert", "Finder", "Giver", "Grower", "Guardian",
    "Healer", "Helper", "Jumper", "Keeper", "Leader", "Learner",
    "Listener", "Maker", "Mentor", "Mover", "Navigator", "Nurturer",
    "Pioneer", "Planner", "Runner", "Scholar", "Seeker", "Sharer",
    "Solver", "Speaker", "Strider", "Supporter", "Teacher", "Thinker",
    "Trainer", "Wanderer", "Watcher", "Worker", "Striver", "Pathfinder",
    "Trailblazer", "Catalyst", "Innovator", "Protector", "Luminary",
]

AVATARS = [
    "avatar_1",
    "avatar_2",
    "avatar_3",
    "avatar_4",
    "avatar_5",
    "avatar_6",
]

_NAME_COUNT = 6


class OnboardState(UserState):
    has_review: str = ""
    license: str = ""
    license_state: str = ""

    # Identity step
    generated_names: list[str] = []
    name_index: int = 0
    name_key: int = 0
    slide_direction: str = "right"

    selected_icon: str = ""

    # ---------------------------------------------------------------------------
    # Computed vars — name carousel
    # ---------------------------------------------------------------------------

    @rx.var
    def display_name(self) -> str:
        if self.generated_names:
            return self.generated_names[self.name_index]
        return ""

    @rx.var
    def can_go_back(self) -> bool:
        return self.name_index > 0

    @rx.var
    def can_go_forward(self) -> bool:
        return self.name_index < len(self.generated_names) - 1

    # ---------------------------------------------------------------------------
    # Event handlers — name carousel
    # ---------------------------------------------------------------------------

    def _new_name(self) -> str:
        first = random.choice(FIRST_ADJECTIVES)
        second = random.choice(SECOND_ADJECTIVES)
        doer = random.choice(DOER_NOUNS)
        return f"{first}{second}{doer}"

    def event_state_generate_display_name(self) -> None:
        """Generate all names at once on identity page load. Idempotent."""
        if not self.generated_names:
            self.generated_names = [self._new_name() for _ in range(_NAME_COUNT)]
            self.name_index = 0
            self.name_key = 0

    def event_state_name_next(self) -> None:
        if self.name_index < len(self.generated_names) - 1:
            self.slide_direction = "right"
            self.name_index += 1
            self.name_key += 1

    def event_state_name_prev(self) -> None:
        if self.name_index > 0:
            self.slide_direction = "left"
            self.name_index -= 1
            self.name_key += 1

    # ---------------------------------------------------------------------------
    # Event handlers — step navigation
    # ---------------------------------------------------------------------------

    def set_license(self, license: str) -> None:
        self.license = license
        self.license_state = ""
        self.has_review = ""
        if license == "Nursing Student":
            self.has_review = "No"

    def event_state_next_from_identity(self) -> Iterable[Callable]:
        if not self.display_name:
            return rx.toast.error("A display name is required.")
        yield rx.redirect("/onboard/avatar")

    def event_state_next_from_avatar(self) -> Iterable[Callable]:
        if not self.selected_icon:
            return rx.toast.error("Please choose an avatar.")
        yield rx.redirect("/onboard/background")

    def event_state_onboard_flow(self) -> Callable:
        return rx.redirect("/dashboard") if not self.user_needs_onboarding else None

    def event_state_submit_onboard(self) -> Iterable[Callable]:
        try:
            if not self.display_name or not self.selected_icon:
                return rx.toast.error("Please complete your identity setup.")

            if not (self.license and self.license_state and self.has_review):
                return rx.toast.error("Please complete all required fields.")

            user_info = {
                "professional": {
                    "license_type": self.license,
                    "license_state": self.license_state,
                    "license_number": "01234567890",
                },
                "account": {
                    "status": "onboard" if self.has_review == "Yes" else "active",
                    "display_name": self.display_name,
                    "icon": self.selected_icon,
                },
            }
            self.update_user_info_and_sync_locally(user_info)

            if self.user_needs_onboarding:
                yield rx.redirect("/search/hospital")
            else:
                yield rx.redirect("/dashboard")

            self.user_is_loading = False

        except Exception as e:
            self.user_is_loading = False
            return rx.toast.error(str(e), close_button=True)
