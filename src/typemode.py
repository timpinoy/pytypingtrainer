import os
from word import Word
from wordlist import WordList
from settings import *

class TypeMode():
    def __init__(self) -> None:
        self._word_list: WordList = self._load_word_list()
        self._first_word: Word = Word("")
        self._active_word: Word = self._first_word
        self.reset()

    def update(self) -> None:
        int_char = pr.get_char_pressed()
        while int_char > 0:
            if int_char >= 32 and int_char <= 125:
                input_char = chr(int_char)
                self._active_word = self._active_word.update(input_char)
            int_char = pr.get_char_pressed()

        if pr.is_key_pressed(pr.KeyboardKey.KEY_BACKSPACE):
            self._active_word = self._active_word.update("", is_backspace=True)

    def draw(self) -> None:
        # centering text so need to calculate how wide the text line will be
        #text_width: int = pr.measure_text(self._text, FONT_SIZE)
        #text_start_pos = (WIN_WIDTH - text_width) // 2
        #x_offset = text_start_pos
        curr = self._first_word
        x_offset = 20
        while True:
            curr.draw(x_offset, 200)
            x_offset += pr.measure_text(curr.get_draw_text(), FONT_SIZE)
            curr = curr.get_next()
            if curr is None:
                break
            x_offset += pr.measure_text(" ", FONT_SIZE) + CHAR_SPACING * 2
    
    def _load_word_list(self) -> WordList:
        filepath = os.path.abspath(os.path.join(
            os.path.dirname( __file__ ), 
            *WORDS_FOLDER,
            "english.json"
            ))
        return WordList(filepath)
    
    def reset(self) -> None:
        self._first_word = self._word_list.get_random_word()
        self._first_word.is_current = True
        cur_word = self._first_word
        for i in range(3):
            w = self._word_list.get_random_word()
            w._previous = cur_word
            cur_word._next = w
            cur_word = w
        self._active_word = self._first_word