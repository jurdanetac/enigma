#!/usr/bin/env python3

"""TODO"""

import sys
from string import ascii_uppercase
from typing import Callable

from rotors import StaticRotor, Rotor


# no plugs
PLUGBOARD: StaticRotor = StaticRotor(key="ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# I
# REFLECTOR = StaticRotor(key="EJMZALYXVBWFCRQUONTSPIKHGD")
# B
REFLECTOR: StaticRotor = StaticRotor(key="YRUHQSLDPXNGOKMIEBFZCWVJAT")
# II
# REFLECTOR = StaticRotor(key="YRUHQSLDPXNGOKMIEBFZCWVJAT")

ROTORS: list[Rotor] = [
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
    Rotor(
        key="EKMFLGDQVZNTOWYHXUSPAIBRCJ",  # I
        notch="Q",
        current_top="A",
        ring_setting="A",
    ),
]


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
    # keep track of how many layers of encryption a letter pass
    ENCRYPTIONS: int = 1

    while True:
        # input prompt
        PLAINTEXT: str = input("> ").strip().upper()
        CYPHERTEXT: str = ""

        for letter in PLAINTEXT:
            # not a letter
            if letter not in ascii_uppercase:
                CYPHERTEXT += letter
                continue

            # TODO make rotor turning dynamic
            # turn other rotors when current rotor notch is on top
            if ROTORS[1].current_top == ROTORS[1].notch:
                ROTORS[1].turn()
                ROTORS[2].turn()

            if ROTORS[0].current_top == ROTORS[0].notch:
                ROTORS[1].turn()

            # right-most rotor turns on every key press
            ROTORS[0].turn()

            # substitute letter in plugboard
            cypher_letter: str = PLUGBOARD.encrypt_letter(letter)

            # rotor encryption
            for rotor in ROTORS:
                cypher_letter: str = rotor.encrypt_letter(cypher_letter)

            # reflect letter
            cypher_letter: str = REFLECTOR.encrypt_letter(cypher_letter)

            # current flowing in reverse direction
            for rotor in reversed(ROTORS):
                cypher_letter: str = rotor.reverse_encrypt_letter(cypher_letter)

            # substitute letter in plugboard
            cypher_letter: str = PLUGBOARD.encrypt_letter(cypher_letter)

            CYPHERTEXT += cypher_letter

            TOPS: str = "".join([rotor.current_top for rotor in reversed(ROTORS)])
            TOPS_ASCII: str = " ".join([f"{(ord(top) - 64)}" for top in TOPS])

            # TODO put correct key
            print(
                f"{ENCRYPTIONS:03} {letter} > {ROTORS[0].key[:ROTORS[0].key.index(letter)]}({letter}){ROTORS[0].key[ROTORS[0].key.index(letter):]} {TOPS} {TOPS_ASCII}"
            )

            ENCRYPTIONS += 1

        print(CYPHERTEXT)


if __name__ == "__main__":
    main()
