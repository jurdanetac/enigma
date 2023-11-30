from typing import Any, Callable

import sys


def quit_safely(func: Callable[..., Any]) -> Callable[..., Any]:
    """Handle KeyboardInterrupt and EOFError on interactive programs"""

    def aux() -> None:
        """Auxiliary function"""

        # handle exit signals
        try:
            func()
        # Ctrl-C / Ctrl-D
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)

    return aux


def next_char_in_string(string: str, char: str) -> str:
    """Return the next character after the first occurrence of `char` in `string`.
    Wraps at the end of the string and returns the first character.
    Raises ValueError if `char` is not in `string`."""

    return string[(string.index(char) + 1) % len(string)]
