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
        reverse: bool = False,  # whether the current is flowing back
    ) -> str:
        """Get the character mappings for a given rotor"""

        # hold output in another variable, since python strings are immutable
        new_key: str = ""

        for key_letter in ascii_uppercase:
            # case current flowing backwards, rotors after reflector
            if reverse and isinstance(rotor, Rotor):
                new_key += rotor.reverse_encrypt_letter(key_letter)
            else:
                new_key += rotor.encrypt_letter(key_letter)

        return new_key

    def _fmt_key(self, key: str, cypher_letter: str, indicator: str = "") -> str:
        """Format key"""

        key = key.strip()

        if not key or not isinstance(key, str):
            return ""

        key_first_half: str = key[: key.index(cypher_letter)]
        key_second_half: str = key[key.index(cypher_letter) + 1 :]
        fmt_key: str = f"{indicator} {key_first_half}({cypher_letter}){key_second_half}"

        return fmt_key.strip()

    def encrypt(self, plaintext: str, verbose: bool = False) -> str:
        """TODO"""

        # input prompt
        cyphertext: str = ""

        for letter in plaintext:
            # not a letter
            if letter not in ascii_uppercase:
                cyphertext += letter
                continue

            # resulting character mapping key
            key: str = ascii_uppercase
            # list of used keys throughout encryption of letter
            keys_used: list[str] = []

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

            # the enciphering of a character resulting from the application of
            # a given component's mapping serves as the input to the mapping of
            # the subsequent component
            cypher_letter: str = letter

            keys_used.append(self._fmt_key(key=key, cypher_letter=cypher_letter))

            # substitute letter in plugboard
            cypher_letter: str = self.plugboard.encrypt_letter(letter)

            # get key for keyboard-plugboard mapping
            key = self._get_key(rotor=self.plugboard, reverse=False)

            # rotor encryption
            for i, rotor in enumerate(self.rotors):
                keys_used.append(
                    self._fmt_key(
                        key=key, cypher_letter=cypher_letter, indicator=str(i + 1)
                    ),
                )

                cypher_letter: str = rotor.encrypt_letter(cypher_letter)
                # update key for rotor-rotor mapping
                key = self._get_key(rotor=rotor, reverse=False)

            keys_used.append(
                self._fmt_key(key=key, cypher_letter=cypher_letter, indicator="R")
            )

            # reflect letter
            cypher_letter: str = self.reflector.encrypt_letter(cypher_letter)

            # update key for rotor-reflector mapping
            key = self._get_key(rotor=self.reflector, reverse=False)

            # current flowing in reverse direction
            for i, rotor in enumerate(reversed(self.rotors)):
                keys_used.append(
                    self._fmt_key(
                        key=key, cypher_letter=cypher_letter, indicator=str(i + 1)
                    )
                )

                cypher_letter: str = rotor.reverse_encrypt_letter(cypher_letter)
                # update key for reflector-rotor mapping
                key = self._get_key(rotor=rotor, reverse=True)

            keys_used.append(
                self._fmt_key(key=key, cypher_letter=cypher_letter, indicator="P")
            )

            # substitute letter in plugboard
            cypher_letter: str = self.plugboard.encrypt_letter(cypher_letter)
            # final update key for rotor-plugboard mapping
            key = self._get_key(rotor=self.plugboard, reverse=False)

            keys_used.append(
                self._fmt_key(
                    key=key,
                    cypher_letter=cypher_letter,
                )
            )

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

                # Log of how and what encryption was performed
                print(f"K > {keys_used[0]}")
                for key in keys_used[1:-1]:
                    print(f"  {key}")
                print(f"{letter} < {keys_used[-1]}")

                print()

                output: str = f"{self.encryptions:04} {letter} < {keys_used[-1]} {''.join(tops)} {''.join(tops_positions)}"
                print(output)

            # increment encrypted-letter count by one
            self.encryptions += 1

        return cyphertext
