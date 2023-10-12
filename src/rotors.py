from dataclasses import dataclass

from string import ascii_uppercase


def next_char_in_string(string: str, letter: str) -> str:
    """TODO"""
    return string[(string.index(letter) + 1) % len(string)]


@dataclass
class StaticRotor:
    """TODO"""

    # substitution key
    key: str

    def encrypt_letter(self, letter) -> str:
        """TODO"""

        return self.key[ord(letter) - 65]


@dataclass
class Rotor(StaticRotor):
    """TODO"""

    # substitution key
    key: str
    # turnover
    notch: str
    # initial letter on top
    current_top: str

    def __post_init__(self):
        """Inherit StaticRotor key and encrypt_letter method"""

        super().__init__(self.key)

    def turn(self) -> None:
        """TODO"""

        # Update current letter on top of the rotor
        self.current_top = next_char_in_string(ascii_uppercase, self.current_top)
        # Rotate key by one
        self.key = self.key[-1] + self.key[:-1]

    def reverse_encrypt_letter(self, letter) -> str:
        """TODO"""

        return chr(self.key.index(letter) + 65)
