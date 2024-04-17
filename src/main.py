import pyray as pr
import math
import os

from settings import *
from wordlist import WordList
from typing import List


class App:
    def __init__(self) -> None:
        pr.init_window(WIN_WIDTH, WIN_HEIGHT, "PY Typing Trainer")
        pr.set_target_fps(TARGET_FPS)
        self.delta_time: float = 0.0
        self.round_time: float = 60.0
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
        self._char_width = pr.measure_text(" ", FONT_SIZE)
        self._load_word_list()
        self._text_lines: List[TextLine] = []
        self.reset()

    def update(self) -> None:
        int_char = pr.get_char_pressed()
        while int_char > 0:
            if int_char >= 32 and int_char <= 125:
                input_char = chr(int_char)
                self._text_lines[self._current_line].update(input_char)
            int_char = pr.get_char_pressed()

        if pr.is_key_pressed(pr.KeyboardKey.KEY_BACKSPACE):
            self._text_lines[self._current_line].update("", is_backspace=True)

    def draw(self) -> None:
        for i in range(len(self._text_lines)):
            self._text_lines[i].draw(140 + (FONT_SIZE + 2) * i)
    
    def _load_word_list(self) -> None:
        filepath = os.path.abspath(os.path.join(
            os.path.dirname( __file__ ), 
            *WORDS_FOLDER,
            "english.json"
            ))
        self._world_list = WordList(filepath)
    
    def _set_active_line(self, active_index: int) -> None:
        if active_index >= len(self._text_lines):
            self.reset()
            return
        self._current_line: int = active_index
        print(active_index)
        for i in range(len(self._text_lines)):
            if i == active_index:
                self._text_lines[i].is_active = True
            else:
                self._text_lines[i].is_active = False

    def _update_line(self) -> None:
        pass

    def reset(self) -> None:
        self._text_lines: List[TextLine] = [TextLine(self._world_list, MAX_LINE_LENGTH) for _ in range(NUM_LINES)]
        self._set_active_line(0)

class TextLine:
    def __init__(self, word_list: WordList, max_length: int) -> None:
        self._word_list: WordList = word_list

        self.first_word = self._word_list.get_random_word2()
        self.first_word.is_current = True
        cur_word = self.first_word
        for i in range(3):
            w = self._word_list.get_random_word2()
            w._previous = cur_word
            cur_word._next = w
            cur_word = w
        self.active_word = self.first_word
    
    def update(self, input_char, is_backspace: bool = False) -> None:
        self.active_word = self.active_word.update(input_char, is_backspace)

    def draw(self, y_offset: int):
        # centering text so need to calculate how wide the text line will be
        #text_width: int = pr.measure_text(self._text, FONT_SIZE)
        #text_start_pos = (WIN_WIDTH - text_width) // 2
        #x_offset = text_start_pos

        curr = self.first_word
        x_offset = 20
        while True:
            curr.draw(x_offset, y_offset)
            x_offset += pr.measure_text(curr.get_text(), FONT_SIZE)
            curr = curr.get_next()
            if curr is None:
                break
            x_offset += pr.measure_text(" ", FONT_SIZE) + CHAR_SPACING * 2

    def get_text(self) -> str:
        return self._text


if __name__ == "__main__":
    app = App()
    app.run()