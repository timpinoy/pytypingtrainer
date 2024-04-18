from __future__ import annotations
from typing import List
from settings import *

class Word:
    def __init__(self, text: str, previous: Word=None, next: Word=None) -> None:
        self.is_current: bool = False
        self._past_word: bool = False
        self._has_been_active: bool = False
        self._text: str = text
        self._characters: List[str] = list(self._text)
        self._len: int = len(text)
        self._previous: Word = previous
        self._next: Word = next
        self._entered_history: List[str] = []
        self._full_entered_history: List[str] = []
        self._draw_list = []
        self.is_accurate = False
        self._update_draw_list()

    def update(self, input: str, is_backspace: bool=False) -> Word:
        if not self.is_current:
            return
        self._has_been_active = True
        if is_backspace:
            if self._previous is not None and len(self._entered_history) == 0:
                self.is_current = False
                self._previous.is_current = True
                self._previous._past_word = False
                return self._previous
            if len(self._entered_history) != 0:
                self._entered_history.pop()
                self._update_draw_list()
                return self
        if input == " ":
            self._past_word = True
            self._validate()
            if not self._next is None:
                self._next.is_current = True
                self.is_current = False
                self._update_draw_list()
                return self._next
            return self
        if len(self._entered_history) < self._len + 4:
            self._entered_history.append(input)
            self._full_entered_history.append(input)
        self._update_draw_list()
        return self

    def _update_draw_list(self) -> None:
        i: int = 0
        self._draw_list = []
        while i < len(self._entered_history):
            if i < self._len:
                if self._entered_history[i] == self._characters[i]:
                    self._draw_list.append((self._characters[i], True))
                else:
                    self._draw_list.append((self._characters[i], False))
            else:
                self._draw_list.append((self._entered_history[i], False))
            i += 1
        while i < len(self._characters):
            if self._past_word:
                self._draw_list.append((self._characters[i], False))
            else:
                self._draw_list.append((self._characters[i], None))
            i += 1
                
    def draw(self, x: int, y: int) -> None:
        x_offset = x
        i = 0
        for i in range(len(self._draw_list)):
            current_char_width = pr.measure_text(self._draw_list[i][0], FONT_SIZE)
            color = FONT_COLOR
            if self._draw_list[i][1] is not None and not self._draw_list[i][1]:
                color = pr.RED
            elif self._draw_list[i][1]:
                color = pr.GREEN
            pr.draw_text(self._draw_list[i][0],
                        x_offset,
                        y,
                        FONT_SIZE,
                        color)
            x_offset += current_char_width + CHAR_SPACING

    def _validate(self) -> None:
        self.is_accurate = False
        if len(self._entered_history) == self._len:
            for i in range(self._len):
                if self._characters[i] != self._entered_history[i]:
                    return
            self.is_accurate = True

    def get_next(self) -> Word:
        return self._next
    
    def get_previous(self) -> Word:
        return self._previous

    def get_text(self) -> str:
        return self._text

    def get_draw_text(self) -> str:
        s = ""
        for i in self._draw_list:
            s = s + i[0]
        return s