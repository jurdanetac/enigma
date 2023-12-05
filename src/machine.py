#!/usr/bin/env python3

# pylint: disable=locally-disabled, fixme, line-too-long

"""Module containing a model of the Enigma machine in a class with methods to encrypt and decrypt text"""

from string import ascii_uppercase
from typing import Callable

from rotors import Rotor, Stator
from utils import letter_to_number


class Enigma:
    """Model of the Enigma machine"""

    def __init__(self, rotors: list[Rotor], plugboard: Stator, reflector: Stator):
        """Initialize Enigma machine with rotors, plugboard and reflector.

        :param rotors: list of rotors to be used; right-most rotor is the first one in the list
        :type rotors: list[Rotor]
        :param plugboard: plugboard to be used
        :type plugboard: Stator
        :param reflector: reflector to be used
        :type reflector: Stator
        :returns: None
        :rtype: None
        :example: Enigma(rotors=[Rotor(...), Rotor(...), Rotor(...)], plugboard=Stator(...), reflector=Stator(...))

        """

        self.rotors = rotors
        self.plugboard = plugboard
        self.reflector = reflector

        # keep track of how many letters have been encrypted
        self.encryptions: int = 0
        # keep track of each individual encryption step
        self.last_encryption_log: list[str] = []

    def _get_keys(self) -> list[str]:
        """Return a list of keys used throughout encryption of a letter.

        :returns: list of keys used throughout encryption of a letter
        :rtype: list[str]
        :example: self._get_keys() -> ["ABC", "DEF", "GHI", "JKL", "MNO", "PQR", "STU", "VWX"]

        """

        keys_used: list[str] = []

        def update_keys(getter_func: Callable) -> None:
            """Update used keys list by appending the return value of the passed function.

            :param getter_func: function to be called to get the cypher key
            :type getter_func: Callable
            :returns: None
            :rtype: None
            :example: update_keys(getter_func=self.plugboard.get_key)
            """

            key = getter_func()
            keys_used.append(key)

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
        update_keys(getter_func=self.get_resulting_key)

        return keys_used

    def _fmt_key(
        self,
        key: str,
        letter: str,
        indicator: str = "",
        delimiters: tuple = ("(", ")"),
    ) -> str:
        """Format a key to be printed to stdout.

        :param key: key to be formatted
        :type key: str
        :param letter: letter to find
        :type letter: str
        :param indicator: indicator of which encryption layer, defaults to ""
        :type indicator: str, optional
        :param delimiters: pair of characters to use to surround the letter in the key, defaults to ("(", ")")
        :type delimiters: tuple, optional
        :returns: formatted key to be printed to stdout
        :rtype: str
        :raises ValueError: if key is empty or not a string
        :example: self._fmt_key(key="ABC", letter="B", indicator="1>") -> "1> A(B)C"

        """

        # remove whitespace from key
        key = key.strip()

        if not key or not isinstance(key, str):
            return ""

        # split key into two halves and surround with a delimiter
        letter_to_find_index: int = letter_to_number(letter)
        key_first_half: str = key[:letter_to_find_index]
        key_second_half: str = key[letter_to_find_index + 1 :]
        fmt_key: str = f"{indicator} {key_first_half}{delimiters[0]}{key[letter_to_find_index]}{delimiters[1]}{key_second_half}"

        return fmt_key

    def get_resulting_key(self) -> str:
        """Get resulting key after applying all layers of encryption for a given machine state.

        :returns: resulting cypher key
        :rtype: str
        :example: self.get_resulting_key() -> "IVFKPCUQAXDOTSLEHWNMGBRJZY"

        """

        final_key: str = ""

        for letter in ascii_uppercase:
            # Pass each alphabet letter by all layers of encryption
            # to get the resulting key in that particular machine state
            final_key += self._encrypt_letter(letter)

        return final_key

    def _turn_rotors(self) -> None:
        """Turn adjacent rotor to any one whose turnover is on top.

        :returns: None
        :rtype: None
        :example: self._turn_rotors()

        """

        # TODO make rotor turning not hardcoded
        # TODO support double notch

        # turn other rotors when current rotor notch is on top
        if self.rotors[1].current_top == self.rotors[1].notch:
            self.rotors[1].turn()
            self.rotors[2].turn()

        if self.rotors[0].current_top == self.rotors[0].notch:
            self.rotors[1].turn()

        # right-most rotor turns on every key press
        self.rotors[0].turn()

    def encrypt_wrapper(
        self, plaintext: str, verbose: bool = False, should_turn: bool = True
    ) -> str:
        """Log and encrypt a plaintext string.

        :param plaintext: text to be encrypted
        :type plaintext: str
        :param verbose: whether to print encryption log, defaults to False
        :type verbose: bool, optional
        :param should_turn: whether to turn rotors, defaults to True
        :type should_turn: bool, optional
        :returns: encrypted text
        :rtype: str
        :example: self.encrypt_wrapper(plaintext="HELLO", verbose=True, should_turn=True) -> "IVFKP"

        """

        # input prompt
        ciphertext: str = ""

        for letter in plaintext:
            # not a letter
            if letter not in ascii_uppercase:
                ciphertext += letter
                continue

            if should_turn is True:
                self._turn_rotors()

            # keyboard layer
            self.last_encryption_log.append(
                f"{self._fmt_key(key=ascii_uppercase, letter=letter)}"
            )

            keys_used: list[str] = self._get_keys()
            cypher_letter = keys_used[0][ord(letter) - 65]

            for key in keys_used[:-1]:
                # plugboard-rotor-reflector-plugboard layers
                self.last_encryption_log.append(
                    f"{self._fmt_key(key=key, letter=cypher_letter)}"
                )

                cypher_letter = key[ord(cypher_letter) - 65]

            # append encrypted letter to enciphered text
            ciphertext += cypher_letter

            if verbose:
                for entry in self.last_encryption_log:
                    print(entry)

            self.last_encryption_log.append(
                f"{cypher_letter} < {self._fmt_key(key=keys_used[-1], letter=cypher_letter)}"
            )

            # increment encrypted-letter count by one
            self.encryptions += 1

        return ciphertext

    def _encrypt_letter(self, letter: str) -> str:
        """Encrypt a single letter.

        :param letter: letter to be encrypted
        :type letter: str
        :returns: encrypted letter
        :rtype: str
        :example: self._encrypt_letter(letter="A") -> "U"

        """

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
