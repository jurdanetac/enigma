#!/usr/bin/env python3

"""TODO"""

from dataclasses import dataclass
from string import ascii_uppercase

from rotors import Rotor, StaticRotor


@dataclass
class Enigma:
    """TODO"""

    rotors: list[Rotor]
    plugboard: StaticRotor
    reflector: StaticRotor

    # keep track of how many layers of encryption a letter pass
    encryptions: int = 1

    def encrypt(self, plaintext: str, verbose: bool = False) -> str:
        """TODO"""

        # input prompt
        cyphertext: str = ""

        for letter in plaintext:
            # not a letter
            if letter not in ascii_uppercase:
                cyphertext += letter
                continue

            # TODO make rotor turning dynamic
            # turn other rotors when current rotor notch is on top
            if self.rotors[1].current_top == self.rotors[1].notch:
                self.rotors[1].turn()
                self.rotors[2].turn()

            if self.rotors[0].current_top == self.rotors[0].notch:
                self.rotors[1].turn()

            # right-most rotor turns on every key press
            self.rotors[0].turn()

            # substitute letter in plugboard
            cypher_letter: str = self.plugboard.encrypt_letter(letter)

            # rotor encryption
            for rotor in self.rotors:
                cypher_letter: str = rotor.encrypt_letter(cypher_letter)

            # reflect letter
            cypher_letter: str = self.reflector.encrypt_letter(cypher_letter)

            # current flowing in reverse direction
            for rotor in reversed(self.rotors):
                cypher_letter: str = rotor.reverse_encrypt_letter(cypher_letter)

            # substitute letter in plugboard
            cypher_letter: str = self.plugboard.encrypt_letter(cypher_letter)

            cyphertext += cypher_letter

            if verbose:
                tops: str = "".join(
                    [rotor.current_top for rotor in reversed(self.rotors)]
                )
                tops_ascii: str = " ".join([f"{(ord(top) - 64)}" for top in tops])

                # TODO put correct key
                print(
                    f"{self.encryptions:03} {letter} > {self.rotors[0].key[:self.rotors[0].key.index(letter)]}({letter}){self.rotors[0].key[self.rotors[0].key.index(letter):]} {tops} {tops_ascii}"
                )

            self.encryptions += 1

        return cyphertext
