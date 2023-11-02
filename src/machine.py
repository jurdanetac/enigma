#!/usr/bin/env python3

"""TODO"""

from dataclasses import dataclass
from io import StringIO
from string import ascii_uppercase
from typing import Callable

from rotors import Rotor, StaticRotor


@dataclass
class Enigma:
    """TODO"""

    rotors: list[Rotor]
    plugboard: StaticRotor
    reflector: StaticRotor

    # keep track of how many layers of encryption a letter pass
    encryptions: int = 1

    def _get_keys(self) -> list[str]:
        """TODO"""
        # list of used keys throughout encryption of letter
        keys_used: list[str] = []

        def update_keys(getter_func: Callable) -> None:
            """Update used keys list by appending the return value of the passed function"""

            key = getter_func()
            keys_used.append(key)

        def get_resulting_key() -> str:
            """Get resulting key after applying all layers of encryption"""

            final_key: str = ""

            for letter in ascii_uppercase:
                # Pass each alphabet letter by all layers of encryption
                # to get the resulting key in that particular machine state
                final_key += self._encrypt_letter(letter)

            return final_key

        # append plugboard key
        update_keys(getter_func=self.plugboard.get_key)

        for rotor in self.rotors:
            # append rotor n key
            update_keys(getter_func=rotor.get_key)

        # append reflector key
        update_keys(getter_func=self.reflector.get_key)

        for rotor in reversed(self.rotors):
            # append rotor n key backwards
            update_keys(getter_func=rotor.reverse_get_key)

        # append plugboard key
        update_keys(getter_func=self.plugboard.get_key)

        # append resulting key
        update_keys(getter_func=get_resulting_key)

        return keys_used

    def _fmt_key(self, key: str, cypher_letter: str, indicator: str = "") -> str:
        """Format key"""

        key = key.strip()

        if not key or not isinstance(key, str):
            return ""

        key_first_half: str = key[: key.index(cypher_letter)]
        key_second_half: str = key[key.index(cypher_letter) + 1 :]
        fmt_key: str = f"{indicator} {key_first_half}({cypher_letter}){key_second_half}"

        return fmt_key.strip()

    def _log_encryption(self, letter: str) -> None:
        """TODO"""

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
        print(f"K > {self._fmt_key(key=ascii_uppercase, cypher_letter=letter)}")
        keys_used: list[str] = self._get_keys()

        cypher_letter: str = letter

        current_rotor: int = 0

        for i, key in enumerate(keys_used[:-1]):
            cypher_letter = key[ord(cypher_letter) - 65]
            indicator: str = ""

            # plugboard
            if i in (0, len(keys_used) - 2):
                indicator = "P"
            # rotors first pass
            elif i < len(self.rotors) + 1:
                current_rotor += 1
                indicator = str(current_rotor)
            # reflector
            elif i == len(self.rotors) + 1:
                indicator = "R"
            # rotors second pass
            else:
                indicator = str(current_rotor)
                current_rotor -= 1

            print(
                f"  {self._fmt_key(key=key, cypher_letter=cypher_letter, indicator=indicator)}"
            )

        print(
            f"{letter} < {self._fmt_key(key=keys_used[-1], cypher_letter=letter)}",
            end="\n\n",
        )

        output: str = f"{self.encryptions:04} {letter} < {keys_used[-1]} {''.join(tops)} {''.join(tops_positions)}"
        print(output)

    def _turn_rotors(self) -> None:
        """TODO"""

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

    def encrypt_wrapper(self, plaintext: str, verbose: bool = False) -> str:
        """TODO"""

        # input prompt
        cyphertext: str = ""

        for letter in plaintext:
            # not a letter
            if letter not in ascii_uppercase:
                cyphertext += letter
                continue

            self._turn_rotors()

            cypher_letter: str = self._encrypt_letter(letter)

            # append encrypted letter to enciphered text
            cyphertext += cypher_letter

            if verbose:
                self._log_encryption(letter=cypher_letter)

            # increment encrypted-letter count by one
            self.encryptions += 1

        return cyphertext

    def _encrypt_letter(self, letter: str) -> str:
        """TODO"""

        # the enciphering of a character resulting from the application of
        # a given component's mapping serves as the input to the mapping of
        # the subsequent component

        # substitute letter in plugboard
        cypher_letter: str = self.plugboard.encrypt_letter(letter)

        # rotor encryption
        for rotor in self.rotors:
            # update key for rotor-rotor mapping
            cypher_letter: str = rotor.encrypt_letter(cypher_letter)

        # reflect letter
        cypher_letter: str = self.reflector.encrypt_letter(cypher_letter)

        # current flowing in reverse direction
        for rotor in reversed(self.rotors):
            # update key for reflector-rotor mapping
            cypher_letter: str = rotor.reverse_encrypt_letter(cypher_letter)

        # substitute letter in plugboard
        cypher_letter: str = self.plugboard.encrypt_letter(cypher_letter)

        return cypher_letter
