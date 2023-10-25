#!/usr/bin/env python3

"""TODO"""

from dataclasses import dataclass
from io import StringIO
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

    def _get_key(
        self,
        rotor: StaticRotor | Rotor,  # rotor to use
        key: str = ascii_uppercase,  # assume normal A-Z on default
        reverse: bool = False,  # whether the current is flowing back
    ) -> str:
        """Get the character mappings for a given configuration of the machine"""

        # TODO allow passing machine state as args, this would allow user
        # access to the function instead of only using it when encrypting,
        # though the creation of a new local rotor will be needed

        # hold output in another variable, since python strings are immutable
        new_key: str = ""

        # the enciphering of a character resulting from the application of a
        # given component's mapping serves as the input to the mapping of the
        # subsequent component
        for key_letter in key:
            # case current flowing backwards
            if reverse and isinstance(rotor, Rotor):
                new_key += rotor.reverse_encrypt_letter(key_letter)
            else:
                new_key += rotor.encrypt_letter(key_letter)

        return new_key

    def encrypt(self, plaintext: str, verbose: bool = False) -> str:
        """TODO"""

        # input prompt
        cyphertext: str = ""
        # resulting character mapping key
        key: str = ascii_uppercase

        for letter in plaintext:
            # not a letter
            if letter not in ascii_uppercase:
                cyphertext += letter
                continue

            # TODO make rotor turning dynamic
            # TODO support double notch
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

            # get key for keyboard-plugboard mapping
            key = self._get_key(rotor=self.plugboard, key=key, reverse=False)

            # rotor encryption
            for rotor in self.rotors:
                cypher_letter: str = rotor.encrypt_letter(cypher_letter)

                # update key for plugboard-rotor mapping
                key = self._get_key(rotor=rotor, key=key, reverse=False)

            # reflect letter
            cypher_letter: str = self.reflector.encrypt_letter(cypher_letter)

            # update key for rotor-reflector mapping
            key = self._get_key(rotor=self.reflector, key=key, reverse=False)

            # current flowing in reverse direction
            for rotor in reversed(self.rotors):
                cypher_letter: str = rotor.reverse_encrypt_letter(cypher_letter)

                # update key for reflector-rotor mapping
                key = self._get_key(rotor=rotor, key=key, reverse=True)

            # substitute letter in plugboard
            cypher_letter: str = self.plugboard.encrypt_letter(cypher_letter)

            # final update key for rotor-plugboard mapping
            key = self._get_key(rotor=self.plugboard, key=key, reverse=False)

            # append encrypted letter to enciphered text
            cyphertext += cypher_letter

            if verbose:
                # list of current top character of each rotor
                tops: list[str] = [rotor.current_top for rotor in reversed(self.rotors)]
                # list of positions of current top character of each rotor
                tops_positions: list[str] = []

                # populate tops_positions list
                for top in tops:
                    # calculate position; starting from A = 01, B = 02...
                    top_position: int = ord(top) - 64
                    # print to temporary variable formatted number
                    tmp: StringIO = StringIO()
                    print(f"{top_position:02}", file=tmp, end=" ")
                    # add calculated position to list
                    tops_positions.append(tmp.getvalue())

                # resulting key mapping for machine state on this encryption
                fmt_key: str = f"{key[:key.index(cypher_letter)]}({cypher_letter}){key[key.index(cypher_letter)+1:]}"

                # Log of how and what encryption was performed
                output: str = f"{self.encryptions:03} {letter} > {fmt_key} {''.join(tops)} {''.join(tops_positions)}"
                print(output)

            # increment encrypted-letter count by one
            self.encryptions += 1

            # reset key to prevent wrong carryover to the next encryption
            key = ascii_uppercase

        return cyphertext
