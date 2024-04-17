import json
import os
import random
from word import *

class WordList():
    def __init__(self, filepath):
        with open(filepath) as file:
            file_content = file.read()

        parsed_json = json.loads(file_content)
        self._words = parsed_json["words"]
        self._num_words = len(self._words)

    def get_random_word(self) -> Word:
        return Word(self._words[random.randrange(0, self._num_words)])  

    def get_word_line(self, max_characters: int) -> str:
        line = self.get_random_word()
        word = self.get_random_word()
        while len(line) + len(word) + 1 <= max_characters:
            line = f"{line} {word}"
            word = self.get_random_word()
        return line