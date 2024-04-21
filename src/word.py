from __future__ import annotations
from typing import List
from enum import Enum
from settings import *

class WordDrawOption(Enum):
    BASE = 1
    CORRECT = 2
    INCORRECT = 3
    UNDERLINE = 4

class Word:
    def __init__(self, text: str, order: int=None, previous: Word=None, next: Word=None) -> None:
        self.is_current: bool = False
        self.is_accurate = False
        self.order = order
        self.previous: Word = previous
        self.next: Word = next
        self._is_past_word: bool = False
        self.has_been_active: bool = False
        self._text: str = text
        self._characters: List[str] = list(self._text)
        self.len: int = len(text)
        self._entered_history: List[str] = []
        self.full_entered_history: List[str] = []
        self._draw_list = []
        self._update_draw_list()

    def update(self, input: str, is_backspace: bool=False) -> Word:
        if not self.is_current:
            return
        self.has_been_active = True
        if is_backspace:
            if self.previous is not None and len(self._entered_history) == 0:
                if self.previous.is_accurate:
                    return self
                self.is_current = False
                self.previous.is_current = True
                self.previous._is_past_word = False
                self.previous._update_draw_list()
                return self.previous
            if len(self._entered_history) != 0:
                self._entered_history.pop()
                self._update_draw_list()
                return self
        if input == " ":
            self._is_past_word = True
            self._validate()
            if not self.next is None:
                self.next.is_current = True
                self.is_current = False
                self._update_draw_list()
                return self.next
            return self
        if len(self._entered_history) < self.len + 4:
            self._entered_history.append(input)
            self.full_entered_history.append(input)
        self._update_draw_list()
        return self

    def _update_draw_list(self) -> None:
        i: int = 0
        self._draw_list = []
        while i < len(self._entered_history):
            if i < self.len:
                if self._entered_history[i] == self._characters[i]:
                    self._draw_list.append((self._characters[i], WordDrawOption.CORRECT))
                else:
                    self._draw_list.append((self._characters[i], WordDrawOption.INCORRECT))
            else:
                self._draw_list.append((self._entered_history[i], WordDrawOption.INCORRECT))
            i += 1
        while i < len(self._characters):
            if self._is_past_word:
                self._draw_list.append((self._characters[i], WordDrawOption.UNDERLINE))
            else:
                self._draw_list.append((self._characters[i], WordDrawOption.BASE))
            i += 1
                
    def draw(self, x: int, y: int) -> None:
        x_offset = x
        i = 0
        for i in range(len(self._draw_list)):
            current_char_width = pr.measure_text(self._draw_list[i][0], FONT_SIZE)
            # draw cursor
            if self.is_current:
                if i == len(self._entered_history):
                    pr.draw_rectangle(x_offset, y, current_char_width, 30, pr.PINK)
            color = FONT_COLOR
            if self._draw_list[i][1] == WordDrawOption.INCORRECT:
                color = pr.RED
            elif self._draw_list[i][1] == WordDrawOption.CORRECT:
                color = pr.GREEN
            elif self._draw_list[i][1] == WordDrawOption.UNDERLINE:
                pr.draw_line(x_offset, 
                             y + 34, 
                             x_offset + current_char_width,
                             y + 34,
                             pr.RED)
            pr.draw_text(self._draw_list[i][0],
                        x_offset,
                        y,
                        FONT_SIZE,
                        color)
            x_offset += current_char_width + CHAR_SPACING
        # draw cursor for space
        if self.is_current:
            if len(self._entered_history) >= self.len:
                pr.draw_rectangle(x_offset, y, 10, 30, pr.PINK)

    def _validate(self) -> None:
        self.is_accurate = False
        if len(self._entered_history) == self.len:
            for i in range(self.len):
                if self._characters[i] != self._entered_history[i]:
                    return
            self.is_accurate = True

    def get_text(self) -> str:
        return self._text

    def get_draw_text(self) -> str:
        s = ""
        for i in self._draw_list:
            s = s + i[0]
        return s
        
    def get_num_accurate_chars(self) -> int:
        if self.is_accurate:
            return self.len
        
        i = 0
        accurate_count = 0
        while i < len(self._entered_history):
            if i == self.len:
                break
            if self._entered_history[i] != self._characters[i]:
                accurate_count += 1
            i += 1
        return accurate_count