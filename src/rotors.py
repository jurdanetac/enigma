# pylint: disable=locally-disabled, fixme, line-too-long

"""Module for Enigma's rotors and reflectors."""


from dataclasses import dataclass
from string import ascii_uppercase

from utils import letter_to_number, next_char_in_string


class Stator:
    """Class for stators, such as the Enigma's plugboard and reflector.

    :param key: character mappings
    :type key: str
    :param kind: type of stator (plugboard or reflector)
    :type kind: str
    :returns: Stator
    :rtype: Stator
    :raises ValueError: if key is not a string of 26 letters
    :example: Stator(key="EJMZALYXVBWFCRQUONTSPIKHGD")

    """

    def check_key(self, key: str) -> bool:
        """Check if key is in valid format.

        :param key: character mappings
        :type key: str
        :returns: True if key is in valid format
        :rtype: bool
        :raises ValueError: if key is not in valid format
        :example: stator.check_key("EJMZALYXVBWFCRQUONTSPIKHGD") -> True

        """

        # convert key to uppercase and remove whitespaces
        key = key.upper().strip()

        ## Check if key is in valid format
        if self.kind == "reflector":
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
        else:
            ## Conditions that must be true for plugboards
            # TODO
            pass

        return True

    def __init__(self, key: str, kind: str) -> None:
        """Initialize stator with character mappings."""

        self.kind: str = kind

        if self.check_key(key):
            self.key: str = key

    def encrypt_letter(self, letter: str) -> str:
        """Substitute a letter using the stator's character mappings.
        The key is a string of 26 characters, where character X is mapped to
        character Y, and B must be mapped to A (contrary to rotors) and so on.

        :param letter: letter to be substituted
        :type letter: str
        :returns: encrypted letter
        :rtype: str
        :example: stator.encrypt_letter("A") -> "E"

        """

        return self.key[letter_to_number(letter)]

    def get_key(self) -> str:
        """Get rotor's character mappings.

        :returns: rotor's character mappings
        :rtype: str
        :example: rotor.get_key() -> "EJMZALYXVBWFCRQUONTSPIKHGD"

        """

        # hold output in another variable, since python strings are immutable
        new_key: str = ""

        for letter in ascii_uppercase:
            # case current flowing backwards, rotors after reflector
            new_key += self.encrypt_letter(letter)

        return new_key


@dataclass
class Rotor(Stator):
    """Class that models Enigma's rotors.
    Can be used to create custom rotors, since some defaults are provided
    as variables at tail of this file.

    :param key: character mappings
    :type key: str
    :param notch: letter at which the rotor will turn the adjacent rotor
    :type notch: str
    :param current_top: letter visible on top window of the rotor
    :type current_top: str
    :param ring_setting: letter at which the wiring will be offset
    :type ring_setting: str
    :returns: Rotor
    :rtype: Rotor
    :example: Rotor(key="EKMFLGDQVZNTOWYHXUSPAIBRCJ", notch="Q", current_top="A", ring_setting="A")

    """

    # substitution key
    key: str
    # turnover
    notch: str
    # initial letter on top
    current_top: str
    # wiring offset
    ring_setting: str

    def set_current_top(self, letter: str) -> None:
        """Set current letter on top of the rotor.

        :param letter: letter to be set on top
        :type current_top: str
        :returns: None
        :rtype: None
        :example: rotor.set_current_top("A")

        """

        # rotate key until letter is on top
        for _ in range(letter_to_number(letter)):
            self.key = self.key[-1] + self.key[:-1]

        # replace current letter on top
        self.current_top = letter

    def encrypt_letter(self, letter: str) -> str:
        """Encrypt a letter using the rotor's character mappings.

        :param letter: letter to be encrypted
        :type letter: str
        :returns: encrypted letter
        :rtype: str
        :example: rotor.encrypt_letter("A") -> "E"

        """
        ltr: str = self.key[letter_to_number(letter)]
        resulting: str = ltr

        for _ in range(letter_to_number(self.ring_setting)):
            resulting = next_char_in_string(ascii_uppercase, resulting)

        return resulting

    def turn(self) -> None:
        """TODO"""

        # Update current letter on top of the rotor
        self.current_top = next_char_in_string(ascii_uppercase, self.current_top)
        # Rotate key by one
        self.key = self.key[-1] + self.key[:-1]

    def reverse_encrypt_letter(self, letter: str) -> str:
        """TODO"""
        ltr: str = chr(self.key.index(letter) + 65)
        resulting: str = ltr

        for _ in range(letter_to_number(self.ring_setting)):
            resulting = next_char_in_string(ascii_uppercase, resulting)

        return resulting

    def reverse_get_key(self) -> str:
        """Get rotor's character mappings when current's flowing backwards"""

        # hold output in another variable, since python strings are immutable
        new_key: str = ""

        for letter in ascii_uppercase:
            # case current flowing backwards, rotors after reflector
            new_key += self.reverse_encrypt_letter(letter)

        return new_key


## Default rotors and reflectors

ROTOR_I: Rotor = Rotor(
    key="EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    notch="Q",
    current_top="A",
    ring_setting="A",
)

ROTOR_II: Rotor = Rotor(
    key="AJDKSIRUXBLHWTMCQGZNPYFVOE",
    notch="E",
    current_top="A",
    ring_setting="A",
)

ROTOR_III: Rotor = Rotor(
    key="BDFHJLCPRTXVZNYEIWGAKMUSQO",
    notch="V",
    current_top="A",
    ring_setting="A",
)

ROTOR_IV: Rotor = Rotor(
    key="ESOVPZJAYQUIRHXLNFTGKDCMWB",
    notch="J",
    current_top="A",
    ring_setting="A",
)

ROTOR_V: Rotor = Rotor(
    key="VZBRGITYUPSDNHLXAWMJQOFECK",
    notch="Z",
    current_top="A",
    ring_setting="A",
)

PLUGBOARD_EMPTY: Stator = Stator(key=ascii_uppercase, kind="plugboard")
REFLECTOR_A: Stator = Stator(key="EJMZALYXVBWFCRQUONTSPIKHGD", kind="reflector")
REFLECTOR_B: Stator = Stator(key="YRUHQSLDPXNGOKMIEBFZCWVJAT", kind="reflector")
REFLECTOR_C: Stator = Stator(key="FVPJIAOYEDRZXWGCTKUQSBNMHL", kind="reflector")
REFLECTOR_B_THIN: Stator = Stator(key="ENKQAUYWJICOPBLMDXZVFTHRGS", kind="reflector")
REFLECTOR_C_THIN: Stator = Stator(key="RDOBJNTKVEHMLFCWZAXGYIPSUQ", kind="reflector")
