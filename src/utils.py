"""Utility functions for the project."""

from typing import Any, Callable

import sys


def quit_safely(func: Callable[..., Any]) -> Callable[..., Any]:
    """Handle KeyboardInterrupt and EOFError on interactive programs to
    exit gracefully.

    :param func: this is the function to be decorated
    :type func: Callable[..., Any]
    :returns: the decorated function which handles interruption signals
    :rtype: Callable[..., Any]
    :example: @quit_safely def main(): pass

    """

    def aux() -> None:
        """Auxiliary function to draft the decorator.

        :returns: None
        :rtype: None

        """

        # handle exit signals
        try:
            func()
        # Ctrl-C / Ctrl-D
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)

    return aux


def next_char_in_string(string: str, char: str) -> str:
    """Find next character of another one in a string.

    :param string: the string to be searched
    :type string: str
    :param char: the character to be searched for
    :type char: str
    :returns: the next character after the first occurrence of `char` in `string`
    :rtype: str
    :example: next_char_in_string('ABC', 'A') -> 'B', next_char_in_string('ABC', 'C') -> 'A'
    :raises valueError: raises an exception if `char` is not in `string`
    :example: next_char_in_string('ABC', 'D') -> ValueError

    """

    return string[(string.index(char) + 1) % len(string)]


def letter_to_number(letter: str) -> int:
    """Convert a letter to its corresponding number.

    :param letter: the letter to be converted
    :type letter: str
    :returns: the corresponding number
    :rtype: int
    :example: letter_to_number('A') -> 0, letter_to_number('Z') -> 25
    :raises ValueError: raises an exception if `letter` is not a string or a single letter
    :example: letter_to_number('AB') -> ValueError

    """

    return ord(letter) - 65
