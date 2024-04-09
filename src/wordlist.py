import json
import os
import random

class WordList():
    def __init__(self, filepath: str):
        with open(filepath) as file:
            file_content = file.read()

        parsed_json = json.loads(file_content)
        self._words = parsed_json["words"]
        self._num_words = len(self._words)

    def get_random_word(self):
        return self._words[random.randrange(0, self._num_words)]
