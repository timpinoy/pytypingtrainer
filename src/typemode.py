import os
import math
from typing import List, Dict
from word import Word
from wordlist import WordList
from settings import *

class TypeMode():
    def __init__(self, time: int) -> None:
        self.is_time_up: bool = False
        self.words: List[Word] = []
        self._word_list: WordList = self._load_word_list()
        self._active_word: Word = None
        self._round_time: float = time
        self._remaining_time: float = self._round_time
        self._words_in_line: int = 5
        self._num_lines: int = 3
        self._current_draw_chunk: List[Word] = []
        self._initialize_words()
        self._update_draw_chunk()

    def update(self) -> None:
        if not self.is_time_up:
            self.delta_time = pr.get_frame_time()
            self._remaining_time -= self.delta_time
            if self._remaining_time < 0:
            #self.remaining_time = self.round_time 
                self.is_time_up = True

            int_char = pr.get_char_pressed()
            while int_char > 0:
                if int_char >= 32 and int_char <= 125:
                    input_char = chr(int_char)
                    self._active_word = self._active_word.update(input_char)
                int_char = pr.get_char_pressed()
                self._update_draw_chunk()

            if pr.is_key_pressed(pr.KeyboardKey.KEY_BACKSPACE):
                self._active_word = self._active_word.update("", is_backspace=True)
                self._update_draw_chunk()

    def _update_draw_chunk(self) -> None:
        self._current_draw_chunk = []
        current_index: int = self._active_word.order
        if current_index <= self._words_in_line:
            for i in range(self._num_lines * self._words_in_line):
               self._current_draw_chunk.append(self.words[i]) 
        else:
            start_index: int = ((current_index // self._words_in_line) - 1) * self._words_in_line
            for i in range(start_index, start_index + self._num_lines * self._words_in_line):
                self._current_draw_chunk.append(self.words[i])

    def draw(self) -> None:
        pr.draw_text(f"{math.ceil(self._remaining_time)}", 20, 80, FONT_SIZE, FONT_COLOR)
        y_pos: int = 120
        for i in range(self._num_lines):
            start_index: int = i * self._words_in_line
            text_width: int = pr.measure_text(
                " ".join(i.get_draw_text() for i in self._current_draw_chunk[start_index:start_index+self._words_in_line]),
                FONT_SIZE)
            text_start_pos: int = (WIN_WIDTH - text_width) // 2
            x_offset: int = text_start_pos
            for j in range(self._words_in_line):
                word: Word = self._current_draw_chunk[i*self._words_in_line + j]
                word_width = pr.measure_text(word.get_draw_text() + " ", FONT_SIZE)
                word.draw(x_offset, y_pos + i * 40)
                x_offset += word_width
    
    def _load_word_list(self) -> WordList:
        filepath = os.path.abspath(os.path.join(
            os.path.dirname( __file__ ), 
            *WORDS_FOLDER,
            "english.json"
            ))
        return WordList(filepath)
    
    def _initialize_words(self) -> None:
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
    
    def get_result(self) -> Dict:
        res = {}
        res["time"] = math.floor(self._round_time)
        entered_characters = 0
        accurate_count = 0
        accurate_word_char_count = 0

        cur: Word = self.words[0]
        # adding 1 for spaces
        while True:
            if not (cur.is_current or cur.has_been_active) or cur is None:
                break
            if cur.is_current:
                entered_characters += len(cur.full_entered_history)
                accurate_count += cur.get_num_accurate_chars()
            else:
                entered_characters += len(cur.full_entered_history) + 1
                accurate_count += cur.get_num_accurate_chars() + 1
            if cur.is_accurate:
                accurate_word_char_count += cur.len + 1
            cur = cur.next
        res["entered_count"] = entered_characters
        res["wpm"] = accurate_word_char_count / 5 / self._round_time * 60
        res["raw_wpm"] = entered_characters / 5 / self._round_time * 60
        res["acc"] = accurate_count / entered_characters * 100
        return res