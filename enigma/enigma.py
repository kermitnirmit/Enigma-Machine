import string
from typing import List, Dict

letters = string.ascii_uppercase


class Rotor:
    """
    Represents a single rotor. Doesn't hold any state about offset
    """

    def __init__(self, alphabet: str):
        assert len(alphabet) == 26
        self.alphabet = alphabet

    def map_letter(self, letter: str, offset: int):
        start = letters.index(letter)
        return self.alphabet[(start + offset) % 26]

    def map_letter_backwards(self, letter: str, offset: int):
        start = self.alphabet.index(letter)
        return letters[(start - offset) % 26]


class Rotors:
    """
    Represents the Rotors of an Enigma Machine. Holds state about offsets.
    """

    def __init__(self, rotors, offset):
        self.rotors = rotors
        self.offset = offset

    def process_letter(self, letter: str) -> str:
        """
        Encodes a letter and increments the offset.
        :param letter: letter to be encoded.
        :return: encoded letter.
        """
        self.offset += 1
        offsets = self._convert_offset()
        # Forwards
        for rotor, offset in zip(self.rotors, offsets):
            letter = rotor.map_letter(letter, offset)
        # Through the reflector
        letter = letters[(letters.index(letter) + 13) % 26]
        # On the way back
        for rotor, offset in zip(self.rotors[::-1], offsets[::-1]):
            letter = rotor.map_letter_backwards(letter, offset)
        return letter

    def process_message(self, message: str) -> str:
        """
        Takes in a message and routes it through the rotors and reflector and back through the rotors.
        :param message:
        :return:
        """
        ret = ""
        for letter in message:
            ret += self.process_letter(letter)
        return ret

    def _convert_offset(self) -> List[int]:
        """
        Converts the numeric offset into a list of offsets for each rotor.
        :return:
        """
        if self.offset >= 26 ** len(self.rotors):
            self.offset = 0
        first = self.offset % 26
        second = (self.offset // 26) % 26
        third = (self.offset // (26 * 26)) % 26
        return [first, second, third][:len(self.rotors)]



class Enigma:
    """
    Represents an Enigma Machine - including the plug board and the rotors.
    """

    def __init__(self, plugs: List[str], rotors: Rotors):
        self._validate_plugs(plugs)
        self.letter_map = self._process_plugs(plugs)
        self.rotors = rotors

    def process_message(self, message: str) -> str:
        """
        Takes in a message and routes it through the plugboard, rotors and then back through the plugboard.
        :param message: message to be encoded/decoded
        :return: Encoded / Decoded Message
        """
        new_message = "".join([self.letter_map[x] for x in message])
        encoded = self.rotors.process_message(new_message)
        return "".join([self.letter_map[x] for x in encoded])

    def _validate_plugs(self, plugs: List[str]):
        """
        At most 10 plugs, and no letter is there more than once
        :param plugs: list of [AB, CD, EF]
        :return: if plugs are valid
        """
        assert len(plugs) <= 10
        for plug_pair in plugs:
            assert len(plug_pair) == 2
        all_plugged_letters = "".join(plugs)
        assert len(set(all_plugged_letters)) == len(all_plugged_letters)

    def _process_plugs(self, plugs) -> Dict[str, str]:
        """
        Creates the letter>letter mapping taking into account the reflective nature of the plugs.
        :param plugs: pairs of letters that should map to each other
        :return:
        """
        ret = dict()
        for plug_pair in plugs:
            l, r = list(plug_pair)
            ret[l] = r
            ret[r] = l
        for letter in letters:
            if letter not in ret.keys():
                ret[letter] = letter
        assert len(ret) == 26
        return ret
