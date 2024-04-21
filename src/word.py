from __future__ import annotations
from typing import List
from settings import *

class Word:
    def __init__(self, text: str, order: int=None, previous: Word=None, next: Word=None) -> None:
        self.is_current: bool = False
        self.is_accurate = False
        self.order = order
        self.previous: Word = previous
        self.next: Word = next
        self._is_past_word: bool = False
        self._has_been_active: bool = False
        self._text: str = text
        self._characters: List[str] = list(self._text)
        self._len: int = len(text)
        self._entered_history: List[str] = []
        self._full_entered_history: List[str] = []
        self._draw_list = []
        self._update_draw_list()

    def update(self, input: str, is_backspace: bool=False) -> Word:
        if not self.is_current:
            return
        self._has_been_active = True
        if is_backspace:
            if self.previous is not None and len(self._entered_history) == 0:
                if self.previous.is_accurate:
                    return self
                self.is_current = False
                self.previous.is_current = True
                self.previous._is_past_word = False
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
            if self._is_past_word:
                self._draw_list.append((self._characters[i], False))
            else:
                self._draw_list.append((self._characters[i], None))
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
        # draw cursor for space
        if self.is_current:
            if len(self._entered_history) >= self._len:
                pr.draw_rectangle(x_offset, y, 10, 30, pr.PINK)

    def _validate(self) -> None:
        self.is_accurate = False
        if len(self._entered_history) == self._len:
            for i in range(self._len):
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