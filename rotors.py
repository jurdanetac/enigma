from dataclasses import dataclass

@dataclass
class StaticRotor:
    """TODO"""

    key: str  # substitution key

    def encrypt_letter(self, letter) -> str:
        """TODO"""

        return self.key[ord(letter) - 65]


@dataclass
class Rotor(StaticRotor):
    """TODO"""

    key: str  # substitution key
    notch: str  # turnover
    initial_top: str  # initial letter on top

    def __post_init__(self):
        """Inherit StaticRotor key and encrypt_letter method"""

        super().__init__(self.key)

    def turn(self) -> None:
        """TODO"""
        self.key = self.key[-1] + self.key[:-1]

    def reverse_encrypt_letter(self, letter) -> str:
        """TODO"""
        return chr(self.key.index(letter) + 65)
