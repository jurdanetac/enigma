#!/usr/bin/env python3

# pylint: disable=locally-disabled, fixme, line-too-long

"""Module for CLI interface."""

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

    machine.rotors[0].set_current_top("Z")

    while True:
        # input prompt
        # plaintext: str = input(">>> ").strip().upper()

        # TODO remove auto testing to allow for interactive use
        plaintext: str = "A"
        ciphertext: str = machine.encrypt_wrapper(
            plaintext=plaintext, verbose=True, should_turn=True
        )
        print()
        print(ciphertext)
        break


if __name__ == "__main__":
    main()
