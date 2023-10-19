#!/usr/bin/env python3

"""TODO"""

import sys
from typing import Callable
from machine import Enigma

from rotors import StaticRotor, Rotor


# I
# REFLECTOR = StaticRotor(key="EJMZALYXVBWFCRQUONTSPIKHGD")
# B
# II
# REFLECTOR = StaticRotor(key="YRUHQSLDPXNGOKMIEBFZCWVJAT")


def quit_safely(func) -> Callable:
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


@quit_safely
def main() -> None:
    """Main program execution"""

    machine: Enigma = Enigma(
        rotors=[
            # right-most rotor
            Rotor(
                key="BDFHJLCPRTXVZNYEIWGAKMUSQO",  # III
                notch="V",
                current_top="T",
                ring_setting="A",
            ),
            # middle rotor
            Rotor(
                key="AJDKSIRUXBLHWTMCQGZNPYFVOE",  # II
                notch="E",
                current_top="D",
                ring_setting="A",
            ),
            # left-most rotor
            # I
            Rotor(
                key="EKMFLGDQVZNTOWYHXUSPAIBRCJ",
                notch="Q",
                current_top="A",
                ring_setting="A",
            ),
        ],
        # no plugs
        plugboard=StaticRotor(key="ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        #
        reflector=StaticRotor(key="YRUHQSLDPXNGOKMIEBFZCWVJAT"),
    )

    while True:
        # input prompt
        plaintext: str = input("> ").strip().upper()
        cyphertext: str = machine.encrypt(plaintext=plaintext, verbose=True)

        print(cyphertext)


if __name__ == "__main__":
    main()
