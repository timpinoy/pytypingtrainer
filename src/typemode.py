import os
import math
from typing import List
from word import Word
from wordlist import WordList
from settings import *

class TypeMode():
    def __init__(self, time: int) -> None:
        self.words: List[Word] = []
        self._word_list: WordList = self._load_word_list()
        self._active_word: Word = None
        self.round_time: float = time
        self.remaining_time: float = self.round_time
        self.reset()

    def update(self) -> None:
        self.delta_time = pr.get_frame_time()
        self.remaining_time -= self.delta_time
        if self.remaining_time < 0:
           self.remaining_time = self.round_time 

        int_char = pr.get_char_pressed()
        while int_char > 0:
            if int_char >= 32 and int_char <= 125:
                input_char = chr(int_char)
                self._active_word = self._active_word.update(input_char)
            int_char = pr.get_char_pressed()

        if pr.is_key_pressed(pr.KeyboardKey.KEY_BACKSPACE):
            self._active_word = self._active_word.update("", is_backspace=True)

    def draw(self) -> None:
        pr.draw_text(f"{math.ceil(self.remaining_time)}", 20, 80, FONT_SIZE, FONT_COLOR)
        # centering text so need to calculate how wide the text line will be
        #text_width: int = pr.measure_text(self._text, FONT_SIZE)
        #text_start_pos = (WIN_WIDTH - text_width) // 2
        #x_offset = text_start_pos
        curr = self._active_word
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
        self.words = []
        for i in range(400):
            if i == 0:
                self.words.append(Word(self._word_list.get_random_word(), i))
                self.words[0].is_current = True
            else:
                self.words.append(Word(self._word_list.get_random_word(), 
                                       i,
                                       self.words[i-1]))
                self.words[i-1].next = self.words[i]
        self._active_word = self.words[0]