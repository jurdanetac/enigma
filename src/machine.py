#!/usr/bin/env python3

# pylint: disable=locally-disabled, fixme, line-too-long

"""Module containing a model of the Enigma machine in a class with methods to encrypt and decrypt text"""

from string import ascii_uppercase

from rotors import Rotor, Stator

# from utils import letter_to_number


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
        self.log: list[tuple] = []

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

    def encrypt(
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

        # result of encryption of `plaintext`
        ciphertext: str = ""

        for letter in plaintext:
            # not a letter
            if letter not in ascii_uppercase:
                # ciphertext += letter
                continue

            # wether to turn rotors or stay in the same state
            if should_turn is True:
                self._turn_rotors()

            # the enciphering of a character resulting from the application of
            # a given component's mapping serves as the input to the mapping of
            # the subsequent component
            self.log.append((ascii_uppercase, letter, letter))

            # substitute letter in plugboard
            cypher_letter: str = self.plugboard.encrypt_letter(letter)
            self.log.append((self.plugboard.key, letter, cypher_letter))

            # aux for logging
            old_cypher_letter: str = cypher_letter

            # rotor encryption
            for rotor in self.rotors:
                # update key for rotor-rotor mapping
                cypher_letter: str = rotor.encrypt_letter(cypher_letter)
                self.log.append((rotor.get_key(), old_cypher_letter, cypher_letter))
                old_cypher_letter: str = cypher_letter

            # reflect letter
            cypher_letter: str = self.reflector.encrypt_letter(cypher_letter)
            self.log.append((self.reflector.key, old_cypher_letter, cypher_letter))
            old_cypher_letter: str = cypher_letter

            # current flowing in reverse direction
            for rotor in reversed(self.rotors):
                # update key for reflector-rotor mapping
                cypher_letter: str = rotor.reverse_encrypt_letter(cypher_letter)
                self.log.append(
                    (rotor.reverse_get_key(), old_cypher_letter, cypher_letter)
                )
                old_cypher_letter: str = cypher_letter

            # substitute letter in plugboard
            cypher_letter: str = self.plugboard.encrypt_letter(cypher_letter)
            self.log.append((self.plugboard.key, old_cypher_letter, cypher_letter))

            ciphertext += cypher_letter

            # increment encrypted-letter count by one
            self.encryptions += 1

            # print encryption log for the letter
            if verbose:
                for entry in self.log:
                    print(entry)

        return ciphertext
