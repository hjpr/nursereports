import reflex as rx


class Confetti(rx.Component):
    """Wrapped react-confetti component. Renders a full-window confetti
    animation. Pass ``run=True`` to start and ``run=False`` to stop."""

    library = "react-confetti"
    tag = "ReactConfetti"
    is_default = True

    # Whether confetti is currently firing.
    run: rx.Var[bool] = True  # type: ignore

    # Number of confetti pieces.
    number_of_pieces: rx.Var[int] = 200  # type: ignore

    # If True, confetti will stop generating new pieces after the initial burst
    # and then fall away.
    recycle: rx.Var[bool] = True  # type: ignore

    # Width of the confetti canvas (defaults to window width via JS).
    width: rx.Var[int]  # type: ignore

    # Height of the confetti canvas (defaults to window height via JS).
    height: rx.Var[int]  # type: ignore

    # Wind strength (-1 to 1).
    wind: rx.Var[float]  # type: ignore

    # Gravity (0 to 1).
    gravity: rx.Var[float]  # type: ignore

    # Opacity of each confetti piece (0 to 1).
    opacity: rx.Var[float]  # type: ignore


confetti = Confetti.create
