#!/usr/bin/env python3

import sys

from string import ascii_uppercase

from rotors import StaticRotor, Rotor


PLUGBOARD = StaticRotor(key="ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # no plugs

REFLECTOR = StaticRotor(key="EJMZALYXVBWFCRQUONTSPIKHGD")  # I
# REFLECTOR = StaticRotor(key="YRUHQSLDPXNGOKMIEBFZCWVJAT")  # II

ROTORS = [
    # right-most rotor
    Rotor(
        key="BDFHJLCPRTXVZNYEIWGAKMUSQO",  # III
        notch="Z",
        current_top="Y",
    ),
    # middle rotor
    Rotor(
        key="AJDKSIRUXBLHWTMCQGZNPYFVOE",  # II
        notch="Z",
        current_top="A",
    ),
    # left-most rotor
    Rotor(
        key="EKMFLGDQVZNTOWYHXUSPAIBRCJ",  # I
        notch="A",
        current_top="A",
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

            # TODO remove debugging prints
            print(ROTORS[0].current_top)
            # right-most rotor turns on every key press
            ROTORS[0].turn()
            print(ROTORS[0].current_top)

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
