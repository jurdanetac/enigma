#!/usr/bin/env python3

import sys

from dataclasses import dataclass
from string import ascii_uppercase


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


PLUGBOARD = StaticRotor(key="ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # no plugs

REFLECTOR = StaticRotor(key="EJMZALYXVBWFCRQUONTSPIKHGD")  # I
# REFLECTOR = StaticRotor(key="YRUHQSLDPXNGOKMIEBFZCWVJAT")  # II

ROTORS = [
    # right-most rotor
    Rotor(
        key="BDFHJLCPRTXVZNYEIWGAKMUSQO",  # III
        notch="Z",
        initial_top="A",
    ),
    # middle rotor
    Rotor(
        key="AJDKSIRUXBLHWTMCQGZNPYFVOE",  # II
        notch="Z",
        initial_top="A",
    ),
    # left-most rotor
    Rotor(
        key="EKMFLGDQVZNTOWYHXUSPAIBRCJ",  # I
        notch="A",
        initial_top="A",
    ),
]


def log_encryption(old_letter: str, letter: str, txt: str = "") -> None:
    """temp"""

    global ENCRYPTIONS
    ENCRYPTIONS += 1
    print(ENCRYPTIONS, end=": ")
    print(f"{old_letter} -> {letter} {txt}")


if __name__ == "__main__":
    # handle exit signals
    try:
        while True:
            # input prompt
            letter = input("> ").strip().upper()

            # if letter is not a char or char is not an ascii
            if len(letter) != 1 or letter not in ascii_uppercase:
                sys.exit(1)

            # keep track of how many layers of encryption a letter pass
            ENCRYPTIONS = 0

            # substitute letter in plugboard
            log_encryption(letter, PLUGBOARD.encrypt_letter(letter), "plugboard")
            letter = PLUGBOARD.encrypt_letter(letter)

            # right-most rotor turns on every key press
            ROTORS[0].turn()

            # encrypt letter
            for rotor in ROTORS:
                # TODO turn other rotors

                log_encryption(letter, rotor.encrypt_letter(letter), "rotor")
                letter = rotor.encrypt_letter(letter)

            # reflect letter
            log_encryption(letter, REFLECTOR.encrypt_letter(letter), "reflector")
            letter = REFLECTOR.encrypt_letter(letter)

            # current flowing in reverse direction
            for rotor in reversed(ROTORS):
                log_encryption(letter, rotor.reverse_encrypt_letter(letter), "rotor")
                letter = rotor.reverse_encrypt_letter(letter)

            # substitute letter in plugboard
            log_encryption(letter, PLUGBOARD.encrypt_letter(letter), "plugboard")
            letter = PLUGBOARD.encrypt_letter(letter)

            print("=", letter, end="\n\n")

    # Ctrl-C / Ctrl-D
    except:
        sys.exit(0)
