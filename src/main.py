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
        notch="V",
        current_top="T",
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

            # TODO remove debugging prints
            for rotor in reversed(ROTORS):
                print(rotor.current_top, end="")
            print()

            # TODO remove debugging prints
            # right-most rotor turns on every key press
            ROTORS[0].turn()

            # TODO remove debugging prints
            for rotor in reversed(ROTORS):
                print(rotor.current_top, end="")
            print()

            # substitute letter in plugboard
            log_encryption(letter, PLUGBOARD.encrypt_letter(letter), "plugboard")
            letter = PLUGBOARD.encrypt_letter(letter)

            # encrypt letter
            for rotor_index, rotor in enumerate(ROTORS):
                # turn other rotors when current rotor notch is on top
                try:
                    if rotor.current_top == rotor.notch and ROTORS[rotor_index + 1]:
                        ROTORS[rotor_index + 1].turn()
                except IndexError:  # no next rotor
                    pass

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
