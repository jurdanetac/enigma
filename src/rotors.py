# pylint: disable=locally-disabled, fixme, line-too-long

"""Module for Enigma's rotors and reflectors."""


from string import ascii_uppercase

from utils import check_key, letter_to_number, next_char_in_string


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

    def __init__(self, key: str, kind: str) -> None:
        """Initialize stator with character mappings."""

        if check_key(key, kind):
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

    def __init__(
        self, key: str, notch: str, current_top: str, ring_setting: str
    ) -> None:
        """Initialize rotor with character mappings and turnover."""

        # initialize stator
        # super().__init__(key, kind="rotor")

        # check key
        if check_key(key=key, kind="rotor"):
            self.key: str = key

        # letter that is visible on top window when turnover happens
        self.notch: str = notch
        # letter visible on top window
        self.current_top: str = current_top
        # relative wiring offset
        self.ring_setting: str = ring_setting

    def set_current_top(self, letter: str) -> None:
        """Set current letter on top of the rotor.

        :param letter: letter to be set on top
        :type current_top: str
        :returns: None
        :rtype: None
        :raises ValueError: if letter is not a single character or not in the alphabet
        :example: rotor.set_current_top("A") -> None

        """

        # convert letter to uppercase and remove whitespaces
        letter = letter.strip().upper()

        # do nothing if letter is already on top
        if self.current_top == letter:
            return
        elif len(letter) != 1:
            raise ValueError("Letter must be a single character.")
        elif letter not in ascii_uppercase:
            raise ValueError("Letter must be in the alphabet.")
        elif letter > self.current_top:
            # rotate key until letter is on top
            for _ in range(
                abs(letter_to_number(self.current_top) - letter_to_number(letter))
            ):
                self.key = self.key[-1] + self.key[:-1]
        elif letter < self.current_top:
            # rotate key backwards until letter is on top
            for _ in range(
                letter_to_number(self.current_top) - letter_to_number(letter)
            ):
                self.key = self.key[1:] + self.key[0]

        # replace current letter on top
        self.current_top = letter

    def turn(self) -> None:
        """Turn rotor by one letter.

        :returns: None
        :rtype: None
        :example: rotor.turn() -> None

        """

        # rotate key by one letter
        self.key = self.key[1:] + self.key[0]

        # rotate current letter on top by one letter
        self.current_top = next_char_in_string(ascii_uppercase, self.current_top)

    def reverse_get_key(self) -> str:
        """Get rotor's character mappings when current's flowing backwards"""

        # hold output in another variable, since python strings are immutable
        new_key: str = ""

        for letter in ascii_uppercase:
            # case current flowing backwards, rotors after reflector
            new_key += self.reverse_encrypt_letter(letter)

        return new_key

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

        # ring setting offset
        for _ in range(letter_to_number(self.ring_setting)):
            resulting = next_char_in_string(ascii_uppercase, resulting)

        return resulting

    def reverse_encrypt_letter(self, letter: str) -> str:
        """TODO"""
        ltr: str = chr(self.key.index(letter) + 65)
        resulting: str = ltr

        for _ in range(letter_to_number(self.ring_setting)):
            resulting = next_char_in_string(ascii_uppercase, resulting)

        return resulting


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
