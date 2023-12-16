#!/usr/bin/env python3

"""Test that the machine works as expected, giving the correct output for a given input"""

from string import ascii_uppercase
import unittest

from machine import Enigma
from rotors import ROTOR_I, ROTOR_II, ROTOR_III, PLUGBOARD_EMPTY, REFLECTOR_B
from utils import switch

from copy import copy


class TestClass(unittest.TestCase):
    """"""

    def setUp(self) -> None:
        """Set up the machine"""

        # build machine with config B-I-II-III AAA 01.01.01 with no plugboard
        self.machine: Enigma = Enigma(
            rotors=[
                # right-most rotor
                copy(ROTOR_III),
                # middle rotor
                copy(ROTOR_II),
                # left-most rotor
                copy(ROTOR_I),
            ],
            plugboard=copy(PLUGBOARD_EMPTY),
            reflector=copy(REFLECTOR_B),
        )

    def test_plugboard(self) -> None:
        """Test that plugboard works as expected."""

        self.machine.plugboard.key = ascii_uppercase
        self.machine.plugboard.key = switch(self.machine.plugboard.key, "A", "B")

        # should be B
        self.assertEqual(self.machine.plugboard.encrypt_letter(letter="A"), "B")
        # should be A
        self.assertEqual(self.machine.plugboard.encrypt_letter(letter="B"), "A")

    def test_rotors(self) -> None:
        """Test that rotors works as expected."""

        # should be B
        self.assertEqual(self.machine.rotors[0].encrypt_letter(letter="A"), "B")
        # should not be A
        self.assertNotEqual(self.machine.rotors[0].encrypt_letter(letter="B"), "A")

        # should be A
        self.assertEqual(self.machine.rotors[0].reverse_encrypt_letter(letter="B"), "A")
        # should not be B
        self.assertNotEqual(
            self.machine.rotors[0].reverse_encrypt_letter(letter="A"), "B"
        )

        # print("\nRotor III - OK!")

        # should be C
        self.assertEqual(self.machine.rotors[1].encrypt_letter(letter="C"), "D")
        # should not be D
        self.assertNotEqual(self.machine.rotors[1].encrypt_letter(letter="D"), "C")

        # should be D
        self.assertEqual(self.machine.rotors[1].reverse_encrypt_letter(letter="D"), "C")
        # should not be C
        self.assertNotEqual(
            self.machine.rotors[1].reverse_encrypt_letter(letter="C"), "D"
        )

        # print("\nRotor II - OK!")

        # should be K
        self.assertEqual(self.machine.rotors[2].encrypt_letter(letter="B"), "K")
        # should not be B
        self.assertNotEqual(self.machine.rotors[2].encrypt_letter(letter="K"), "B")

        # should be B
        self.assertEqual(self.machine.rotors[2].reverse_encrypt_letter(letter="K"), "B")
        # should not be K
        self.assertNotEqual(
            self.machine.rotors[2].reverse_encrypt_letter(letter="B"), "K"
        )

    def test_reflector(self) -> None:
        """Test that reflector works as expected."""

        # should be Y
        self.assertEqual(self.machine.reflector.encrypt_letter(letter="A"), "Y")
        # should be A
        self.assertEqual(self.machine.reflector.encrypt_letter(letter="Y"), "A")

    def test_turnovers(self) -> None:
        """Test that turnover works as expected.
        https://www.ciphermachinesandcryptology.com/en/enigmatech.htm#steppingmechanism
        """

        self.machine.rotors[2] = copy(ROTOR_III)  # leftmost
        self.machine.rotors[2].current_top = "K"
        self.machine.rotors[1] = copy(ROTOR_II)  # middle
        self.machine.rotors[1].current_top = "D"
        self.machine.rotors[0] = copy(ROTOR_I)  # rightmost
        self.machine.rotors[0].current_top = "N"

        expected_windows: list[str] = ["KDO", "KDP", "KDQ", "KER", "LFS", "LFT", "LFU"]

        for letters in expected_windows:
            # print(
            #     "\n" + self.machine.rotors[2].current_top,
            #     self.machine.rotors[1].current_top,
            #     self.machine.rotors[0].current_top,
            #     end=""
            # )
            self.machine._turn_rotors()
            # print(
            #     " -> " + self.machine.rotors[2].current_top,
            #     self.machine.rotors[1].current_top,
            #     self.machine.rotors[0].current_top,
            # )

            self.assertEqual(
                self.machine.rotors[2].current_top
                + self.machine.rotors[1].current_top
                + self.machine.rotors[0].current_top,
                letters,
            )

    def test_turnoverless_encryption(self) -> None:
        """Test that we can correctly encrypt without turning rotors.
        Test taken from https://www.codesandciphers.org.uk/enigma/example1.htm"""

        # reset plugboard test changes
        self.machine.plugboard.key = ascii_uppercase

        # the pairs that should be binded using this particular configuration
        # (AU)(BE)(CJ)(DO)(FT)(GP)(HZ)(IW)(KN)(LS)(MR)(QV)(XY)
        plaintext: str = "UEJOBTPZWCNSRKDGVMLFAQIYXH"
        # should be ABCDEFGHIJKLMNOPQRSTUVWXYZ
        ciphertext: str = self.machine.encrypt(plaintext=plaintext, should_turn=False)

        self.assertEqual(ciphertext, ascii_uppercase)

    def test_offset(self) -> None:
        """Test that we can correctly encrypt a string.
        https://en.wikipedia.org/wiki/Enigma_rotor_details#Rotor_offset"""

        # current state: AAA 01.01.01 with no plugboard changes
        self.machine.rotors[0] = copy(ROTOR_III)
        self.machine.rotors[0].times_turned = 0
        self.machine.rotors[0].current_top = "A"
        self.machine.rotors[1] = copy(ROTOR_II)
        self.machine.rotors[1].times_turned = 0
        self.machine.rotors[1].current_top = "A"
        self.machine.rotors[2] = copy(ROTOR_I)
        self.machine.rotors[2].times_turned = 0
        self.machine.rotors[2].current_top = "A"

        plaintext: str = "AAAAA"
        ciphertext: str = self.machine.encrypt(plaintext=plaintext, verbose=True, should_turn=True)

        self.assertEqual(ciphertext, "BDZGO")

# ring
# https://en.wikipedia.org/wiki/Enigma_rotor_details#Ring_setting

if __name__ == "__main__":
    unittest.main()
