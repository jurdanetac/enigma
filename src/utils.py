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


def format_key(
    key: str,
    letter: str,
    indicator: str = "",
    delimiters: tuple = ("(", ")"),
) -> str:
    """Format a key to be printed to stdout.

    :param key: key to be formatted
    :type key: str
    :param letter: letter to find
    :type letter: str
    :param indicator: indicator of which encryption layer, defaults to ""
    :type indicator: str, optional
    :param delimiters: pair of characters to use to surround the letter in the key, defaults to ("(", ")")
    :type delimiters: tuple, optional
    :returns: formatted key to be printed to stdout
    :rtype: str
    :raises ValueError: if key is empty or not a string
    :example: self._fmt_key(key="ABC", letter="B", indicator="1>") -> "1> A(B)C"

    """

    # remove whitespace from key
    key = key.strip()

    if not key or not isinstance(key, str):
        return ""

    # split key into two halves and surround with a delimiter
    letter_to_find_index: int = letter_to_number(letter)
    key_first_half: str = key[:letter_to_find_index]
    key_second_half: str = key[letter_to_find_index + 1 :]
    formatted_key: str = f"{indicator} {key_first_half}{delimiters[0]}{key[letter_to_find_index]}{delimiters[1]}{key_second_half}"

    return formatted_key


def check_key(key: str, kind: str) -> bool:
    """Check if key is in valid format.

    :param key: character mappings
    :type key: str
    :param kind: type of key to be checked
    :type kind: str
    :returns: True if key is in valid format
    :rtype: bool
    :raises ValueError: if key is not in valid format
    :example: stator.check_key("EJMZALYXVBWFCRQUONTSPIKHGD") -> True

    """

    # convert key to uppercase and remove whitespaces
    key = key.upper().strip()

    ## Check if key is in valid format
    if kind == "reflector":
        ## Conditions that must be true for reflectors
        # True if key is a string, False otherwise
        instance: bool = isinstance(key, str)
        # True if key has 26 characters, False otherwise
        length: bool = len(key) == 26
        # True if key only contains letters, False otherwise
        alphabetical: bool = key.isalpha()
        # True if all characters in key are unique, False otherwise
        unique: bool = len(set(key)) == len(key)

        # check if key is alphabetical and has 26 non-repeating characters
        if not (instance and length and alphabetical and unique):
            raise ValueError("Key must be a string of 26 letters.")

        # list of tuples which represent the wirings of the reflector
        pairs: list[tuple] = [(key[i], chr(i + 65)) for i in range(26)]

        # the wirings are connected as a loop between two letters
        if len(set(map(tuple, map(sorted, pairs)))) != 13:
            raise ValueError("Wrong characters mappings.")
    # plugboard
    elif kind == "plugboard":
        ## Conditions that must be true for plugboards
        # TODO
        pass
    # rotors
    else:
        ## Conditions that must be true for rotors
        # TODO
        pass

    return True


def switch(string: str, a: str, b: str) -> str:
    """Returns a string with all occurrences of `a` replaced by `b` and vice-versa.

    :param string: string to be switched
    :type string: str
    :param a: first character
    :type a: str
    :param b: second character
    :type b: str
    :returns: switched string
    :rtype: str
    :raises ValueError: if `a` or `b` are not single characters or not in the alphabet
    :example: switch("ABC", "A", "B") -> "BAC"

    """

    return string.translate(str.maketrans({a: b, b: a}))
