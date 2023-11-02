"""TODO"""

from dataclasses import dataclass

from string import ascii_uppercase


def next_char_in_string(string: str, letter: str) -> str:
    """TODO"""
    return string[(string.index(letter) + 1) % len(string)]


@dataclass(frozen=True)
class DefaultKeys:
    """TODO"""

    ROTORS = {
        "I": {"key": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "notch": "Q"},
        "II": {"key": "AJDKSIRUXBLHWTMCQGZNPYFVOE", "notch": "E"},
        "III": {"key": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "notch": "V"},
        "IV": {"key": "ESOVPZJAYQUIRHXLNFTGKDCMWB", "notch": "J"},
        "V": {"key": "VZBRGITYUPSDNHLXAWMJQOFECK", "notch": "Z"},
        # TODO implement other rotors
        # "VI": {"key": "JPGVOUMFYQBENHZRDKASXLICTW", "notch": ""},
        # "VII": {"key": "NZJHGRCXMYSWBOUFAIVLPEKQDT", "notch": ""},
        # "VIII": {"key": "FKQHTLXOCBJSPDZRAMEWNIUYGV", "notch": ""},
    }

    PLUGBOARD = {
        "empty": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "test": "CBADEIGHFJKLMNOPQRSTUVWXYZ",
    }

    REFLECTORS = {
        "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
        "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
        "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL",
        "B Thin": "ENKQAUYWJICOPBLMDXZVFTHRGS",
        "C Thin": "RDOBJNTKVEHMLFCWZAXGYIPSUQ",
    }


@dataclass
class StaticRotor:
    """TODO"""

    # substitution key
    key: str

    def encrypt_letter(self, letter: str) -> str:
        """TODO"""

        return self.key[ord(letter) - 65]

    def get_key(self) -> str:
        """Get rotor's character mappings"""

        # hold output in another variable, since python strings are immutable
        new_key: str = ""

        for letter in ascii_uppercase:
            # case current flowing backwards, rotors after reflector
            new_key += self.encrypt_letter(letter)

        return new_key


@dataclass
class Rotor(StaticRotor):
    """TODO"""

    # substitution key
    key: str
    # turnover
    notch: str
    # initial letter on top
    current_top: str
    # wiring offset
    ring_setting: str

    def __post_init__(self) -> None:
        """Perform after-initialization rotor tasks"""

        # Inherit StaticRotor key and encrypt_letter method
        super().__init__(self.key)

        # Change position of alphabet ring
        for _ in range(ord(self.ring_setting) - 65):
            # Each character means first character encrypts to the nth position
            # The ring setting will rotate the wiring. Where rotor I in the
            # A-position normally encodes an A into an E, with a ring setting
            # offset B-02 it will be encoded into K
            self.key = self.key[1:] + self.key[0]

    def turn(self) -> None:
        """TODO"""

        # Update current letter on top of the rotor
        self.current_top = next_char_in_string(ascii_uppercase, self.current_top)
        # Rotate key by one
        self.key = self.key[-1] + self.key[:-1]

    def reverse_encrypt_letter(self, letter: str) -> str:
        """TODO"""

        return chr(self.key.index(letter) + 65)

    def reverse_get_key(self) -> str:
        """Get rotor's character mappings when current's flowing backwards"""

        # hold output in another variable, since python strings are immutable
        new_key: str = ""

        for letter in ascii_uppercase:
            # case current flowing backwards, rotors after reflector
            new_key += self.reverse_encrypt_letter(letter)

        return new_key
