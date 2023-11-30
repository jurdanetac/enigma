#!/usr/bin/env python3

# pylint: disable=locally-disabled, fixme, line-too-long

"""TODO"""

from machine import Enigma
from rotors import StaticRotor, Rotor, DefaultKeys
from utils import quit_safely


@quit_safely
def main() -> None:
    """Main program execution"""

    machine: Enigma = Enigma(
        rotors=[
            # right-most rotor
            Rotor(
                key=DefaultKeys.ROTORS["III"]["key"],
                notch=DefaultKeys.ROTORS["III"]["notch"],
                current_top="T",
                ring_setting="A",
            ),
            # middle rotor
            Rotor(
                key=DefaultKeys.ROTORS["II"]["key"],
                notch=DefaultKeys.ROTORS["II"]["notch"],
                current_top="D",
                ring_setting="A",
            ),
            # left-most rotor
            Rotor(
                key=DefaultKeys.ROTORS["I"]["key"],
                notch=DefaultKeys.ROTORS["I"]["notch"],
                current_top="A",
                ring_setting="A",
            ),
        ],
        plugboard=StaticRotor(key=DefaultKeys.PLUGBOARD["empty"]),
        reflector=StaticRotor(key=DefaultKeys.REFLECTORS["B"]),
    )

    while True:
        # input prompt
        plaintext: str = input(">>> ").strip().upper()
        cyphertext: str = machine.encrypt_wrapper(plaintext=plaintext, verbose=True)

        print(cyphertext, end="\n\n")


if __name__ == "__main__":
    main()
