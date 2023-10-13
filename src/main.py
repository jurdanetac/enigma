#!/usr/bin/env python3

import sys

from string import ascii_uppercase

from rotors import StaticRotor, Rotor


# no plugs
PLUGBOARD = StaticRotor(key="ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# I
# REFLECTOR = StaticRotor(key="EJMZALYXVBWFCRQUONTSPIKHGD")
# B
REFLECTOR = StaticRotor(key="YRUHQSLDPXNGOKMIEBFZCWVJAT")
# II
# REFLECTOR = StaticRotor(key="YRUHQSLDPXNGOKMIEBFZCWVJAT")

ROTORS = [
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
        encryptions = 1

        while True:
            # input prompt
            plaintext = input("> ").strip().upper()
            cyphertext = ""

            for letter_count, letter in enumerate(plaintext):
                tops = "".join([rotor.current_top for rotor in reversed(ROTORS)])
                tops_ascii = " ".join([f"{(ord(top) - 64)}" for top in tops])

                # right-most rotor turns on every key press
                ROTORS[0].turn()

                # substitute letter in plugboard
                cypher_letter = PLUGBOARD.encrypt_letter(letter)

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
                    cypher_letter = rotor.encrypt_letter(cypher_letter)

                # reflect letter
                cypher_letter = REFLECTOR.encrypt_letter(cypher_letter)

                # current flowing in reverse direction
                for rotor in reversed(ROTORS):
                    cypher_letter = rotor.reverse_encrypt_letter(cypher_letter)

                # substitute letter in plugboard
                cypher_letter = PLUGBOARD.encrypt_letter(cypher_letter)

                cyphertext += cypher_letter

                print(
                    f"{encryptions:03} {letter} > {ROTORS[0].key[:ROTORS[0].key.index(letter)]}({letter}){ROTORS[0].key[ROTORS[0].key.index(letter):]} {tops} {tops_ascii}"
                )

                encryptions += 1

            print(cyphertext)

    # Ctrl-C / Ctrl-D
    except:
        sys.exit(0)
