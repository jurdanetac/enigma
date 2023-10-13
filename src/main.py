#!/usr/bin/env python3

"""TODO"""

import sys
from string import ascii_uppercase

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
        current_top="A",
    ),
    # middle rotor
    Rotor(
        key="AJDKSIRUXBLHWTMCQGZNPYFVOE",  # II
        notch="E",
        current_top="A",
    ),
    # left-most rotor
    Rotor(
        key="EKMFLGDQVZNTOWYHXUSPAIBRCJ",  # I
        notch="Q",
        current_top="A",
    ),
]


if __name__ == "__main__":
    # handle exit signals
    try:
        # keep track of how many layers of encryption a letter pass
        ENCRYPTIONS: int = 1

        while True:
            # input prompt
            PLAINTEXT: str = input("> ").strip().upper()
            CYPHERTEXT: str = ""

            for letter_count, letter in enumerate(PLAINTEXT):
                # not a letter
                if letter not in ascii_uppercase:
                    CYPHERTEXT += letter
                    continue

                TOPS: str = "".join([rotor.current_top for rotor in reversed(ROTORS)])
                TOPS_ASCII: str = " ".join([f"{(ord(top) - 64)}" for top in TOPS])

                # right-most rotor turns on every key press
                ROTORS[0].turn()

                # substitute letter in plugboard
                cypher_letter: str = PLUGBOARD.encrypt_letter(letter)

                # encrypt letter
                for rotor_index, rotor in enumerate(ROTORS):
                    # turn other rotors when current rotor notch is on top
                    try:
                        if rotor.current_top == rotor.notch and ROTORS[rotor_index + 1]:
                            ROTORS[rotor_index + 1].turn()
                    # no next rotor
                    except IndexError:
                        pass

                    # rotor encryption
                    cypher_letter: str = rotor.encrypt_letter(cypher_letter)

                # reflect letter
                cypher_letter: str = REFLECTOR.encrypt_letter(cypher_letter)

                # current flowing in reverse direction
                for rotor in reversed(ROTORS):
                    cypher_letter: str = rotor.reverse_encrypt_letter(cypher_letter)

                # substitute letter in plugboard
                cypher_letter: str = PLUGBOARD.encrypt_letter(cypher_letter)

                CYPHERTEXT += cypher_letter

                print(
                    f"{ENCRYPTIONS:03} {letter} > {ROTORS[0].key[:ROTORS[0].key.index(letter)]}({letter}){ROTORS[0].key[ROTORS[0].key.index(letter):]} {TOPS} {TOPS_ASCII}"
                )

                ENCRYPTIONS += 1

            print(CYPHERTEXT)

    # Ctrl-C / Ctrl-D
    except (KeyboardInterrupt, EOFError):
        sys.exit(0)
