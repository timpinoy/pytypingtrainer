from __future__ import annotations
from typing import List

class Word:
    def __init__(self, text: str, previous: Word=None, next: Word=None) -> None:
        self.is_current: bool = False
        self._text: str = text
        self._characters: List[str] = list(self._text)
        self._len: int = len(text)
        self._previous: Word = previous
        self._next: Word = next

    def update(self, input: str, is_backspace: bool=False) -> Word:
        if is_backspace:
            if self._previous is not None:
                self.is_current = False
                self._previous.is_current = True
                return self._previous
            return self
        if input == " ":
            if not self._next is None:
                self._next.is_current = True
                self.is_current = False
                return self._next
            return self

    def draw(self) -> None:
        pass

    def get_next(self) -> Word:
        return self._next
    
    def get_previous(self) -> Word:
        return self._previous