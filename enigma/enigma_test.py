import string
import unittest
from enigma import Enigma, Rotors, Rotor

import unittest
from enigma import Rotor, Rotors, Enigma


class TestRotor(unittest.TestCase):
    def setUp(self):
        self.rotor = Rotor("DMTWSILRUYQNKFEJCAZBPGXOHV")

    def test_map_letter(self):
        self.assertEqual(self.rotor.map_letter('A', 0), 'D')
        self.assertEqual(self.rotor.map_letter('A', 1), 'M')
        self.assertEqual(self.rotor.map_letter('Z', 1), 'D')

    def test_map_letter_backwards(self):
        self.assertEqual(self.rotor.map_letter_backwards('D', 0), 'A')
        self.assertEqual(self.rotor.map_letter_backwards('M', 1), 'A')
        self.assertEqual(self.rotor.map_letter_backwards('D', 1), 'Z')


class TestRotors(unittest.TestCase):
    def setUp(self):
        self.r1 = Rotor("DMTWSILRUYQNKFEJCAZBPGXOHV")
        self.r2 = Rotor("HQZGPJTMOBLNCIFDYAWVEUSRKX")
        self.r3 = Rotor("UQNTLSZFMREHDPXKIBVYGJCWOA")
        self.rotors = Rotors([self.r1, self.r2, self.r3], 0)

    def test_process_letter(self):
        self.assertEqual(self.rotors.process_letter('A'), 'P')
        self.assertEqual(self.rotors.process_letter('B'), 'R')

    def test_process_message(self):
        self.assertEqual(self.rotors.process_message('HELLO'), 'UCCUY')


class TestEnigma(unittest.TestCase):

    def setUp(self):
        self.r1 = Rotor("DMTWSILRUYQNKFEJCAZBPGXOHV")
        self.r2 = Rotor("HQZGPJTMOBLNCIFDYAWVEUSRKX")
        self.r3 = Rotor("UQNTLSZFMREHDPXKIBVYGJCWOA")
        self.rotors = Rotors([self.r1, self.r2, self.r3], 0)
        self.enigma = Enigma(["AB", "CD"], self.rotors)

    def test_process_message(self):
        self.assertEqual(self.enigma.process_message('HELLO'), 'UDDUY')

    def test_validate_plugs(self):
        valid_plugs = ["AB", "CD"]
        self.enigma._validate_plugs(valid_plugs)
        invalid_plugs = ["AB", "AA"]
        with self.assertRaises(AssertionError):
            self.enigma._validate_plugs(invalid_plugs)

    def test_process_plugs(self):
        plugs = ["AB", "CD"]
        expected_map = {'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C'}
        result_map = self.enigma._process_plugs(plugs)
        for k, v in expected_map.items():
            self.assertEqual(result_map[k], v)
        # Ensure all letters are mapped to themselves if not in plugs
        for letter in string.ascii_uppercase:
            if letter not in expected_map:
                self.assertEqual(result_map[letter], letter)


if __name__ == '__main__':
    unittest.main()
