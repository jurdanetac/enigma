#!/usr/bin/env python3

# pylint: disable=locally-disabled, fixme, line-too-long

"""Module for CLI interface."""

import sys

from machine import Enigma
from rotors import ROTOR_I, ROTOR_II, ROTOR_III, PLUGBOARD_EMPTY, REFLECTOR_B
from utils import quit_safely


@quit_safely
def main() -> None:
    """This function is executed when the script is run directly.
    Intended to be used for interactive testing.

    :returns: None
    :rtype: None
    :example: main()

    """

    machine: Enigma = Enigma(
        rotors=[
            # right-most rotor
            ROTOR_III,
            # middle rotor
            ROTOR_II,
            # left-most rotor
            ROTOR_I,
        ],
        plugboard=PLUGBOARD_EMPTY,
        reflector=REFLECTOR_B,
    )

    verbose: bool = False

    if len(sys.argv) > 1 and sys.argv[1] in ("--verbose", "-v"):
        verbose = True

    while True:
        # get current settings
        settings: str = ""
        for rotor in reversed(machine.rotors):
            settings += f"{rotor.current_top}"
        settings += "\n"
        for rotor in machine.rotors:
            settings += f"{rotor.key}\n"

        # input prompt
        plaintext: str = input(">>> ").strip().upper()

        print(f"Current settings: {settings}")
        ciphertext: str = machine.encrypt(plaintext=plaintext, verbose=verbose)
        print(f"\nEncrypted: {ciphertext}")


if __name__ == "__main__":
    main()
