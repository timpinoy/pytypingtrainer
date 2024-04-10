import pyray as pr
import math
import os

from typing import List
from settings import *
from wordlist import WordList


class App:
    def __init__(self) -> None:
        pr.init_window(WIN_WIDTH, WIN_HEIGHT, "PY Typing Trainer")
        pr.set_target_fps(TARGET_FPS)
        self.delta_time: float = 0.0
        self.round_time: float = 15.0
        self.remaining_time: float = self.round_time
        self.type_mode: TypeMode = TypeMode(self)
    
    def update(self) -> None:
        self.delta_time = pr.get_frame_time()
        self.remaining_time -= self.delta_time
        if self.remaining_time < 0:
           self.remaining_time = self.round_time 
           self.type_mode.reset()
        self.type_mode.update()
    
    def draw(self) -> None:
        pr.begin_drawing()
        pr.clear_background(BG_COLOR)
        pr.draw_fps(10, 10)
        pr.draw_text(f"{math.ceil(self.remaining_time)}", 20, 80, FONT_SIZE, FONT_COLOR)
        self.type_mode.draw()
        pr.end_drawing()

    def run(self) -> None:
        while not pr.window_should_close():
            self.update()
            self.draw()
        pr.close_window()

class TypeMode():
    def __init__(self, app: App) -> None:
        self._app = app
        self._load_word_list()
        self._text_lines: List[TextLine] = []
        self._current_line: int = 0
        self.reset()

    def update(self) -> None:
        int_char = pr.get_char_pressed()
        while int_char > 0:
            if int_char >= 32 and int_char <= 125:
                input_char = chr(int_char)
                if self._text_lines[self._current_line].input_char(input_char):
                    self._current_line += 1
            int_char = pr.get_char_pressed()

    def draw(self) -> None:
        for i in range(len(self._text_lines)):
            # centering text so need to calculate how wide the text line will be
            text_width = pr.measure_text(self._text_lines[i].get_text(), FONT_SIZE)
            text_start_pos = (WIN_WIDTH - text_width) // 2
            pr.draw_text(f"{self._text_lines[i].get_text()}",
                         text_start_pos,
                         140 + (FONT_SIZE + 2) * i,
                         FONT_SIZE,
                         FONT_COLOR)
    
    def _load_word_list(self) -> None:
        filepath = os.path.abspath(os.path.join(
            os.path.dirname( __file__ ), 
            *WORDS_FOLDER,
            "english.json"
            ))
        self._world_list = WordList(filepath)

    def _update_line(self) -> None:
        pass

    def reset(self) -> None:
        self._current_line = 0
        self._text_lines: List[TextLine] = [TextLine(self._world_list, MAX_LINE_LENGTH) for _ in range(3)]

class TextLine:
    def __init__(self, word_list: WordList, max_length: int) -> None:
        self._word_list: WordList = word_list
        self._max_length: int = max_length
        self._text: str = self._word_list.get_random_word()
        self._current_char: int = 0
        word = self._word_list.get_random_word()
        while len(self._text) + len(word) <= self._max_length:
            self._text = f"{self._text} {word}"
            word = self._word_list.get_random_word()
        self._text = f"{self._text} "
        self._text_len = len(self._text)

    def get_text(self) -> str:
        return self._text

    def input_char(self, char: str) -> bool:
        print(char)
        self._text = f"{self._text[:self._current_char]}{char}{self._text[self._current_char+1:]}"
        self._current_char += 1
        if self._current_char == self._text_len:
            return True
        return False


if __name__ == "__main__":
    app = App()
    app.run()